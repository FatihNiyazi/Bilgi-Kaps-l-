
from flask import (Flask, render_template, request, redirect, url_for, 
                   flash, send_file, send_from_directory)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (LoginManager, UserMixin, login_user, logout_user, 
                         login_required, current_user)
from werkzeug.security import generate_password_hash, check_password_hash
from fpdf import FPDF
import os
from dotenv import load_dotenv
import uuid
from datetime import datetime
import requests
import io
load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__)) 
instance_path = os.path.join(basedir, 'instance')   

if not os.path.exists(instance_path):
    os.makedirs(instance_path)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(instance_path, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Bu sayfayı görmek için lütfen giriş yapın."
login_manager.login_message_category = "info"


PDF_UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'user_pdfs')
if not os.path.exists(PDF_UPLOAD_FOLDER):
    os.makedirs(PDF_UPLOAD_FOLDER)


class BilgiKapsuluPDF(FPDF):
    def header(self):
        logo_path = os.path.join(os.path.dirname(__file__), 'static', 'logo.png')
        if os.path.exists(logo_path):
            self.image(logo_path, 10, 8, 25)
        self.set_font('DejaVu', '', 15)
        self.cell(80) 
        self.cell(30, 10, 'Bilgi Kapsülü', 0, 0, 'C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu', '', 8)
        self.cell(0, 10, f'Sayfa {self.page_no()}/{{nb}}', 0, 0, 'C')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    pdfs = db.relationship('PdfHistory', backref='owner', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class PdfHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(300), nullable=False)
    filename = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form.get('username')).first()
        if user and user.check_password(request.form.get('password')):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Kullanıcı adı veya şifre hatalı.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        if User.query.filter_by(username=request.form.get('username')).first():
            flash('Bu kullanıcı adı zaten alınmış.', 'warning')
            return redirect(url_for('register'))
        new_user = User(username=request.form.get('username'))
        new_user.set_password(request.form.get('password'))
        db.session.add(new_user)
        db.session.commit()
        flash('Hesabınız başarıyla oluşturuldu! Şimdi giriş yapabilirsiniz.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/kapsullerim')
@login_required
def kapsullerim():
    user_pdfs = db.session.execute(db.select(PdfHistory).filter_by(user_id=current_user.id).order_by(PdfHistory.created_at.desc())).scalars().all()
    return render_template('kapsullerim.html', kapsuller=user_pdfs)

@app.route('/download/<filename>')
@login_required
def download_pdf(filename):
    pdf_record = db.session.execute(db.select(PdfHistory).filter_by(filename=filename, user_id=current_user.id)).scalar_one_or_none()
    if not pdf_record:
        return "Dosya bulunamadı veya bu dosyaya erişim yetkiniz yok.", 404
    return send_from_directory(PDF_UPLOAD_FOLDER, filename, as_attachment=True, download_name=f"{pdf_record.topic.replace(' ', '_')}.pdf")

@app.route('/generate-pdf', methods=['POST'])
def create_pdf():
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

    topic = request.form.get('topic', '').strip()
    if not topic:
        flash('Lütfen geçerli bir konu girin.', 'warning')
        return redirect(url_for('index'))

    prompt = (
        f"'{topic}' konusunu, bu konuyu daha önce hiç duymamış 15 yaşındaki birine anlatır gibi açıkla. "
        "Açıklamanı şu bölümlere ayır ve her bölüm için başlık kullan:\n"
        "1. **Basitçe Nedir?:** Konunun en temel tanımı.\n"
        "2. **Bir Benzetme ile Anlayalım:** Konuyu somutlaştırmak için günlük hayattan bir analoji veya benzetme yap.\n"
        "3. **Nasıl Çalışır?:** Adım adım, basit bir dille çalışma prensibi.\n"
        "4. **Neden Önemli?:** Bu konunun neden değerli olduğunu anlatan 2-3 cümle.\n"
        "Lütfen akıcı, anlaşılır ve pozitif bir dil kullan. Matematiksel formüller veya özel semboller kullanmaktan kaçın.\n\n"
        "**ÇOK ÖNEMLİ: Cevabın dili MUTLAKA TÜRKÇE olmalıdır.**"
    )
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    data = {"model": "llama3-8b-8192", "messages": [{"role": "user", "content": prompt}], "temperature": 0.7}

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=data)
        response.raise_for_status()
        ai_content = response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print(f"API Hatası: {e}")
        flash('Yapay zeka ile iletişim kurarken bir sorun oluştu. Lütfen tekrar deneyin.', 'danger')
        return redirect(url_for('index'))

    pdf = BilgiKapsuluPDF()
    pdf.alias_nb_pages()
    try:
        pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
    except RuntimeError:
        pass

    pdf.add_page()
    pdf.set_font('DejaVu', '', 24)
    pdf.cell(0, 10, f"Konu: {topic}", ln=True, align='C')
    pdf.ln(15)

    lines = ai_content.split('\n')
    for line in lines:
        if line.strip().startswith('**') and line.strip().endswith('**'):
            title_text = line.strip().strip('*').strip()
            pdf.set_font('DejaVu', '', 16)
            pdf.multi_cell(0, 10, title_text, ln=True)
            pdf.ln(4)
        elif line.strip().startswith('* '):
            item_text = line.strip().strip('*').strip()
            pdf.set_font('DejaVu', '', 12)
            pdf.multi_cell(0, 7, f'  •  {item_text}', ln=True)
        else:
            pdf.set_font('DejaVu', '', 12)
            pdf.multi_cell(0, 10, line, ln=True)

    if current_user.is_authenticated:
        unique_filename = f"{uuid.uuid4().hex}.pdf"
        filepath = os.path.join(PDF_UPLOAD_FOLDER, unique_filename)
        pdf.output(filepath)
        new_pdf_record = PdfHistory(topic=topic, filename=unique_filename, owner=current_user)
        db.session.add(new_pdf_record)
        db.session.commit()

    pdf_buffer = io.BytesIO()
    pdf.output(pdf_buffer)
    pdf_buffer.seek(0)
    
    safe_download_name = topic.encode('ascii', 'ignore').decode('ascii').replace(' ', '_').replace('/', '_')
    if not safe_download_name:
        safe_download_name = "bilgi_kapsulu"
    
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f'{safe_download_name}.pdf',
        mimetype='application/pdf'
    )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
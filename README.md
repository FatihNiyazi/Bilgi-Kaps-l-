# Bilgi-Kaps-l-
 Yapay zeka akademisi için yapılmıştır
Bilgi Kapsülü
Proje Tanımı
Bilgi Kapsülü, kullanıcıların anlamadıkları konuları yapay zeka destekli bir şekilde özetleyen ve basit bir dille açıklayan yenilikçi bir uygulamadır. Kullanıcılar, "Lineer cebiri anlamadım" gibi bir ifadeyle girdiklerinde, uygulama ilgili konunun temel prensiplerini ve ana hatlarını içeren tek bir PDF dosyası oluşturacaktır. Bu sayede, kullanıcılar karmaşık konulara hızlı ve anlaşılır bir giriş yapabilir, dilerlerse daha sonraki etkileşimlerde konuyu derinleştirebilirler.

Nasıl Çalışır?
Kullanıcı Girişi: Kullanıcı, anlamadığı konuyu metin olarak girer (örneğin: "Kuantum fiziği nedir?").

Yapay Zeka İşleme: Uygulama, kullanıcının girdisini işlemek için gelişmiş yapay zeka modellerini kullanır. Bu modeller, konuyu analiz eder, temel kavramları belirler ve bunları basit bir dilde özetler.

PDF Oluşturma: İşlenen bilgiler, okuyucunun kolayca anlayabileceği, sade ve anlaşılır bir formatta PDF dosyası olarak derlenir. Bu PDF, konunun tamamını öğretmek yerine, bir başlangıç noktası ve temel bir anlayış sağlamayı hedefler.

Tekrarlı İyileştirme: Eğer kullanıcı ilk PDF'i yeterli bulmazsa, daha fazla detay veya farklı bir açıklama için tekrar istekte bulunabilir.

Sprint 1: Temel Fonksiyonalite ve Mimari Planlaması
Bu sprint, Bilgi Kapsülü uygulamasının temel iskeletini oluşturmaya ve mimariyi belirlemeye odaklanacaktır.

Hedefler:
Kullanıcıdan metin girişi alabilen bir arayüz taslağı oluşturmak.

Yapay zeka modelini (şimdilik placeholder olarak) entegre etmek ve basit metin işleme yeteneği kazandırmak.

İşlenmiş metni temel bir PDF dosyasına dönüştürme mekanizmasını kurmak.

Geliştirme ortamını ve temel bağımlılıkları ayarlamak.

Yapılacaklar Listesi:
Kullanıcı Arayüzü (Frontend):

Basit bir metin giriş alanı ve "PDF Oluştur" butonu içeren HTML sayfası (placeholder).

Kullanıcı girdisini alıp backend'e gönderecek JavaScript fonksiyonları.

Backend (API):

Python (Flask/Django) veya Node.js (Express) gibi bir framework kullanarak temel bir API servisi oluşturma.

Kullanıcıdan gelen metin girdisini kabul eden bir endpoint (/generate_pdf).

Yapay Zeka Entegrasyonu (Placeholder): Şimdilik, gelen metni basitçe işleyen (örneğin, ilk birkaç cümleyi alan veya anahtar kelimeleri çıkaran) bir fonksiyon. Gerçek AI entegrasyonu sonraki sprintlerde yapılacak.

PDF Oluşturma Modülü: Gelen basit metni bir PDF dosyasına yazabilen bir kütüphane (örneğin Python için ReportLab veya Fpdf) entegrasyonu.

Altyapı ve Bağımlılıklar:

Geliştirme ortamı kurulumu (Python/Node.js, sanal ortamlar).

Gerekli kütüphanelerin (API framework, PDF kütüphanesi) requirements.txt veya package.json dosyasına eklenmesi.

Temel proje yapısının ve klasörleme şemasının belirlenmesi.

Çıktılar:
Basit bir web sayfası ile çalışan, metin girişi alıp placeholder bir metni PDF olarak döndüren bir prototip.

API endpoint'inin temel işlevselliğinin test edilebilir olması.

Projenin temel bağımlılıklarını içeren requirements.txt dos

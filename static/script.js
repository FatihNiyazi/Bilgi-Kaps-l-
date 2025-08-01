
document.addEventListener('DOMContentLoaded', () => {

    const pdfForm = document.getElementById('pdfForm');
    const topicInput = document.getElementById('topicInput'); 
    const submitButton = document.getElementById('submitButton');
    
    
    const buttonText = submitButton ? submitButton.querySelector('.button-text') : null;
    const spinner = submitButton ? submitButton.querySelector('.spinner') : null;
    
   
    const topicButtons = document.querySelectorAll('.topic-btn');


    
    if (pdfForm) {
        pdfForm.addEventListener('submit', () => {
            
            if (topicInput.value.trim() === '') {
                alert('Lütfen bir konu girin!');
                event.preventDefault(); 
                return;
            }
            
            
            if (submitButton && buttonText && spinner) {
                submitButton.disabled = true;

                buttonText.classList.add('hidden');
                
                spinner.classList.remove('hidden');
            }
        });
    }



    topicButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();

            const topic = button.textContent;
            
            
            if (topicInput) {
                topicInput.value = topic;
            
                topicInput.focus();
            }
        });
    });

});
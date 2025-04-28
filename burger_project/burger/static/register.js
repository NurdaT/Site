document.getElementById("registrationForm").addEventListener("submit", async function(event) {
    console.log("Событие submit сработало");
    event.preventDefault();
});

document.getElementById("registrationForm").addEventListener("submit", async function(event) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);
    let isValid = true;

    document.querySelectorAll('.error').forEach(el => el.textContent = '');

    if (formData.get('username').trim().length < 3) {
        document.getElementById("usernameError").textContent = "Пайдаланушы аты кемінде 3 таңбадан тұруы керек";
        isValid = false;
    }
    if (formData.get('first_name').trim().length < 2) {
        document.getElementById("firstnameError").textContent = "Аты кемінде 2 таңбадан тұруы керек";
        isValid = false;
    }
    if (!formData.get('email').trim().includes('@') || !formData.get('email').trim().includes('.')) {
        document.getElementById("emailError").textContent = "Жарамды email енгізіңіз";
        isValid = false;
    }
    if (formData.get('password').trim().length < 6) {
        document.getElementById("passwordError").textContent = "Құпия сөз кемінде 6 таңбадан тұруы керек";
        isValid = false;
    }
    if (formData.get('password') !== formData.get('confirmPassword')) {
        document.getElementById("confirmPasswordError").textContent = "Құпия сөздер сәйкес келмейді";
        isValid = false;
    }

    if (isValid) {
        console.log('Метод формы:', form.method);
        console.log('Отправляемые данные:', [...formData]);

        try {
    const response = await fetch(form.action, {
        method: 'POST',
        headers: {
            'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams(formData)
    });

    const text = await response.text();
    console.log('Ответ сервера:', text); // Смотри, что приходит

    const result = JSON.parse(text);

    if (result.success) {
        window.location.href = result.redirect_url || '/success/';
    } else if (result.errors) {
        for (const [field, message] of Object.entries(result.errors)) {
            const errorElement = document.getElementById(`${field}Error`);
            if (errorElement) errorElement.textContent = message;
        }
    }
} catch (error) {
    console.error('Қате:', error);
    alert('Серверде қате орын алды. Өтінемін, әрекетті қайталаңыз.');
}
});



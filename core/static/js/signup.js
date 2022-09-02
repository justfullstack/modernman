"use strict";



console.log('Signup JS Loaded');


// variable declaration
const emailInputField = document.querySelector('#id_email');
const emailFeedbackField = document.querySelector('.email__feedback');
const submitBtn = document.querySelector('.submit__button');


// init
emailFeedbackField.style.display = 'none';




// functions 
const validateEmail = async function (email) {
    const res = await fetch('/auth/validate-email/', {
        body: JSON.stringify({ "email": `${email}` }),
        method: "POST"
    });

    const data = await res.json();




    if (data.email_valid !== true) {
        emailInputField.classList.remove('is-valid');
        emailInputField.classList.add('is-invalid');

        emailFeedbackField.classList = '';
        emailFeedbackField.classList = 'alert alert-danger';
        emailFeedbackField.textContent = `${email} doesn't look valid.`;

        submitBtn.classList.add('disabled');
        console.log("INVALID");
    } else {
        emailInputField.classList.remove('is-invalid');
        emailInputField.classList.add('is-valid');

        // emailFeedbackField.classList.remove('alert-info');
        // emailFeedbackField.classList.remove('alert-error');
        // emailFeedbackField.classList.add('alert-success');
        emailFeedbackField.classList = '';
        emailFeedbackField.classList = 'alert alert-success';
        emailFeedbackField.textContent = `${email} look good!`;

        submitBtn.classList.remove('disabled');
        console.log("VALID");

    };
}



// event listeners
// 1. very validation of email address format

emailInputField.addEventListener('keyup', (e) => {
    let emailVal = e.target.value


    if (emailVal.length < 1) {
        emailFeedbackField.style.display = 'none';
    } else {
        emailFeedbackField.style.display = 'block';
        emailFeedbackField.classList.add('alert-info');
        emailFeedbackField.textContent = `checking ${emailVal}...`
        validateEmail(`${emailVal}`);
    }
});




console.log('EOF Signup JS');























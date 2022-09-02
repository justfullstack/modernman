"use strict";



console.log('Signup JS Loaded');


// variable declaration
const emailInputField = document.querySelector('#id_email');
const emailFeedbackField = document.querySelector('.email__feedback');
const passwordOneInputField = document.querySelector('#id_password1');
const passwordOneFeedbackField = document.querySelector('.password1__feedback');


const submitBtn = document.querySelector('.submit__button');
// init
emailFeedbackField.style.display = 'none';
passwordOneFeedbackField.style.display = 'none';




// functions
// 1. validate email
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



// 2. validate password one
const validatePasswordOne = async function (pass) {
    const res = await fetch('/auth/validate-password1/', {
        body: JSON.stringify({ "password1": `${pass}` }),
        method: "POST"
    });

    const data = await res.json();

    console.log(data);


    if (data.password1_valid !== true) {
        passwordOneInputField.classList.remove('is-valid');
        passwordOneInputField.classList.add('is-invalid');

        passwordOneFeedbackField.classList = '';
        passwordOneFeedbackField.classList = 'alert alert-danger';
        passwordOneFeedbackField.textContent = `${data.message}`;

        submitBtn.classList.add('disabled');
        console.log("INVALID");
    } else {
        passwordOneInputField.classList.remove('is-invalid');
        passwordOneInputField.classList.add('is-valid');

        // passwordOneFeedbackField.classList.remove('alert-info');
        // passwordOneFeedbackField.classList.remove('alert-error');
        // passwordOneFeedbackField.classList.add('alert-success');
        passwordOneFeedbackField.classList = '';
        passwordOneFeedbackField.classList = 'alert alert-success';
        passwordOneFeedbackField.textContent = `${data.message} `;

        submitBtn.classList.remove('disabled');
        console.log("VALID");

    };



    if (data.message === 'OK password! You can do better though.') {
        passwordOneInputField.classList.remove('is-valid');
        passwordOneInputField.classList.add('is-invalid');

        passwordOneFeedbackField.classList = '';
        passwordOneFeedbackField.classList = 'alert alert-warning';
        passwordOneFeedbackField.textContent = `${data.message}`;

        submitBtn.classList.remove('disabled');
        console.log("WEAK");
    }
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



// 2. validate password quality
passwordOneInputField.addEventListener('keyup', (e) => {
    let pass1Val = e.target.value


    if (pass1Val.length < 1) {
        passwordOneFeedbackField.style.display = 'none';
    } else {
        passwordOneFeedbackField.style.display = 'block';
        passwordOneFeedbackField.classList.add('alert-info');
        passwordOneFeedbackField.textContent = `checking password...`
        validatePasswordOne(`${pass1Val}`);
    }
});


// 2. validate password match

console.log('EOF Signup JS');























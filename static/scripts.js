async function makeRequest(url, method, body) {
    let headers = {
        "X-Requested-With": 'XMLHttpRequest',
        "Content-Type": 'application/json'
    }

    let response = fetch(url, {
        method: method,
        headers: headers,
        body: body
    })

    return await response
}

async function register() {
    normalizeAllAfterValidity();

    let username = document.getElementById('inputUsername').value;
    let email = document.getElementById('inputEmail').value;
    let first_name = document.getElementById('inputFirstName').value;
    let last_name = document.getElementById('inputLastName').value;
    let password = document.getElementById('inputPassword1').value;
    let password2 = document.getElementById('inputPassword2').value;
    let response;

    if (password === password2) {
        response = await makeRequest('/api/users/', 'post', JSON.stringify({
            username: username,
            first_name: first_name,
            last_name: last_name,
            email: email,
            password: password
        }))
    }
    else {
        checkValidity("Passwords do not match", 'inputPassword2', 'password2-error')
        response = await makeRequest('/api/users/', 'post', JSON.stringify({
            username: username,
            first_name: first_name,
            last_name: last_name,
            email: email,
        }))
    }

    let data = await response.json()
    console.log(data)

    if(response.status === 201) {
        document.getElementById("success_register_message").innerHTML = 'We have sent a letter to your email';
        document.getElementById("success_register_message").style.visibility = 'visible';
    }
    else if(response.status === 400) {
        allRegisterCheckValidity(data)
        if (password === password2 && password !== null) {
            checkValidity(data.password, 'inputPassword1', 'password1-error')
        }
    }
    else {
        document.getElementById("success_register_message").innerHTML = 'Something went wrong. Try later';
        document.getElementById("success_register_message").style.visibility = 'visible';
    }
}
function allRegisterCheckValidity(data) {
    checkValidity(data.username, 'inputUsername', 'username-error')
    checkValidity(data.email, 'inputEmail', 'email-error')
    checkValidity(data.first_name, 'inputFirstName', 'firstname-error')
    checkValidity(data.last_name, 'inputLastName', 'lastname-error')
}

function checkValidity(error, inputId, textId) {
    if(error !== undefined) {
        document.getElementById(inputId).className = 'input-invalid';
        document.getElementById(textId).innerHTML = error;
        document.getElementById(textId).style.visibility = 'visible';
    }
}

function normalizeAllAfterValidity() {
    normalizeAfterValidity('inputUsername', 'username-error')
    normalizeAfterValidity('inputEmail', 'email-error')
    normalizeAfterValidity('inputFirstName', 'firstname-error')
    normalizeAfterValidity('inputLastName', 'lastname-error')
    normalizeAfterValidity('inputPassword1', 'password1-error')
    normalizeAfterValidity('inputPassword2', 'password2-error')
}

function normalizeAfterValidity(inputId, textId) {
    document.getElementById(inputId).className = 'form-control';
    document.getElementById(textId).innerHTML = null;
    document.getElementById(textId).style.visibility = 'hidden';
}

const confirmationText = document.getElementById("confirmation-text");

confirmationText.addEventListener("load", async function () {
    let currentUrl = document.URL;
    let queryStart = currentUrl.indexOf("?") + 1
    let params = currentUrl.slice(queryStart)

    alert(params);
});

async function confirmRegister() {
    let currentUrl = document.URL;
    let queryStart = currentUrl.indexOf("?") + 1
    let params = currentUrl.slice(queryStart)

    alert(params);
}

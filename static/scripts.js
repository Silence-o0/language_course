async function makeRequest(url, method, body, additionalHeaders) {
    let headers = {
        "X-Requested-With": 'XMLHttpRequest',
        "Content-Type": 'application/json',
        ...additionalHeaders,
    }

    let response = fetch(url, {
        method: method,
        headers: headers,
        body: body
    })

    return await response
}

async function makeRequestAuthorized(url, method, body, additionalHeaders) {
    await updateTokens();
    let accessToken = getAccessToken();

    let token = 'Bearer ' + accessToken;

    additionalHeaders = {
        'Authorization': token,
    }

    let response = await makeRequest(url, method, body, additionalHeaders);
    return await response;
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

async function profileLoad() {
    let response = await makeRequestAuthorized('/api/users/me', 'get');
    let data = await response.json()
    let time = localStorage.getItem("accessTokenTime");
    console.log(data)
}

function addMinutes(date, minutes) {
  date.setMinutes(date.getMinutes() + minutes);

  return date;
}

async function login() {
    normalizeAllAfterLoginValidity();
    let username = document.getElementById('inputUsername').value;
    let password = document.getElementById('inputPassword1').value;

    let response = await makeRequest('/api/jwt/create', 'post', JSON.stringify({
        username: username,
        password: password
    }))

    let data = await response.json()

    if(response.status === 200) {
        const accessDate = addMinutes(new Date(), 10);
        const refreshDate = addMinutes(new Date(), 24 * 60);

        localStorage.setItem("accessToken", data.access);
        localStorage.setItem("accessTokenTime", accessDate.toString());
        localStorage.setItem("refreshToken", data.refresh);
        localStorage.setItem("refreshTokenTime", refreshDate.toString());
        window.location.href = "/profile/me";
    }
    else {
        allLoginCheckValidity(data)
    }
}

function allLoginCheckValidity(data) {
    checkValidity(data.username, 'inputUsername', 'username-error')
    checkValidity(data.password, 'inputPassword1', 'password1-error')
    if (data.detail !== undefined) {
        checkValidity("Login or password is incorrect", 'inputPassword1', 'password1-error')
    }
}

function normalizeAllAfterLoginValidity() {
    normalizeAfterValidity('inputUsername', 'username-error')
    normalizeAfterValidity('inputPassword1', 'password1-error')
}

function getAccessToken() {
    if (checkAccessToken()) {
        console.log('True');
        return localStorage.getItem("accessToken");
    }
    else {
        console.log('False');
        localStorage.removeItem("accessToken");
        return undefined;
    }
}

function checkAccessToken() {
    const time = localStorage.getItem("accessTokenTime");
    const currentTime = new Date().toString();
    return currentTime < time;
}

async function updateTokens() {
    let accessToken = getAccessToken();
    if (accessToken === undefined) {
        const refresh = localStorage.getItem("refreshToken");
        if (new Date().toString() < localStorage.getItem("refreshTokenTime")) {
            let response = await makeRequest('/api/jwt/refresh', 'post', JSON.stringify({
                refresh: refresh,
            }));
            let data = await response.json();
            console.log(data);
            localStorage.setItem("accessToken", data.access);
            const accessDate = addMinutes(new Date(), 10);
            localStorage.setItem("accessTokenTime", accessDate.toString());
        }
        else {
            window.location.href = "/login";
            throw new Error('Not valid refresh token.')
        }
    }
}

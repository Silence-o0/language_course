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

    return await response;
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
            password: password,
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
    let currentUrl = document.URL;
    const arrayOfParams = currentUrl.split('/');
    let userId = arrayOfParams[arrayOfParams.length-1];
    let id;
    if (userId === 'me') {
        let role;
        console.log('me')
        let response = await makeRequestAuthorized('/api/users/me', 'get');
        let dataId = await response.json();
        if (dataId.groups[0] === 1) {
            role = 'student';
        }
        else if (dataId.groups[0] === 2) {
            role = 'teacher';
        }
        else if(dataId.groups[0] === 3) {
            role = 'admin';
        }
        id = dataId.id;
        localStorage.setItem("role", role);
        localStorage.setItem("user_id", id);
        document.getElementById('profile-me-logout').style.visibility = 'visible';
    }
    else {
        console.log(userId)
        id = userId;
    }
    await userProfileLoad(id);
}

async function userProfileLoad(id) {
    let url = '/api/students/' + id;
    let currentRole = 'student';
    let response = await makeRequestAuthorized(url, 'get');
    if (response.status !== 200) {
        currentRole = 'teacher';
        url = '/api/teachers/' + id;
        response = await makeRequestAuthorized(url, 'get');
        if (response.status !== 200) {
            currentRole = 'admin';
            url = '/api/admins/' + id;
            response = await makeRequestAuthorized(url, 'get');
            if (response.status !== 200) {
                throw new Error('404');
            }
        }
    }
    let data = await response.json()
    console.log(data)
    document.title = data.username;
    generateProfile(data, currentRole);
}

function generateProfile(data, currentRole) {
    addDiv('Name: ', data.first_name+' '+data.last_name);
    addDiv('Username: ', data.username);
    addDiv('Email: ', data.email);
    if (data.birth_date === null) {
        data.birth_date = '';
    }
    addDiv('Birthdate: ', data.birth_date);
    if (currentRole === 'teacher') {
        addDiv('Education: ', data.education);
        addDiv('Years of experience: ', data.years_experience);
    }
    else if (currentRole === 'admin') {
        addDiv('Position: ', data.position);
    }
}

function addDiv(profLabel, profValue){
    const cont = document.createElement("div");
    cont.classList.add("container-fluid");
    cont.classList.add("profile-info");

    const label = document.createElement("p");
    label.classList.add("profile-label");
    const labelNode = document.createTextNode(profLabel);
    const value = document.createElement("p");
    value.classList.add("profile-value");
    const valueNode = document.createTextNode(profValue);

    label.appendChild(labelNode);
    value.appendChild(valueNode);

    cont.appendChild(label);
    cont.appendChild(value);

    const mainDiv = document.getElementById('mainDiv');
    mainDiv.appendChild(cont);
}

function addDivWithLink(profLabel, profValue, link){
    const cont = document.createElement("div");
    cont.classList.add("container-fluid");
    cont.classList.add("profile-info");

    const label = document.createElement("p");
    label.classList.add("profile-label");
    const labelNode = document.createTextNode(profLabel);
    const value = document.createElement("a");
    value.classList.add("profile-value");
    value.href = link;
    const valueNode = document.createTextNode(profValue);

    label.appendChild(labelNode);
    value.appendChild(valueNode);

    cont.appendChild(label);
    cont.appendChild(value);

    const mainDiv = document.getElementById('mainDiv');
    mainDiv.appendChild(cont);
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
        return localStorage.getItem("accessToken");
    }
    else {
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
        const currentDate = Date.parse(new Date().toString());
        const expirationDate = Date.parse(localStorage.getItem("refreshTokenTime"));
        if (currentDate < expirationDate) {
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

async function logout() {
    localStorage.removeItem("accessToken");
    localStorage.removeItem("accessTokenTime");
    localStorage.removeItem("refreshToken");
    localStorage.removeItem("refreshTokenTime");
}

async function groupsListLoad() {
    let response = await makeRequestAuthorized('/api/groups/', 'get');
    let data = await response.json();
    console.log(data)

    for (const obj of data) {
        console.log(obj);

        let responseLang = await makeRequestAuthorized('/api/languages/'+obj.language, 'get');
        let dataLang = await responseLang.json();
        let text = dataLang.name + ' ' + obj.lang_level;
        addListElement(text, obj.id);
    }
}

const redirect = e => {
    console.log(e.target.id);
    window.location.href = document.URL+e.target.id;
}

function addListElement(text, id) {
    let cont = document.createElement("div");
    cont.setAttribute('id', id)
    cont.classList.add("container");
    cont.classList.add("list-element");
    cont.addEventListener('click', redirect);
    console.log(cont.id);


    const groupName = document.createElement("p");
    groupName.classList.add("profile-value");
    const valueNode = document.createTextNode(text);

    groupName.appendChild(valueNode);
    cont.appendChild(groupName);

    const mainDiv = document.getElementById('mainDiv');
    mainDiv.appendChild(cont);
}

async function listLoad() {
    const url = document.URL;
    const index = url.indexOf('groups');
    const result = url.slice(index);

    console.log(result);
    const arrayOfParams = result.split('/');
    console.log(arrayOfParams);
    const role = localStorage.getItem("role");
    const user_id = localStorage.getItem("user_id");

    switch (arrayOfParams.length) {
        case 2:
            document.title = 'Groups';
            await groupsListLoad();
            break;
        case 3:
            if (role === 'admin' || role === 'teacher') {
                await groupInfoListLoad(arrayOfParams[1]);
            }
            else if (role === 'student') {
                console.log('stud')
                window.location.href = "/groups/"+arrayOfParams[1]+'/'+user_id;
            }
            break;
        case 4:
            if (role === 'student') {
                if (arrayOfParams[2] !== user_id) {
                    window.location.href = "/groups/"+arrayOfParams[1]+'/'+user_id;
                }
                await studentInfoListLoad(arrayOfParams[1], arrayOfParams[2]);
            }
            else if (role === 'admin' || role === 'teacher') {
                await studentInfoListLoad(arrayOfParams[1], arrayOfParams[2]);
            }
            break;
    }
}

async function groupInfoListLoad(group_id) {
    let response = await makeRequestAuthorized('/api/groups/'+group_id, 'get');
    let data = await response.json();
    console.log(data);

    let responseLang = await makeRequestAuthorized('/api/languages/'+data.language, 'get');
    let dataLang = await responseLang.json();
    console.log(dataLang);
    let name = dataLang.name + ' ' +  data.lang_level;
    console.log(name);
    document.title = name;

    const mainLabel = document.createElement("p");
    mainLabel.classList.add("page-name-label");
    const labelNode = document.createTextNode(name);
    mainLabel.appendChild(labelNode);
    const mainDiv = document.getElementById('mainDiv');
    mainDiv.appendChild(mainLabel);

    let responseTeacher = await makeRequestAuthorized('/api/teachers/'+data.teacher, 'get');
    let dataTeacher = await responseTeacher.json();
    console.log(dataTeacher);

    addDivWithLink('Teacher: ', dataTeacher.first_name + ' ' + dataTeacher.last_name, '/profile/'+data.teacher);
    let responseStudent = await makeRequestAuthorized('/api/students/?group_id='+group_id, 'get');
    let dataStudent = await responseStudent.json();
    console.log(dataStudent)

    for (const obj of dataStudent) {
        console.log(obj);
        addListElement(obj.first_name + ' ' + obj.last_name, obj.user_id);
    }
}

async function studentInfoListLoad(group_id, student_id) {
    const role = localStorage.getItem("role");
    let name;
    let link;
    if (role === 'student') {
        let responseGroup = await makeRequestAuthorized('/api/groups/'+group_id, 'get');
        let dataGroup = await responseGroup.json();

        let responseTeacher = await makeRequestAuthorized('/api/teachers/'+dataGroup.teacher, 'get');
        let dataTeacher = await responseTeacher.json();
        link = '/profile/' + dataGroup.teacher;

        let responseLang = await makeRequestAuthorized('/api/languages/'+dataGroup.language, 'get');
        let dataLang = await responseLang.json();
        console.log(dataLang)

        document.title = dataLang.name + ' ' + dataGroup.lang_level;
        name = dataTeacher.first_name + ' ' + dataTeacher.last_name;
    }
    else {
        let response = await makeRequestAuthorized('/api/students/'+student_id, 'get');
        let data = await response.json();
        link = '/profile/' + student_id;
        name = data.first_name + ' ' +  data.last_name;
        document.title = data.username;
    }
    const mainLabel = document.createElement("a");
    mainLabel.classList.add("page-name-label");
    const labelNode = document.createTextNode(name);
    mainLabel.appendChild(labelNode);
    mainLabel.href = link;
    const mainDiv = document.getElementById('mainDiv');
    mainDiv.appendChild(mainLabel);

    const requestUrl = '/api/marks/?student_id=' + student_id + "&group_id=" + group_id;
    let responseMark = await makeRequestAuthorized(requestUrl, 'get');
    let dataMark = await responseMark.json();
    console.log(dataMark)

    for (const obj of dataMark) {
        console.log(obj);
        if (obj.description === '' || obj.description === null) {
            addListElement(obj.mark, obj.id);
        }
        else {
            addListElement(obj.mark + " - " + obj.description, obj.id);
        }
    }
    if (role !== 'student') {
        const addElement = document.createElement("a");
        addElement.classList.add("profile-value");
        addElement.href = document.URL + 'add-mark';
        const textNode = document.createTextNode('Add mark');
        addElement.appendChild(textNode);
        mainDiv.appendChild(addElement);
    }
}

async function markManage() {
    const url = document.URL;
    const index = url.indexOf('groups');
    const result = url.slice(index);

    console.log(result);
    const arrayOfParams = result.split('/');
    console.log(arrayOfParams);

    if (arrayOfParams[arrayOfParams.length - 2] === 'add-mark') {
        document.title = 'New mark';
        await newMark();
    }
    else {
        document.title = 'Edit mark';
        await manageMark(arrayOfParams[3]);
    }
}

async function newMark() {
    document.getElementById('add-change-btn').innerHTML = 'Add';
    document.getElementById('delete-btn').style.display = "none";
}

async function addEditMark() {
    const url = document.URL;
    const index = url.indexOf('groups');
    const result = url.slice(index);

    console.log(result);
    const arrayOfParams = result.split('/');
    console.log(arrayOfParams);

    if (arrayOfParams[arrayOfParams.length - 2] === 'add-mark') {
        await addNewMark(arrayOfParams[1], arrayOfParams[2]);
    }
    else {
        await editMark(arrayOfParams[1], arrayOfParams[2], arrayOfParams[3]);
    }
}

async function addNewMark(group_id, student_id) {
    let mark = document.getElementById('inputMark').value;
    let description = document.getElementById('inputDescription').value;

    let response = await makeRequestAuthorized('/api/marks/', 'post', JSON.stringify({
        mark: mark,
        description: description,
        student_id: student_id,
        group_id: group_id
    }));

    if (response.status === 201) {
        window.location.href = "/groups/" + group_id + "/" + student_id;
    }
    else {
        if (mark === '') {
            checkValidity('This field can not be blank.', 'inputMark', 'mark-error')
        }
        alert(response.status);
    }
}

async function editMark(gr_id, stud_id, mark_id) {
    const mark = document.getElementById('inputMark').value;
    const description = document.getElementById('inputDescription').value;

    let response = await makeRequestAuthorized('/api/marks/'+mark_id+'/', 'put', JSON.stringify({
        mark: mark,
        description: description,
    }));

    let data = await response.json();
    console.log(data)

    if (response.status === 200) {
        window.location.href = "/groups/" + gr_id + "/" + stud_id;
    }
    else if (response.status === 400) {
        checkValidity(data.mark, 'inputMark', 'mark-error')
    }
    else {
        alert(response.status);
    }
    console.log(response.status)
}

async function deleteMark() {
    const url = document.URL;
    const index = url.indexOf('groups');
    const result = url.slice(index);

    console.log(result);
    const arrayOfParams = result.split('/');
    console.log(arrayOfParams);

    let response = await makeRequestAuthorized('/api/marks/'+arrayOfParams[3], 'delete');
    if (response.status === 204) {
        window.location.href = "/groups/" + arrayOfParams[1] + "/" + arrayOfParams[2];
    }
    else {
        alert(response.status)
    }
}

async function manageMark(mark_id) {
    document.getElementById('add-change-btn').innerHTML = 'Edit';
    document.getElementById('delete-btn').innerHTML = 'Delete';

    let response = await makeRequestAuthorized('/api/marks/'+mark_id, 'get');
    let data = await response.json();

    document.getElementById('inputMark').value = data.mark;
    document.getElementById('inputDescription').value = data.description;
}

const API_BASE = "http://localhost:8000/auth/";  // آدرس API

let mobileNumber = "";

// ارسال OTP
function sendOTP() {
    mobileNumber = document.getElementById("mobile").value;
    fetch(API_BASE + "send-otp/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mobile: mobileNumber })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert("کد ارسال شد.");
            document.getElementById("step1").style.display = "none";
            document.getElementById("step2").style.display = "block";
        } else {
            alert("خطا در ارسال کد!");
        }
    });
}

// تأیید OTP
function verifyOTP() {
    let otp = document.getElementById("otp").value;
    fetch(API_BASE + "verify-otp/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mobile: mobileNumber, otp: otp })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert("کد تأیید شد.");
            document.getElementById("step2").style.display = "none";
            document.getElementById("step3").style.display = "block";
        } else {
            alert("کد نادرست است!");
        }
    });
}

// ثبت‌نام
function register() {
    let name = document.getElementById("name").value;
    let password = document.getElementById("password").value;
    
    fetch(API_BASE + "register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mobile: mobileNumber, name: name, password: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert("ثبت‌نام موفق!");
            document.getElementById("step3").style.display = "none";
            document.getElementById("loginForm").style.display = "block";
        } else {
            alert("خطا: " + data.error);
        }
    });
}

// ورود
function login() {
    let loginMobile = document.getElementById("loginMobile").value;
    let loginPassword = document.getElementById("loginPassword").value;

    fetch(API_BASE + "login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mobile: loginMobile, password: loginPassword })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert("ورود موفق!");
            document.getElementById("loginForm").style.display = "none";
            document.getElementById("logoutBtn").style.display = "block";
        } else {
            alert("خطا در ورود!");
        }
    });
}

// خروج
function logout() {
    fetch(API_BASE + "logout/", {
        method: "POST",
        headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert("خروج موفق!");
            document.getElementById("logoutBtn").style.display = "none";
            document.getElementById("step1").style.display = "block";
        }
    });
}

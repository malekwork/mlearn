const API_BASE = "http://localhost:8000/auth/";

let mobileNumber = "";

// ارسال OTP
function sendOTP() {
    mobileNumber = document.getElementById("mobile").value;
    localStorage.setItem("mobile", mobileNumber);
    fetch(API_BASE + "send-otp/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ "mobile": mobileNumber.toString() })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert("کد ارسال شد.");
            window.location.href = "/verify-otp/";
        } else {
            alert("خطا در ارسال کد!");
        }
    });
}

// تأیید OTP
function verifyOTP() {
    let otp = document.getElementById("otp").value;
    let mobile = localStorage.getItem("mobile");
    if (!mobile) {
        alert("شماره موبایل موجود نیست!");
        return;
    }
    fetch(API_BASE + "verify-otp/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ "mobile": mobile, otp: otp })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert("کد تأیید شد.");
            window.location.href = "/register/";
        } else {
            alert("کد نادرست است!");
        }
    });
}


function register() {
    let name = document.getElementById("name").value;
    let password = document.getElementById("password").value;
    let mobile = localStorage.getItem("mobile");
    
    fetch(API_BASE + "register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ mobile: mobile, name: name, password: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert("ثبت‌نام موفق!");
            window.location.href = "/login/";
        } else {
            alert("خطا: " + data.error);
        }
    });
}


function login() {
    console.log("login...");

    let loginMobile = $("#loginMobile").val();
    let loginPassword = $("#loginPassword").val();

    let csrfToken = $("input[name='csrfmiddlewaretoken']").val();
    
    $.ajax({
        url: API_BASE + "login/",
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken
        },
        data: JSON.stringify({
            "mobile": loginMobile,
            "password": loginPassword
        }),
        success: function(data) {
            if (data.message) {
                alert("ورود موفق!");
                window.location.href = "/";
            } else {
                alert("خطا در ورود!");
            }
        },
        error: function(xhr, status, error) {
            alert("خطا در برقراری ارتباط با سرور!");
        }
    });
}


// function login() {
//     let loginMobile = document.getElementById("loginMobile").value;
//     let loginPassword = document.getElementById("loginPassword").value;

//     fetch(API_BASE + "login/", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
        
//         body: JSON.stringify({ mobile: loginMobile, password: loginPassword })
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.message) {
//             alert("ورود موفق!");
//             window.location.href = "/";
//         } else {
//             alert("خطا در ورود!");
//         }
//     });
// }

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

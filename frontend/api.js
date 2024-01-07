// $.ajax({
//     type: 'GET',
//       dataType:"jsonp",
//     url: 'https://jsonplaceholder.typicode.com/todos/1',
//     headers:{         
//         'Authorization' : 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhcHBWZXIiOiIwLjAuMCIsImV4cCI6NDcyNjM4OTEyMiwibG9jYWxlIjoiIiwibWFzdGVyVmVyIjoiIiwicGxhdGZvcm0iOiIiLCJwbGF0Zm9ybVZlciI6IiIsInVzZXJJZCI6IiJ9.QIZbmB5_9Xlap_gDhjETfMI6EAmR15yBtIQkWFWJkrg',
//     },
//     success: function (data, status, xhr) {
//       console.log('data: ', data);
//     }
//   });

const showPopupBtn = document.querySelector(".login-btn");
const hidePopupBtn = document.querySelector(".form-popup .close-btn");
// const formPopup = document.querySelector(".form-popup");
// const loginSignupLink = document.querySelectorAll(".form-box .bottom-link a");

// Show form popup
showPopupBtn.addEventListener("click", () =>{
  document.body.classList.toggle("show-popup");
});

// Hide form popup
hidePopupBtn.addEventListener("click", () => showPopupBtn.click());

const showPopupBtn1 = document.querySelector(".button");
const hidePopupBtn1 = document.querySelector(".thng-tin-nhn-vin-W2Z .close-btn");
// const formPopup = document.querySelector(".form-popup");
// const loginSignupLink = document.querySelectorAll(".form-box .bottom-link a");

// Show form popup
showPopupBtn1.addEventListener("click", () =>{
  document.body.classList.toggle("show-popup");
});

// Hide form popup
hidePopupBtn1.addEventListener("click", () => showPopupBtn1.click());

// loginSignupLink.forEach(link =>{
//   link.addEventListener("click", (e) =>{
//     e.preventDefault();
//     formPopup.classList[link.id === "signup-link" ? 'add': 'remove'] ("show-signup");
//   });

// })

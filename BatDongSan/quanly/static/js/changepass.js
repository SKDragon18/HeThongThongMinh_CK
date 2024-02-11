// script.js

// Get the elements from the document
const oldPassword = document.getElementById("old-password");
const newPassword = document.getElementById("new-password");
const confirmPassword = document.getElementById("confirm-password");
const showPassword = document.querySelectorAll(".show-password");
const submitButton = document.getElementById("submit-button");

// Add event listeners to the show password icons
showPassword.forEach((icon) => {
  icon.addEventListener("click", () => {
    // Toggle the type attribute of the input element
    const input = icon.previousElementSibling; // The input element is the previous sibling of the icon element
    if (input.type === "password") {
      input.type = "text";
      icon.innerHTML = '<i class="fas fa-eye-slash"></i>'; // Change the icon to eye-slash
    } else {
      input.type = "password";
      icon.innerHTML = '<i class="fas fa-eye"></i>'; // Change the icon to eye
    }
  });
});

// Add event listener to the submit button
submitButton.addEventListener("click", (e) => {
  // Prevent the default action of the form
  e.preventDefault();

  // Validate the input values
  if (!oldPassword.value || !newPassword.value || !confirmPassword.value) {
    // If any of the inputs is empty, alert the user
    alert("Vui lòng nhập đầy đủ thông tin");
  } else if (newPassword.value !== confirmPassword.value) {
    // If the new password and confirm password do not match, alert the user
    alert("Mật khẩu mới và xác nhận mật khẩu không khớp");
  } else if (newPassword.value.length < 8) {
    // If the new password is less than 8 characters, alert the user
    alert("Mật khẩu mới phải có ít nhất 8 ký tự");
  } else {
    // If everything is valid, send a post request to the server with the input values
    fetch("/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        oldPassword: oldPassword.value,
        newPassword: newPassword.value,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        // Handle the response from the server
        if (data.success) {
          // If the server returns success, alert the user and redirect to another page
          alert(data.message);
          window.location.href = data.redirectUrl; // The url to redirect after changing password successfully
        } else {
          // If the server returns error, alert the user
          alert(data.message);
        }
      })
      .catch((error) => {
        // Handle any network error
        console.error(error);
        alert("Có lỗi xảy ra, vui lòng thử lại sau");
      });
  }
});

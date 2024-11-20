function validateForm() {
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const seats = document.getElementById('seats').value;

    if (name === "" || email === "" || phone === "" || seats === "") {
        alert("All fields are required!");
        return false;
    }

    if (!/^[0-9]{10}$/.test(phone)) {
        alert("Please enter a valid 10-digit phone number.");
        return false;
    }

    return true;
}

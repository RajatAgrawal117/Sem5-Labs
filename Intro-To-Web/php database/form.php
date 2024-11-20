<?php
$servername = "localhost";
$username = "root";
$password = "1234";
$dbname = "college";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $firstName = htmlspecialchars($_POST['first_name']);

    $email = htmlspecialchars($_POST['email']);  
    $password = $_POST['password'];  


    $sql = "INSERT INTO user (Name, Email, Password) VALUES ('$firstName', '$email', '$password')";

    if ($conn->query($sql) === TRUE) {
        echo "New record created successfully";
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }
}

$conn->close();
?>
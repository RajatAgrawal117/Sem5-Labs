<?php
$servername = "localhost";  // Your MySQL server host name
$username = "root";     // Your MySQL username
$password = "1234";     // Your MySQL password
$dbname = "college"; 

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>

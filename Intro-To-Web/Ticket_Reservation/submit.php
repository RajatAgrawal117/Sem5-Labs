<?php
include 'db_config.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = $_POST['name'];
    $email = $_POST['email'];
    $phone = $_POST['phone'];
    $seats = $_POST['seats'];

    $sql = "INSERT INTO train_users (name, email, phone, seats) VALUES ('$name', '$email', '$phone', '$seats')";

    if ($conn->query($sql) === TRUE) {
        echo "Reservation successful. <a href='list_users.php'>View Reservations</a>";
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }

    $conn->close();
}
?>

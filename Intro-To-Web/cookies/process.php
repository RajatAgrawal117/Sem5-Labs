<?php
session_start();

// Set session timeout duration (10 seconds)
$session_timeout = 10;

// Check if session variable is set
if (isset($_SESSION['last_activity'])) {
    // Calculate the session's "age"
    $session_duration = time() - $_SESSION['last_activity'];

    // If session has expired, destroy it and redirect to the form
    if ($session_duration > $session_timeout) {
        session_unset(); // Unset session variables
        session_destroy(); // Destroy session
        echo "<div style='text-align:center; padding:20px;'>
                <h2>Session expired. Please submit the form again.</h2>
                <a href='index.html'>Go back to form</a>
              </div>";
        exit();
    }
}

// Update last activity time stamp
$_SESSION['last_activity'] = time();

// Check if the form has been submitted
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = htmlspecialchars($_POST['name']); // Get the form data

    // Set a cookie that expires in 5 seconds
    setcookie("userName", $name, time() + 5, "/");

    // Set session variable to store the name
    $_SESSION['name'] = $name;

    // Display a message and redirect to the form page
    echo "<div style='text-align:center; padding:20px;'>
            <h2>Hi, $name!</h2>
            <p>Session started. You will be redirected shortly...</p>
          </div>";
    // Redirect to the form page after 6 seconds
    header("refresh:6;url=index.html");
    exit();
}

// Check if the session is still active and display the stored name
if (isset($_SESSION['name'])) {
    echo "<div style='text-align:center; padding:20px;'>
            <h2>Welcome back, " . $_SESSION['name'] . "!</h2>
          </div>";
}
?>

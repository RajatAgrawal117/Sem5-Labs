<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Train Ticket Reservations</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <div class="container">
        <h1>Existing Reservations</h1>

        <?php
        include 'db_config.php';

        $sql = "SELECT id, name, email, phone, seats FROM train_users";
        $result = $conn->query($sql);

        if ($result->num_rows > 0) {
            echo "<table class='styled-table'>";
            echo "<thead><tr><th>ID</th><th>Name</th><th>Email</th><th>Phone</th><th>Seats</th></tr></thead>";
            echo "<tbody>";
            while ($row = $result->fetch_assoc()) {
                echo "<tr><td>" . $row["id"] . "</td><td>" . $row["name"] . "</td><td>" . $row["email"] . "</td><td>" . $row["phone"] . "</td><td>" . $row["seats"] . "</td></tr>";
            }
            echo "</tbody></table>";
        } else {
            echo "<p>No reservations found.</p>";
        }

        $conn->close();
        ?>
    </div>
</body>
</html>

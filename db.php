<?php
$servername = "localhost";
$username = "root";
$password = "";   // agar password set nahi hai to empty
$database = "test"; // ya jo bhi DB name ho

$conn = new mysqli($servername, $username, $password, $database);

if ($conn->connect_error) {
    die("Connection Failed: " . $conn->connect_error);
}
echo "Database Connected Successfully!";
?>

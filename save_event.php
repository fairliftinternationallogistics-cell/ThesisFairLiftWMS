<?php
// save_event.php
// Default config for XAMPP: host=localhost, user=root, pass="", db=fairlift_db
$host = 'localhost';
$user = 'root';
$pass = '';
$db   = 'fairlift_db';

function respond($msg) { echo $msg; exit; }

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    respond('error: invalid method');
}

$title = isset($_POST['title']) ? trim($_POST['title']) : '';
$description = isset($_POST['description']) ? trim($_POST['description']) : '';
$start = isset($_POST['start']) ? trim($_POST['start']) : '';
$end = isset($_POST['end']) ? trim($_POST['end']) : '';
$type = isset($_POST['type']) ? trim($_POST['type']) : '';

if ($title === '' || $start === '') {
    respond('error: missing fields');
}

// Normalize datetime-local input to MySQL datetime format (replace T with space if present)
$start = str_replace('T', ' ', $start);
$end = $end ? str_replace('T', ' ', $end) : null;

$conn = new mysqli($host, $user, $pass, $db);
if ($conn->connect_error) {
    respond('error: db conn');
}

$stmt = $conn->prepare('INSERT INTO events (title, description, start_datetime, end_datetime, type) VALUES (?, ?, ?, ?, ?)');
if (!$stmt) respond('error: prepare');
$stmt->bind_param('sssss', $title, $description, $start, $end, $type);
if ($stmt->execute()) {
    respond('success');
} else {
    respond('error: exec');
}
?>
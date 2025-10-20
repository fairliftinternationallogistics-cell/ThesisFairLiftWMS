<?php
// get_events.php - returns events in FullCalendar friendly format
header('Content-Type: application/json; charset=utf-8');
$host = 'localhost';
$user = 'root';
$pass = '';
$db   = 'fairlift_db';

$conn = new mysqli($host, $user, $pass, $db);
if ($conn->connect_error) {
    echo json_encode([]);
    exit;
}

$sql = "SELECT id, title, description, start_datetime AS start, end_datetime AS end, type FROM events ORDER BY start_datetime ASC";
$res = $conn->query($sql);
$out = [];
if ($res) {
    while ($row = $res->fetch_assoc()) {
        $out[] = [
            'id' => $row['id'],
            'title' => $row['title'],
            'start' => $row['start'],
            'end' => $row['end'],
            'extendedProps' => ['description' => $row['description'], 'type' => $row['type']]
        ];
    }
}

echo json_encode($out);
?>
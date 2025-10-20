<?php
// fetch_parcels.php - returns JSON array of parcels
header('Content-Type: application/json; charset=utf-8');
require 'db.php';

$sql = "SELECT * FROM parcels ORDER BY arrival_date DESC, id DESC";
if ($result = $mysqli->query($sql)) {
    $rows = [];
    while ($row = $result->fetch_assoc()) {
        $rows[] = $row;
    }
    echo json_encode($rows);
    $result->free();
} else {
    http_response_code(500);
    echo json_encode(['error' => $mysqli->error]);
}
$mysqli->close();
?>

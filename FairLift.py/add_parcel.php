<?php
// add_parcel.php - accepts JSON POST and inserts a parcel
header('Content-Type: application/json; charset=utf-8');
require 'db.php';

$input = json_decode(file_get_contents('php://input'), true);
if (!$input) {
    echo json_encode(['success'=>false,'error'=>'Invalid JSON']);
    exit;
}

// basic sanitation
$tracking_number = $mysqli->real_escape_string(trim($input['tracking_number'] ?? ''));
$size = $mysqli->real_escape_string(trim($input['size'] ?? 'S'));
$weight = floatval($input['weight'] ?? 0);
$arrival_date = $mysqli->real_escape_string(trim($input['arrival_date'] ?? date('Y-m-d')));
$destination = $mysqli->real_escape_string(trim($input['destination'] ?? ''));
$status = $mysqli->real_escape_string(trim($input['status'] ?? 'stored'));
$location_rack = $mysqli->real_escape_string(trim($input['location_rack'] ?? ''));

if ($tracking_number === '' || $destination === '') {
    echo json_encode(['success'=>false,'error'=>'Missing tracking_number or destination']);
    exit;
}

$sql = "INSERT INTO parcels (tracking_number, size, weight, arrival_date, destination, status, location_rack)
        VALUES (?, ?, ?, ?, ?, ?, ?)";
$stmt = $mysqli->prepare($sql);
if (!$stmt) {
    echo json_encode(['success'=>false,'error'=>$mysqli->error]);
    exit;
}
$stmt->bind_param('ssdssss', $tracking_number, $size, $weight, $arrival_date, $destination, $status, $location_rack);
$ok = $stmt->execute();
if ($ok) {
    echo json_encode(['success'=>true,'id'=>$stmt->insert_id]);
} else {
    echo json_encode(['success'=>false,'error'=>$stmt->error]);
}
$stmt->close();
$mysqli->close();
?>

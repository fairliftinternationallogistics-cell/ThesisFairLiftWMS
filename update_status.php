<?php
// update_status.php - accepts JSON POST {id, status} and updates record
header('Content-Type: application/json; charset=utf-8');
require 'db.php';

$input = json_decode(file_get_contents('php://input'), true);
if (!$input) {
    echo json_encode(['success'=>false,'error'=>'Invalid JSON']);
    exit;
}
$id = intval($input['id'] ?? 0);
$status = $mysqli->real_escape_string(trim($input['status'] ?? ''));

if ($id <= 0 || $status === '') {
    echo json_encode(['success'=>false,'error'=>'Missing id or status']);
    exit;
}

$sql = "UPDATE parcels SET status = ? WHERE id = ?";
$stmt = $mysqli->prepare($sql);
if (!$stmt) {
    echo json_encode(['success'=>false,'error'=>$mysqli->error]);
    exit;
}
$stmt->bind_param('si', $status, $id);
$ok = $stmt->execute();
if ($ok) {
    echo json_encode(['success'=>true,'affected'=>$stmt->affected_rows]);
} else {
    echo json_encode(['success'=>false,'error'=>$stmt->error]);
}
$stmt->close();
$mysqli->close();
?>

<?php
header('Content-type: application/json');

if(isset($_GET['id'])) {
    $id = $_GET['id'];
}
else{
    $id = "No enviado";
}

$respuesta = array();
$respuesta["respuesta"] = [];
$respuesta["respuesta"]["id"] = $id;
$respuesta["respuesta"]["sonar"] = true;
$respuesta["status"] = "ok";

echo json_encode($respuesta);

?>
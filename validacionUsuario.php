<?php
session_start();
$User=$_POST['User'];
$Pass=$_POST['Pass'];

$conexionValidacion = mysqli_connect("localhost","root","MOOzwDvIrY[C0i]r","iberasis__bbdd");
$consultaValidacion = "SELECT * FROM usuario WHERE Nombre_usuario='$User' AND Contrasena_usuario='$Pass' AND idUsuario LIKE '%IB_AS%'";

$resultadoValidacion = mysqli_query($conexionValidacion,$consultaValidacion);

$filas=mysqli_num_rows($resultadoValidacion);

if ($filas>0) {
    $_SESSION['User']=$User;
     header("location:index.php");

}else{
    header("location:404.php");
}

mysqli_free_result($resultadoValidacion);
mysqli_close($conexion);
?>


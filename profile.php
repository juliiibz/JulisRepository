<!DOCTYPE html>
<html>
<head>
	<?php include('include/head.php');?>
	<link rel="stylesheet" type="text/css" href="src/plugins/cropperjs/dist/cropper.css">
</head>
<body>
	<?php include('include/header.php'); ?>
	<?php include('include/sidebar.php'); ?>
	<div class="main-container">
		<div class="pd-ltr-20 customscroll customscroll-10-p height-100-p xs-pd-20-10">
			<div class="min-height-200px">
				<div class="page-header">
					<div class="row">
						<div class="col-md-12 col-sm-12">
							<div class="title">
								<h4>Profile</h4>
							</div>
							<nav aria-label="breadcrumb" role="navigation">
								<ol class="breadcrumb">
									<li class="breadcrumb-item"><a href="index.php">Home</a></li>
									<li class="breadcrumb-item active" aria-current="page">Mi perfil</li>
								</ol>
							</nav>
						</div>
					</div>
				</div>
				<div class="bg-white pd-20 box-shadow border-radius-5 mb-30">
							<div class="profile-photo">
								<?php
									$UsuarioLogeado = $_SESSION['User'];
									include("conexion_bbdd.php");

									$consultaUsuarioLogeado = "SELECT * FROM usuario WHERE Nombre_usuario = '$UsuarioLogeado'";
									$resultadoUsuarioLogeado = mysqli_query($conexion, $consultaUsuarioLogeado);

									while($rowUsuarioLogeado = mysqli_fetch_array($resultadoUsuarioLogeado)){
										echo '<img src="data:image;base64, '.base64_encode($rowUsuarioLogeado['Imagen']).'" alt="Imagen" class="avatar-photo">';
										$nombreUsuarioLogeado = $rowUsuarioLogeado['Nombre_usuario'];
										$correoUsuarioLogeado = $rowUsuarioLogeado['Correo_electronico'];
										$idUsuarioLogeado = $rowUsuarioLogeado['idUsuario'];
										$fechaUsuarioLogeado = $rowUsuarioLogeado['Fecha_registro'];
								}
								?>
							</div>
							
							<h5 class="text-center"><?php echo ($_SESSION['User']); ?></h5>
							<p class="text-center text-muted">Grupo de IberAsis</p>
							<div class="profile-info">
								<h5 class="mb-20 weight-500">Información del perfil:</h5>
								<ul>
									<li>
										<span>Nombre de usuario:</span>
										<?php echo $nombreUsuarioLogeado; ?>
									</li>
									<li>
										<span>Correo Electrónico:</span>
										<?php echo $correoUsuarioLogeado; ?>
									</li>
									
									<li>
										<span>Identificador:</span>
										<?php echo $idUsuarioLogeado; ?>
									</li>
									<li>
										<span>Fecha de registro:</span>
										<?php echo $fechaUsuarioLogeado; ?>
									</li>
								</ul>
							</div>
				</div>
			</div>
		</div>
	</div>
	<?php include('include/script.php'); ?>
	<script src="src/plugins/cropperjs/dist/cropper.js"></script>
</body>
</html>
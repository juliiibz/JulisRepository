<!-------------------- HEADER -------------------->	
<?php session_start();?>
	<div class="pre-loader"></div>
	<div class="header clearfix">
		<div class="header-right">
			<div class="brand-logo">
				<a href="index.php">
					<img src="vendors/images/logo.png" alt="" class="mobile-logo">
				</a>
			</div>
			<div class="menu-icon">
				<span></span>
				<span></span>
			</div>
			<div class="user-info-dropdown">
				<div class="dropdown">
					<a class="dropdown-toggle" href="#" role="button" data-toggle="dropdown">
						<?php
									$UsuarioLogeado = $_SESSION['User'];
									include("conexion_bbdd.php");

									$consultaUsuarioLogeado = "SELECT * FROM usuario WHERE Nombre_usuario = '$UsuarioLogeado'";
									$resultadoUsuarioLogeado = mysqli_query($conexion, $consultaUsuarioLogeado);

									while($rowUsuarioLogeado = mysqli_fetch_array($resultadoUsuarioLogeado)){
										echo '<img src="data:image;base64, '.base64_encode($rowUsuarioLogeado['Imagen']).'" alt="Imagen" class="user-icon">';
								}
						?>
						<span class="user-name"><?php echo ($_SESSION['User']); ?></span>
					</a>
					<div class="dropdown-menu dropdown-menu-right">
						<a class="dropdown-item" href="profile.php"><i class="fa fa-user"></i>Mi perfil</a>
						<a class="dropdown-item" href="login.php"><i class="fa fa-sign-out" aria-hidden="true"></i> Cerrar sesión</a>
					</div>
				</div>
			</div>
		</div>
	</div>
<!-------------------- HEADER -------------------->	
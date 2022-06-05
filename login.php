<!DOCTYPE html>
<html>
<head>
	<?php include('include/head.php'); ?>
</head>
<body>	
	<form action="validacionUsuario.php" method="post">
		<div class="login-wrap customscroll d-flex align-items-center flex-wrap justify-content-center pd-20">
			<div class="login-box bg-white box-shadow pd-30 border-radius-5">
				<img src="vendors/images/logo2.png" alt="login" class="login-img">
					<h2 class="text-center mb-30">Iniciar sesión</h2>
					<div class="input-group custom input-group-lg">
						<input type="text" class="form-control" placeholder="Ingrese su usuario" name="User">
						<div class="input-group-append custom">
							<span class="input-group-text"><i class="fa fa-user" aria-hidden="true"></i></span>
						</div>
					</div>
					<div class="input-group custom input-group-lg">
						<input type="password" class="form-control" placeholder="Ingrese su contraseña" name="Pass">
						<div class="input-group-append custom">
							<span class="input-group-text"><i class="fa fa-lock" aria-hidden="true"></i></span>
						</div>
					</div>
					<div class="row">
						<div class="col-sm-6">
							<div class="input-group">
								<input class="btn btn-outline-primary btn-lg btn-block" type="submit" value="Iniciar sesión">
							</div>
						</div>
					</div>
			</div>
		</div>
	</form>
		<?php include('include/script.php'); ?>
</body>
</html>
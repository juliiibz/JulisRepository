<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
	<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.3.1/dist/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
	<?php include('include/head.php'); ?>
</head>
<body>	
	<?php include('include/header.php'); ?>
	<?php include('include/sidebar.php'); ?>
	<div class="main-container">
		<div class="pd-ltr-20 customscroll customscroll-10-p height-100-p xs-pd-20-10">

			<!-------------------- GRÁFICOS BARRA PROGRESO -------------------->
			<div class="row clearfix progress-box">

			<!-- Informes de vida laboral verídicos -->
			<?php
    			$inc = include("conexion_bbdd.php");
    			if ($inc) {
       				 $consulta1="SELECT COUNT( cuidador.idUsuario_Cuidador ) AS Nro_informes_VL_veridicos, 
                    ( SELECT TRUNCATE(COUNT( cuidador.Informe_VidaLaboral_Validado) *100 / COUNT( c.idUsuario_Cuidador),2)
                    FROM cuidador AS c
                    ) as porcentaje_informes_VL_veridicos
                    FROM cuidador
                    WHERE cuidador.Informe_VidaLaboral_Validado=1	
                    GROUP BY cuidador.Informe_VidaLaboral_Validado";
                    
                    $resultado1=mysqli_query($conexion,$consulta1);

      			  if($resultado1) {
            			while($row1 = $resultado1->fetch_array()){
                		$porcentaje_informes_VL_veridicos = $row1['porcentaje_informes_VL_veridicos']; 
            			?>
								<!-- Diseño gráfico: Informes de vida laboral verídicos -->
								<div class="col-lg-3 col-md-6 col-sm-12 mb-30">
									<div class="bg-white pd-20 box-shadow border-radius-5 height-100-p">
										<div class="project-info clearfix">
											<div class="project-info-left">
												<div class="icon box-shadow bg-blue text-white">
													<i class="fa fa-briefcase"></i>
												</div>
											</div>
											<div class="project-info-right">
												<p class="weight-400 font-18"><?php echo $porcentaje_informes_VL_veridicos; ?>%</p>
												<span class="no text-blue weight-500 font-16">Informes de vida laboral verídicos</span>
											</div>
										</div>
										
										<div class="project-info-progress">
											<div class="row clearfix">
												<div class="col-sm-6 text-muted weight-500 font-14 text-muted">0%</div>
												<div class="col-sm-6 text-right weight-500 font-14 text-muted">100%</div>
											</div>
											<div class="progress" style="height: 10px;">
												<div class="progress-bar bg-blue progress-bar-striped progress-bar-animated" role="progressbar" style="width: <?php echo $porcentaje_informes_VL_veridicos; ?>%;" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
											</div>
										</div>
									</div>
								</div>
            			<?php
            				}
        				}
					}
			?>
				
			<!-- Certificados de antecedentes verídicos -->
			<?php
    			$inc = include("conexion_bbdd.php");
    			if ($inc) {
       				 $consulta2="SELECT COUNT( cuidador.idUsuario_Cuidador ) AS Nro_certificados_A_veridicos, 
						( SELECT TRUNCATE(COUNT( cuidador.Certificado_Antecedentes_Verificado) *100 / COUNT( c.idUsuario_Cuidador),2)
						FROM cuidador AS c
						) as porcentaje_certificados_A_veridicos
						FROM cuidador
						WHERE cuidador.Certificado_Antecedentes_Verificado=1	
						GROUP BY cuidador.Certificado_Antecedentes_Verificado";
                    
                    $resultado2=mysqli_query($conexion,$consulta2);

      			  if($resultado2) {
            			while($row2 = $resultado2->fetch_array()){
                		$porcentaje_certificados_A_veridicos = $row2['porcentaje_certificados_A_veridicos']; 
            			?>
           				 		<!-- Diseño gráfico: Certificados de antecedentes verídicos -->
								<div class="col-lg-3 col-md-6 col-sm-12 mb-30">
									<div class="bg-white pd-20 box-shadow border-radius-5 height-100-p">
										<div class="project-info clearfix">
											<div class="project-info-left">
												<div class="icon box-shadow bg-light-green text-white">
													<i class="fa fa-user-secret"></i>
												</div>
											</div>
											<div class="project-info-right">
												<p class="weight-400 font-18"><?php echo $porcentaje_certificados_A_veridicos; ?>%</p>
												<span class="no text-light-green weight-500 font-16">Certificados antecedentes verídicos</span>
											</div>
										</div>
										<div class="project-info-progress">
												<div class="row clearfix">
													<div class="col-sm-6 text-muted weight-500 font-14 text-muted">0%</div>
													<div class="col-sm-6 text-right weight-500 font-14 text-muted">100%</div>
												</div>
												<div class="progress" style="height: 10px;">
													<div class="progress-bar bg-light-green progress-bar-striped progress-bar-animated" role="progressbar" style="width: <?php echo $porcentaje_certificados_A_veridicos; ?>%;" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
												</div>
										</div>
									</div>
								</div>
            			<?php
            				}
        				}
					}
			?>

			<!-- Porcentaje de usuarios cuidadores -->
			<?php
    			$inc = include("conexion_bbdd.php");
    			if ($inc) {
       				 $consulta3="SELECT COUNT( usuario.idUsuario ) AS Nro_usuarios, 
						( SELECT TRUNCATE(COUNT( usuario.idUsuario) *100 / COUNT( u.idUsuario),2)
						FROM usuario AS u
						) as porcentaje_cuidadores
						FROM usuario
						WHERE idUsuario LIKE '%CU%'";
                    
                    $resultado3=mysqli_query($conexion,$consulta3);

      			  if($resultado3) {
            			while($row3 = $resultado3->fetch_array()){
                		$porcentaje_cuidadores = $row3['porcentaje_cuidadores']; 
            			?>
           				 		<!-- Diseño gráfico: Porcentaje de usuarios cuidadores -->
								<div class="col-lg-3 col-md-6 col-sm-12 mb-30">
									<div class="bg-white pd-20 box-shadow border-radius-5 height-100-p">
										<div class="project-info clearfix">
											<div class="project-info-left">
												<div class="icon box-shadow bg-light-orange text-white">
													<i class="fa fa-heartbeat"></i>
												</div>
											</div>
											<div class="project-info-right">
												<p class="weight-400 font-18"><?php echo $porcentaje_cuidadores; ?>%</p>
												<span class="no text-light-orange weight-500 font-16">Porcentaje de usuarios cuidadores</span>
											</div>
										</div>
										<div class="project-info-progress">
											<div class="row clearfix">
												<div class="col-sm-6 text-muted weight-500 font-14 text-muted">0%</div>
												<div class="col-sm-6 text-right weight-500 font-14 text-muted">100%</div>
											</div>
											<div class="progress" style="height: 10px;">
												<div class="progress-bar bg-light-orange progress-bar-striped progress-bar-animated" role="progressbar" style="width: <?php echo $porcentaje_cuidadores; ?>%;" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
											</div>
										</div>
									</div>
								</div>
            			<?php
            				}
        				}
					}
			?>

			<!-- Porcentaje de usuarios clientes -->
			<?php
    			$inc = include("conexion_bbdd.php");
    			if ($inc) {
       				 $consulta4="SELECT COUNT( usuario.idUsuario ) AS Nro_usuarios, 
						( SELECT TRUNCATE(COUNT( usuario.idUsuario) *100 / COUNT( u.idUsuario),2)
						FROM usuario AS u
						) as porcentaje_clientes
						FROM usuario
						WHERE idUsuario LIKE '%CL%'";
                    
                    $resultado4=mysqli_query($conexion,$consulta4);

      			  if($resultado4) {
            			while($row4 = $resultado4->fetch_array()){
                		$porcentaje_clientes = $row4['porcentaje_clientes']; 
            			?>
           				 		<!-- Diseño gráfico: Porcentaje de usuarios clientes -->
								<div class="col-lg-3 col-md-6 col-sm-12 mb-30">
									<div class="bg-white pd-20 box-shadow border-radius-5 margin-5 height-100-p">
										<div class="project-info clearfix">
											<div class="project-info-left">
												<div class="icon box-shadow bg-light-purple text-white">
													<i class="fa fa-user"></i>
												</div>
											</div>
											<div class="project-info-right">
												<p class="weight-400 font-18"><?php echo $porcentaje_clientes; ?>%</p>
												<span class="no text-light-purple weight-500 font-16">Porcentaje de usuarios clientes</span>
											</div>
										</div>
										<div class="project-info-progress">
											<div class="row clearfix">
											<div class="col-sm-6 text-muted weight-500 font-14 text-muted">0%</div>
												<div class="col-sm-6 text-right weight-500 font-14 text-muted">100%</div>
											</div>
											<div class="progress" style="height: 10px;">
												<div class="progress-bar bg-light-purple progress-bar-striped progress-bar-animated" role="progressbar" style="width: 20%;" aria-valuenow="25" aria-valuemin="0" aria-valuemax="100"></div>
											</div>
										</div>
									</div>
								</div>
            			<?php
            				}
        				}
					}
			?>
			</div>
			<!-------------------- GRÁFICOS BARRA PROGRESO -------------------->

			<!-------------------- GRÁFICOS TABLEAU NUEVOS-USUARIOS Y NÚMERO-CONTRATACIONES -------------------->
			<div class="bg-white pd-20 box-shadow border-radius-5 mb-30">
				<h4 class="mb-50">Estadísticos mensuales: </h4>
			</div> 

				<!-------------------- GRÁFICO TABLEAU NUEVOS-USUARIOS DE ÁREAS -------------------->
			<div class="bg-white pd-20 box-shadow border-radius-5 mb-30">
				<div class='tableauPlaceholder' id='viz1654421301579' style='position: relative'>
					<noscript>
						<a href='#'>
							<img alt='Usuarios nuevos registrados ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Us&#47;UsuariosNuevos&#47;Usuariosnuevos&#47;1_rss.png' style='border: none' />
						</a>
					</noscript>
					<object class='tableauViz'  style='display:none;'>
						<param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> 
						<param name='embed_code_version' value='3' /> <param name='site_root' value='' />
						<param name='name' value='UsuariosNuevos&#47;Usuariosnuevos' /><param name='tabs' value='no' />
						<param name='toolbar' value='yes' />
						<param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Us&#47;UsuariosNuevos&#47;Usuariosnuevos&#47;1.png' /> 
						<param name='animate_transition' value='yes' />
						<param name='display_static_image' value='yes' />
						<param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' />
						<param name='display_count' value='yes' /><param name='language' value='es-ES' />
					</object>					
				</div>                
				<script type='text/javascript'>                    
					var divElement = document.getElementById('viz1654421301579');                    
					var vizElement = divElement.getElementsByTagName('object')[0];                    
					vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.35)+'px';                    
					var scriptElement = document.createElement('script');                    
					scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    
					vizElement.parentNode.insertBefore(scriptElement, vizElement);                
				</script>
			</div>
				<!-------------------- GRÁFICO TABLEAU NUEVOS-USUARIOS DE ÁREAS -------------------->

				<!-------------------- GRÁFICO TABLEAU NÚMERO-CONTRATACIONES DE BARRAS -------------------->
			<div class="bg-white pd-20 box-shadow border-radius-5 mb-30">
				<div class='tableauPlaceholder' id='viz1654422287509' style='position: relative'>
					<noscript>
						<a href='#'>
							<img alt='Número de contrataciones ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Nu&#47;NumeroContrataciones&#47;NumeroContrataciones&#47;1_rss.png' style='border: none' />
						</a>
					</noscript>
					<object class='tableauViz'  style='display:none;'>
						<param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> 
						<param name='embed_code_version' value='3' /> <param name='site_root' value='' />
						<param name='name' value='NumeroContrataciones&#47;NumeroContrataciones' />
						<param name='tabs' value='no' /><param name='toolbar' value='yes' />
						<param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Nu&#47;NumeroContrataciones&#47;NumeroContrataciones&#47;1.png' /> 
						<param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' />
						<param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' />
						<param name='display_count' value='yes' /><param name='language' value='es-ES' />
						<param name='filter' value='publish=yes' />
					</object>
				</div>                
				<script type='text/javascript'>                    
					var divElement = document.getElementById('viz1654422287509');                    
					var vizElement = divElement.getElementsByTagName('object')[0];                    
					vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.22)+'px';                    
					var scriptElement = document.createElement('script');                    
					scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    
					vizElement.parentNode.insertBefore(scriptElement, vizElement);                
				</script>
			</div>
				<!-------------------- GRÁFICO TABLEAU NÚMERO-CONTRTACIONES DE BARRAS -------------------->
			<!-------------------- GRÁFICO ÁREAS -------------------->

			<!-------------------- GRÁFICO DONUT 1 -------------------->
			<div class="row clearfix">
				<div class="col-xl-4 col-lg-12 col-md-12 col-sm-12 mb-30">
					<div class="bg-white pd-20 box-shadow border-radius-5 height-100-p">
						<h4 class="mb-30">Dependencias que cubren los usuarios cuidadores</h4>
						<div class="clearfix device-usage-chart">
							<div class="width-50-p pull-left">
								<div id="device-usage-1" style="min-width: 180px; height: 200px; margin: 0 auto"></div>
							</div>
							<div class="width-50-p pull-left">
								<table style="width: 100%;">
									<thead>
										<tr>
											<th class="weight-500"><p>-Tipo</p></th>
											<th class="text-right weight-500"><p>%</p></th>
										</tr>
									</thead>
									<tbody>
										<!-------------------- Porcentaje 3ªEdad -------------------->
										<?php
											$inc = include("conexion_bbdd.php");
											if ($inc) {
												$consulta5="SELECT COUNT( cuidador.Cuidados_ofrecidos ) AS Cuidados_totales, 
												( SELECT TRUNCATE(COUNT( cuidador.Cuidados_ofrecidos) *100 / COUNT( c.Cuidados_ofrecidos),2)
												FROM cuidador AS c
												) as porcentaje_3Edad_Cuidador
												FROM cuidador
												WHERE Cuidados_ofrecidos LIKE '%Dependencia por edad%'";
												
												$resultado5=mysqli_query($conexion,$consulta5);

											if($resultado5) {
													while($row5 = $resultado5->fetch_array()){
													$porcentaje_3Edad_Cuidador = $row5['porcentaje_3Edad_Cuidador']; 
													?>
																	<tr>
																		<td width="70%"><p class="weight-500 mb-5"><i class="fa fa-square text-yellow"></i>3ªEdad</p></td>
																		<td class="text-right weight-300"><?php echo $porcentaje_3Edad_Cuidador; ?>%</td>
																	</tr>
																	<?php
														}
													}
												}
										?>
										<!-------------------- Porcentaje Enfermedad -------------------->
										<?php
											$inc = include("conexion_bbdd.php");
											if ($inc) {
												$consulta6="SELECT COUNT( cuidador.Cuidados_ofrecidos ) AS Cuidados_totales, 
												( SELECT TRUNCATE(COUNT( cuidador.Cuidados_ofrecidos) *100 / COUNT( c.Cuidados_ofrecidos),2)
												FROM cuidador AS c
												) as porcentaje_Enfermedad_Cuidador
												FROM cuidador
												WHERE Cuidados_ofrecidos LIKE '%Dependencia por enfermedad%'";
												
												$resultado6=mysqli_query($conexion,$consulta6);

											if($resultado6) {
													while($row6 = $resultado6->fetch_array()){
													$porcentaje_Enfermedad_Cuidador = $row6['porcentaje_Enfermedad_Cuidador']; 
													?>
																	<tr>
																		<td width="70%"><p class="weight-500 mb-5"><i class="fa fa-square text-green"></i>Enfermedad</p></td>
																		<td class="text-right weight-300"><?php echo $porcentaje_Enfermedad_Cuidador; ?>%</td>
																	</tr>
																	<?php
														}
													}
												}
										?>
										<!-------------------- Porcentaje Discapacidad -------------------->
										<?php
											$inc = include("conexion_bbdd.php");
											if ($inc) {
												$consulta7="SELECT COUNT( cuidador.Cuidados_ofrecidos ) AS Cuidados_totales, 
												( SELECT TRUNCATE(COUNT( cuidador.Cuidados_ofrecidos) *100 / COUNT( c.Cuidados_ofrecidos),2)
												FROM cuidador AS c
												) as porcentaje_Discapacidad_Cuidador
												FROM cuidador
												WHERE Cuidados_ofrecidos LIKE '%Dependencia por discapacidad%'";
												
												$resultado7=mysqli_query($conexion,$consulta7);

											if($resultado7) {
													while($row7 = $resultado7->fetch_array()){
													$porcentaje_Discapacidad_Cuidador = $row7['porcentaje_Discapacidad_Cuidador']; 
													?>
																	<tr>
																		<td width="70%"><p class="weight-500 mb-5"><i class="fa fa-square text-orange-50"></i>Discapacidad</p></td>
																		<td class="text-right weight-300"><?php echo $porcentaje_Discapacidad_Cuidador; ?>%</td>
																	</tr>
																	<?php
														}
													}
												}
										?>
										<!-------------------- Porcentaje Infancia -------------------->
										<?php
											$inc = include("conexion_bbdd.php");
											if ($inc) {
												$consulta8="SELECT COUNT( cuidador.Cuidados_ofrecidos ) AS Cuidados_totales, 
												( SELECT TRUNCATE(COUNT( cuidador.Cuidados_ofrecidos) *100 / COUNT( c.Cuidados_ofrecidos),2)
												FROM cuidador AS c
												) as porcentaje_Infancia_Cuidador
												FROM cuidador
												WHERE Cuidados_ofrecidos LIKE '%Dependencia por infancia%'";
												
												$resultado8=mysqli_query($conexion,$consulta8);

											if($resultado8) {
													while($row8 = $resultado8->fetch_array()){
													$porcentaje_Infancia_Cuidador = $row8['porcentaje_Infancia_Cuidador']; 
													?>
																	<tr>
																		<td width="70%"><p class="weight-500 mb-5"><i class="fa fa-square text-blue-50"></i>Infancia</p></td>
																		<td class="text-right weight-300"><?php echo $porcentaje_Infancia_Cuidador; ?>%</td>
																	</tr>
																	<?php
														}
													}
												}
										?>
									</tbody>
								</table>
							</div>
						</div>
					</div>
				</div>
				<!-------------------- GRÁFICO DONUT 1 -------------------->

				<!-------------------- GRÁFICO DONUT 2 -------------------->
				<div class="col-xl-4 col-lg-6 col-md-6 col-sm-12 mb-30">
					<div class="bg-white pd-20 box-shadow border-radius-5 height-100-p">
						<h4 class="mb-30">Dependencias que reclaman los usuarios clientes</h4>
						<div class="clearfix device-usage-chart">
							<div class="width-50-p pull-left">
								<div id="device-usage-2" style="min-width: 180px; height: 200px; margin: 0 auto"></div>
							</div>
							<div class="width-50-p pull-left">
								<table style="width: 100%;">
									<thead>
										<tr>
											<th class="weight-500"><p>-Tipo</p></th>
											<th class="text-right weight-500"><p>%</p></th>
										</tr>
									</thead>
									<tbody>
										<!-------------------- Porcentaje 3ªEdad -------------------->
										<?php
											$inc = include("conexion_bbdd.php");
											if ($inc) {
												$consulta9="SELECT COUNT( cliente.Dependencia_reclamada ) AS Cuidados_totales, 
												( SELECT TRUNCATE(COUNT( cliente.Dependencia_reclamada) *100 / COUNT( c.Dependencia_reclamada),2)
												FROM cliente AS c
												) as porcentaje_3Edad_Cliente
												FROM cliente
												WHERE Dependencia_reclamada LIKE '%Dependencia por edad%'";
												
												$resultado9=mysqli_query($conexion,$consulta9);

											if($resultado9) {
													while($row9 = $resultado9->fetch_array()){
													$porcentaje_3Edad_Cliente = $row9['porcentaje_3Edad_Cliente']; 
													?>
																	<tr>
																		<td width="70%"><p class="weight-500 mb-5"><i class="fa fa-square text-yellow"></i>3ªEdad</p></td>
																		<td class="text-right weight-300"><?php echo $porcentaje_3Edad_Cliente; ?>%</td>
																	</tr>
																	<?php
														}
													}
												}
										?>
										<!-------------------- Porcentaje Enfermedad -------------------->
										<?php
											$inc = include("conexion_bbdd.php");
											if ($inc) {
												$consulta10="SELECT COUNT( cliente.Dependencia_reclamada ) AS Cuidados_totales, 
												( SELECT TRUNCATE(COUNT( cliente.Dependencia_reclamada) *100 / COUNT( c.Dependencia_reclamada),2)
												FROM cliente AS c
												) as porcentaje_Enfermedad_Cliente
												FROM cliente
												WHERE Dependencia_reclamada LIKE '%Dependencia por enfermedad%'";
												
												$resultado10=mysqli_query($conexion,$consulta10);

											if($resultado10) {
													while($row10 = $resultado10->fetch_array()){
													$porcentaje_Enfermedad_Cliente = $row10['porcentaje_Enfermedad_Cliente']; 
													?>
																	<tr>
																		<td width="70%"><p class="weight-500 mb-5"><i class="fa fa-square text-green"></i>Enfermedad</p></td>
																		<td class="text-right weight-300"><?php echo $porcentaje_Enfermedad_Cliente; ?>%</td>
																	</tr>
																	<?php
														}
													}
												}
										?>
										<!-------------------- Porcentaje Discapacidad -------------------->
										<?php
											$inc = include("conexion_bbdd.php");
											if ($inc) {
												$consulta11="SELECT COUNT( cliente.Dependencia_reclamada ) AS Cuidados_totales, 
												( SELECT TRUNCATE(COUNT( cliente.Dependencia_reclamada) *100 / COUNT( c.Dependencia_reclamada),2)
												FROM cliente AS c
												) as porcentaje_Discapacidad_Cliente
												FROM cliente
												WHERE Dependencia_reclamada LIKE '%Dependencia por discapacidad%'";
												
												$resultado11=mysqli_query($conexion,$consulta11);

											if($resultado11) {
													while($row11 = $resultado11->fetch_array()){
													$porcentaje_Discapacidad_Cliente = $row11['porcentaje_Discapacidad_Cliente']; 
													?>
																	<tr>
																		<td width="70%"><p class="weight-500 mb-5"><i class="fa fa-square text-orange-50"></i>Discapacidad</p></td>
																		<td class="text-right weight-300"><?php echo $porcentaje_Discapacidad_Cliente; ?>%</td>
																	</tr>
																	<?php
														}
													}
												}
										?>
										<!-------------------- Porcentaje Infancia -------------------->
										<?php
											$inc = include("conexion_bbdd.php");
											if ($inc) {
												$consulta12="SELECT COUNT( cliente.Dependencia_reclamada ) AS Cuidados_totales, 
												( SELECT TRUNCATE(COUNT( cliente.Dependencia_reclamada) *100 / COUNT( c.Dependencia_reclamada),2)
												FROM cliente AS c
												) as porcentaje_Infancia_Cliente
												FROM cliente
												WHERE Dependencia_reclamada LIKE '%Dependencia por infancia%'";
												
												$resultado12=mysqli_query($conexion,$consulta12);

											if($resultado12) {
													while($row12 = $resultado12->fetch_array()){
													$porcentaje_Infancia_Cliente = $row12['porcentaje_Infancia_Cliente']; 
													?>
																	<tr>
																		<td width="70%"><p class="weight-500 mb-5"><i class="fa fa-square text-blue-50"></i>Infancia</p></td>
																		<td class="text-right weight-300"><?php echo $porcentaje_Infancia_Cliente; ?>%</td>
																	</tr>
																	<?php
														}
													}
												}
										?>	
									</tbody>
								</table>
							</div>
						</div>
					</div>
				</div>
				<!-------------------- GRÁFICO DONUT 2 -------------------->

				<!-------------------- GRÁFICO SCROLL -------------------->
				<div class="col-xl-4 col-lg-6 col-md-6 col-sm-12 mb-30">
				<div class="bg-white pd-20 box-shadow border-radius-5 height-100-p">
					<?php
						$inc = include("conexion_bbdd.php");
						if ($inc) {
							$consulta13="SELECT cuidador.*, cliente.*, datos_persona_dependiente.*, contratacion.*, 
							TIMESTAMPDIFF(MINUTE, contratacion.FechaHoraContratacion, now()) AS Hace_cuanto, 
							cuidador.Nombre AS Nombre_contratado, cuidador.Apellidos AS Apellidos_contratado, 
							cuidador.Cuidados_ofrecidos AS Dependencia_contratacion, 
							cliente.Nombre AS Nombre_cliente, cliente.Apellidos AS Apellidos_cliente, 
							datos_persona_dependiente.Nombre AS Nombre_dependiente, datos_persona_dependiente.Apellidos AS Apellidos_dependiente 
							FROM contratacion INNER JOIN cuidador ON contratacion.idUsuario_Cuidador_Contrato = cuidador.idUsuario_Cuidador 
							INNER JOIN cliente ON contratacion.idUsuario_Cliente_Contrato = cliente.idUsuario_Cliente 
							INNER JOIN datos_persona_dependiente 
							ON contratacion.idUsuario_Dependiente_Contrato = datos_persona_dependiente.idUsuario_Dependiente 
							ORDER BY Hace_cuanto ASC";												
							$resultado13=mysqli_query($conexion,$consulta13);
							if($resultado13) {
					?>				
									<h4 class="mb-20">Últimos cuidadores contratados</h4>
									<div class="notification-list mx-h-300 customscroll">
										<ul>
											<?php
											while($row13=mysqli_fetch_array($resultado13)){
											?>
													<li type="button" data-toggle="modal" data-target="#exampleModal">
														<a href="#">
														<img src="vendors/images/contrato.png" alt="">
														<p>Hace <?php echo $row13['Hace_cuanto']; ?> minutos.</p>
														<small><b><?php echo $row13['Dependencia_contratacion']; ?></b></small>
														<br><small><b><?php echo $row13['idUsuario_Cuidador']; ?></b>: <?php echo $row13['Nombre_contratado']; ?> <?php echo $row13['Apellidos_contratado']; ?></small>
														<br><small><b><?php echo $row13['idUsuario_Cliente']; ?></b>: <?php echo $row13['Nombre_cliente']; ?> <?php echo $row13['Apellidos_cliente']; ?></small>
														<br><small><b><?php echo $row13['idUsuario_Dependiente']; ?></b>: <?php echo $row13['Nombre_dependiente']; ?> <?php echo $row13['Apellidos_dependiente']; ?></small>
														</a>
													</li>
											<?php
											}
											?>
										</ul>
									</div>
						<?php
								
							}
						}
						?>
										
				<!-------------------- GRÁFICO SCROLL -------------------->
				</div>
			</div>

			<!-------------------- Footer -------------------->
			<?php include('include/footer.php'); ?>
		</div>
	</div>

<!-------------------------------------------------- CARACTERÍSTICAS DE LOS GRÁFICOS --------------------------------------------------->

	<?php include('include/script.php'); ?>
	<script src="src/plugins/highcharts-6.0.7/code/highcharts.js"></script>
	<script src="src/plugins/highcharts-6.0.7/code/highcharts-more.js"></script>
	<script type="text/javascript">

	// CARACTERÍSTICAS GRÁFICO DONUT 1
		Highcharts.chart('device-usage-1', {
			chart: {
				type: 'pie'
			},
			title: {
				text: ''
			},
			subtitle: {
				text: ''
			},
			credits: {
				enabled: false
			},
			plotOptions: {
				series: {
					dataLabels: {
						enabled: false,
						format: '{point.name}: {point.y:.1f}%'
					}
				},
				pie: {
					innerSize: 127,
					depth: 45
				}
			},

			tooltip: {
				headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
				pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}%</b> of total<br/>'
			},
			series: [{
				name: 'Tipo dependencia',
				colorByPoint: true,
				data: [{
					name: '3ªEdad',
					y: <?php echo $porcentaje_3Edad_Cuidador; ?>,
					color: '#ecc72f'
				}, {
					name: 'Enfermedad',
					y: <?php echo $porcentaje_Enfermedad_Cuidador; ?>,
					color: '#46be8a'
				}, {
					name: 'Discapacidad',
					y: <?php echo $porcentaje_Discapacidad_Cuidador; ?>,
					color: '#f2a654'
				}, {
					name: 'Infancia',
					y: <?php echo $porcentaje_Infancia_Cuidador; ?>,
					color: '#62a8ea'
				}]
			}]
		});
	// CARACTERÍSTICAS GRÁFICO DONUT 1

	// CARACTERÍSTICAS GRÁFICO DONUT 2
		Highcharts.chart('device-usage-2', {
			chart: {
				type: 'pie'
			},
			title: {
				text: ''
			},
			subtitle: {
				text: ''
			},
			credits: {
				enabled: false
			},
			plotOptions: {
				series: {
					dataLabels: {
						enabled: false,
						format: '{point.name}: {point.y:.1f}%'
					}
				},
				pie: {
					innerSize: 127,
					depth: 45
				}
			},

			tooltip: {
				headerFormat: '<span style="font-size:11px">{series.name}</span><br>',
				pointFormat: '<span style="color:{point.color}">{point.name}</span>: <b>{point.y:.2f}%</b> of total<br/>'
			},
			series: [{
				name: 'Tipo dependencia',
				colorByPoint: true,
				data: [{
					name: '3ªEdad',
					y: <?php echo $porcentaje_3Edad_Cliente; ?>,
					color: '#ecc72f'
				}, {
					name: 'Enfermedad',
					y: <?php echo $porcentaje_Enfermedad_Cliente; ?>,
					color: '#46be8a'
				}, {
					name: 'Discapacidad',
					y: <?php echo $porcentaje_Discapacidad_Cliente; ?>,
					color: '#f2a654'
				}, {
					name: 'Infancia',
					y: <?php echo $porcentaje_Infancia_Cliente; ?>,
					color: '#62a8ea'
				}]
			}]
		});
	// CARACTERÍSTICAS GRÁFICO DONUT 2
	</script>
<!---------------------------------------------- FIN CARACTERÍSTICAS DE LOS GRÁFICOS --------------------------------------------------->
</body>
</html>
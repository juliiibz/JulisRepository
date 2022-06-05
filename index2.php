<!DOCTYPE html>
<html>
<head>
	<?php include('include/head.php'); ?>
</head>
<body>
	<?php include('include/header.php'); ?>
	<?php include('include/sidebar.php'); ?>
	<div class="main-container">
		<div class="customscroll customscroll-10-p height-100-p xs-pd-20-10 pd-ltr-20">
			<div class="page-header">
				<div class="row">
					<div class="col-md-6 col-sm-12">
						<div class="title">
							<h4>Mapa IberAsis</h4>
						</div>
						<nav aria-label="breadcrumb" role="navigation">
							<ol class="breadcrumb">
								<li class="breadcrumb-item"><a href="index.php">Dashboard</a></li>
							</ol>
						</nav>
					</div>
				</div>
			</div>
			
			<!-------------------- MAPA -------------------->
			<div class="bg-white pd-30 box-shadow border-radius-5 mb-30 xs-pd-20-10">
				<div class='tableauPlaceholder' id='viz1654385566243' style='position: relative'>
					<noscript>
						<a href='#'>
							<img alt='Mapa_IberAsis ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;69&#47;696N5X536&#47;1_rss.png' style='border: none' />
						</a>
					</noscript>
					<object class='tableauViz'  style='display:none;'>
						<param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> 
						<param name='embed_code_version' value='3' /> <param name='path' value='shared&#47;696N5X536' /> 
						<param name='toolbar' value='yes' />
						<param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;69&#47;696N5X536&#47;1.png' /> 
						<param name='animate_transition' value='yes' />
						<param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' />
						<param name='display_overlay' value='yes' /><param name='display_count' value='yes' />
						<param name='language' value='es-ES' /><param name='filter' value='publish=yes' />
					</object>
				</div>                
				<script type='text/javascript'>                    
					var divElement = document.getElementById('viz1654385566243');                    
					var vizElement = divElement.getElementsByTagName('object')[0];                    
					vizElement.style.width='100%';
					vizElement.style.height=(divElement.offsetWidth*0.60)+'px';                    
					var scriptElement = document.createElement('script');                    
					scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    
					vizElement.parentNode.insertBefore(scriptElement, vizElement);                
				</script>
			</div>
			
			<?php include('include/footer.php'); ?>
		</div>
	</div>
	<?php include('include/script.php'); ?>
</body>
</html>
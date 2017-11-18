<html> 
    <head> 
        <title>Tyrell Corporation Network Access</title> 
		<style>
			body {
				margin: auto;
				text-align: center;
				background-color: rgb(255, 137, 0);
			}
			.flag {
				font-size: xx-large;
			}
		</style>
	</head> 
  <body> 
  <h1>Tyrell Corporation</h1>
<?php 

    if (!isset($_COOKIE['count']))
    {
        $cookie = 1;
        setcookie("count", $cookie);
    }
    else
    {
        $cookie = ++$_COOKIE['count'];
        setcookie("count", $cookie);  
	}// end else  ?> 
	
<?php 

    if ($cookie == 581)
    {
        ?> 
		<p class="flag">The flag is:  acsc2017{KeepClickin}</p> 
		<?php 
    }
    else
    {
        ?> 
		<a href=index.php><img src="Tyrell_Corporation.png" alt="Tyrell Corporation"></a>
		<p>Click here to enter the system (581 times)</p> 
		<?php  
	}// end else  ?> 
   </body> 
</html>

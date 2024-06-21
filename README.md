RewriteEngine on
RewriteCond %{SERVER_PORT} 80
RewriteRule ^(.*)$ https://SKYjustin1225.github.io/stock/app.py$1 [R,L]

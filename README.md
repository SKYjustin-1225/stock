RewriteEngine on
RewriteCond %{SERVER_PORT} 80
RewriteRule ^(.*)$ https://SKYjustin1225.github.io/stock/股市分析/app.py$1 [R,L]

path = r'C:\Users\mateu\Downloads\Projeto Dudu\Buzz 2.0\generate_remaining_pages.py'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

pos_start = text.find('htaccess_content = """AddDefaultCharset UTF-8')
pos_end = text.find('"""\nwith open(os.path.join(SITE_DIR, \'.htaccess\')', pos_start)

if pos_start != -1 and pos_end != -1:
    new_htaccess = '''htaccess_content = """AddDefaultCharset UTF-8
AddCharset UTF-8 .html .htm .css .js .xml .json .txt
<IfModule mod_headers.c>
  <FilesMatch "\\\\.(html|htm)$">
    Header set Content-Type "text/html; charset=UTF-8"
  </FilesMatch>
</IfModule>
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteRule ^comprar\\\\.html$ /simulador-imobiliario/comprar.html [R=301,L]
  RewriteRule ^proprietario\\\\.html$ /simulador-imobiliario/proprietario.html [R=301,L]
  RewriteRule ^simulador-imobiliario$ /simulador-imobiliario/ [R=301,L]
</IfModule>
'''
    text = text[:pos_start] + new_htaccess + text[pos_end:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print("SUCCESS: htaccess_content replaced!")
else:
    print("Failed to find positions:", pos_start, pos_end)

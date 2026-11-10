import os
import zipfile

src_app = r"c:\Users\mateu\Projects\rewarded-tasks\app-facebook"
downloads_dir = r"C:\Users\mateu\Downloads\Projeto Dudu"
zip_path = os.path.join(downloads_dir, "app-facebook-100-corrigido.zip")

# Load Cloaker files from spotify-funnel
spotify_dir = r"c:\Users\mateu\Projects\rewarded-tasks\spotify-funnel"
with open(os.path.join(spotify_dir, "index.php"), "r", encoding="utf-8") as f:
    index_php = f.read()
with open(os.path.join(spotify_dir, "white.html"), "r", encoding="utf-8") as f:
    white_html = f.read()
with open(os.path.join(spotify_dir, ".htaccess"), "r", encoding="utf-8") as f:
    htaccess = f.read()

with open(os.path.join(src_app, "index.html"), "r", encoding="utf-8") as f:
    offer_html = f.read()

with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("index.html", offer_html)
    z.writestr("offer.html", offer_html)
    z.writestr("index.php", index_php)
    z.writestr("white.html", white_html)
    z.writestr(".htaccess", htaccess)
    
    # Add assets
    assets_dir = os.path.join(src_app, "assets")
    for root, dirs, files in os.walk(assets_dir):
        for file in files:
            full_path = os.path.join(root, file)
            arcname = os.path.relpath(full_path, src_app)
            z.write(full_path, arcname)

print("ZIP criado com sucesso em:", zip_path)

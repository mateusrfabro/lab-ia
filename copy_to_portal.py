import shutil
import os

src_dir = r"C:\Users\mateu\Downloads\Projeto Dudu\mydollar_unpacked\quiz"
portal_public = r"C:\Users\mateu\Projects\portal-eua\public"

# 1. results.html
src_results = os.path.join(src_dir, "results.html")
dest_quiz_results = os.path.join(portal_public, "quiz", "results.html")
dest_root_results = os.path.join(portal_public, "results.html")

shutil.copy2(src_results, dest_quiz_results)
shutil.copy2(src_results, dest_root_results)

# 2. css/style.css
src_css = os.path.join(src_dir, "css", "style.css")
dest_quiz_css = os.path.join(portal_public, "quiz", "css", "style.css")
dest_root_css = os.path.join(portal_public, "css", "style.css")

shutil.copy2(src_css, dest_quiz_css)
shutil.copy2(src_css, dest_root_css)

print("Arquivos copiados com sucesso para portal-eua/public!")

import urllib.request
import urllib.parse
import zipfile
import os

def upload_dpaste(content):
    data = urllib.parse.urlencode({'content': content, 'expiry_days': 14}).encode('utf-8')
    req = urllib.request.Request('https://dpaste.org/api/', data=data, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        url = resp.read().decode('utf-8').strip().strip('"').strip()
        if not url.endswith('/raw'):
            url += '/raw'
        return url

# Repackage zip
staging = r'C:\Users\mateu\Projects\lab-ia\staging_spotify'
zip_path = r'C:\Users\mateu\Projects\lab-ia\pacotes-prontos-hostinger\PACOTE-1-SPOTIFY-FUNNEL.zip'

with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(staging):
        for file in files:
            full_path = os.path.join(root, file)
            arcname = os.path.relpath(full_path, staging)
            zipf.write(full_path, arcname)

print(f'Repackaged {zip_path} ({os.path.getsize(zip_path)} bytes)')

# Upload offer.html and chat.html
with open(os.path.join(staging, 'offer.html'), 'r', encoding='utf-8') as f:
    offer_c = f.read()

with open(os.path.join(staging, 'chat.html'), 'r', encoding='utf-8') as f:
    chat_c = f.read()

u_offer = upload_dpaste(offer_c)
u_chat = upload_dpaste(chat_c)

print('NEW offer.html DPaste URL ->', u_offer)
print('NEW chat.html DPaste URL ->', u_chat)

cmd = (
    'cd ~/domains/portaltechmidia.com/public_html 2>/dev/null || cd public_html 2>/dev/null; '
    f'curl -sL "{u_offer}" -o index.html; '
    f'curl -sL "{u_chat}" -o chat.html; '
    'echo ">>> PORTALTECHMIDIA 100% ATUALIZADO (OFFER + CHAT COM VSLs NOVAS)! <<<"'
)

with open(r'C:\Users\mateu\Projects\lab-ia\deploy_spotify_full.txt', 'w', encoding='utf-8') as f:
    f.write(cmd)

print('\nComando pronto em deploy_spotify_full.txt:')
print(cmd)

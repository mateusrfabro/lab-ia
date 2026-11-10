import urllib.request
import urllib.parse

def upload_dpaste(content):
    data = urllib.parse.urlencode({'content': content, 'expiry_days': 14}).encode('utf-8')
    req = urllib.request.Request('https://dpaste.org/api/', data=data, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        url = resp.read().decode('utf-8').strip().strip('"').strip()
        if not url.endswith('/raw'):
            url += '/raw'
        return url

with open(r'C:\Users\mateu\Projects\lab-ia\staging_spotify\chat.html', 'r', encoding='utf-8') as f:
    chat_c = f.read()

u_chat = upload_dpaste(chat_c)

print('NEW chat.html DPaste URL ->', u_chat)
cmd = f'cd ~/domains/portaltechmidia.com/public_html 2>/dev/null || cd public_html 2>/dev/null; curl -sL "{u_chat}" -o chat.html; echo ">>> CHAT.HTML ATUALIZADO COM AS NOVAS VSLs 1 E 2! <<<"'

with open(r'C:\Users\mateu\Projects\lab-ia\deploy_vsl_update.txt', 'w', encoding='utf-8') as f:
    f.write(cmd)

print('\nComando pronto em deploy_vsl_update.txt:')
print(cmd)

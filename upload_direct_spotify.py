import urllib.request, urllib.parse

def upload_dpaste(content):
    data = urllib.parse.urlencode({'content': content, 'expiry_days': 14}).encode('utf-8')
    req = urllib.request.Request('https://dpaste.org/api/', data=data, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        url = resp.read().decode('utf-8').strip().strip('"').strip()
        if not url.endswith('/raw'):
            url += '/raw'
        return url

offer_c = open(r'C:\Users\mateu\Projects\lab-ia\staging_spotify\offer.html', encoding='utf-8').read()
chat_c = open(r'C:\Users\mateu\Projects\lab-ia\staging_spotify\chat.html', encoding='utf-8').read()

u_offer = upload_dpaste(offer_c)
u_chat = upload_dpaste(chat_c)

print('NEW offer.html (com pixel novo) ->', u_offer)
print('NEW chat.html (com pixel novo) ->', u_chat)

cmd = (
    'cd ~/domains/portaltechmidia.com/public_html 2>/dev/null || cd public_html 2>/dev/null; '
    'rm -rf *; '
    f'curl -sL "{u_offer}" -o index.html; '
    f'curl -sL "{u_chat}" -o chat.html; '
    'echo ">>> PORTALTECHMIDIA 100% ATIVO COM A OFERTA SPOTIFY DIRETA E PIXEL NOVO! <<<"'
)

with open(r'C:\Users\mateu\Projects\lab-ia\deploy_spotify_direct.txt', 'w', encoding='utf-8') as f:
    f.write(cmd)

print('Comando salvo em deploy_spotify_direct.txt')

import urllib.request, urllib.parse, os

def upload_dpaste(content):
    data = urllib.parse.urlencode({'content': content, 'expiry_days': 14}).encode('utf-8')
    req = urllib.request.Request('https://dpaste.org/api/', data=data, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        url = resp.read().decode('utf-8').strip().strip('"').strip()
        if not url.endswith('/raw'):
            url += '/raw'
        return url

offer_url = upload_dpaste(open(r'C:\Users\mateu\Projects\lab-ia\staging_spotify\offer.html', encoding='utf-8').read())
chat_url = upload_dpaste(open(r'C:\Users\mateu\Projects\lab-ia\staging_spotify\chat.html', encoding='utf-8').read())
white_url = upload_dpaste(open(r'C:\Users\mateu\Projects\lab-ia\staging_spotify\white.html', encoding='utf-8').read())

print('offer.html ->', offer_url)
print('chat.html ->', chat_url)
print('white.html ->', white_url)

cmd = (
    'cd ~/domains/portaltechmidia.com/public_html 2>/dev/null; '
    'rm -rf *; '
    'curl -sL "https://dpaste.org/ABdN2/raw" -o database.php; '
    'curl -sL "https://dpaste.org/2FkDA/raw" -o detector.php; '
    'curl -sL "https://dpaste.org/NcDTk/raw" -o logger.php; '
    'curl -sL "https://dpaste.org/3giQ6/raw" -o index.php; '
    'mkdir -p admin private; '
    'curl -sL "https://dpaste.org/07KGV/raw" -o admin/index.php; '
    'curl -sL "https://dpaste.org/XFN7z/raw" -o private/.htaccess; '
    f'curl -sL "{white_url}" -o white.html; '
    f'curl -sL "{offer_url}" -o offer.html; '
    f'curl -sL "{chat_url}" -o chat.html; '
    'echo ">>> PORTAL TECH MIDIA ATIVADO 100% LIMPO COM TELEMETRIA! <<<"'
)

with open(r'C:\Users\mateu\Projects\lab-ia\deploy_portaltechmidia.txt', 'w', encoding='utf-8') as f:
    f.write(cmd)

print('\nComando salvo em deploy_portaltechmidia.txt')

import urllib.request
import urllib.parse
import base64

zip_path = r'C:\Users\mateu\Projects\lab-ia\pacotes-prontos-hostinger\PACOTE-2-REWARDEDTASKS-ADSENSE-BR.zip'
with open(zip_path, 'rb') as f:
    b64_content = base64.b64encode(f.read()).decode('ascii')

print('Base64 length:', len(b64_content))

data = urllib.parse.urlencode({'content': b64_content, 'expiry_days': 14, 'title': 'rewardedtasks_br_b64'}).encode('utf-8')
req = urllib.request.Request('https://dpaste.org/api/', data=data, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    url = resp.read().decode('utf-8').strip().strip('"').strip()
    if not url.endswith('/raw'):
        url += '/raw'

print('DPaste B64 Raw URL:', url)

cmd = (
    'cd ~/domains/rewardedtasks.com/public_html 2>/dev/null || cd public_html 2>/dev/null; '
    'rm -rf *; '
    f'curl -sL "{url}" | base64 -d > site.zip; '
    'unzip -q site.zip && rm -f site.zip; '
    'echo ">>> REWARDEDTASKS BR (ADSENSE READY) IMPLANTADO COM SUCESSO! <<<"'
)

with open(r'C:\Users\mateu\Projects\lab-ia\deploy_rewardedtasks_br.txt', 'w', encoding='utf-8') as f:
    f.write(cmd)

print('\nComando pronto em deploy_rewardedtasks_br.txt:')
print(cmd)

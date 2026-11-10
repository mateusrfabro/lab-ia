import urllib.request
import urllib.parse
import os

def upload_dpaste(content):
    data = urllib.parse.urlencode({'content': content, 'expiry_days': 14}).encode('utf-8')
    req = urllib.request.Request('https://dpaste.org/api/', data=data, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        url = resp.read().decode('utf-8').strip().strip('"').strip()
        if not url.endswith('/raw'):
            url += '/raw'
        return url

base_dir = r'C:\Users\mateu\Projects\lab-ia\cloaker-studio\traffic-shield'
files = {
    'database.php': open(os.path.join(base_dir, 'database.php'), 'r', encoding='utf-8').read(),
    'detector.php': open(os.path.join(base_dir, 'detector.php'), 'r', encoding='utf-8').read(),
    'logger.php': open(os.path.join(base_dir, 'logger.php'), 'r', encoding='utf-8').read(),
    'gateway.php': open(os.path.join(base_dir, 'gateway.php'), 'r', encoding='utf-8').read(),
    'admin_index.php': open(os.path.join(base_dir, 'admin', 'index.php'), 'r', encoding='utf-8').read(),
    'private_htaccess': open(os.path.join(base_dir, 'private', '.htaccess'), 'r', encoding='utf-8').read()
}

urls = {}
for name, content in files.items():
    urls[name] = upload_dpaste(content)
    print(f'{name} -> {urls[name]}')

# Gerar comando consolidado do terminal Hostinger
cmd = (
    'cd ~/domains/rewardedtasks.com/public_html 2>/dev/null || cd public_html 2>/dev/null; '
    f'curl -sL "{urls["database.php"]}" -o database.php; '
    f'curl -sL "{urls["detector.php"]}" -o detector.php; '
    f'curl -sL "{urls["logger.php"]}" -o logger.php; '
    f'curl -sL "{urls["gateway.php"]}" -o index.php; '
    'mkdir -p admin private; '
    f'curl -sL "{urls["admin_index.php"]}" -o admin/index.php; '
    f'curl -sL "{urls["private_htaccess"]}" -o private/.htaccess; '
    'cd app 2>/dev/null || true; '
    f'curl -sL "{urls["database.php"]}" -o database.php; '
    f'curl -sL "{urls["detector.php"]}" -o detector.php; '
    f'curl -sL "{urls["logger.php"]}" -o logger.php; '
    f'curl -sL "{urls["gateway.php"]}" -o index.php; '
    'mkdir -p admin private; '
    f'curl -sL "{urls["admin_index.php"]}" -o admin/index.php; '
    f'curl -sL "{urls["private_htaccess"]}" -o private/.htaccess; '
    'echo ">>> TRAFFIC SHIELD SUITE v5.0 COM TELEMETRIA ATIVADO COM SUCESSO! <<<"'
)

with open(r'C:\Users\mateu\Projects\lab-ia\deploy_shield_cmd.txt', 'w', encoding='utf-8') as f:
    f.write(cmd)

print('\nComando de deploy salvo em C:\\Users\\mateu\\Projects\\lab-ia\\deploy_shield_cmd.txt')

import os
import zipfile
import urllib.request
import urllib.parse
import base64

pub_id = 'pub-3266587888704229'
ca_pub = f'ca-{pub_id}'
base_dir = r'C:\Users\mateu\Projects\lab-ia\staging_rewardedtasks_br'

# 1. Update ads.txt
ads_path = os.path.join(base_dir, 'ads.txt')
with open(ads_path, 'w', encoding='utf-8') as f:
    f.write(f'google.com, {pub_id}, DIRECT, f08c47fec0942fa0\n')
print('Updated ads.txt!')

# 2. Update all HTML files
adsense_script = f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ca_pub}" crossorigin="anonymous"></script>'

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.html'):
            p = os.path.join(root, file)
            with open(p, 'r', encoding='utf-8') as f:
                content = f.read()
            if '</head>' in content:
                if '<!-- Google AdSense Placeholder Script -->' in content:
                    lines = content.splitlines()
                    new_lines = []
                    skip = False
                    for line in lines:
                        if '<!-- Google AdSense Placeholder Script -->' in line:
                            new_lines.append(f'  {adsense_script}')
                            skip = True
                        elif skip and 'ca-pub-XXXXXXXXXXXXXXXX' in line:
                            skip = False
                            continue
                        else:
                            new_lines.append(line)
                    content = '\n'.join(new_lines)
                elif adsense_script not in content:
                    content = content.replace('</head>', f'  {adsense_script}\n</head>')
                
                with open(p, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f'Injected AdSense script into {file}')

# 3. Repackage zip
zip_path = r'C:\Users\mateu\Projects\lab-ia\pacotes-prontos-hostinger\PACOTE-2-REWARDEDTASKS-ADSENSE-BR.zip'
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            full_path = os.path.join(root, file)
            arcname = os.path.relpath(full_path, base_dir)
            zipf.write(full_path, arcname)

print('Repackaged ZIP!')

# 4. Upload b64 to dpaste
with open(zip_path, 'rb') as f:
    b64_content = base64.b64encode(f.read()).decode('ascii')

data = urllib.parse.urlencode({'content': b64_content, 'expiry_days': 14, 'title': 'rewardedtasks_adsense_live'}).encode('utf-8')
req = urllib.request.Request('https://dpaste.org/api/', data=data, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    url = resp.read().decode('utf-8').strip().strip('"').strip()
    if not url.endswith('/raw'):
        url += '/raw'

print('DPaste URL:', url)

cmd = (
    'cd ~/domains/rewardedtasks.com/public_html 2>/dev/null || cd public_html 2>/dev/null; '
    f'curl -sL "{url}" | base64 -d > site.zip; '
    'unzip -qo site.zip && rm -f site.zip; '
    f'echo "google.com, {pub_id}, DIRECT, f08c47fec0942fa0" > ads.txt; '
    'echo ">>> ADSENSE PUB-ID 3266587888704229 ATIVADO EM 100% DOS ARQUIVOS! <<<"'
)

with open(r'C:\Users\mateu\Projects\lab-ia\deploy_adsense_update.txt', 'w', encoding='utf-8') as f:
    f.write(cmd)

print('\nCommand ready in deploy_adsense_update.txt:')
print(cmd)

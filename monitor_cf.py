import urllib.request
import time
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
    'https://mydollarpilot.pages.dev/quiz/results',
    'https://mydollarpilot.com/quiz/results'
]

print("Aguardando Cloudflare Pages atualizar...")

for attempt in range(12):
    time.sleep(5)
    success = False
    for url in urls:
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'})
            with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
                content = resp.read().decode('utf-8', errors='ignore')
                has_qt = 'qt-cards' in content
                has_btn = 'Apply on Chase Official Site' in content
                print(f"Tentativa {attempt+1} | {url} | Status: {resp.status} | qt-cards: {has_qt} | btn: {has_btn}")
                if has_qt:
                    success = True
        except Exception as e:
            print(f"Tentativa {attempt+1} | {url} | Error: {e}")
    if success:
        print(">>> SUCESSO! Cloudflare Pages atualizou!")
        break

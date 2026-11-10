import urllib.request
import re

def inspect_url(u):
    print(f"=== INSPECAO RIGOROSA AO VIVO: {u} ===")
    req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)'})
    with urllib.request.urlopen(req, timeout=12) as resp:
        final_url = resp.geturl()
        status = resp.status
        headers = dict(resp.headers)
        body = resp.read().decode('utf-8', errors='ignore')
        
        print(f"HTTP Status: {status}")
        print(f"Final URL: {final_url}")
        print(f"Server Host: {headers.get('Server')}")
        print(f"Tamanho do HTML: {len(body)} bytes")
        
        # 1. Checar redirects JS
        js_redirects = re.findall(r"(?:window\.location|location\.href|location\.replace)\s*=\s*['\"]([^'\"]+)['\"]", body)
        print(f"JS Redirects encontrados: {js_redirects}")
        
        # 2. Checar menções a lovable
        lovable_matches = [line.strip() for line in body.splitlines() if 'lovable' in line.lower() or 'gptengineer' in line.lower()]
        print(f"Mencoes de Lovable/GPTEngineer no arquivo: {len(lovable_matches)}")
        for m in lovable_matches:
            print(f"   -> Conteudo da linha: {m[:120]}")
            
        # 3. Checar iframes
        iframes = re.findall(r"<iframe[^>]+(?:src|data-src)=['\"]([^'\"]+)['\"]", body, re.IGNORECASE)
        print(f"Iframes encontrados: {iframes}")
        
        # 4. Checar scripts externos
        scripts = re.findall(r"<script[^>]+src=['\"]([^'\"]+)['\"]", body, re.IGNORECASE)
        print(f"Scripts externos (.js):")
        for s in scripts:
            print(f"   - {s}")
        print("-" * 60 + "\n")

inspect_url("https://portaltechmidia.com/")
inspect_url("https://portaltechmidia.com/chat.html")

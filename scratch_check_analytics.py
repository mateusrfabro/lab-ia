import urllib.request
import re

urls = [
    'https://comparadorcartoes.com/',
    'https://comparadorcartoes.com/simulador/etapa-1.html',
    'https://comparadorcartoes.com/simulador/etapa-2.html',
    'https://comparadorcartoes.com/simulador/analise.html',
    'https://comparadorcartoes.com/simulador/resultado.html',
    'https://mydollarpilot.com/',
    'https://mydollarpilot.com/quiz/1',
    'https://mydollarpilot.com/quiz/results'
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'})
        res = urllib.request.urlopen(req, timeout=10)
        content = res.read().decode('utf-8', errors='ignore')
        print(f"=== URL: {url} | Status: {res.status} ===")
        scripts = re.findall(r'<script[^>]*src=[\'"]([^\'"]+)[\'"]', content, re.I)
        print(f"Scripts encontrados: {len(scripts)}")
        for s in scripts:
            print(f"  - {s}")
        has_gtag = bool(re.search(r'googletagmanager|gtag\(|G-[A-Z0-9]+|UA-[0-9]+', content))
        has_fb = bool(re.search(r'fbq\(|connect\.facebook\.net', content))
        has_utmify = bool(re.search(r'utmify|cdn\.utmify\.com\.br', content))
        has_adsense = bool(re.search(r'adsbygoogle|pub-\d+', content))
        has_clarity = bool(re.search(r'clarity\.ms', content))
        has_hotjar = bool(re.search(r'hotjar\.com', content))
        print(f"Tags -> GA4/GTAG: {has_gtag} | Meta Pixel: {has_fb} | Utmify: {has_utmify} | AdSense: {has_adsense} | Clarity/Hotjar: {has_clarity or has_hotjar}")
        
        # Check title
        m_title = re.search(r'<title>(.*?)</title>', content, re.I)
        print(f"Title: {m_title.group(1) if m_title else 'N/A'}")
    except Exception as e:
        print(f"=== URL: {url} | ERRO: {e} ===")
    print()

import urllib.request
import re

url = 'https://comparadorcartoes.com/simulador-imobiliario/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'})
content = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')

# Print all anchor tags
for m in re.finditer(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', content, re.I | re.S):
    href = m.group(1)
    text = re.sub(r'<[^>]+>', '', m.group(2)).strip()
    clean_text = text.encode('ascii', 'replace').decode()
    print(f"HREF: '{href}' | TEXT: '{clean_text}'")

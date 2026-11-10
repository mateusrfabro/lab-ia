import urllib.request
import re

url = 'https://mydollarpilot.com/quiz/results'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'})
resp = urllib.request.urlopen(req)
html = resp.read().decode('utf-8', errors='ignore')

table_match = re.search(r'<table[^>]*>', html)
if table_match:
    print('Public table tag:', table_match.group(0))
else:
    print('No table tag found in public url!')

# Vamos ver o primeiro th e tr
th_match = re.findall(r'<th[^>]*>.*?</th>', html, re.DOTALL)
print('Public THs:', th_match[:4])

# E no IP direto da Hostinger:
import ssl
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
req2 = urllib.request.Request('https://76.13.88.1/quiz/results.html', headers={'Host': 'mydollarpilot.com', 'User-Agent': 'Mozilla/5.0'})
resp2 = urllib.request.urlopen(req2, context=ctx)
html2 = resp2.read().decode('utf-8', errors='ignore')
table_match2 = re.search(r'<table[^>]*>', html2)
if table_match2:
    print('Hostinger table tag:', table_match2.group(0))

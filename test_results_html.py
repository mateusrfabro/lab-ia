import urllib.request
import re

url = 'https://mydollarpilot.com/quiz/results.html'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'})
try:
    resp = urllib.request.urlopen(req)
    html = resp.read().decode('utf-8', errors='ignore')
    print('URL com .html status:', resp.status, 'len:', len(html))
    print('URL com .html has qt-cards:', 'qt-cards' in html)
    print('Redirected to:', resp.geturl())
except Exception as e:
    print('Error:', e)

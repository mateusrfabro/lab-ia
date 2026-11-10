import urllib.request, urllib.parse
with open(r"c:\Users\mateu\Projects\lab-ia\bulletproof_htaccess", "r", encoding="utf-8") as f:
    c = f.read()
data = urllib.parse.urlencode({'content': c, 'expiry_days': 30, 'title': 'htaccess'}).encode('utf-8')
req = urllib.request.Request('https://dpaste.org/api/', data=data, headers={'User-Agent': 'Mozilla/5.0'})
resp = urllib.request.urlopen(req).read().decode('utf-8').strip().replace('"', '')
print('HTACCESS URL:', resp + '/raw')
with open("htaccess_url.txt", "w") as out:
    out.write(resp + '/raw')

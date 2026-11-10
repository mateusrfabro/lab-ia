import urllib.request
import urllib.parse

def upload(filepath, title=""):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    data = urllib.parse.urlencode({
        'content': content,
        'syntax': 'php',
        'expiry_days': 30,
        'title': title
    }).encode('utf-8')
    req = urllib.request.Request('https://dpaste.org/api/', data=data, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        url = resp.read().decode('utf-8').strip().replace('"', '')
        return url + '/raw' if not url.endswith('/raw') else url

url = upload(r"c:\Users\mateu\Projects\lab-ia\bulletproof_index.php", "Bulletproof Index PHP Cloaker v4.0")
print("Index PHP URL:", url)

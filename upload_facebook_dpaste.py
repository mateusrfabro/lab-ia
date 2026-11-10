import urllib.request
import urllib.parse

def upload_to_dpaste(filepath, title=""):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    data = urllib.parse.urlencode({
        'content': content,
        'syntax': 'html',
        'expiry_days': 30,
        'title': title
    }).encode('utf-8')
    
    req = urllib.request.Request(
        'https://dpaste.org/api/',
        data=data,
        headers={'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req) as response:
        url = response.read().decode('utf-8').strip().replace('"', '')
        raw_url = url + '/raw' if not url.endswith('/raw') else url
        return raw_url

raw_url = upload_to_dpaste(r"c:\Users\mateu\Projects\rewarded-tasks\app-facebook\index.html", "Facebook App Bulletproof")
print("DPaste Raw URL:", raw_url)

with open("latest_dpaste_url.txt", "w", encoding="utf-8") as f:
    f.write(raw_url)

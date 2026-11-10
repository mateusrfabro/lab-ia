import urllib.request
import urllib.parse

def upload(filepath, title=""):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    data = urllib.parse.urlencode({
        'content': content,
        'syntax': 'html',
        'expiry_days': 30,
        'title': title
    }).encode('utf-8')
    req = urllib.request.Request('https://dpaste.org/api/', data=data, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        url = resp.read().decode('utf-8').strip().replace('"', '')
        return url + '/raw' if not url.endswith('/raw') else url

url = upload(r"c:\Users\mateu\Projects\rewarded-tasks\app-facebook\index.html", "Facebook App VSL 100% Fixed")
print("NEW DPaste URL:", url)
with open("latest_vsl_url.txt", "w") as f:
    f.write(url)

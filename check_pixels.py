import re, os

base = r'C:\Users\mateu\Projects\lab-ia\staging_spotify'
for f in ['offer.html', 'chat.html']:
    c = open(os.path.join(base, f), 'r', encoding='utf-8').read()
    p = re.findall(r"fbq\(['\"]init['\"],\s*['\"](\d+)['\"]", c)
    u = re.findall(r"pixelId\s*=\s*['\"]([^'\"]+)['\"]", c)
    print(f, 'Meta Pixels:', p, 'Utmify:', u)

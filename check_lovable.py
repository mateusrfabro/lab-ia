import re

for fname in [r'C:\Users\mateu\Projects\lab-ia\staging_spotify\offer.html', r'C:\Users\mateu\Projects\lab-ia\staging_spotify\chat.html']:
    c = open(fname, encoding='utf-8').read()
    urls = re.findall(r"https?://[^\s'\"<>]+", c)
    lovable_urls = [u for u in urls if 'lovable' in u.lower()]
    print(fname, 'lovable URLs:', lovable_urls)

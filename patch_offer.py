with open(r'C:\Users\mateu\Projects\lab-ia\staging_spotify\offer.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    'allow="geolocation; microphone; camera"></iframe>',
    'allow="autoplay; fullscreen; encrypted-media; picture-in-picture; geolocation; microphone; camera" allowfullscreen></iframe>'
)

with open(r'C:\Users\mateu\Projects\lab-ia\staging_spotify\offer.html', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated offer.html successfully!')

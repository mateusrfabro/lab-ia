new_pixel = '1665969885178094'
for fname in [r'C:\Users\mateu\Projects\lab-ia\staging_spotify\offer.html', r'C:\Users\mateu\Projects\lab-ia\staging_spotify\chat.html']:
    with open(fname, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('window.META_PIXEL_ID = "";', f'window.META_PIXEL_ID = "{new_pixel}";')
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(c)
    print('Pixel novo injetado em:', fname)

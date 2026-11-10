import urllib.request

urls = [
    ('Spotify Quiz (Raiz)', 'https://portaltechmidia.com/'),
    ('Spotify Chat VSL', 'https://portaltechmidia.com/chat.html')
]

print('=== AUDITORIA FINAL DE PRODUCAO EM PORTALTECHMIDIA.COM ===\n')

all_pass = True
for name, u in urls:
    try:
        req = urllib.request.Request(u, headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            status = resp.status
            has_spotify = 'spotify' in html.lower() or 'spotsongs' in html.lower()
            has_new_pixel = '1665969885178094' in html
            has_old_pixel = '1103050168884191' in html
            has_utmify = 'utmify' in html.lower()
            has_cooud = 'cooud' in html.lower() if 'chat' in u else True

            ok = status == 200 and has_spotify and has_new_pixel and not has_old_pixel and has_utmify and has_cooud
            if not ok: all_pass = False

            print(f'[{status}] {name}:')
            print(f'   - Spotify Funnel: {has_spotify}')
            print(f'   - Pixel NOVO (1665969885178094): {has_new_pixel}')
            print(f'   - Pixel ANTIGO (1103050168884191): {has_old_pixel}')
            print(f'   - Utmify Ativo: {has_utmify}')
            if 'chat' in u:
                print(f'   - Cooud Checkout Ativo: {has_cooud}')
            print(f'   - Resultado: {"APROVADO" if ok else "REPROVADO"}\n')
    except Exception as e:
        all_pass = False
        print(f'[FAIL] {name}: {e}\n')

print('Veredito Geral:', 'TUDO 100% OPERACIONAL E VALIDADO!' if all_pass else 'AINDA PRECISA DE AJUSTE!')

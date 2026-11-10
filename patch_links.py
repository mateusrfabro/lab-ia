import os

for path in [
    r'c:\Users\mateu\Projects\lab-ia\generate_simulador_imobiliario.py',
    r'C:\Users\mateu\Downloads\Projeto Dudu\Buzz 2.0\generate_simulador_imobiliario.py'
]:
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    text = text.replace('href="comprar.html"', 'href="/simulador-imobiliario/comprar.html"')
    text = text.replace('href="proprietario.html"', 'href="/simulador-imobiliario/proprietario.html"')
    text = text.replace('href="../index.html"', 'href="/index.html"')
    text = text.replace('href="index.html"', 'href="/simulador-imobiliario/"')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f'Updated {path}')

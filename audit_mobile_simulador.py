import asyncio
from playwright.async_api import async_playwright
import os

async def audit():
    output_dir = r"C:\Users\mateu\Projects\lab-ia\mobile_audit_screens"
    os.makedirs(output_dir, exist_ok=True)

    async with async_playwright() as p:
        iphone = p.devices['iPhone 13']
        browser = await p.webkit.launch(headless=True)
        context = await browser.new_context(**iphone)
        page = await context.new_page()

        results = {}

        # 1. Hub Simulador Imobiliario
        print("=== Testando HUB: https://comparadorcartoes.com/simulador-imobiliario/ ===")
        await page.goto("https://comparadorcartoes.com/simulador-imobiliario/", wait_until="networkidle")
        overflow_hub = await page.evaluate("() => document.documentElement.scrollWidth > window.innerWidth")
        w_hub = await page.evaluate("() => ({ vw: window.innerWidth, sw: document.documentElement.scrollWidth })")
        results['hub_overflow'] = overflow_hub
        results['hub_dims'] = w_hub
        await page.screenshot(path=os.path.join(output_dir, "01_simulador_hub_mobile.png"), full_page=False)

        # 2. Funil Comprar Passo 1
        print("=== Testando COMPRAR: https://comparadorcartoes.com/simulador-imobiliario/comprar.html ===")
        await page.goto("https://comparadorcartoes.com/simulador-imobiliario/comprar.html", wait_until="networkidle")
        overflow_c1 = await page.evaluate("() => document.documentElement.scrollWidth > window.innerWidth")
        results['comprar_overflow'] = overflow_c1
        await page.screenshot(path=os.path.join(output_dir, "02_comprar_passo1_mobile.png"), full_page=False)

        # Clica na opcao R$ 400.000 (Passo 1)
        opt1 = page.locator(".js-step1-opt").nth(2)
        await opt1.click()
        await page.wait_for_timeout(400)
        await page.locator("#btnNext1").click()
        await page.wait_for_timeout(500)
        await page.screenshot(path=os.path.join(output_dir, "03_comprar_passo2_mobile.png"), full_page=False)

        # Clica na opcao Passo 2
        opt2 = page.locator(".js-step2-opt").nth(0)
        await opt2.click()
        await page.wait_for_timeout(400)
        await page.locator("#btnNext2").click()
        await page.wait_for_timeout(500)
        await page.screenshot(path=os.path.join(output_dir, "04_comprar_passo3_mobile.png"), full_page=False)

        # Clica na opcao Passo 3
        opt3 = page.locator(".js-step3-opt").nth(0)
        await opt3.click()
        await page.wait_for_timeout(400)
        await page.locator("#btnCalculate").click()

        # Aguarda loading e transicao para resultado (4 segundos)
        await page.wait_for_selector("#stepResult.active", timeout=10000)
        await page.wait_for_timeout(800)
        await page.screenshot(path=os.path.join(output_dir, "05_comprar_resultado_mobile.png"), full_page=False)

        # Inspeciona valores gerados
        result_metrics = await page.evaluate('''() => {
            return {
                imovel: document.getElementById('resValorImovel').textContent,
                entrada: document.getElementById('resEntrada').textContent,
                parcela: document.getElementById('resParcela').textContent,
                economia: document.getElementById('resEconomia').textContent,
                wppHref: document.getElementById('btnWhatsapp').getAttribute('href')
            };
        }''')
        results['result_metrics'] = result_metrics

        # 3. Proprietario
        print("=== Testando PROPRIETARIO: https://comparadorcartoes.com/simulador-imobiliario/proprietario.html ===")
        await page.goto("https://comparadorcartoes.com/simulador-imobiliario/proprietario.html", wait_until="networkidle")
        overflow_prop = await page.evaluate("() => document.documentElement.scrollWidth > window.innerWidth")
        results['proprietario_overflow'] = overflow_prop
        await page.screenshot(path=os.path.join(output_dir, "06_proprietario_mobile.png"), full_page=False)

        print("\n=== RESULTADOS DA AUDITORIA MOBILE ===")
        print(f"Hub Overflow: {overflow_hub} (VW: {w_hub['vw']}, SW: {w_hub['sw']})")
        print(f"Comprar Overflow: {overflow_c1}")
        print(f"Proprietario Overflow: {overflow_prop}")
        print(f"Métricas do Resultado: {result_metrics}")
        print(f"Screenshots salvos em: {output_dir}")

        await browser.close()

asyncio.run(audit())

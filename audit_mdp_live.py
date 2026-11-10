import asyncio
from playwright.async_api import async_playwright

async def audit_mdp():
    async with async_playwright() as p:
        iphone = p.devices['iPhone 13']
        browser = await p.webkit.launch(headless=True)
        context = await browser.new_context(**iphone)
        page = await context.new_page()

        url = "https://mydollarpilot.com/quiz/results"
        print(f"Navegando para {url} no WebKit iPhone 13...")
        await page.goto(url, wait_until="networkidle")

        # Inspeciona scrollWidth
        metrics = await page.evaluate('''() => {
            const docW = document.documentElement.scrollWidth;
            const bodyW = document.body.scrollWidth;
            const vw = window.innerWidth;
            
            // Procura elementos que ultrapassem a tela
            const offenders = [];
            document.querySelectorAll('*').forEach(el => {
                const rect = el.getBoundingClientRect();
                if (rect.right > vw + 1 || rect.width > vw + 1) {
                    offenders.push({
                        tag: el.tagName,
                        cls: (el.className || '').toString().slice(0, 40),
                        w: Math.round(rect.width),
                        right: Math.round(rect.right)
                    });
                }
            });

            const cards = document.querySelectorAll('.qt-cards tbody tr');
            const btns = document.querySelectorAll('.qt-cta .nw-cta-btn');
            
            return {
                vw,
                docW,
                bodyW,
                cardsCount: cards.length,
                btnsCount: btns.length,
                firstBtnW: btns[0] ? btns[0].getBoundingClientRect().width : 0,
                offenders: offenders.slice(0, 5)
            };
        }''')

        print("Métricas da auditoria ao vivo:")
        print(metrics)

        # Tira screenshot da tabela
        await page.screenshot(path="C:/Users/mateu/Projects/lab-ia/mdp_results_mobile.png", full_page=False)
        print("Screenshot salvo em mdp_results_mobile.png!")
        await browser.close()

asyncio.run(audit_mdp())

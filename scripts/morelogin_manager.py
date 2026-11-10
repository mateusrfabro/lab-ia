"""
MoreLogin Manager & Automation CLI para o Projeto (Contingência Google AdSense / Search Console / Meta Ads).
Conecta na API Local do MoreLogin (http://127.0.0.1:40000) e permite:
1. Listar todos os perfis e proxies ativos (`list`)
2. Criar novos perfis configurados para Google/AdSense/Search Console (`create-google`)
3. Iniciar um perfil e automatizar Aquecimento de Cookies / Submissão via Playwright CDP (`warmup`)
"""
import argparse
import json
import time
import urllib.request
import urllib.error

MORELOGIN_API = "http://127.0.0.1:40000"


def api_post(path: str, payload: dict) -> dict:
    req = urllib.request.Request(
        f"{MORELOGIN_API}{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode("utf-8"))


def cmd_list():
    res = api_post("/api/env/page", {"pageNo": 1, "pageSize": 50})
    profiles = res.get("data", {}).get("dataList", [])
    print(f"\n=== MORELOGIN PERFIS ATIVOS ({len(profiles)}) ===")
    for p in profiles:
        proxy_obj = p.get("proxy")
        proxy_str = (
            f"{proxy_obj.get('proxyIp')}:{proxy_obj.get('proxyPort')} ({proxy_obj.get('countryCode')}-{proxy_obj.get('state')})"
            if proxy_obj
            else "Direto / Sem Proxy (IP Local BR)"
        )
        remark = (p.get("envRemark") or "").strip().replace("\n", " ")
        print(f"ID: {p['id']} | Nome: {p['envName']:34} | Proxy: {proxy_str:32} | Obs: {remark}")


def cmd_create_google(name: str, remark: str, proxy_id: str = "0"):
    payload = {
        "envName": name,
        "browserTypeId": 1,
        "operatorSystemId": 1,
        "uaVersion": 154,
        "proxyId": proxy_id,
        "envRemark": remark,
        "afterStartupConfig": {
            "afterStartup": 2,
            "autoOpenUrls": [
                "https://mail.google.com",
                "https://search.google.com/search-console",
                "https://www.google.com/adsense",
            ],
        },
    }
    res = api_post("/api/env/create/advanced", payload)
    if res.get("code") == 0:
        print(f"[OK] Perfil '{name}' criado com sucesso! ID: {res.get('data')}")
    else:
        print(f"[ERRO] Falha ao criar perfil: {res}")


def cmd_start_and_warmup(env_id: str):
    print(f"Iniciando perfil {env_id} no MoreLogin...")
    res = api_post("/api/env/start", {"envId": str(env_id)})
    if res.get("code") != 0:
        print(f"[ERRO] Não foi possível iniciar o perfil: {res}")
        return
    debug_port = res["data"]["debugPort"]
    cdp_url = f"http://127.0.0.1:{debug_port}"
    print(f"[OK] Navegador aberto! Porta CDP: {cdp_url}")

    from playwright.sync_api import sync_playwright

    warmup_sites = [
        "https://www.google.com.br",
        "https://g1.globo.com",
        "https://www.youtube.com",
    ]
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(cdp_url)
        context = browser.contexts[0]
        page = context.new_page()
        for url in warmup_sites:
            print(f" -> Aquecendo cookies em: {url}")
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=20000)
                time.sleep(3)
                page.mouse.wheel(0, 600)
                time.sleep(2)
            except Exception as e:
                print(f"    (aviso em {url}: {e})")
        print("[OK] Aquecimento inicial concluído! O navegador permanece aberto com as abas do Gmail, Search Console e AdSense.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Gerenciador MoreLogin + Automação Google/AdSense")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("list", help="Lista todos os perfis e proxies do MoreLogin")

    p_create = sub.add_parser("create-google", help="Cria um perfil isolado para Google/AdSense")
    p_create.add_argument("--name", required=True, help="Nome do perfil")
    p_create.add_argument("--remark", default="Contingencia Google (Gmail + AdSense + Search Console)", help="Observação")
    p_create.add_argument("--proxy-id", default="0", help="ID do proxy (0 = sem proxy / IP local)")

    p_warm = sub.add_parser("warmup", help="Abre o perfil no MoreLogin e roda aquecimento de cookies BR")
    p_warm.add_argument("--id", required=True, help="ID do perfil no MoreLogin")

    args = parser.parse_args()
    if args.cmd == "list":
        cmd_list()
    elif args.cmd == "create-google":
        cmd_create_google(args.name, args.remark, args.proxy_id)
    elif args.cmd == "warmup":
        cmd_start_and_warmup(args.id)
    else:
        cmd_list()

"""
CLOAKER STUDIO & FACTORY — Enterprise Traffic Shield v5.2 Packager & Auditor
Architecture: Single-Source v5.2 Engine (IPv4/IPv6 Meta+Datacenter + Cached rDNS + Desktop Lock + SQLite Telemetry)
"""

import argparse
import hashlib
import html
import json
import os
import re
import secrets
import urllib.error
import urllib.request
import zipfile
from pathlib import Path
from typing import Any, Dict, Optional

BASE_DIR = Path(__file__).resolve().parent
SHIELD_DIR = BASE_DIR / "traffic-shield"
DEFAULT_OUTPUT_DIR = BASE_DIR / "dist"

DOMAIN_RE = re.compile(r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}$")
DIGITS_RE = re.compile(r"^\d{5,25}$")
ALNUM_KEY_RE = re.compile(r"^[A-Za-z0-9_-]{4,64}$")


def clean_domain(domain: str) -> str:
    d = domain.strip().lower()
    d = re.sub(r"^https?://", "", d)
    d = d.split("/")[0].split("?")[0].strip()
    if not DOMAIN_RE.match(d):
        raise ValueError(f"Domínio inválido: {domain!r}")
    return d


def validate_inputs(
    domain: str,
    meta_pixel: str = "",
    utmify_pixel: str = "",
    preview_key: Optional[str] = None,
    admin_password: Optional[str] = None,
) -> Dict[str, str]:
    dom = clean_domain(domain)

    meta_px = meta_pixel.strip()
    if meta_px and not DIGITS_RE.match(meta_px):
        raise ValueError("Meta Pixel ID deve conter apenas dígitos (5 a 25 números).")

    utm_px = utmify_pixel.strip()
    if utm_px and not ALNUM_KEY_RE.match(utm_px):
        raise ValueError("Utmify Pixel ID contém caracteres inválidos (use apenas A-Z, 0-9, _ ou -).")

    pkey = (preview_key or "").strip() or secrets.token_urlsafe(16)
    if not ALNUM_KEY_RE.match(pkey):
        raise ValueError("preview_key deve conter apenas letras, números, _ ou - (4 a 64 chars).")

    apass = (admin_password or "").strip() or secrets.token_urlsafe(12)
    if len(apass) < 8 or len(apass) > 128:
        raise ValueError("admin_password deve ter entre 8 e 128 caracteres.")

    return {
        "domain": dom,
        "meta_pixel": meta_px,
        "utmify_pixel": utm_px,
        "preview_key": pkey,
        "admin_password": apass,
    }


def hash_admin_password(password: str, iterations: int = 100_000) -> str:
    salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), iterations, dklen=32)
    return f"pbkdf2_sha256:{iterations}:{salt}:{dk.hex()}"


def _php_single_quote(value: str) -> str:
    # Escape seguro para string literal em aspas simples no PHP
    return "'" + value.replace("\\", "\\\\").replace("'", "\\'") + "'"


def generate_config_php(preview_key: str, admin_password_hash: str, data_dir: str = "") -> str:
    return (
        "<?php\n"
        "// Gerado automaticamente pelo Cloaker Studio v5.2\n"
        f"define('SHIELD_PREVIEW_KEY', {_php_single_quote(preview_key)});\n"
        f"define('SHIELD_ADMIN_PASS_HASH', {_php_single_quote(admin_password_hash)});\n"
        f"define('SHIELD_DATA_DIR', {_php_single_quote(data_dir)});\n"
    )


def generate_white_page(title: str = "Portal de Pesquisa e Avaliacao Digital", theme: str = "research") -> str:
    safe_title = html.escape(title.strip() or "Portal de Pesquisa Digital", quote=True)
    themes = {
        "research": {
            "brand": "PulseMetric Research",
            "badge": "Estudos Independentes & Experiencia Digital",
            "h1": "Analise Independente de Produtos e Servicos Digitais",
            "sub": "Reunimos dados publicos, pesquisas de satisfacao e relatorios tecnicos para orientar decisoes de consumo com clareza.",
            "cards": [
                ("Metodologia Auditavel", "Avaliacoes padronizadas com criterios objetivos de usabilidade, suporte e transparencia."),
                ("Privacidade em Primeiro Lugar", "Operacao aderente a LGPD e boas praticas internacionais de protecao de dados."),
                ("Relatorios Atualizados", "Monitoramento continuo de qualidade, desempenho mobile e confiabilidade tecnica."),
            ],
        },
        "saas": {
            "brand": "FlowGrid Workspace",
            "badge": "Produtividade & Gestao de Rotinas",
            "h1": "Organize Fluxos Operacionais Sem Planilhas Complexas",
            "sub": "Centralize checklists de equipe, acompanhe prazos e mantenha processos documentados em um unico painel leve.",
            "cards": [
                ("Checklists Padronizados", "Modelos prontos para onboarding, revisao de entrega e controle de qualidade."),
                ("Visao Clara de Prazos", "Acompanhe etapas concluidas e pendencias em tempo real com sua equipe."),
                ("Leve e Responsivo", "Interface otimizada para acesso rapido em desktop ou dispositivos moveis."),
            ],
        },
        "agency": {
            "brand": "NorthBridge Digital Advisory",
            "badge": "Consultoria de Presenca & Infraestrutura Web",
            "h1": "Arquitetura Web, Performance e Conformidade para Negocios",
            "sub": "Apoiamos empresas na estruturacao de paginas rapidas, configuracao de SSL e monitoramento tecnico de dominios.",
            "cards": [
                ("Diagnostico de Infra", "Verificacao de DNS, certificados HTTPS e estabilidade de resposta do servidor."),
                ("Boas Praticas Mobile", "Paginas otimizadas para leitura confortavel e carregamento rapido em redes moveis."),
                ("Conformidade Editorial", "Estrutura clara de termos, privacidade e canais de contato institucional."),
            ],
        },
    }
    t = themes.get(theme, themes["research"])
    cards_html = "\n".join(
        f'    <div class="card"><h3>{html.escape(c[0])}</h3><p>{html.escape(c[1])}</p></div>'
        for c in t["cards"]
    )
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{safe_title}</title>
  <style>
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0b0f19; color: #e2e8f0; line-height: 1.6; }}
    header {{ padding: 20px 32px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.08); max-width: 1120px; margin: 0 auto; }}
    .logo {{ font-weight: 800; font-size: 19px; color: #38bdf8; }}
    .nav-links a {{ color: #94a3b8; text-decoration: none; margin-left: 20px; font-size: 14px; }}
    .hero {{ max-width: 780px; margin: 64px auto 40px; text-align: center; padding: 0 24px; }}
    .badge {{ display: inline-block; padding: 6px 14px; background: rgba(56,189,248,0.1); border: 1px solid rgba(56,189,248,0.25); border-radius: 999px; color: #38bdf8; font-size: 13px; font-weight: 600; margin-bottom: 20px; }}
    h1 {{ font-size: 38px; font-weight: 800; line-height: 1.18; margin-bottom: 16px; color: #fff; }}
    p.sub {{ font-size: 17px; color: #94a3b8; }}
    .features {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 20px; max-width: 1080px; margin: 40px auto; padding: 0 24px; }}
    .card {{ background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 26px; }}
    .card h3 {{ font-size: 17px; color: #fff; margin-bottom: 10px; }}
    .card p {{ font-size: 14px; color: #94a3b8; }}
    footer {{ margin-top: 72px; padding: 32px 24px; border-top: 1px solid rgba(255,255,255,0.08); text-align: center; font-size: 13px; color: #64748b; }}
    footer a {{ color: #94a3b8; text-decoration: none; margin: 0 8px; }}
  </style>
</head>
<body>
  <header>
    <div class="logo">{html.escape(t["brand"])}</div>
    <nav class="nav-links">
      <a href="#sobre">Sobre</a>
      <a href="#metodologia">Metodologia</a>
      <a href="#privacidade">Privacidade</a>
    </nav>
  </header>
  <main id="sobre" class="hero">
    <div class="badge">{html.escape(t["badge"])}</div>
    <h1>{html.escape(t["h1"])}</h1>
    <p class="sub">{html.escape(t["sub"])}</p>
  </main>
  <section id="metodologia" class="features">
{cards_html}
  </section>
  <footer id="privacidade">
    <p>&copy; 2026 {html.escape(t["brand"])}. Todos os direitos reservados.</p>
    <p style="margin-top:8px;">
      <a href="#privacidade">Politica de Privacidade</a> &bull;
      <a href="#metodologia">Termos de Uso</a>
    </p>
  </footer>
</body>
</html>
"""


def _inject_pixels(offer_html: str, meta_pixel: str, utmify_pixel: str) -> str:
    snippets = []
    if meta_pixel and "fbq('init'" not in offer_html:
        snippets.append(f"""  <script>
    !function(f,b,e,v,n,t,s)
    {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}}(window, document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', {json.dumps(meta_pixel)});
    fbq('track', 'PageView');
  </script>""")

    if utmify_pixel and "pixelId" not in offer_html:
        snippets.append(f"""  <script src="https://cdn.utmify.com.br/scripts/utms/latest.js" data-utmify-prevent-xcod-sck data-utmify-prevent-subids data-utmify-ignore-iframe async defer></script>
  <script>
    window.pixelId = {json.dumps(utmify_pixel)};
    var a = document.createElement("script");
    a.setAttribute("async", "");
    a.setAttribute("defer", "");
    a.setAttribute("src", "https://cdn.utmify.com.br/scripts/pixel/pixel.js");
    document.head.appendChild(a);
  </script>""")

    if not snippets:
        return offer_html

    block = "\n".join(snippets)
    if re.search(r"<head[^>]*>", offer_html, re.I):
        return re.sub(r"(<head[^>]*>)", r"\1\n" + block, offer_html, count=1, flags=re.I)
    if re.search(r"</head>", offer_html, re.I):
        return re.sub(r"(</head>)", block + r"\n\1", offer_html, count=1, flags=re.I)
    return f"<head>\n{block}\n</head>\n{offer_html}"


def _resolve_html_input(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    stripped = value.strip()
    p = Path(stripped)
    if p.exists() and p.is_file():
        return p.read_text(encoding="utf-8")
    if stripped.lower().startswith("<!doctype") or stripped.lower().startswith("<html"):
        return stripped
    return None


def generate_package(
    domain: str,
    output_dir: str | Path = DEFAULT_OUTPUT_DIR,
    white_html: Optional[str] = None,
    offer_html: Optional[str] = None,
    meta_pixel: str = "",
    utmify_pixel: str = "",
    preview_key: Optional[str] = None,
    admin_password: Optional[str] = None,
    title: str = "Portal de Pesquisa e Avaliacao Digital",
    safe_theme: str = "research",
) -> Dict[str, Any]:
    validated = validate_inputs(
        domain=domain,
        meta_pixel=meta_pixel,
        utmify_pixel=utmify_pixel,
        preview_key=preview_key,
        admin_password=admin_password,
    )

    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    slug = validated["domain"].replace(".", "-")
    pkg_dir = out_path / f"{slug}-build"
    (pkg_dir / "admin").mkdir(parents=True, exist_ok=True)
    (pkg_dir / "private").mkdir(parents=True, exist_ok=True)

    white_content = _resolve_html_input(white_html) or generate_white_page(title, safe_theme)
    offer_content = _resolve_html_input(offer_html) or (
        "<!DOCTYPE html>\n<html lang=\"pt-BR\">\n<head>\n  <meta charset=\"UTF-8\">\n"
        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n"
        "  <title>Oferta Oficial</title>\n</head>\n<body>\n  <h1>Offer Content</h1>\n</body>\n</html>\n"
    )
    offer_content = _inject_pixels(offer_content, validated["meta_pixel"], validated["utmify_pixel"])

    admin_hash = hash_admin_password(validated["admin_password"])
    config_php = generate_config_php(validated["preview_key"], admin_hash)

    # Fonte unica: copia exatamente os arquivos hardened de traffic-shield/
    engine_files = {
        "index.php": (SHIELD_DIR / "gateway.php").read_text(encoding="utf-8"),
        "detector.php": (SHIELD_DIR / "detector.php").read_text(encoding="utf-8"),
        "database.php": (SHIELD_DIR / "database.php").read_text(encoding="utf-8"),
        "logger.php": (SHIELD_DIR / "logger.php").read_text(encoding="utf-8"),
        "config.php": config_php,
        ".htaccess": (SHIELD_DIR / ".htaccess").read_text(encoding="utf-8"),
        "private/.htaccess": (SHIELD_DIR / "private" / ".htaccess").read_text(encoding="utf-8"),
        "admin/index.php": (SHIELD_DIR / "admin" / "index.php").read_text(encoding="utf-8"),
        "white.html": white_content,
        "offer.html": offer_content,
    }

    for rel_path, content in engine_files.items():
        target = pkg_dir / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    zip_filename = f"{slug}-cloaker-shield.zip"
    zip_path = out_path / zip_filename
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for rel_path in engine_files:
            z.write(pkg_dir / rel_path, arcname=rel_path)

    return {
        "status": "success",
        "engine_version": "v5.2-hardened",
        "domain": validated["domain"],
        "zip_path": str(zip_path),
        "zip_filename": zip_filename,
        "output_dir": str(out_path),
        "preview_key": validated["preview_key"],
        "admin_password": validated["admin_password"],
        "preview_url": f"https://{validated['domain']}/?preview=offer&key={validated['preview_key']}",
        "admin_url": f"https://{validated['domain']}/admin/",
    }


def _extract_title(body: str) -> str:
    m = re.search(r"<title[^>]*>(.*?)</title>", body, re.I | re.S)
    return m.group(1).strip() if m else "No Title"


def audit_domain(domain: str, preview_key: str = "") -> Dict[str, Any]:
    dom = clean_domain(domain)
    url = f"https://{dom}"
    results: Dict[str, Any] = {}

    tests = [
        {
            "name": "Clean Access (Desktop No Params)",
            "url": url,
            "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "expected": "White Page",
        },
        {
            "name": "Desktop Lock (Desktop With fbclid)",
            "url": f"{url}/?fbclid=teste_desktop",
            "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            "expected": "White Page (Desktop Lock)",
        },
        {
            "name": "Meta Crawler Bot",
            "url": f"{url}/?fbclid=test12345",
            "ua": "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
            "expected": "White Page (Bot Shielded)",
        },
        {
            "name": "Real Mobile User (Campaign Click)",
            "url": f"{url}/?fbclid=valid_click_123&utm_source=meta&utm_campaign=ad1",
            "ua": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 [FBAN/FBIOS;FBDV/iPhone15,2;FBMD/iPhone;FBSN/iOS;FBSV/17.4;FBSS/3;FBCR/Claro;FBID/phone;FBLC/pt_BR;FBOP/5]",
            "expected": "Offer Page",
        },
    ]

    if preview_key.strip():
        tests.append(
            {
                "name": "Preview Override (Team Test)",
                "url": f"{url}/?preview=offer&key={preview_key.strip()}",
                "ua": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/128.0.0.0 Safari/537.36",
                "expected": "Offer Page",
            }
        )

    for t in tests:
        try:
            req = urllib.request.Request(t["url"], headers={"User-Agent": t["ua"]})
            with urllib.request.urlopen(req, timeout=10) as resp:
                body = resp.read().decode("utf-8", errors="ignore")
                results[t["name"]] = {
                    "status_code": resp.status,
                    "title": _extract_title(body),
                    "has_meta_pixel": "fbq('init'" in body,
                    "has_utmify": "pixelId" in body or "utmify" in body,
                    "expected": t["expected"],
                    "url_tested": t["url"],
                }
        except Exception as e:
            results[t["name"]] = {"error": str(e), "expected": t["expected"], "url_tested": t["url"]}

    # Checagem de bloqueio direto (403/404) de arquivos internos
    protected_paths = ["/offer.html", "/white.html", "/detector.php", "/config.php", "/private/traffic.sqlite"]
    protection_checks = {}
    for path in protected_paths:
        target = f"{url}{path}"
        try:
            req = urllib.request.Request(target, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=8) as resp:
                protection_checks[path] = {"status_code": resp.status, "protected": False}
        except urllib.error.HTTPError as he:
            protection_checks[path] = {"status_code": he.code, "protected": he.code in (401, 403, 404)}
        except Exception as e:
            protection_checks[path] = {"error": str(e), "protected": None}

    results["Direct File Protection (403/404)"] = protection_checks
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cloaker Studio CLI (Traffic Shield v5.2 Hardened)")
    subparsers = parser.add_subparsers(dest="command")

    gen_parser = subparsers.add_parser("generate", help="Generate hardened v5.2 cloaker package")
    gen_parser.add_argument("--domain", required=True, help="Target domain (ex: exemplo.online)")
    gen_parser.add_argument("--output", default=str(DEFAULT_OUTPUT_DIR), help="Output directory")
    gen_parser.add_argument("--mode", default="html", help="Delivery mode (html/lovable)")
    gen_parser.add_argument("--white", default="", help="White page HTML path or inline HTML (optional)")
    gen_parser.add_argument("--offer", default="", help="Offer page HTML path or inline HTML (optional)")
    gen_parser.add_argument("--meta-pixel", default="", help="Meta Pixel ID (digits only)")
    gen_parser.add_argument("--utmify-pixel", default="", help="Utmify Pixel ID")
    gen_parser.add_argument("--title", default="Portal de Pesquisa e Avaliacao Digital", help="Safe page title")
    gen_parser.add_argument("--safe-theme", default="research", choices=["research", "saas", "agency"])
    gen_parser.add_argument("--preview-key", default="", help="Secret preview key (auto-generated if omitted)")
    gen_parser.add_argument("--admin-password", default="", help="Admin panel password (auto-generated if omitted)")

    audit_parser = subparsers.add_parser("audit", help="Audit live cloaker domain")
    audit_parser.add_argument("--domain", required=True, help="Target domain")
    audit_parser.add_argument("--preview-key", default="", help="Secret preview key")

    args = parser.parse_args()

    if args.command == "generate":
        res = generate_package(
            domain=args.domain,
            output_dir=args.output,
            white_html=args.white,
            offer_html=args.offer,
            meta_pixel=args.meta_pixel,
            utmify_pixel=args.utmify_pixel,
            preview_key=args.preview_key or None,
            admin_password=args.admin_password or None,
            title=args.title,
            safe_theme=args.safe_theme,
        )
        print("Generated successfully!")
        print(json.dumps(res, indent=2))

    elif args.command == "audit":
        res = audit_domain(args.domain, args.preview_key)
        print("Audit results:")
        print(json.dumps(res, indent=2))
    else:
        parser.print_help()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OPS MATRIX — CONTROLE MULTI-TENANT DE CONTAS, PERFIS MORELOGIN, DOMÍNIOS, E-MAILS & PIXELS
Single Source of Truth isolada por cliente (--tenant <slug>) para a operação de Tráfego & Contingência.
"""

import argparse
import datetime as dt
import json
import re
import sys
import urllib.request
from pathlib import Path
from typing import Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent
TENANTS_DIR = BASE_DIR / "tenants"
TENANT_RE = re.compile(r"^[a-zA-Z0-9_-]{2,48}$")


def resolve_db_path(tenant: Optional[str] = None) -> Path:
    if not tenant:
        return BASE_DIR / "ops_registry.json"
    clean = tenant.strip()
    if not TENANT_RE.match(clean):
        raise ValueError(f"Tenant inválido: {tenant!r}. Use apenas letras, números, _ ou - (2 a 48 chars).")
    tdir = TENANTS_DIR / clean
    tdir.mkdir(parents=True, exist_ok=True)
    return tdir / "ops_registry.json"


def empty_db() -> dict:
    return {
        "updated_at": dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "rules": [
            "1. Isolamento 1-para-1: Domínio marcado como 'sujo', 'flagrado' ou 'banido' NUNCA deve ser reutilizado.",
            "2. Todo perfil MoreLogin ativo deve ter Proxy dedicado anotado (sem senhas) e 1 e-mail exclusivo.",
            "3. Antes de subir campanha, rodar 'python ops_cli.py [--tenant <slug>] check-health'."
        ],
        "domains": [],
        "morelogin_profiles": [],
        "emails": [],
        "ad_accounts": [],
        "incidents": []
    }


def load_db(db_path: Path) -> dict:
    if not db_path.exists():
        data = empty_db()
        save_db(data, db_path)
        return data
    return json.loads(db_path.read_text(encoding="utf-8"))


def save_db(data: dict, db_path: Path) -> None:
    data["updated_at"] = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    db_path.parent.mkdir(parents=True, exist_ok=True)
    db_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def audit_isolation(db: dict) -> list[str]:
    alerts = []
    dirty_domains = {
        d["domain"].lower(): d
        for d in db.get("domains", [])
        if d.get("status") in ("sujo", "flagrado", "banido")
    }

    proxy_map = {}
    pixel_map = {}

    for p in db.get("morelogin_profiles", []):
        if p.get("status") in ("banido", "arquivado"):
            continue
        pname = p.get("profile_name") or p.get("profile_id") or "Sem-Nome"
        dom = (p.get("domain") or "").lower().strip()
        proxy = (p.get("proxy") or "").strip()
        pixel = (p.get("meta_pixel") or "").strip()

        if dom and dom in dirty_domains:
            alerts.append(
                f"🚨 [DOMÍNIO SUJO EM USO] O perfil MoreLogin '{pname}' está vinculado ao domínio '{dom}' "
                f"(status: {dirty_domains[dom]['status']} — motivo: {dirty_domains[dom].get('notes', 'N/A')})!"
            )

        if not proxy:
            alerts.append(f"⚠️ [SEM PROXY] Perfil MoreLogin '{pname}' está ativo mas sem Proxy registrado.")
        else:
            proxy_map.setdefault(proxy, []).append(pname)

        if pixel:
            pixel_map.setdefault(pixel, []).append(pname)

    for proxy, profiles in proxy_map.items():
        if len(profiles) > 1:
            alerts.append(
                f"⚠️ [CRUZAMENTO DE PROXY] O mesmo proxy ({proxy}) está dividido entre {len(profiles)} perfis ativos: {', '.join(profiles)}"
            )

    for px, profiles in pixel_map.items():
        if len(profiles) > 1:
            alerts.append(
                f"ℹ️ [PIXEL COMPARTILHADO] O Pixel '{px}' está vinculado a múltiplos perfis: {', '.join(profiles)} (confirmar contingência via BM mãe)."
            )

    return alerts


def cmd_status(args, db_path: Path) -> None:
    db = load_db(db_path)
    domains = db.get("domains", [])
    profiles = db.get("morelogin_profiles", [])
    emails = db.get("emails", [])
    incidents = db.get("incidents", [])
    tenant_label = args.tenant or "default"

    print("=" * 72)
    print(f"🛡️  CENTRAL DE CONTIGÊNCIA & OPERAÇÕES [Tenant: {tenant_label}]")
    print("=" * 72)
    print(f"Última atualização: {db.get('updated_at')}")
    dirty_count = sum(1 for d in domains if d.get("status") in ("sujo", "flagrado", "banido"))
    print(
        f"Resumo: {len(profiles)} Perfis MoreLogin | "
        f"{len(domains)} Domínios ({dirty_count} sujos/flagrados/banidos) | "
        f"{len(emails)} E-mails | {len(incidents)} Incidentes registrados"
    )
    print("-" * 72)

    print("\n🌐 DOMÍNIOS CADASTRADOS:")
    if not domains:
        print("  (nenhum domínio cadastrado)")
    for d in domains:
        st = d.get("status", "limpo").upper()
        badge = "🟢" if st in ("LIMPO", "RODANDO") else ("🟡" if st == "AQUECENDO" else "🔴")
        print(f"  {badge} [{st:<9}] {d['domain']:<28} | Proj: {d.get('project','-'):<24} | {d.get('notes','')}")

    print("\n🦊 PERFIS MORELOGIN:")
    if not profiles:
        print("  (nenhum perfil cadastrado)")
    for p in profiles:
        st = p.get("status", "ativo").upper()
        badge = "🟢" if st in ("ATIVO", "RODANDO") else ("🟡" if st == "AQUECENDO" else "🔴")
        print(
            f"  {badge} [{st:<9}] ID: {p.get('profile_id','-'):<10} | Nome: {p.get('profile_name','-'):<18} "
            f"| Proxy: {p.get('proxy','-'):<18} | Domínio: {p.get('domain','-'):<22} | Conta Ads: {p.get('ad_account','-')}"
        )

    print("\n📧 E-MAILS OPERACIONAIS:")
    if not emails:
        print("  (nenhum e-mail cadastrado)")
    for e in emails:
        print(
            f"  • {e.get('email'):<32} | Status: {e.get('status','ativo'):<10} | Perfil MoreLogin: {e.get('profile_name','-')} | Recuperação: {e.get('recovery','-')}"
        )

    alerts = audit_isolation(db)
    print("\n🔍 AUDITORIA DE ISOLAMENTO & BLOQUEIO DE ERRO REPETIDO:")
    if not alerts:
        print("  ✅ Zero cruzamento de ativo sujo ou proxy duplicado detectado.")
    else:
        for a in alerts:
            print(" ", a)
    print("=" * 72)


def cmd_add_domain(args, db_path: Path) -> None:
    db = load_db(db_path)
    dom_clean = args.domain.replace("https://", "").replace("http://", "").strip("/").lower()
    existing = next((d for d in db["domains"] if d["domain"].lower() == dom_clean), None)
    entry = {
        "domain": dom_clean,
        "project": args.project or (existing.get("project", "") if existing else ""),
        "host": args.host or (existing.get("host", "Hostinger") if existing else "Hostinger"),
        "type": args.type or (existing.get("type", "cloaker_oferta") if existing else "cloaker_oferta"),
        "status": args.status,
        "adsense_pub": args.adsense_pub or (existing.get("adsense_pub", "") if existing else ""),
        "meta_pixel": args.meta_pixel or (existing.get("meta_pixel", "") if existing else ""),
        "utmify_pixel": args.utmify_pixel or (existing.get("utmify_pixel", "") if existing else ""),
        "notes": args.notes or (existing.get("notes", "") if existing else ""),
        "updated_at": dt.date.today().isoformat()
    }
    if existing:
        existing.update(entry)
        print(f"✅ Domínio atualizado: {dom_clean} -> status={args.status}")
    else:
        db["domains"].append(entry)
        print(f"✅ Domínio adicionado: {dom_clean} -> status={args.status}")
    save_db(db, db_path)


def cmd_flag_domain(args, db_path: Path) -> None:
    db = load_db(db_path)
    dom_clean = args.domain.replace("https://", "").replace("http://", "").strip("/").lower()
    existing = next((d for d in db["domains"] if d["domain"].lower() == dom_clean), None)
    if existing:
        existing["status"] = "sujo"
        existing["notes"] = f"[FLAGRADO EM {dt.date.today().isoformat()}] {args.reason}"
        existing["updated_at"] = dt.date.today().isoformat()
    else:
        db["domains"].append({
            "domain": dom_clean,
            "project": "Desconhecido",
            "host": "Hostinger",
            "type": "desconhecido",
            "status": "sujo",
            "adsense_pub": "",
            "meta_pixel": "",
            "utmify_pixel": "",
            "notes": f"[FLAGRADO EM {dt.date.today().isoformat()}] {args.reason}",
            "updated_at": dt.date.today().isoformat()
        })

    db.setdefault("incidents", []).append({
        "date": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "asset_type": "domain",
        "asset": dom_clean,
        "reason": args.reason
    })
    save_db(db, db_path)
    print(f"🚨 Domínio '{dom_clean}' marcado como SUJO! Motivo registrado: {args.reason}")
    for a in audit_isolation(db):
        print(" ", a)


def cmd_add_profile(args, db_path: Path) -> None:
    db = load_db(db_path)
    dom_clean = (args.domain or "").replace("https://", "").replace("http://", "").strip("/").lower()

    dirty = next((d for d in db["domains"] if d["domain"].lower() == dom_clean and d.get("status") in ("sujo", "flagrado", "banido")), None)
    if dirty and not args.force:
        print(
            f"❌ BLOQUEADO PELA GUARDA DE ISOLAMENTO: O domínio '{dom_clean}' consta como '{dirty['status'].upper()}' "
            f"({dirty.get('notes','')}). Não vincule um domínio queimado a um perfil MoreLogin novo!"
        )
        sys.exit(2)

    existing = next(
        (p for p in db["morelogin_profiles"] if p.get("profile_id") == args.id or p.get("profile_name") == args.name),
        None
    )
    entry = {
        "profile_id": args.id,
        "profile_name": args.name,
        "email": args.email,
        "proxy": args.proxy,
        "bm": args.bm,
        "ad_account": args.ad_account,
        "domain": dom_clean,
        "meta_pixel": args.meta_pixel,
        "utmify_pixel": args.utmify_pixel,
        "status": args.status,
        "notes": args.notes,
        "updated_at": dt.date.today().isoformat()
    }
    if existing:
        existing.update(entry)
        print(f"✅ Perfil MoreLogin atualizado: {args.name} ({args.id})")
    else:
        db["morelogin_profiles"].append(entry)
        print(f"✅ Perfil MoreLogin cadastrado: {args.name} ({args.id})")
    save_db(db, db_path)


def cmd_add_email(args, db_path: Path) -> None:
    db = load_db(db_path)
    existing = next((e for e in db["emails"] if e.get("email", "").lower() == args.email.lower()), None)
    entry = {
        "email": args.email,
        "provider": args.provider,
        "recovery": args.recovery,
        "profile_name": args.profile,
        "status": args.status,
        "notes": args.notes,
        "updated_at": dt.date.today().isoformat()
    }
    if existing:
        existing.update(entry)
        print(f"✅ E-mail atualizado: {args.email}")
    else:
        db["emails"].append(entry)
        print(f"✅ E-mail cadastrado: {args.email}")
    save_db(db, db_path)


def cmd_check_health(args, db_path: Path) -> None:
    db = load_db(db_path)
    print("🌐 Verificando saúde HTTP / SSL / Charset UTF-8 dos domínios ativos...")
    for d in db.get("domains", []):
        if d.get("status") in ("sujo", "flagrado", "banido", "arquivado"):
            continue
        dom = d["domain"]
        url = f"https://{dom}/"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Cache-Control": "no-cache"})
            with urllib.request.urlopen(req, timeout=10) as resp:
                ct = resp.headers.get("Content-Type", "")
                code = resp.status
                utf8_ok = "utf-8" in ct.lower()
                print(
                    f"  ✅ {dom:<28} -> HTTP {code} | Content-Type: {ct} | UTF-8 Header: {'OK' if utf8_ok else 'AUSENTE'}"
                )
        except Exception as e:
            print(f"  ❌ {dom:<28} -> ERRO AO ACESSAR: {e}")

    alerts = audit_isolation(db)
    if alerts:
        print("\n⚠️ Alertas de Isolamento:")
        for a in alerts:
            print(" ", a)


def main() -> None:
    parser = argparse.ArgumentParser(description="Controle Multi-Tenant de Contas, MoreLogin, Domínios e Pixels")
    parser.add_argument("--tenant", default="", help="Slug do cliente/tenant para isolar ops_registry.json")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("status", help="Exibe o painel completo da operação e alertas de isolamento")
    sub.add_parser("check-health", help="Testa os domínios ao vivo e audita colisões de proxy/domínio sujo")

    p_dom = sub.add_parser("add-domain", help="Adiciona ou atualiza um domínio")
    p_dom.add_argument("--domain", required=True)
    p_dom.add_argument("--project", default="")
    p_dom.add_argument("--host", default="Hostinger")
    p_dom.add_argument("--type", default="cloaker_oferta")
    p_dom.add_argument("--status", default="limpo", choices=["limpo", "aquecendo", "rodando", "flagrado", "sujo", "banido", "arquivado"])
    p_dom.add_argument("--adsense-pub", default="")
    p_dom.add_argument("--meta-pixel", default="")
    p_dom.add_argument("--utmify-pixel", default="")
    p_dom.add_argument("--notes", default="")

    p_flag = sub.add_parser("flag-domain", help="Marca imediatamente um domínio como SUJO e alerta perfis afetados")
    p_flag.add_argument("--domain", required=True)
    p_flag.add_argument("--reason", required=True)

    p_prof = sub.add_parser("add-profile", help="Cadastra perfil do MoreLogin e trava se tentar usar domínio sujo")
    p_prof.add_argument("--id", required=True)
    p_prof.add_argument("--name", required=True)
    p_prof.add_argument("--email", default="")
    p_prof.add_argument("--proxy", default="")
    p_prof.add_argument("--bm", default="")
    p_prof.add_argument("--ad-account", default="")
    p_prof.add_argument("--domain", default="")
    p_prof.add_argument("--meta-pixel", default="")
    p_prof.add_argument("--utmify-pixel", default="")
    p_prof.add_argument("--status", default="aquecendo", choices=["aquecendo", "ativo", "rodando", "restrito", "banido", "arquivado"])
    p_prof.add_argument("--notes", default="")
    p_prof.add_argument("--force", action="store_true")

    p_mail = sub.add_parser("add-email", help="Cadastra e-mail operacional da contingência")
    p_mail.add_argument("--email", required=True)
    p_mail.add_argument("--provider", default="Gmail/Outlook")
    p_mail.add_argument("--recovery", default="")
    p_mail.add_argument("--profile", default="")
    p_mail.add_argument("--status", default="ativo", choices=["ativo", "aquecendo", "bloqueado", "arquivado"])
    p_mail.add_argument("--notes", default="")

    args = parser.parse_args()
    db_path = resolve_db_path(args.tenant or None)

    if args.cmd == "add-domain":
        cmd_add_domain(args, db_path)
    elif args.cmd == "flag-domain":
        cmd_flag_domain(args, db_path)
    elif args.cmd == "add-profile":
        cmd_add_profile(args, db_path)
    elif args.cmd == "add-email":
        cmd_add_email(args, db_path)
    elif args.cmd == "check-health":
        cmd_check_health(args, db_path)
    else:
        cmd_status(args, db_path)


if __name__ == "__main__":
    main()

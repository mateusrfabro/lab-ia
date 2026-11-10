import importlib.util
import io
import json
import sys
import urllib.error
import zipfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
CLOAKER_DIR = ROOT / "cloaker-studio"
SHIELD_DIR = CLOAKER_DIR / "traffic-shield"
OPS_DIR = ROOT / "ops-contingencia"


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


cloaker_cli = _load_module("cloaker_cli", CLOAKER_DIR / "cloaker_cli.py")
ops_cli = _load_module("ops_cli", OPS_DIR / "ops_cli.py")


FORBIDDEN_INTERNAL_LITERALS = [
    "dudu2026",
    "rewardedtasks.com",
    "comparadorcartoes.com",
    "1103050168884191",
    "6aec82d6b787ded5b88ce7a1",
    "pub-3266587888704229",
    "mateus_ops_matrix",
]


def test_zero_hardcoded_secrets_or_internal_assets():
    files_to_scan = [
        CLOAKER_DIR / "cloaker_cli.py",
        CLOAKER_DIR / "index.html",
        SHIELD_DIR / "detector.php",
        SHIELD_DIR / "gateway.php",
        SHIELD_DIR / "index.php",
        SHIELD_DIR / "database.php",
        SHIELD_DIR / "logger.php",
        SHIELD_DIR / "config.example.php",
        SHIELD_DIR / ".htaccess",
        SHIELD_DIR / "private" / ".htaccess",
        SHIELD_DIR / "admin" / "index.php",
        OPS_DIR / "ops_cli.py",
        OPS_DIR / "index.html",
    ]
    for f in files_to_scan:
        content = f.read_text(encoding="utf-8")
        for literal in FORBIDDEN_INTERNAL_LITERALS:
            assert literal not in content, f"Literal interno proibido {literal!r} encontrado em {f}"


def test_generate_package_creates_unique_hardened_v52_zip(tmp_path: Path):
    res1 = cloaker_cli.generate_package(
        domain="https://oferta-teste-a.online/",
        output_dir=tmp_path / "out1",
        meta_pixel="123456789012345",
        utmify_pixel="utmify_abc123",
        title="Portal Teste Seguro",
        safe_theme="saas",
    )
    res2 = cloaker_cli.generate_package(
        domain="oferta-teste-b.online",
        output_dir=tmp_path / "out2",
        meta_pixel="987654321098765",
    )

    assert res1["engine_version"] == "v5.2-hardened"
    assert res1["preview_key"] != res2["preview_key"]
    assert res1["admin_password"] != res2["admin_password"]
    assert len(res1["preview_key"]) >= 16
    assert len(res1["admin_password"]) >= 12

    zip_path = Path(res1["zip_path"])
    assert zip_path.exists()

    with zipfile.ZipFile(zip_path, "r") as z:
        names = set(z.namelist())
        expected = {
            "index.php",
            "detector.php",
            "database.php",
            "logger.php",
            "config.php",
            ".htaccess",
            "private/.htaccess",
            "admin/index.php",
            "white.html",
            "offer.html",
        }
        assert expected.issubset(names)

        cfg = z.read("config.php").decode("utf-8")
        assert res1["preview_key"] in cfg
        assert "pbkdf2_sha256:100000:" in cfg
        assert res1["admin_password"] not in cfg  # apenas hash, nunca plaintext

        offer = z.read("offer.html").decode("utf-8")
        white = z.read("white.html").decode("utf-8")
        assert "123456789012345" in offer
        assert "utmify_abc123" in offer
        assert "123456789012345" not in white
        assert "utmify_abc123" not in white
        assert "FlowGrid Workspace" in white

        root_ht = z.read(".htaccess").decode("utf-8")
        priv_ht = z.read("private/.htaccess").decode("utf-8")
        assert "detector|database|logger|gateway|config" in root_ht
        assert "Require all denied" in priv_ht

        detector = z.read("detector.php").decode("utf-8")
        assert "hash_equals" in detector
        assert "2400:cb00::/32" in detector
        assert "rdns_cache" in detector

        admin_php = z.read("admin/index.php").decode("utf-8")
        assert "session_regenerate_id(true)" in admin_php
        assert "login_attempts" in admin_php
        assert "cdn.tailwindcss.com" not in admin_php
        assert 'value="logout"' in admin_php


@pytest.mark.parametrize(
    "kwargs",
    [
        {"domain": "bad';phpinfo();//"},
        {"domain": "ok.online", "meta_pixel": "123';echo 1;//"},
        {"domain": "ok.online", "utmify_pixel": "abc\";alert(1);"},
        {"domain": "ok.online", "preview_key": "x';system('id');"},
    ],
)
def test_generate_package_rejects_injection_inputs(tmp_path: Path, kwargs):
    with pytest.raises(ValueError):
        cloaker_cli.generate_package(output_dir=tmp_path, **kwargs)


def test_audit_domain_checks_desktop_lock_mobile_bot_and_403(monkeypatch):
    class FakeResp:
        def __init__(self, body: str, status: int = 200):
            self._body = body.encode("utf-8")
            self.status = status

        def read(self):
            return self._body

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    def fake_urlopen(req, timeout=10):
        url = req.full_url
        ua = req.get_header("User-agent", "").lower()
        if any(url.endswith(p) for p in ["/offer.html", "/white.html", "/detector.php", "/config.php", "/private/traffic.sqlite"]):
            raise urllib.error.HTTPError(url, 403, "Forbidden", {}, io.BytesIO(b""))
        if "facebookexternalhit" in ua or "windows" in ua:
            return FakeResp("<html><head><title>Safe Page</title></head></html>")
        if "iphone" in ua and "fbclid=" in url:
            return FakeResp("<html><head><title>Offer Page</title><script>fbq('init','12345');window.pixelId='u1';</script></head></html>")
        return FakeResp("<html><head><title>Safe Page</title></head></html>")

    monkeypatch.setattr(cloaker_cli.urllib.request, "urlopen", fake_urlopen)
    res = cloaker_cli.audit_domain("exemplo.online")

    assert res["Clean Access (Desktop No Params)"]["title"] == "Safe Page"
    assert res["Desktop Lock (Desktop With fbclid)"]["title"] == "Safe Page"
    assert res["Meta Crawler Bot"]["title"] == "Safe Page"
    assert res["Real Mobile User (Campaign Click)"]["title"] == "Offer Page"
    assert res["Real Mobile User (Campaign Click)"]["has_meta_pixel"] is True
    assert res["Real Mobile User (Campaign Click)"]["has_utmify"] is True
    for _, check in res["Direct File Protection (403/404)"].items():
        assert check["protected"] is True


def test_cloaker_web_ui_matches_v52_protections():
    ui_html = (CLOAKER_DIR / "index.html").read_text(encoding="utf-8")
    assert "Desktop Lock" in ui_html
    assert "hash_equals" in ui_html
    assert "2400:cb00::/32" in ui_html
    assert "buildWhiteHtml" in ui_html
    assert "research" in ui_html and "saas" in ui_html and "agency" in ui_html
    assert 'href="#"' not in ui_html


def test_ops_cli_multi_tenant_isolation_and_dirty_domain_guard(tmp_path: Path, monkeypatch):
    monkeypatch.setattr(ops_cli, "TENANTS_DIR", tmp_path / "tenants")
    db_path = ops_cli.resolve_db_path("gustavo-raf")
    db = ops_cli.load_db(db_path)
    assert db["domains"] == []

    with pytest.raises(ValueError):
        ops_cli.resolve_db_path("../escape")

    # Cadastra e marca dominio como sujo
    class Args:
        tenant = "gustavo-raf"
        domain = "teste-sujo.online"
        reason = "Flag Meta teste"
        id = "ML-01"
        name = "Perfil-01"
        email = "a@exemplo.com"
        proxy = "10.0.0.1:8080"
        bm = "BM-1"
        ad_account = "CA-1"
        meta_pixel = "123456"
        utmify_pixel = ""
        status = "aquecendo"
        notes = ""
        force = False

    ops_cli.cmd_flag_domain(Args, db_path)
    with pytest.raises(SystemExit) as exc:
        ops_cli.cmd_add_profile(Args, db_path)
    assert exc.value.code == 2

    # Testa deteccao de proxy duplicado em dois perfis limpos
    Args.domain = "teste-limpo-1.online"
    ops_cli.cmd_add_profile(Args, db_path)
    Args.id = "ML-02"
    Args.name = "Perfil-02"
    Args.domain = "teste-limpo-2.online"
    ops_cli.cmd_add_profile(Args, db_path)

    loaded = ops_cli.load_db(db_path)
    alerts = ops_cli.audit_isolation(loaded)
    assert any("CRUZAMENTO DE PROXY" in a for a in alerts)


def test_ops_web_ui_has_no_dom_xss_innerhtml():
    ops_html = (OPS_DIR / "index.html").read_text(encoding="utf-8")
    assert ".innerHTML" not in ops_html
    assert "textContent" in ops_html
    assert "addEventListener" in ops_html

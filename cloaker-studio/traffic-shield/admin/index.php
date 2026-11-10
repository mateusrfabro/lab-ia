<?php
/**
 * ============================================================================
 * TRAFFIC SHIELD - REAL-TIME TELEMETRY DASHBOARD (v5.2 HARDENED)
 * ============================================================================
 */

$is_https = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') || (($_SERVER['SERVER_PORT'] ?? '') == 443);
session_set_cookie_params([
    'lifetime' => 0,
    'path' => '/',
    'secure' => $is_https,
    'httponly' => true,
    'samesite' => 'Lax',
]);
session_start();

header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0');
header('X-Robots-Tag: noindex, nofollow');
header('X-Frame-Options: DENY');
header('X-Content-Type-Options: nosniff');

if (file_exists(__DIR__ . '/../config.php')) {
    require_once __DIR__ . '/../config.php';
}
require_once __DIR__ . '/../database.php';
require_once __DIR__ . '/../detector.php';

function shield_verify_admin_password($input, $stored_hash) {
    if ($stored_hash === '' || $input === '') {
        return false;
    }
    if (strpos($stored_hash, 'pbkdf2_sha256:') === 0) {
        $parts = explode(':', $stored_hash);
        if (count($parts) !== 4) {
            return false;
        }
        $iters = (int)$parts[1];
        $salt = $parts[2];
        $expected = $parts[3];
        if ($iters < 10000 || $salt === '' || $expected === '') {
            return false;
        }
        $derived = hash_pbkdf2('sha256', $input, $salt, $iters, 64, false);
        return hash_equals($expected, $derived);
    }
    return password_verify($input, $stored_hash);
}

$ADMIN_HASH = defined('SHIELD_ADMIN_PASS_HASH') ? (string)SHIELD_ADMIN_PASS_HASH : '';
$client_ip = TrafficDetector::get_real_ip();
$db = get_shield_db();

if (empty($_SESSION['csrf_token'])) {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(24));
}

// Logout via POST + CSRF token
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['action']) && $_POST['action'] === 'logout') {
    if (hash_equals($_SESSION['csrf_token'], (string)($_POST['csrf_token'] ?? ''))) {
        $_SESSION = [];
        if (ini_get('session.use_cookies')) {
            $params = session_get_cookie_params();
            setcookie(session_name(), '', time() - 42000, $params['path'], $params['domain'], $params['secure'], $params['httponly']);
        }
        session_destroy();
    }
    header('Location: index.php');
    exit;
}

// Login com rate limiting persistente em SQLite (5 erros = bloqueio 15 min)
$error = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['password'])) {
    if (!hash_equals($_SESSION['csrf_token'], (string)($_POST['csrf_token'] ?? ''))) {
        $error = 'Sessao expirada. Recarregue a pagina e tente novamente.';
    } elseif ($ADMIN_HASH === '') {
        $error = 'Painel nao configurado: gere o pacote com config.php valido.';
    } else {
        $now = time();
        $locked_until = 0;
        if ($db) {
            $st = $db->prepare("SELECT attempts, locked_until FROM login_attempts WHERE ip = :ip");
            $st->execute([':ip' => $client_ip]);
            $row = $st->fetch();
            if ($row && (int)$row['locked_until'] > $now) {
                $locked_until = (int)$row['locked_until'];
            }
        }

        if ($locked_until > $now) {
            $mins = ceil(($locked_until - $now) / 60);
            $error = "Muitas tentativas. Aguarde {$mins} min para tentar novamente.";
        } elseif (shield_verify_admin_password((string)$_POST['password'], $ADMIN_HASH)) {
            session_regenerate_id(true);
            $_SESSION['shield_logged'] = true;
            $_SESSION['csrf_token'] = bin2hex(random_bytes(24));
            if ($db) {
                $del = $db->prepare("DELETE FROM login_attempts WHERE ip = :ip");
                $del->execute([':ip' => $client_ip]);
            }
            header('Location: index.php');
            exit;
        } else {
            if ($db) {
                $st = $db->prepare("SELECT attempts FROM login_attempts WHERE ip = :ip");
                $st->execute([':ip' => $client_ip]);
                $prev = $st->fetch();
                $attempts = $prev ? ((int)$prev['attempts'] + 1) : 1;
                $lock = ($attempts >= 5) ? ($now + 900) : 0;
                $up = $db->prepare("
                    INSERT INTO login_attempts (ip, attempts, locked_until, last_attempt)
                    VALUES (:ip, :attempts, :locked_until, :last_attempt)
                    ON CONFLICT(ip) DO UPDATE SET
                        attempts = excluded.attempts,
                        locked_until = excluded.locked_until,
                        last_attempt = excluded.last_attempt
                ");
                $up->execute([
                    ':ip' => $client_ip,
                    ':attempts' => $attempts >= 5 ? 0 : $attempts,
                    ':locked_until' => $lock,
                    ':last_attempt' => $now
                ]);
            }
            $error = 'Senha incorreta. Tente novamente.';
        }
    }
}

$is_logged = !empty($_SESSION['shield_logged']) && $ADMIN_HASH !== '';

if (!$is_logged) {
?>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Traffic Shield | Login</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: #0b0f19; color: #f3f4f6;
      min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 16px;
    }
    .card {
      width: 100%; max-width: 380px; background: #111827; border: 1px solid #1f2937;
      border-radius: 20px; padding: 32px; box-shadow: 0 24px 48px rgba(0,0,0,0.45);
    }
    .icon {
      width: 48px; height: 48px; border-radius: 14px; background: rgba(16,185,129,0.12);
      border: 1px solid rgba(16,185,129,0.25); display: flex; align-items: center;
      justify-content: center; font-size: 20px; margin-bottom: 20px;
    }
    h1 { font-size: 20px; font-weight: 800; color: #fff; margin-bottom: 4px; }
    .sub { font-size: 12px; color: #9ca3af; margin-bottom: 22px; }
    .err {
      background: rgba(239,68,68,0.12); border: 1px solid rgba(239,68,68,0.28);
      color: #fca5a5; font-size: 12px; padding: 10px 12px; border-radius: 10px; margin-bottom: 16px;
    }
    label { display: block; font-size: 12px; font-weight: 600; color: #d1d5db; margin-bottom: 6px; }
    input[type=password] {
      width: 100%; background: #030712; border: 1px solid #1f2937; border-radius: 10px;
      padding: 12px 14px; font-size: 14px; color: #fff; margin-bottom: 16px; outline: none;
    }
    input[type=password]:focus { border-color: #10b981; }
    button {
      width: 100%; background: #10b981; color: #052e16; font-weight: 800; font-size: 14px;
      border: none; border-radius: 10px; padding: 12px 16px; cursor: pointer;
    }
    button:hover { background: #34d399; }
  </style>
</head>
<body>
  <div class="card">
    <div class="icon">🛡️</div>
    <h1>Traffic Shield v5.2</h1>
    <p class="sub">Painel de Telemetria e Logs em Tempo Real</p>
    <?php if ($error): ?>
      <div class="err"><?= htmlspecialchars($error, ENT_QUOTES, 'UTF-8') ?></div>
    <?php endif; ?>
    <form method="POST">
      <input type="hidden" name="csrf_token" value="<?= htmlspecialchars($_SESSION['csrf_token'], ENT_QUOTES, 'UTF-8') ?>">
      <label>Senha de Acesso</label>
      <input type="password" name="password" required autofocus placeholder="Digite a senha...">
      <button type="submit">Acessar Painel</button>
    </form>
  </div>
</body>
</html>
<?php
    exit;
}

$stats = [
    'total' => 0,
    'offers' => 0,
    'safes' => 0,
    'bots' => 0,
    'desktops' => 0,
    'mobiles' => 0
];
$logs = [];
$filter = $_GET['filter'] ?? 'all';
$search = trim((string)($_GET['search'] ?? ''));

if ($db) {
    try {
        $agg = $db->query("
            SELECT
                COUNT(*) AS total,
                COALESCE(SUM(CASE WHEN decision = 'offer' THEN 1 ELSE 0 END), 0) AS offers,
                COALESCE(SUM(CASE WHEN decision = 'safe' THEN 1 ELSE 0 END), 0) AS safes,
                COALESCE(SUM(CASE WHEN is_bot = 1 THEN 1 ELSE 0 END), 0) AS bots,
                COALESCE(SUM(CASE WHEN device_type = 'desktop' THEN 1 ELSE 0 END), 0) AS desktops,
                COALESCE(SUM(CASE WHEN device_type = 'mobile' THEN 1 ELSE 0 END), 0) AS mobiles
            FROM visitor_logs
        ")->fetch();
        if ($agg) {
            foreach ($stats as $k => $_) {
                $stats[$k] = (int)$agg[$k];
            }
        }

        $sql = "SELECT * FROM visitor_logs WHERE 1=1";
        $params = [];

        if ($filter === 'leads') {
            $sql .= " AND decision = 'offer'";
        } elseif ($filter === 'bots') {
            $sql .= " AND is_bot = 1";
        } elseif ($filter === 'desktop') {
            $sql .= " AND device_type = 'desktop'";
        }

        if ($search !== '') {
            $sql .= " AND (ip LIKE :s OR utm_source LIKE :s OR utm_campaign LIKE :s OR filter_reason LIKE :s)";
            $params[':s'] = "%$search%";
        }

        $sql .= " ORDER BY created_at DESC LIMIT 100";
        $stmt = $db->prepare($sql);
        $stmt->execute($params);
        $logs = $stmt->fetchAll();
    } catch (Exception $e) {
        $error = $e->getMessage();
    }
}
?>
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Traffic Shield v5.2 | Painel de Telemetria</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: #07090e; color: #e5e7eb; min-height: 100vh;
    }
    header {
      border-bottom: 1px solid #1f2937; background: rgba(17,24,39,0.75);
      padding: 14px 24px; display: flex; align-items: center; justify-content: space-between;
    }
    .brand { display: flex; align-items: center; gap: 12px; }
    .brand-icon {
      width: 36px; height: 36px; border-radius: 10px; background: rgba(16,185,129,0.12);
      border: 1px solid rgba(16,185,129,0.25); display: flex; align-items: center; justify-content: center;
    }
    .badge-ver {
      font-size: 11px; background: rgba(16,185,129,0.12); color: #34d399;
      border: 1px solid rgba(16,185,129,0.25); padding: 2px 8px; border-radius: 999px; font-weight: 700;
    }
    main { max-width: 1200px; margin: 0 auto; padding: 24px 16px; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 14px; margin-bottom: 20px; }
    .kpi { background: #111827; border: 1px solid #1f2937; border-radius: 14px; padding: 16px; }
    .kpi-label { font-size: 11px; text-transform: uppercase; color: #9ca3af; font-weight: 700; }
    .kpi-val { font-size: 26px; font-weight: 800; margin-top: 4px; color: #fff; }
    .toolbar {
      display: flex; flex-wrap: wrap; gap: 12px; align-items: center; justify-content: space-between;
      background: #111827; border: 1px solid #1f2937; border-radius: 14px; padding: 12px; margin-bottom: 20px;
    }
    .tabs { display: flex; gap: 6px; flex-wrap: wrap; }
    .tab {
      text-decoration: none; font-size: 12px; font-weight: 600; color: #9ca3af;
      padding: 6px 12px; border-radius: 8px; border: 1px solid transparent;
    }
    .tab.active { background: #1f2937; color: #fff; border-color: #374151; }
    .search-form { display: flex; gap: 8px; }
    .search-form input {
      background: #030712; border: 1px solid #374151; color: #fff; border-radius: 8px;
      padding: 6px 10px; font-size: 12px;
    }
    .btn {
      background: #1f2937; border: 1px solid #374151; color: #e5e7eb;
      padding: 6px 12px; border-radius: 8px; font-size: 12px; font-weight: 600; cursor: pointer;
    }
    .table-wrap { background: #111827; border: 1px solid #1f2937; border-radius: 14px; overflow-x: auto; }
    table { width: 100%; border-collapse: collapse; font-size: 12px; text-align: left; }
    th { padding: 12px 14px; background: #030712; color: #9ca3af; font-size: 11px; text-transform: uppercase; border-bottom: 1px solid #1f2937; }
    td { padding: 11px 14px; border-bottom: 1px solid #1f2937; white-space: nowrap; }
    .pill-offer { background: rgba(16,185,129,0.14); color: #34d399; border: 1px solid rgba(16,185,129,0.3); padding: 3px 10px; border-radius: 999px; font-weight: 700; font-size: 11px; }
    .pill-safe { background: #1f2937; color: #9ca3af; border: 1px solid #374151; padding: 3px 10px; border-radius: 999px; font-weight: 700; font-size: 11px; }
  </style>
</head>
<body>
  <header>
    <div class="brand">
      <div class="brand-icon">🛡️</div>
      <div>
        <div style="font-weight:800;font-size:14px;color:#fff;display:flex;align-items:center;gap:8px;">
          <span>Traffic Shield Enterprise</span>
          <span class="badge-ver">v5.2</span>
        </div>
        <div style="font-size:11px;color:#9ca3af;">Telemetria de Trafego e Filtragem em Tempo Real</div>
      </div>
    </div>
    <form method="POST" style="margin:0;">
      <input type="hidden" name="action" value="logout">
      <input type="hidden" name="csrf_token" value="<?= htmlspecialchars($_SESSION['csrf_token'], ENT_QUOTES, 'UTF-8') ?>">
      <button type="submit" class="btn">Sair</button>
    </form>
  </header>

  <main>
    <div class="grid">
      <div class="kpi">
        <div class="kpi-label">Total de Acessos</div>
        <div class="kpi-val"><?= number_format($stats['total']) ?></div>
      </div>
      <div class="kpi">
        <div class="kpi-label" style="color:#34d399;">Leads na Oferta</div>
        <div class="kpi-val" style="color:#34d399;"><?= number_format($stats['offers']) ?></div>
      </div>
      <div class="kpi">
        <div class="kpi-label" style="color:#fb7185;">Robos Bloqueados</div>
        <div class="kpi-val" style="color:#fb7185;"><?= number_format($stats['bots']) ?></div>
      </div>
      <div class="kpi">
        <div class="kpi-label" style="color:#fbbf24;">Desktop (Safe Page)</div>
        <div class="kpi-val" style="color:#fbbf24;"><?= number_format($stats['desktops']) ?></div>
      </div>
    </div>

    <div class="toolbar">
      <div class="tabs">
        <a href="?filter=all" class="tab <?= $filter === 'all' ? 'active' : '' ?>">Todos</a>
        <a href="?filter=leads" class="tab <?= $filter === 'leads' ? 'active' : '' ?>">Oferta (Leads)</a>
        <a href="?filter=bots" class="tab <?= $filter === 'bots' ? 'active' : '' ?>">Robos</a>
        <a href="?filter=desktop" class="tab <?= $filter === 'desktop' ? 'active' : '' ?>">Desktop</a>
      </div>
      <form method="GET" class="search-form">
        <input type="hidden" name="filter" value="<?= htmlspecialchars($filter, ENT_QUOTES, 'UTF-8') ?>">
        <input type="text" name="search" value="<?= htmlspecialchars($search, ENT_QUOTES, 'UTF-8') ?>" placeholder="Buscar por IP, UTM...">
        <button type="submit" class="btn">Filtrar</button>
      </form>
    </div>

    <div class="table-wrap">
      <table>
        <thead>
          <tr>
            <th>Hora</th>
            <th>IP</th>
            <th>Dispositivo</th>
            <th>Destino</th>
            <th>Motivo / Assinatura</th>
            <th>Campanha / UTM</th>
          </tr>
        </thead>
        <tbody>
          <?php if (empty($logs)): ?>
            <tr><td colspan="6" style="text-align:center;color:#6b7280;padding:24px;">Nenhum registro encontrado para este filtro.</td></tr>
          <?php else: ?>
            <?php foreach ($logs as $row): ?>
              <tr>
                <td style="font-family:monospace;color:#9ca3af;"><?= htmlspecialchars(date('d/m H:i:s', strtotime($row['created_at'])), ENT_QUOTES, 'UTF-8') ?></td>
                <td style="font-family:monospace;font-weight:700;"><?= htmlspecialchars($row['ip'], ENT_QUOTES, 'UTF-8') ?></td>
                <td><?= htmlspecialchars(($row['os'] ?: 'OS') . ' / ' . ($row['browser'] ?: 'Nav'), ENT_QUOTES, 'UTF-8') ?></td>
                <td>
                  <?php if ($row['decision'] === 'offer'): ?>
                    <span class="pill-offer">OFERTA</span>
                  <?php else: ?>
                    <span class="pill-safe">SAFE PAGE</span>
                  <?php endif; ?>
                </td>
                <td style="max-width:320px;overflow:hidden;text-overflow:ellipsis;">
                  <?= htmlspecialchars($row['filter_reason'] ?: '-', ENT_QUOTES, 'UTF-8') ?>
                  <?php if (!empty($row['bot_signature'])): ?>
                    <span style="color:#fb7185;font-family:monospace;">[<?= htmlspecialchars($row['bot_signature'], ENT_QUOTES, 'UTF-8') ?>]</span>
                  <?php endif; ?>
                </td>
                <td style="font-family:monospace;color:#9ca3af;">
                  <?= htmlspecialchars(($row['utm_source'] ?: ($row['fbclid'] ? 'fb' : '-')) . (!empty($row['utm_campaign']) ? ' / ' . $row['utm_campaign'] : ''), ENT_QUOTES, 'UTF-8') ?>
                </td>
              </tr>
            <?php endforeach; ?>
          <?php endif; ?>
        </tbody>
      </table>
    </div>
  </main>
</body>
</html>

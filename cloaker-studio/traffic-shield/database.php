<?php
/**
 * ============================================================================
 * TRAFFIC SHIELD - DATABASE MANAGER (SQLite / PDO - v5.2 Hardened)
 * ============================================================================
 */

if (file_exists(__DIR__ . '/config.php')) {
    require_once __DIR__ . '/config.php';
}

function shield_resolve_data_dir() {
    if (defined('SHIELD_DATA_DIR') && SHIELD_DATA_DIR !== '') {
        $custom = rtrim((string)SHIELD_DATA_DIR, '/\\');
        if (is_dir($custom) || @mkdir($custom, 0750, true)) {
            if (@is_writable($custom)) {
                return $custom;
            }
        }
    }

    // Preferencialmente fora da webroot (public_html)
    $parent = dirname(__DIR__);
    if (@is_dir($parent) && @is_writable($parent)) {
        $outside = $parent . '/.shield_data_' . substr(hash('sha256', __DIR__), 0, 12);
        if (is_dir($outside) || @mkdir($outside, 0750, true)) {
            if (@is_writable($outside)) {
                return $outside;
            }
        }
    }

    // Fallback dentro de /private com protecao Apache 2.4 + 2.2
    $fallback = __DIR__ . '/private';
    if (!is_dir($fallback)) {
        @mkdir($fallback, 0750, true);
    }
    $ht = $fallback . '/.htaccess';
    if (!file_exists($ht)) {
        @file_put_contents(
            $ht,
            "<IfModule mod_authz_core.c>\n    Require all denied\n</IfModule>\n<IfModule !mod_authz_core.c>\n    Order allow,deny\n    Deny from all\n</IfModule>\n"
        );
    }
    return $fallback;
}

function get_shield_db() {
    static $db = null;
    if ($db !== null) {
        return $db;
    }

    $db_dir = shield_resolve_data_dir();
    $db_path = $db_dir . '/traffic.sqlite';

    try {
        $db = new PDO('sqlite:' . $db_path);
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $db->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);

        // WAL mode para alto desempenho de leitura/escrita concorrente
        $db->exec('PRAGMA journal_mode = WAL;');
        $db->exec('PRAGMA synchronous = NORMAL;');

        $db->exec("
            CREATE TABLE IF NOT EXISTS visitor_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                ip VARCHAR(45) NOT NULL,
                device_type VARCHAR(20) NOT NULL,
                browser VARCHAR(50),
                os VARCHAR(50),
                is_bot INTEGER DEFAULT 0,
                bot_signature VARCHAR(100),
                classification VARCHAR(40) NOT NULL,
                decision VARCHAR(20) NOT NULL,
                filter_reason TEXT,
                utm_source VARCHAR(100),
                utm_campaign VARCHAR(100),
                utm_medium VARCHAR(100),
                fbclid VARCHAR(150),
                referer TEXT,
                user_agent TEXT
            );

            CREATE TABLE IF NOT EXISTS rdns_cache (
                ip VARCHAR(45) PRIMARY KEY,
                is_bad INTEGER NOT NULL,
                checked_at INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS login_attempts (
                ip VARCHAR(45) PRIMARY KEY,
                attempts INTEGER NOT NULL DEFAULT 0,
                locked_until INTEGER NOT NULL DEFAULT 0,
                last_attempt INTEGER NOT NULL DEFAULT 0
            );

            CREATE INDEX IF NOT EXISTS idx_logs_created ON visitor_logs(created_at DESC);
            CREATE INDEX IF NOT EXISTS idx_logs_ip ON visitor_logs(ip);
            CREATE INDEX IF NOT EXISTS idx_logs_decision ON visitor_logs(decision);
        ");

        // Retencao automatica leve (30 dias de logs, 24h de cache rDNS)
        if (mt_rand(1, 100) === 1) {
            $db->exec("DELETE FROM visitor_logs WHERE created_at < datetime('now', '-30 days');");
            $cutoff = time() - 86400;
            $stmt = $db->prepare("DELETE FROM rdns_cache WHERE checked_at < :cutoff");
            $stmt->execute([':cutoff' => $cutoff]);
        }
    } catch (Exception $e) {
        error_log("Traffic Shield DB Error: " . $e->getMessage());
        return null;
    }

    return $db;
}

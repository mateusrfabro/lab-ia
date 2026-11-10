<?php
/**
 * ============================================================================
 * TRAFFIC SHIELD - DATABASE MANAGER (SQLite / PDO)
 * ============================================================================
 */

function get_shield_db() {
    static $db = null;
    if ($db !== null) {
        return $db;
    }

    $db_dir = __DIR__ . '/private';
    if (!is_dir($db_dir)) {
        @mkdir($db_dir, 0755, true);
    }

    $db_path = $db_dir . '/traffic.sqlite';
    $is_new = !file_exists($db_path);

    try {
        $db = new PDO('sqlite:' . $db_path);
        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        $db->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);

        // WAL mode para alto desempenho de leitura/escrita concorrente
        $db->exec('PRAGMA journal_mode = WAL;');
        $db->exec('PRAGMA synchronous = NORMAL;');

        if ($is_new) {
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

                CREATE INDEX IF NOT EXISTS idx_logs_created ON visitor_logs(created_at DESC);
                CREATE INDEX IF NOT EXISTS idx_logs_ip ON visitor_logs(ip);
                CREATE INDEX IF NOT EXISTS idx_logs_decision ON visitor_logs(decision);
            ");
        }
    } catch (Exception $e) {
        error_log("Traffic Shield DB Error: " . $e->getMessage());
        return null;
    }

    return $db;
}

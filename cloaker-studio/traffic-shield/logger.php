<?php
/**
 * ============================================================================
 * TRAFFIC SHIELD - ASYNC REQUEST LOGGER (Truncated & Hardened)
 * ============================================================================
 */

require_once __DIR__ . '/database.php';

function shield_trunc($val, $max) {
    if ($val === null || $val === '') {
        return null;
    }
    $str = (string)$val;
    return strlen($str) > $max ? substr($str, 0, $max) : $str;
}

function shield_log_request($eval) {
    try {
        $db = get_shield_db();
        if (!$db) {
            return;
        }

        $stmt = $db->prepare("
            INSERT INTO visitor_logs (
                ip, device_type, browser, os, is_bot, bot_signature,
                classification, decision, filter_reason, utm_source,
                utm_campaign, utm_medium, fbclid, referer, user_agent
            ) VALUES (
                :ip, :device_type, :browser, :os, :is_bot, :bot_signature,
                :classification, :decision, :filter_reason, :utm_source,
                :utm_campaign, :utm_medium, :fbclid, :referer, :user_agent
            )
        ");

        $stmt->execute([
            ':ip' => shield_trunc($eval['ip'] ?? '0.0.0.0', 45) ?? '0.0.0.0',
            ':device_type' => shield_trunc($eval['device'] ?? 'unknown', 20) ?? 'unknown',
            ':browser' => shield_trunc($eval['browser'] ?? null, 50),
            ':os' => shield_trunc($eval['os'] ?? null, 50),
            ':is_bot' => (int)($eval['is_bot'] ?? 0),
            ':bot_signature' => shield_trunc($eval['bot_signature'] ?? null, 100),
            ':classification' => shield_trunc($eval['classification'] ?? 'unknown', 40) ?? 'unknown',
            ':decision' => shield_trunc($eval['decision'] ?? 'safe', 20) ?? 'safe',
            ':filter_reason' => shield_trunc($eval['reason'] ?? null, 255),
            ':utm_source' => shield_trunc($_GET['utm_source'] ?? null, 100),
            ':utm_campaign' => shield_trunc($_GET['utm_campaign'] ?? null, 100),
            ':utm_medium' => shield_trunc($_GET['utm_medium'] ?? null, 100),
            ':fbclid' => shield_trunc($_GET['fbclid'] ?? null, 150),
            ':referer' => shield_trunc($_SERVER['HTTP_REFERER'] ?? null, 500),
            ':user_agent' => shield_trunc($_SERVER['HTTP_USER_AGENT'] ?? null, 500)
        ]);
    } catch (Exception $e) {
        error_log("Traffic Shield Log Error: " . $e->getMessage());
    }
}

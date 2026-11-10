<?php
/**
 * ============================================================================
 * TRAFFIC SHIELD - ASYNC REQUEST LOGGER (Zero Latency)
 * ============================================================================
 */

require_once __DIR__ . '/database.php';

function shield_log_request($eval) {
    try {
        $db = get_shield_db();
        if (!$db) return;

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
            ':ip' => $eval['ip'],
            ':device_type' => $eval['device'],
            ':browser' => $eval['browser'],
            ':os' => $eval['os'],
            ':is_bot' => $eval['is_bot'],
            ':bot_signature' => $eval['bot_signature'],
            ':classification' => $eval['classification'],
            ':decision' => $eval['decision'],
            ':filter_reason' => $eval['reason'],
            ':utm_source' => $_GET['utm_source'] ?? null,
            ':utm_campaign' => $_GET['utm_campaign'] ?? null,
            ':utm_medium' => $_GET['utm_medium'] ?? null,
            ':fbclid' => $_GET['fbclid'] ?? null,
            ':referer' => $_SERVER['HTTP_REFERER'] ?? null,
            ':user_agent' => substr($_SERVER['HTTP_USER_AGENT'] ?? '', 0, 500)
        ]);
    } catch (Exception $e) {
        error_log("Traffic Shield Log Error: " . $e->getMessage());
    }
}

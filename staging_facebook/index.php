<?php
/**
 * ============================================================================
 * TRAFFIC SHIELD GATEWAY v5.2 (Enterprise Hardened Smart Mirror)
 * ============================================================================
 */

// 1. Headers anti-cache e segurança avançada
if (!headers_sent()) {
    header('Cache-Control: no-store, no-cache, must-revalidate, max-age=0');
    header('Pragma: no-cache');
    header('Expires: 0');
    header('X-Robots-Tag: noindex, nofollow, noarchive, nosnippet');
    header('X-Content-Type-Options: nosniff');
    header('X-Frame-Options: SAMEORIGIN');
    header('X-XSS-Protection: 1; mode=block');
}

require_once __DIR__ . '/detector.php';
require_once __DIR__ . '/logger.php';

// 2. Avaliação do Visitante
$eval = TrafficDetector::evaluate_request();

// 3. Gravação no Banco de Logs SQLite
shield_log_request($eval);

// 4. Entrega da Rota Selecionada (Modo Mirror sem Redirecionamento)
if ($eval['decision'] === 'offer') {
    serve_offer();
} else {
    serve_safe();
}

function serve_safe() {
    if (file_exists(__DIR__ . '/white.html')) {
        include __DIR__ . '/white.html';
    } elseif (file_exists(__DIR__ . '/safepage.html')) {
        include __DIR__ . '/safepage.html';
    } else {
        echo '<!DOCTYPE html><html><head><title>Research Portal</title></head><body><h1>Official Research Portal</h1></body></html>';
    }
    exit;
}

function serve_offer() {
    if (file_exists(__DIR__ . '/offer.html')) {
        include __DIR__ . '/offer.html';
    } elseif (file_exists(__DIR__ . '/index.html')) {
        include __DIR__ . '/index.html';
    } else {
        serve_safe();
    }
    exit;
}

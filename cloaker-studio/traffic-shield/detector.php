<?php
/**
 * ============================================================================
 * TRAFFIC SHIELD - INTELLIGENT TRAFFIC DETECTOR & CLASSIFIER (v5.2 HARDENED)
 * ============================================================================
 */

if (file_exists(__DIR__ . '/config.php')) {
    require_once __DIR__ . '/config.php';
}
require_once __DIR__ . '/database.php';

class TrafficDetector {

    // Lista abrangente de assinaturas de Crawlers e Scrapers (CrawlerDetect Standard)
    private static $bot_signatures = [
        'facebookexternalhit', 'facebot', 'meta-externalagent', 'meta-externalfetcher',
        'googlebot', 'bingbot', 'yandexbot', 'baiduspider', 'duckduckbot',
        'bytespider', 'slurp', 'crawler', 'spider', 'curl', 'wget', 'python',
        'headless', 'phantom', 'puppeteer', 'selenium', 'lighthouse', 'pagespeed',
        'screaming frog', 'ahrefs', 'semrush', 'adbeat', 'whatrun', 'builtwith',
        'mediapartners-google', 'adsbot-google', 'bot', 'crawl', 'postman',
        'insomnia', 'node-fetch', 'axios', 'go-http-client', 'httpclient', 'restsharp'
    ];

    // Subnets IPv4 de Big Techs & Datacenters (Meta, AWS, Google, DO)
    private static $datacenter_ipv4 = [
        // Meta / Facebook
        "31.13.24.0/21", "31.13.64.0/18", "66.220.144.0/20", "69.63.176.0/20",
        "69.171.224.0/19", "74.119.76.0/22", "103.4.96.0/22", "129.134.0.0/16",
        "157.240.0.0/16", "173.252.64.0/18", "179.60.192.0/22", "185.60.216.0/22",
        "204.15.20.0/22", "57.141.0.0/16",
        // AWS
        "3.0.0.0/9", "13.32.0.0/12", "18.192.0.0/12", "52.0.0.0/11", "54.0.0.0/10",
        // Google Cloud & Datacenters
        "34.64.0.0/10", "35.184.0.0/13", "104.196.0.0/14",
        // DigitalOcean
        "138.68.0.0/16", "159.203.0.0/16", "167.99.0.0/16"
    ];

    // Subnets IPv6 oficiais da Meta / Facebook & Big Techs
    private static $datacenter_ipv6 = [
        "2a03:2880::/32", // Facebook Core
        "2620:0:1c00::/40", // Facebook ASN
        "2a03:2884::/32", // Meta Edge
        "2a03:2887::/32", // Meta CDN
        "2600:1f00::/24", // AWS IPv6
        "2001:4860::/32"  // Google IPv6
    ];

    // IPs oficiais da Cloudflare (IPv4 + IPv6) para validacao de proxy reverso seguro
    private static $cloudflare_ipv4 = [
        "173.245.48.0/20", "103.21.244.0/22", "103.22.200.0/22", "103.31.4.0/22",
        "141.101.64.0/18", "108.162.192.0/18", "190.93.240.0/20", "188.114.96.0/20",
        "197.234.240.0/22", "198.41.128.0/17", "162.158.0.0/15", "104.16.0.0/13",
        "104.24.0.0/14", "172.64.0.0/13", "131.0.72.0/22"
    ];

    private static $cloudflare_ipv6 = [
        "2400:cb00::/32", "2606:4700::/32", "2803:f800::/32", "2405:b500::/32",
        "2405:8100::/32", "2a06:98c0::/29", "2c0f:f248::/32"
    ];

    public static function get_real_ip() {
        $remote_ip = $_SERVER['REMOTE_ADDR'] ?? '127.0.0.1';

        $is_cf = false;
        if (filter_var($remote_ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4)) {
            foreach (self::$cloudflare_ipv4 as $cf_cidr) {
                if (self::ipv4_in_range($remote_ip, $cf_cidr)) {
                    $is_cf = true;
                    break;
                }
            }
        } elseif (filter_var($remote_ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV6)) {
            foreach (self::$cloudflare_ipv6 as $cf_cidr) {
                if (self::ipv6_in_range($remote_ip, $cf_cidr)) {
                    $is_cf = true;
                    break;
                }
            }
        }

        if ($is_cf && !empty($_SERVER['HTTP_CF_CONNECTING_IP'])) {
            $ip = trim($_SERVER['HTTP_CF_CONNECTING_IP']);
            if (filter_var($ip, FILTER_VALIDATE_IP)) {
                return $ip;
            }
        }

        return $remote_ip;
    }

    public static function ipv4_in_range($ip, $range) {
        if (!filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4)) return false;
        if (strpos($range, '/') === false) {
            $range .= '/32';
        }
        list($subnet, $bits) = explode('/', $range);
        $ip_long = ip2long($ip);
        $subnet_long = ip2long($subnet);
        $mask = -1 << (32 - (int)$bits);
        $subnet_long &= $mask;
        return ($ip_long & $mask) == $subnet_long;
    }

    public static function ipv6_in_range($ip, $range) {
        if (!filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV6)) return false;
        list($subnet, $bits) = explode('/', $range);
        $bits = (int)$bits;

        $ip_bin = inet_pton($ip);
        $subnet_bin = inet_pton($subnet);
        if (!$ip_bin || !$subnet_bin) return false;

        $bytes = (int)($bits / 8);
        $rem_bits = $bits % 8;

        for ($i = 0; $i < $bytes; $i++) {
            if ($ip_bin[$i] !== $subnet_bin[$i]) return false;
        }

        if ($rem_bits > 0) {
            $mask = ~(0xFF >> $rem_bits) & 0xFF;
            if ((ord($ip_bin[$bytes]) & $mask) !== (ord($subnet_bin[$bytes]) & $mask)) {
                return false;
            }
        }

        return true;
    }

    public static function detect_device($user_agent) {
        $ua = strtolower($user_agent);
        $device = 'desktop';
        if (strpos($ua, 'ipad') !== false || strpos($ua, 'tablet') !== false) {
            $device = 'tablet';
        } elseif (strpos($ua, 'mobile') !== false || strpos($ua, 'android') !== false || strpos($ua, 'iphone') !== false) {
            $device = 'mobile';
        }
        return $device;
    }

    public static function detect_os($user_agent) {
        $ua = strtolower($user_agent);
        if (strpos($ua, 'iphone') !== false || strpos($ua, 'ipad') !== false) return 'iOS';
        if (strpos($ua, 'android') !== false) return 'Android';
        if (strpos($ua, 'windows') !== false) return 'Windows';
        if (strpos($ua, 'macintosh') !== false || strpos($ua, 'mac os') !== false) return 'macOS';
        if (strpos($ua, 'linux') !== false) return 'Linux';
        return 'Other';
    }

    public static function detect_browser($user_agent) {
        $ua = strtolower($user_agent);
        if (strpos($ua, 'edg') !== false) return 'Edge';
        if (strpos($ua, 'opr') !== false || strpos($ua, 'opera') !== false) return 'Opera';
        if (strpos($ua, 'chrome') !== false && strpos($ua, 'safari') !== false) return 'Chrome';
        if (strpos($ua, 'safari') !== false) return 'Safari';
        if (strpos($ua, 'firefox') !== false) return 'Firefox';
        return 'Unknown';
    }

    public static function is_bot($user_agent) {
        $ua = strtolower($user_agent);
        if (empty($ua) || strlen($ua) < 15) {
            return ['is_bot' => true, 'bot_name' => 'Empty/Short UA'];
        }
        foreach (self::$bot_signatures as $sig) {
            if (strpos($ua, $sig) !== false) {
                return ['is_bot' => true, 'bot_name' => $sig];
            }
        }
        return ['is_bot' => false, 'bot_name' => null];
    }

    public static function is_datacenter_ip($ip) {
        if (filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4)) {
            foreach (self::$datacenter_ipv4 as $cidr) {
                if (self::ipv4_in_range($ip, $cidr)) {
                    return true;
                }
            }
        }

        if (filter_var($ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV6)) {
            foreach (self::$datacenter_ipv6 as $cidr) {
                if (self::ipv6_in_range($ip, $cidr)) {
                    return true;
                }
            }
        }

        return false;
    }

    public static function is_datacenter_hostname($ip) {
        if (!filter_var($ip, FILTER_VALIDATE_IP)) return false;

        // Consulta cache rDNS em SQLite (TTL 24h) para evitar latencia repetida no lead mobile
        $db = get_shield_db();
        if ($db) {
            try {
                $stmt = $db->prepare("SELECT is_bad, checked_at FROM rdns_cache WHERE ip = :ip");
                $stmt->execute([':ip' => $ip]);
                $cached = $stmt->fetch();
                if ($cached && (time() - (int)$cached['checked_at']) < 86400) {
                    return ((int)$cached['is_bad']) === 1;
                }
            } catch (Exception $e) {
                // fallback silencioso para lookup direto
            }
        }

        $is_bad = false;
        $hostname = @gethostbyaddr($ip);
        if ($hostname && $hostname !== $ip) {
            $host = strtolower($hostname);
            $bad = [
                'facebook', 'facebot', 'fbcdn', 'meta', 'google', 'googlebot',
                'amazon', 'amazonaws', 'azure', 'digitalocean', 'hetzner', 'ovh',
                'linode', 'headless', 'crawl', 'spider', 'proxy', 'tor'
            ];
            foreach ($bad as $b) {
                if (strpos($host, $b) !== false) {
                    $is_bad = true;
                    break;
                }
            }
        }

        if ($db) {
            try {
                $stmt = $db->prepare("
                    INSERT INTO rdns_cache (ip, is_bad, checked_at)
                    VALUES (:ip, :is_bad, :checked_at)
                    ON CONFLICT(ip) DO UPDATE SET is_bad = excluded.is_bad, checked_at = excluded.checked_at
                ");
                $stmt->execute([
                    ':ip' => $ip,
                    ':is_bad' => $is_bad ? 1 : 0,
                    ':checked_at' => time()
                ]);
            } catch (Exception $e) {
                // ignora erro de gravacao de cache
            }
        }

        return $is_bad;
    }

    public static function has_ad_traffic_param() {
        return !empty($_GET['fbclid']) ||
               !empty($_GET['gclid']) ||
               !empty($_GET['ttclid']) ||
               !empty($_GET['utm_source']) ||
               !empty($_GET['utm_campaign']) ||
               !empty($_GET['utm_medium']) ||
               !empty($_GET['utm_content']);
    }

    public static function evaluate_request() {
        $ip = self::get_real_ip();
        $ua = $_SERVER['HTTP_USER_AGENT'] ?? '';
        $device = self::detect_device($ua);
        $os = self::detect_os($ua);
        $browser = self::detect_browser($ua);

        // 1. Chave de Bypass de Preview da Equipe (fail-closed se config ausente)
        $configured_key = defined('SHIELD_PREVIEW_KEY') ? (string)SHIELD_PREVIEW_KEY : '';
        $provided_key = isset($_GET['key']) ? (string)$_GET['key'] : '';
        if (
            $configured_key !== '' &&
            isset($_GET['preview']) &&
            $_GET['preview'] === 'offer' &&
            $provided_key !== '' &&
            hash_equals($configured_key, $provided_key)
        ) {
            return [
                'decision' => 'offer',
                'classification' => 'team_preview',
                'reason' => 'Chave Privada de Preview',
                'ip' => $ip, 'device' => $device, 'os' => $os, 'browser' => $browser,
                'is_bot' => 0, 'bot_signature' => null
            ];
        }

        if (isset($_GET['preview']) && $_GET['preview'] === 'safe') {
            return [
                'decision' => 'safe',
                'classification' => 'team_preview',
                'reason' => 'Forcado Safe Page via preview=safe',
                'ip' => $ip, 'device' => $device, 'os' => $os, 'browser' => $browser,
                'is_bot' => 0, 'bot_signature' => null
            ];
        }

        // 2. Deteccao de Bot por Assinatura de Crawler
        $bot_check = self::is_bot($ua);
        if ($bot_check['is_bot']) {
            return [
                'decision' => 'safe',
                'classification' => 'bot',
                'reason' => 'Bot/Crawler detectado: ' . $bot_check['bot_name'],
                'ip' => $ip, 'device' => $device, 'os' => $os, 'browser' => $browser,
                'is_bot' => 1, 'bot_signature' => $bot_check['bot_name']
            ];
        }

        // 3. Checagem de IP de Datacenter (IPv4 + IPv6 Meta)
        if (self::is_datacenter_ip($ip)) {
            return [
                'decision' => 'safe',
                'classification' => 'datacenter_ip',
                'reason' => 'IP de Datacenter ou Rede Meta Ads (IPv4/IPv6)',
                'ip' => $ip, 'device' => $device, 'os' => $os, 'browser' => $browser,
                'is_bot' => 1, 'bot_signature' => 'Datacenter CIDR'
            ];
        }

        // 4. Regra de Ouro: Desktop Lock (Revisor de mesa do Meta) - antes de rDNS para economizar DNS
        if ($device !== 'mobile' && $device !== 'tablet') {
            return [
                'decision' => 'safe',
                'classification' => 'desktop_filter',
                'reason' => 'Dispositivo Desktop travado para Safe Page',
                'ip' => $ip, 'device' => $device, 'os' => $os, 'browser' => $browser,
                'is_bot' => 0, 'bot_signature' => null
            ];
        }

        // 5. Blindagem de Acesso Direto: Exigencia de Parametro de Campanha
        if (!self::has_ad_traffic_param()) {
            return [
                'decision' => 'safe',
                'classification' => 'direct_clean_visit',
                'reason' => 'Acesso direto sem parametro de anuncio (Safe Page)',
                'ip' => $ip, 'device' => $device, 'os' => $os, 'browser' => $browser,
                'is_bot' => 0, 'bot_signature' => null
            ];
        }

        // 6. Checagem de Hostname Reverso com cache SQLite (barra emuladores mobile em nuvem)
        if (self::is_datacenter_hostname($ip)) {
            return [
                'decision' => 'safe',
                'classification' => 'datacenter_host',
                'reason' => 'Hostname Reverso de Nuvem/Crawler',
                'ip' => $ip, 'device' => $device, 'os' => $os, 'browser' => $browser,
                'is_bot' => 1, 'bot_signature' => 'Reverse DNS Host'
            ];
        }

        // 7. Lead Real Mobile Qualificado de Campanha
        return [
            'decision' => 'offer',
            'classification' => 'real_lead',
            'reason' => 'Lead Mobile Qualificado de Anuncio (' . $os . ' / ' . $browser . ')',
            'ip' => $ip, 'device' => $device, 'os' => $os, 'browser' => $browser,
            'is_bot' => 0, 'bot_signature' => null
        ];
    }
}

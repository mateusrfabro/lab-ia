# -*- coding: utf-8 -*-
import os

SITE_DIR = r"C:\Users\mateu\Downloads\Projeto Dudu\Buzz 2.0\site"
TARGET_DIR = os.path.join(SITE_DIR, "simulador-imobiliario")
os.makedirs(TARGET_DIR, exist_ok=True)

PUB_ID = "pub-3266587888704229"
PIXEL_ID = "1510786527551026"

HEAD_COMMON = f"""  <meta charset="UTF-8">
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
  <link rel="stylesheet" href="../css/style.css?v=20261108c">
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%23008254'><path d='M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z'/></svg>">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-{PUB_ID}" crossorigin="anonymous"></script>
  <!-- Meta Pixel Code -->
  <script>
  !function(f,b,e,v,n,t,s)
  {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
  if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
  n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];
  s.parentNode.insertBefore(t,s)}}(window, document,'script',
  'https://connect.facebook.net/en_US/fbevents.js');
  fbq('init', '{PIXEL_ID}');
  fbq('track', 'PageView');
  </script>
  <noscript><img height="1" width="1" style="display:none"
  src="https://www.facebook.com/tr?id={PIXEL_ID}&ev=PageView&noscript=1"
  /></noscript>
  <!-- End Meta Pixel Code -->
"""

HEADER_HTML = """  <!-- Header Ultra-Clean Mobile-First -->
  <header style="background:#FFFFFF; border-bottom:1px solid #E2E8F0; padding:10px 0; position:relative; z-index:10;">
    <div class="container" style="display:flex; justify-content:space-between; align-items:center; max-width:640px; padding:0 14px;">
      <a href="/index.html" style="text-decoration:none; display:flex; align-items:center; gap:8px;">
        <span style="background:#008254; color:#FFFFFF; border-radius:8px; width:34px; height:34px; display:inline-flex; align-items:center; justify-content:center; font-weight:800; font-size:15px; flex-shrink:0;">CC</span>
        <div style="display:flex; flex-direction:column; line-height:1.2;">
          <span style="font-weight:800; color:#111827; font-size:15px; letter-spacing:-0.01em;">Comparador <span style="color:#008254;">Cartões</span></span>
          <span style="font-size:10.5px; color:#6B7280;">Crédito & Habitação</span>
        </div>
      </a>
      <div style="font-size:11px; font-weight:700; color:#008254; background:#E6F5EF; padding:4px 10px; border-radius:99px; white-space:nowrap; display:flex; align-items:center; gap:4px;">
        <span>🏛️</span>
        <span>Normas BACEN</span>
      </div>
    </div>
  </header>
"""

FOOTER_HTML = """  <footer style="background:#0B251C; color:#94A3B8; padding:28px 0 20px; margin-top:32px; font-size:12px; border-top:1px solid rgba(255,255,255,0.08);">
    <div class="container" style="text-align:center; max-width:640px; padding:0 14px;">
      <p style="margin-bottom:8px; color:#E2E8F0; font-weight:600; font-size:12.5px;">Comparador Independente de Finanças, Cartões e Crédito Imobiliário</p>
      <p style="margin-bottom:10px; line-height:1.5; font-size:11px; color:#94A3B8;">O portal atua como ferramenta informativa e de simulação comparativa. As condições de financiamento bancário e de cotas de consórcio são regulamentadas pelo Banco Central do Brasil (Lei nº 11.795/2008 e Resolução BCB 285). Não realizamos cobrança de valores antecipados para aprovação de crédito.</p>
      <p style="font-size:11px; color:#64748B;">&copy; 2026 ComparadorCartoes.com &bull; Todos os direitos reservados.</p>
    </div>
  </footer>
"""

# ==============================================================================
# 1. INDEX.HTML (HUB AGRESSIVO COM DESTAQUE TOTAL AOS 2 BOTÕES)
# ==============================================================================
index_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
{HEAD_COMMON}
  <title>Simulador de Habitação 2026: Fuja dos Juros Abusivos e Aprove Seu Crédito — Comparador Cartões</title>
  <meta name="description" content="Simule a aprovação do seu financiamento sem pagar o triplo do imóvel em juros para o banco, ou venda sua casa em até 60 dias com renda garantida.">
  <link rel="canonical" href="https://comparadorcartoes.com/simulador-imobiliario/">
  <style>
    @keyframes pulseCta {{
      0%, 100% {{ transform: scale(1); box-shadow: 0 4px 16px rgba(0,130,84,0.35); }}
      50% {{ transform: scale(1.02); box-shadow: 0 8px 24px rgba(0,130,84,0.55); }}
    }}
    .btn-agressivo-comprar {{
      animation: pulseCta 2.5s infinite;
    }}
  </style>
</head>
<body class="sim-page" style="margin:0; padding:0; background:#F8FAFC; overflow-x:hidden;">

{HEADER_HTML}

  <!-- HERO ULTRA-AGRESSIVO (PRIMEIRA DOBRA DE ALTO IMPACTO) -->
  <section class="pillar-hero" style="padding: 18px 0 14px; background: #F8FAFC;">
    <div class="container" style="max-width: 600px; text-align: center; padding: 0 14px;">
      
      <!-- BADGE DE ALERTA VISCERAL -->
      <div style="display:inline-flex; align-items:center; gap:6px; background:#FEF2F2; color:#DC2626; border:1px solid #FECACA; font-size:11.5px; font-weight:800; padding:5px 12px; border-radius:99px; margin-bottom:12px; text-transform:uppercase; letter-spacing:0.02em;">
        <span>🚨 PARE DE PAGAR O TRIPLO DO IMÓVEL EM JUROS</span>
      </div>

      <h1 class="pillar-title" style="font-size: clamp(21px, 4.2vw, 30px); line-height: 1.22; margin-bottom: 10px; color:#0F172A; font-weight:800;">
        Simule a Liberação da Sua Casa Própria Sem Depender das Filas da Caixa
      </h1>

      <p class="pillar-subtitle" style="font-size: 14px; color:#475569; margin-bottom: 20px; line-height: 1.5;">
        Cansado de ter financiamento reprovado ou ver o banco cobrar <strong>juros de 12% ao ano</strong>? Compare alternativas homologadas pelo Banco Central com entrada facilitada ou liquide seu imóvel parado sem despesas.
      </p>

      <!-- CAIXA COM OS 2 GRANDES BOTÕES DE AÇÃO IMEDIATA (DISPARO DO VIGNETTE) -->
      <div style="background:#FFFFFF; border:2.5px solid #008254; border-radius:16px; padding:20px 14px; box-shadow:0 12px 32px -4px rgba(0,130,84,0.18); margin-bottom:14px;">
        <p style="font-size:14.5px; font-weight:800; color:#0F172A; margin-bottom:14px; text-transform:uppercase; letter-spacing:0.03em;">
          Qual é o seu objetivo imediato hoje?
        </p>

        <!-- BOTÃO 1: COMPRADOR (SUPER AGRESSIVO E DESTACADO) -->
        <a href="/simulador-imobiliario/comprar.html" class="nw-cta-btn btn-agressivo-comprar js-keep-utms" style="display:flex; flex-direction:column; align-items:center; justify-content:center; width:100%; min-height:68px; padding:14px 16px; margin-bottom:12px; background:linear-gradient(180deg, #008254 0%, #006B44 100%); color:#FFFFFF; border-radius:10px; text-decoration:none; transition:all 0.2s;">
          <span style="display:flex; align-items:center; gap:8px; font-size:16px; font-weight:800; letter-spacing:0.01em;">
            <span>🟢</span>
            <span>QUERO APROVAR MEU FINANCIAMENTO</span>
            <span style="font-size:18px;">&rarr;</span>
          </span>
          <span style="font-size:11.5px; color:#D1FAE5; font-weight:600; margin-top:3px;">
            Entrada de 15% + Parcela planejada de 0,8%/mês (sem juros de banco)
          </span>
        </a>

        <!-- BOTÃO 2: PROPRIETÁRIO (URGÊNCIA DE 60 DIAS) -->
        <a href="/simulador-imobiliario/proprietario.html" class="js-keep-utms" style="display:flex; flex-direction:column; align-items:center; justify-content:center; width:100%; min-height:64px; padding:12px 16px; background:#0F172A; color:#FFFFFF; border-radius:10px; text-decoration:none; border:1px solid #334155; transition:all 0.2s;">
          <span style="display:flex; align-items:center; gap:8px; font-size:15px; font-weight:800; color:#FBBF24;">
            <span>⚡</span>
            <span>QUERO VENDER MINHA CASA EM ATÉ 60 DIAS</span>
            <span style="font-size:18px;">&rarr;</span>
          </span>
          <span style="font-size:11.5px; color:#94A3B8; font-weight:600; margin-top:2px;">
            15% à vista na assinatura + Renda mensal garantida sem vacância
          </span>
        </a>

        <!-- COMPLIANCE DISCLAIMER -->
        <span style="display:block; font-size:11px; color:#64748B; margin-top:12px; line-height:1.4;">
          🛡️ Consulta 100% gratuita, sem consulta restritiva prévia e em conformidade com o Banco Central.
        </span>
      </div>

    </div>
  </section>

  <!-- BLOCO DE ANÚNCIO SEGURO (ANTI-CLS, MIN-HEIGHT 250PX, MARGEM 20PX) -->
  <div class="container" style="max-width: 600px; padding: 0 14px;">
    <div class="ad-safe-slot" style="margin: 14px auto 20px; min-height:250px; background:#F1F5F9; border:1px dashed #CBD5E1; border-radius:12px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; padding:10px;">
      <span class="ad-safe-label" style="font-size:10px; font-weight:700; color:#94A3B8; text-transform:uppercase; margin-bottom:6px;">Publicidade &bull; Espaço Patrocinado</span>
      <ins class="adsbygoogle"
           style="display:block; width:100%; max-width:336px; height:250px;"
           data-ad-client="ca-{PUB_ID}"
           data-ad-slot="auto"
           data-ad-format="auto"
           data-full-width-responsive="true"></ins>
      <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
    </div>
  </div>

  <!-- CONTEÚDO AGRESSIVO: RAIO-X DA SANGRIA BANCÁRIA -->
  <main class="container" style="max-width: 640px; padding: 0 14px 24px;">
    
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:20px 16px; margin-bottom:20px; box-shadow:0 4px 14px rgba(0,0,0,0.04);">
      
      <div style="display:inline-flex; align-items:center; gap:6px; background:#FEF3C7; color:#B45309; font-size:11.5px; font-weight:800; padding:4px 10px; border-radius:99px; margin-bottom:10px;">
        <span>📉 O Raio-X do Financiamento Tradicional</span>
      </div>

      <h2 style="font-size:18px; font-weight:800; color:#0F172A; margin-bottom:12px; line-height:1.3;">
        Por Que a Caixa e os Grandes Bancos Fazem Você Pagar 3 Casas Para Ter 1?
      </h2>

      <p style="font-size:13.5px; color:#334155; line-height:1.6; margin-bottom:16px;">
        No financiamento SAC convencional, um imóvel de <strong>R$ 400.000</strong> custa mais de <strong>R$ 980.000</strong> ao término de 360 meses. Mais de <strong>R$ 580.000</strong> são juros puros, seguros obrigatórios (MIP/DFI) e taxas bancárias que não aumentam em 1 centavo o valor do seu patrimônio.
      </p>

      <!-- CARD COMPARATIVO DE IMPACTO -->
      <div style="display:grid; grid-template-columns:1fr; gap:10px; margin-bottom:18px;">
        
        <div style="background:#FEF2F2; border:1.5px solid #FCA5A5; border-radius:10px; padding:14px;">
          <div style="font-size:13px; font-weight:800; color:#991B1B; margin-bottom:4px;">❌ FINANCIAMENTO TRADICIONAL (BANCOS):</div>
          <ul style="font-size:12.5px; color:#7F1D1D; line-height:1.6; padding-left:16px; margin:0;">
            <li>Exige 20% a 30% de entrada à vista (R$ 80k a R$ 120k no bolso);</li>
            <li>Juros abusivos de 11% a 13% ao ano com amortização lenta;</li>
            <li>Reprova autônomos e 67% das famílias que não têm holerite formal.</li>
          </ul>
        </div>

        <div style="background:#F0FDF4; border:1.5px solid #86EFAC; border-radius:10px; padding:14px;">
          <div style="font-size:13px; font-weight:800; color:#166534; margin-bottom:4px;">✅ AQUISIÇÃO PLANEJADA / ALUGUEL COM OPÇÃO (BACEN):</div>
          <ul style="font-size:12.5px; color:#14532D; line-height:1.6; padding-left:16px; margin:0;">
            <li>Entrada acessível de <strong>15%</strong> e parcelas de <strong>0,8% ao mês</strong>;</li>
            <li><strong>Zero Juros Compostos:</strong> Taxa administrativa fixa e diluída;</li>
            <li>Possibilidade de <strong>ocupar o imóvel de imediato</strong> enquanto quita o plano.</li>
          </ul>
        </div>

      </div>

      <!-- TABELA COMPARATIVA -->
      <div class="quick-table-wrap" style="overflow-x:auto; margin:14px 0 16px; border-radius:8px; border:1px solid #E2E8F0;">
        <table style="width:100%; min-width:440px; border-collapse:collapse; font-size:12.5px; text-align:left;">
          <thead>
            <tr style="background:#0F172A; color:#FFFFFF;">
              <th style="padding:10px 10px;">Valor do Imóvel</th>
              <th style="padding:10px 10px;">Entrada (15%)</th>
              <th style="padding:10px 10px;">Parcela (0,8%)</th>
              <th style="padding:10px 10px;">Economia em Juros</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom:1px solid #E2E8F0; background:#F8FAFC;">
              <td style="padding:9px 10px; font-weight:700;">R$ 200.000</td>
              <td style="padding:9px 10px;">R$ 30.000</td>
              <td style="padding:9px 10px; color:#008254; font-weight:800;">R$ 1.600/mês</td>
              <td style="padding:9px 10px; color:#059669; font-weight:700;">Economiza ~R$ 140 mil</td>
            </tr>
            <tr style="border-bottom:1px solid #E2E8F0;">
              <td style="padding:9px 10px; font-weight:700;">R$ 400.000</td>
              <td style="padding:9px 10px;">R$ 60.000</td>
              <td style="padding:9px 10px; color:#008254; font-weight:800;">R$ 3.200/mês</td>
              <td style="padding:9px 10px; color:#059669; font-weight:700;">Economiza ~R$ 240 mil</td>
            </tr>
            <tr style="border-bottom:1px solid #E2E8F0; background:#F8FAFC;">
              <td style="padding:9px 10px; font-weight:700;">R$ 600.000</td>
              <td style="padding:9px 10px;">R$ 90.000</td>
              <td style="padding:9px 10px; color:#008254; font-weight:800;">R$ 4.800/mês</td>
              <td style="padding:9px 10px; color:#059669; font-weight:700;">Economiza ~R$ 320 mil</td>
            </tr>
            <tr>
              <td style="padding:9px 10px; font-weight:700;">R$ 1.000.000</td>
              <td style="padding:9px 10px;">R$ 150.000</td>
              <td style="padding:9px 10px; color:#008254; font-weight:800;">R$ 8.000/mês</td>
              <td style="padding:9px 10px; color:#059669; font-weight:700;">Economiza ~R$ 450 mil</td>
            </tr>
          </tbody>
        </table>
      </div>

    </div>

    <!-- BOTÃO FINAL DE CHAMADA -->
    <div style="text-align:center; margin:20px 0;">
      <a href="/simulador-imobiliario/comprar.html" class="nw-cta-btn js-keep-utms" style="display:inline-block; max-width:440px; width:100%; padding:15px 18px; font-size:15.5px; font-weight:800; background:#008254; color:#fff; border-radius:8px; text-decoration:none; box-shadow:0 4px 14px rgba(0,130,84,0.3);">
        QUERO APROVAR MEU FINANCIAMENTO AGORA &rarr;
      </a>
    </div>

  </main>

{FOOTER_HTML}

<script src="../js/afiliados-config.js"></script>
<script src="../js/app.js"></script>
</body>
</html>
"""

# ==============================================================================
# 2. COMPRAR.HTML (FUNIL COMPRADOR COM GATILHOS DE URGÊNCIA & TIMER)
# ==============================================================================
comprar_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
{HEAD_COMMON}
  <title>Aprovação de Financiamento & Aluguel com Opção: Simulação Oficial — Comparador Cartões</title>
  <meta name="description" content="Simulação de financiamento imobiliário sem juros bancários. Saiba sua parcela exata para imóveis de R$ 120 mil a R$ 1 milhão.">
  <link rel="canonical" href="https://comparadorcartoes.com/simulador-imobiliario/comprar.html">
  <style>
    .step-box {{ display: none; }}
    .step-box.active {{ display: block; }}
    .opt-card {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      min-height: 54px;
      padding: 12px 14px;
      margin-bottom: 10px;
      background: #FFFFFF;
      border: 1.5px solid #E2E8F0;
      border-radius: 10px;
      cursor: pointer;
      font-weight: 700;
      color: #1E293B;
      font-size: 13.5px;
      transition: all 0.18s ease;
      -webkit-tap-highlight-color: transparent;
    }}
    .opt-card:hover {{
      border-color: #008254;
      background: #F0FDF4;
    }}
    .opt-card.selected {{
      border-color: #008254;
      background: #F0FDF4;
      box-shadow: 0 0 0 2px rgba(0,130,84,0.2);
    }}
    .opt-radio {{
      width: 22px;
      height: 22px;
      border: 2px solid #CBD5E1;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }}
    .opt-card.selected .opt-radio {{
      border-color: #008254;
      background: #008254;
    }}
    .opt-card.selected .opt-radio::after {{
      content: "✓";
      color: #FFFFFF;
      font-size: 12px;
      font-weight: 800;
    }}
    @keyframes pulseWpp {{
      0%, 100% {{ transform: scale(1); box-shadow: 0 4px 14px rgba(22,163,74,0.35); }}
      50% {{ transform: scale(1.02); box-shadow: 0 8px 24px rgba(22,163,74,0.6); }}
    }}
    .btn-pulse-wpp {{
      animation: pulseWpp 2.2s infinite;
    }}
  </style>
</head>
<body class="sim-page" style="margin:0; padding:0; background:#F8FAFC; overflow-x:hidden;">

{HEADER_HTML}

  <section class="pillar-hero" style="padding: 12px 0 10px;">
    <div class="container" style="max-width: 540px; padding: 0 14px;">
      
      <!-- BARRA DE PROGRESSO DINÂMICA -->
      <div class="sim-progress-wrap" style="background:#fff; border:1px solid #E2E8F0; border-radius:12px; padding:10px 14px; margin-bottom:12px;">
        <div class="sim-progress-header" style="display:flex; justify-content:space-between; font-size:11.5px; font-weight:800; color:#008254; text-transform:uppercase; margin-bottom:6px;">
          <span id="progressText">Etapa 1 de 3 (33%)</span>
          <span id="stepTitle">Valor do Imóvel</span>
        </div>
        <div class="sim-progress-track" style="width:100%; height:8px; background:#E2E8F0; border-radius:99px; overflow:hidden;">
          <div id="progressBar" class="sim-progress-fill" style="width: 33%; height:100%; background:linear-gradient(90deg, #008254 0%, #10B981 100%); transition:width 0.3s ease;"></div>
        </div>
      </div>

      <!-- ALERTA DE COMPATIBILIDADE BACEN -->
      <div style="background:#FEF3C7; border:1px solid #FCD34D; border-radius:10px; padding:10px 12px; margin-bottom:14px; font-size:12px; color:#92400E; line-height:1.45;">
        <strong>⚠️ CRITÉRIO OFICIAL DE COMPATIBILIDADE BACEN:</strong>
        <p style="margin:3px 0 0;">As regras do Sistema Financeiro Nacional garantem entrada justa de 15% e parcelas mensais de 0,8%, protegendo seu score contra juros bancários compostos.</p>
      </div>

      <!-- ================= PASSO 1 ================= -->
      <div id="step1" class="step-box active">
        <div class="sim-question-card" style="background:#fff; border:2px solid #008254; border-radius:14px; padding:18px 14px; margin-bottom:16px; box-shadow:0 6px 18px rgba(0,130,84,0.08);">
          <span style="font-size:11px; font-weight:800; color:#008254; text-transform:uppercase; letter-spacing:0.04em; display:block; margin-bottom:6px;">Pergunta 1 de 3</span>
          <h2 style="font-size:18px; font-weight:800; color:#0F172A; margin-bottom:14px; line-height:1.3;">
            Qual é a faixa de valor do imóvel que você deseja conquistar?
          </h2>

          <div class="opt-card js-step1-opt" data-val="150000">
            <span>R$ 150.000 &bull; Parcela estimada: R$ 1.200/mês</span>
            <div class="opt-radio"></div>
          </div>
          <div class="opt-card js-step1-opt" data-val="250000">
            <span>R$ 250.000 &bull; Parcela estimada: R$ 2.000/mês</span>
            <div class="opt-radio"></div>
          </div>
          <div class="opt-card js-step1-opt selected" data-val="400000">
            <span>R$ 400.000 &bull; Parcela estimada: R$ 3.200/mês</span>
            <div class="opt-radio"></div>
          </div>
          <div class="opt-card js-step1-opt" data-val="600000">
            <span>R$ 600.000 &bull; Parcela estimada: R$ 4.800/mês</span>
            <div class="opt-radio"></div>
          </div>
          <div class="opt-card js-step1-opt" data-val="1000000">
            <span>R$ 1.000.000 &bull; Parcela estimada: R$ 8.000/mês</span>
            <div class="opt-radio"></div>
          </div>

          <div id="step1Action" style="margin-top:14px; padding-top:12px; border-top:1px solid #E2E8F0;">
            <button type="button" id="btnNext1" class="nw-cta-btn" style="width:100%; min-height:50px; background:#008254; color:#fff; border:none; border-radius:8px; font-weight:800; font-size:15px; cursor:pointer; box-shadow:0 4px 12px rgba(0,130,84,0.3);">
              AVANÇAR PARA A ETAPA 2 &rarr;
            </button>
          </div>
        </div>
      </div>

      <!-- ================= PASSO 2 ================= -->
      <div id="step2" class="step-box">
        <div class="sim-question-card" style="background:#fff; border:2px solid #008254; border-radius:14px; padding:18px 14px; margin-bottom:16px; box-shadow:0 6px 18px rgba(0,130,84,0.08);">
          <span style="font-size:11px; font-weight:800; color:#008254; text-transform:uppercase; letter-spacing:0.04em; display:block; margin-bottom:6px;">Pergunta 2 de 3</span>
          <h2 style="font-size:18px; font-weight:800; color:#0F172A; margin-bottom:14px; line-height:1.3;">
            Qual é a sua urgência para sair do aluguel ou mudar?
          </h2>

          <div class="opt-card js-step2-opt selected" data-urgency="imediata">
            <span>🚨 Quero morar já (Cansei de queimar dinheiro com aluguel)</span>
            <div class="opt-radio"></div>
          </div>
          <div class="opt-card js-step2-opt" data-urgency="planejado_12">
            <span>📅 Planejamento em 12 meses (Quero me livrar de juros bancários)</span>
            <div class="opt-radio"></div>
          </div>
          <div class="opt-card js-step2-opt" data-urgency="investimento">
            <span>📈 Investimento patrimonial / Construção futura</span>
            <div class="opt-radio"></div>
          </div>

          <div id="step2Action" style="margin-top:14px; padding-top:12px; border-top:1px solid #E2E8F0;">
            <button type="button" id="btnNext2" class="nw-cta-btn" style="width:100%; min-height:50px; background:#008254; color:#fff; border:none; border-radius:8px; font-weight:800; font-size:15px; cursor:pointer;">
              AVANÇAR PARA A ÚLTIMA ETAPA &rarr;
            </button>
          </div>
        </div>
      </div>

      <!-- ================= PASSO 3 ================= -->
      <div id="step3" class="step-box">
        <div class="sim-question-card" style="background:#fff; border:2px solid #008254; border-radius:14px; padding:18px 14px; margin-bottom:16px; box-shadow:0 6px 18px rgba(0,130,84,0.08);">
          <span style="font-size:11px; font-weight:800; color:#008254; text-transform:uppercase; letter-spacing:0.04em; display:block; margin-bottom:6px;">Pergunta 3 de 3</span>
          <h2 style="font-size:18px; font-weight:800; color:#0F172A; margin-bottom:14px; line-height:1.3;">
            Como está a sua situação cadastral hoje?
          </h2>

          <div class="opt-card js-step3-opt selected" data-doc="limpo">
            <span>Nome sem restrições (Score regular ou alto)</span>
            <div class="opt-radio"></div>
          </div>
          <div class="opt-card js-step3-opt" data-doc="autonomo">
            <span>Autônomo / Renda sem holerite (Bancos tradicionais reprovam)</span>
            <div class="opt-radio"></div>
          </div>
          <div class="opt-card js-step3-opt" data-doc="restricao">
            <span>Possuo restrição ativa / Score em recuperação</span>
            <div class="opt-radio"></div>
          </div>

          <div id="step3Action" style="margin-top:14px; padding-top:12px; border-top:1px solid #E2E8F0;">
            <button type="button" id="btnCalculate" class="nw-cta-btn" style="width:100%; min-height:52px; background:#008254; color:#fff; border:none; border-radius:8px; font-weight:800; font-size:16px; cursor:pointer; box-shadow:0 4px 12px rgba(0,130,84,0.3);">
              GERAR CÁLCULO DA PARCELA OFICIAL &rarr;
            </button>
          </div>
        </div>
      </div>

      <!-- ================= LOADING / ANÁLISE ================= -->
      <div id="stepLoading" class="step-box" style="text-align:center; padding:28px 14px;">
        <div style="width:50px; height:50px; border:4px solid #E2E8F0; border-top:4px solid #008254; border-radius:50%; animation:spin 0.9s linear infinite; margin:0 auto 14px;"></div>
        <h3 id="loadingText" style="font-size:17px; font-weight:800; color:#0F172A; margin-bottom:6px;">
          Cruzando respostas com as regras do Banco Central...
        </h3>
        <p style="font-size:12.5px; color:#64748B;">
          Calculando cota dimensionada, entrada de 15% e eliminando juros bancários...
        </p>
      </div>

      <!-- ================= RESULTADO COM TIMER & URGÊNCIA ================= -->
      <div id="stepResult" class="step-box">
        <div style="background:#FFFFFF; border:2px solid #008254; border-radius:14px; padding:20px 16px; box-shadow:0 8px 24px rgba(0,130,84,0.12); margin-bottom:16px;">
          
          <!-- TIMER REGRESSIVO DE RESERVA DE VAGA -->
          <div style="background:#FEF2F2; border:1px solid #FECACA; border-radius:8px; padding:8px 10px; margin-bottom:12px; display:flex; justify-content:space-between; align-items:center; font-size:12px;">
            <span style="color:#991B1B; font-weight:700;">⏱️ Condição reservada por:</span>
            <span id="countdownTimer" style="background:#DC2626; color:#fff; font-weight:800; padding:2px 8px; border-radius:4px; font-family:monospace; font-size:13px;">09:59</span>
          </div>

          <div style="display:inline-flex; align-items:center; gap:6px; background:#DCFCE7; color:#15803D; font-size:11.5px; font-weight:800; padding:4px 10px; border-radius:99px; margin-bottom:10px;">
            <span>✅ Pré-Aprovação de Parcela Concluída</span>
          </div>

          <h2 style="font-size:19px; font-weight:800; color:#0F172A; margin-bottom:14px; line-height:1.3;">
            Plano de Aquisição Planejada Autorizado
          </h2>

          <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:10px; padding:14px; margin-bottom:14px;">
            <div style="display:flex; justify-content:space-between; margin-bottom:6px; font-size:13.5px;">
              <span style="color:#64748B;">Valor do Imóvel:</span>
              <strong id="resValorImovel" style="color:#0F172A;">R$ 400.000</strong>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:6px; font-size:13.5px;">
              <span style="color:#64748B;">Entrada Reduzida (15%):</span>
              <strong id="resEntrada" style="color:#008254; font-size:15px;">R$ 60.000</strong>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:6px; font-size:13.5px; border-top:1px dashed #CBD5E1; padding-top:8px;">
              <span style="color:#64748B;">Parcela Mensal Estimada (0,8%):</span>
              <strong id="resParcela" style="color:#008254; font-size:18px; font-weight:800;">R$ 3.200/mês</strong>
            </div>
          </div>

          <!-- COMPARATIVO ECONOMIA VS BANCO -->
          <div style="background:#EFF6FF; border:1px solid #BFDBFE; border-radius:10px; padding:12px; margin-bottom:16px; font-size:12.5px; color:#1E40AF; line-height:1.45;">
            <strong>📉 Economia Estimada vs. Financiamento de Banco:</strong>
            <p style="margin:3px 0 0;">No modelo bancário Caixa/Itaú (juros de 12% a.a.), este imóvel custaria mais de <span id="resCustoBanco">R$ 960.000</span> ao final. No programa planejado, você economiza aproximadamente <strong><span id="resEconomia">R$ 240.000</span> em juros não pagos</strong>.</p>
          </div>

          <!-- BOTAO WHATSAPP CONVERSAO SUPER AGRESSIVO -->
          <a id="btnWhatsapp" href="#" target="_blank" class="nw-cta-btn btn-pulse-wpp" style="display:flex; align-items:center; justify-content:center; gap:8px; width:100%; min-height:54px; background:#16A34A; color:#FFFFFF; border-radius:8px; font-size:15px; font-weight:800; text-decoration:none;">
            <span>💬 LIBERAR MINHA CARTA NO WHATSAPP</span>
          </a>
          <span style="display:block; text-align:center; font-size:11px; color:#64748B; margin-top:8px;">
            Fale com o especialista para validar a disponibilidade de vaga do seu grupo regional.
          </span>
        </div>

        <!-- BLOCO DE ESCAPE RSOC / ADSENSE -->
        <div class="ad-safe-slot" style="margin: 16px auto 20px; min-height:250px; background:#F8FAFC; border:1px dashed #CBD5E1; border-radius:12px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; padding:10px;">
          <span class="ad-safe-label" style="font-size:10.5px; font-weight:700; color:#64748B; margin-bottom:6px;">
            Prefere pesquisar taxas de financiamento bancário convencional Caixa ou leilões?
          </span>
          <ins class="adsbygoogle"
               style="display:block; width:100%; max-width:336px; height:250px;"
               data-ad-client="ca-{PUB_ID}"
               data-ad-slot="auto"
               data-ad-format="auto"
               data-full-width-responsive="true"></ins>
          <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
        </div>
      </div>

    </div>
  </section>

{FOOTER_HTML}

<style>
  @keyframes spin {{
    0% {{ transform: rotate(0deg); }}
    100% {{ transform: rotate(360deg); }}
  }}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {{
  var selectedValor = 400000;
  var selectedUrgency = 'imediata';
  var selectedDoc = 'limpo';

  // Leitura dinamica do numero de WhatsApp (?wpp=55...) com fallback central
  var urlParams = new URLSearchParams(window.location.search);
  var targetPhone = urlParams.get('wpp') || '5511999999999';

  // Timer Regressivo de 10 minutos
  var timeLeft = 599;
  function startTimer() {{
    var timerEl = document.getElementById('countdownTimer');
    var timerInterval = setInterval(function() {{
      var m = Math.floor(timeLeft / 60);
      var s = timeLeft % 60;
      timerEl.textContent = (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
      timeLeft--;
      if (timeLeft < 0) clearInterval(timerInterval);
    }}, 1000);
  }}

  // Passo 1
  document.querySelectorAll('.js-step1-opt').forEach(function(opt) {{
    opt.addEventListener('click', function() {{
      document.querySelectorAll('.js-step1-opt').forEach(function(o) {{ o.classList.remove('selected'); }});
      opt.classList.add('selected');
      selectedValor = parseInt(opt.getAttribute('data-val'), 10);
    }});
  }});

  document.getElementById('btnNext1').addEventListener('click', function() {{
    document.getElementById('step1').classList.remove('active');
    document.getElementById('step2').classList.add('active');
    document.getElementById('progressText').textContent = 'Etapa 2 de 3 (66%)';
    document.getElementById('stepTitle').textContent = 'Urgência & Prazo';
    document.getElementById('progressBar').style.width = '66%';
    if (window.fbq) fbq('trackCustom', 'ImovelStep2');
    window.scrollTo({{ top: 60, behavior: 'smooth' }});
  }});

  // Passo 2
  document.querySelectorAll('.js-step2-opt').forEach(function(opt) {{
    opt.addEventListener('click', function() {{
      document.querySelectorAll('.js-step2-opt').forEach(function(o) {{ o.classList.remove('selected'); }});
      opt.classList.add('selected');
      selectedUrgency = opt.getAttribute('data-urgency');
    }});
  }});

  document.getElementById('btnNext2').addEventListener('click', function() {{
    document.getElementById('step2').classList.remove('active');
    document.getElementById('step3').classList.add('active');
    document.getElementById('progressText').textContent = 'Etapa 3 de 3 (99%)';
    document.getElementById('stepTitle').textContent = 'Diagnóstico CPF';
    document.getElementById('progressBar').style.width = '99%';
    if (window.fbq) fbq('trackCustom', 'ImovelStep3');
    window.scrollTo({{ top: 60, behavior: 'smooth' }});
  }});

  // Passo 3
  document.querySelectorAll('.js-step3-opt').forEach(function(opt) {{
    opt.addEventListener('click', function() {{
      document.querySelectorAll('.js-step3-opt').forEach(function(o) {{ o.classList.remove('selected'); }});
      opt.classList.add('selected');
      selectedDoc = opt.getAttribute('data-doc');
    }});
  }});

  // Processar Cálculo
  document.getElementById('btnCalculate').addEventListener('click', function() {{
    document.getElementById('step3').classList.remove('active');
    document.getElementById('stepLoading').classList.add('active');
    document.getElementById('progressText').textContent = 'Processando (100%)';
    document.getElementById('stepTitle').textContent = 'Análise Final';
    document.getElementById('progressBar').style.width = '100%';
    if (window.fbq) fbq('trackCustom', 'ImovelAnalyzing');

    var texts = [
      'Cruzando respostas com as regras do Banco Central...',
      'Verificando elegibilidade para entrada reduzida de 15%...',
      'Calculando amortização sem juros compostos...',
      'Liberando opções com ocupação imediata...'
    ];
    var i = 0;
    var interval = setInterval(function() {{
      i++;
      if (texts[i]) {{
        document.getElementById('loadingText').textContent = texts[i];
      }}
    }}, 900);

    setTimeout(function() {{
      clearInterval(interval);
      document.getElementById('stepLoading').classList.remove('active');
      document.getElementById('stepResult').classList.add('active');
      startTimer();

      // Fórmulas Oficiais
      var entrada = selectedValor * 0.15;
      var parcela = selectedValor * 0.008;
      var custoBanco = selectedValor * 2.45;
      var economia = custoBanco - (selectedValor * 1.35);

      function fmt(val) {{
        return 'R$ ' + val.toLocaleString('pt-BR', {{ maximumFractionDigits: 0 }});
      }}

      document.getElementById('resValorImovel').textContent = fmt(selectedValor);
      document.getElementById('resEntrada').textContent = fmt(entrada);
      document.getElementById('resParcela').textContent = fmt(parcela) + '/mês';
      document.getElementById('resCustoBanco').textContent = fmt(custoBanco);
      document.getElementById('resEconomia').textContent = fmt(economia);

      var msg = encodeURIComponent(
        'Olá! Fiz a simulação no comparador imobiliário para um imóvel de ' + fmt(selectedValor) + 
        ' (Entrada de ' + fmt(entrada) + ' e parcela de ' + fmt(parcela) + '/mês). Desejo verificar a liberação da minha carta.'
      );
      var wppBtn = document.getElementById('btnWhatsapp');
      wppBtn.setAttribute('href', 'https://wa.me/' + targetPhone + '?text=' + msg);

      wppBtn.addEventListener('click', function() {{
        if (window.fbq) {{
          fbq('track', 'InitiateCheckout', {{
            content_name: 'Simulador Imobiliario WhatsApp',
            value: parcela,
            currency: 'BRL'
          }});
        }}
      }});

      if (window.fbq) {{
        fbq('track', 'Lead', {{
          content_name: 'Simulacao Imovel Concluida',
          value: entrada,
          currency: 'BRL'
        }});
        fbq('trackCustom', 'ImovelQuizComplete');
      }}

      window.scrollTo({{ top: 40, behavior: 'smooth' }});
    }}, 3600);
  }});
}});
</script>

<script src="../js/afiliados-config.js"></script>
<script src="../js/app.js"></script>
</body>
</html>
"""

# ==============================================================================
# 3. PROPRIETARIO.HTML (VENDA EM ATÉ 60 DIAS)
# ==============================================================================
proprietario_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
{HEAD_COMMON}
  <title>Venda Sua Casa em Até 60 Dias com Renda Garantida — Comparador Cartões</title>
  <meta name="description" content="Proprietário: Venda seu imóvel parado em até 60 dias. Receba 15% à vista na assinatura, mensalidade sem vacância e quitação total de 85%.">
  <link rel="canonical" href="https://comparadorcartoes.com/simulador-imobiliario/proprietario.html">
</head>
<body class="sim-page" style="margin:0; padding:0; background:#F8FAFC; overflow-x:hidden;">

{HEADER_HTML}

  <section class="pillar-hero" style="padding: 16px 0 12px;">
    <div class="container" style="max-width: 600px; padding: 0 14px;">
      
      <div style="background:#0F172A; color:#FFFFFF; border-radius:14px; padding:20px 16px; box-shadow:0 8px 24px rgba(0,0,0,0.12); margin-bottom:16px;">
        <div style="display:inline-flex; align-items:center; gap:6px; background:rgba(251,191,36,0.2); color:#FBBF24; font-size:11.5px; font-weight:800; padding:4px 10px; border-radius:99px; margin-bottom:10px;">
          <span>⚡ VENDA RÁPIDA EM ATÉ 60 DIAS</span>
        </div>
        
        <h1 style="font-size: clamp(20px, 3.6vw, 25px); font-weight:800; line-height:1.25; margin-bottom:8px;">
          Cansado de Perder Dinheiro com Imóvel Parado, IPTU e Condomínio?
        </h1>
        
        <p style="font-size:13.5px; color:#CBD5E1; line-height:1.5; margin-bottom:16px;">
          Enquanto as imobiliárias convencionais deixam sua casa parada por meses acumulando contas, nosso programa conecta seu imóvel a compradores qualificados: receba <strong>15% à vista na assinatura</strong>, uma <strong>renda mensal de ocupação sem vacância</strong> e o saldo de <strong>85% quitado</strong> via crédito homologado pelo Banco Central.
        </p>

        <!-- OS 3 PILARES DO PROPRIETÁRIO -->
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:6px; margin-bottom:16px; text-align:center;">
          <div style="background:rgba(255,255,255,0.06); padding:10px 4px; border-radius:8px; border:1px solid rgba(52,211,153,0.3);">
            <div style="font-size:18px; font-weight:800; color:#34D399;">15%</div>
            <div style="font-size:10.5px; color:#D1FAE5;">Na Assinatura</div>
          </div>
          <div style="background:rgba(255,255,255,0.06); padding:10px 4px; border-radius:8px; border:1px solid rgba(56,189,248,0.3);">
            <div style="font-size:18px; font-weight:800; color:#38BDF8;">Renda</div>
            <div style="font-size:10.5px; color:#E0F2FE;">Mensal Todo Dia 10</div>
          </div>
          <div style="background:rgba(255,255,255,0.06); padding:10px 4px; border-radius:8px; border:1px solid rgba(251,191,36,0.3);">
            <div style="font-size:18px; font-weight:800; color:#FBBF24;">85%</div>
            <div style="font-size:10.5px; color:#FEF3C7;">Quitação na Escritura</div>
          </div>
        </div>

        <a id="btnProprietarioWpp" href="https://wa.me/5511999999999?text=Ol%C3%A1!%20Tenho%20um%20im%C3%B3vel%20e%20quero%20vender%20em%20at%C3%A9%2060%20dias%20com%20renda%20garantida." target="_blank" class="nw-cta-btn" style="display:flex; align-items:center; justify-content:center; gap:8px; width:100%; min-height:52px; background:#16A34A; color:#fff; border-radius:8px; font-weight:800; font-size:15px; text-decoration:none; box-shadow:0 4px 14px rgba(22,163,74,0.4);">
          <span>FALAR COM EQUIPE DE LIQUIDEZ NO WHATSAPP &rarr;</span>
        </a>
      </div>

      <!-- VANTAGENS DO MODELO -->
      <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:16px 14px; margin-bottom:16px;">
        <h3 style="font-size:16px; font-weight:800; color:#0F172A; margin-bottom:10px;">
          Por que este modelo é mais seguro que o mercado comum:
        </h3>
        <ul style="font-size:13px; color:#334155; line-height:1.65; padding-left:18px; margin:0;">
          <li><strong>Zero Visitas Inúteis:</strong> Nada de curiosos sem limite bancário passeando pela sua casa.</li>
          <li><strong>Encargos 100% Transferidos:</strong> IPTU, condomínio, luz e água são quitados pelo ocupante.</li>
          <li><strong>Garantia Jurídica em Cartório:</strong> Contrato de locação com opção resolutiva e vistoria prévia.</li>
          <li><strong>Preço Cheio Preservado:</strong> Venda sem deságios abusivos de leilão ou intermediários.</li>
        </ul>
      </div>

      <!-- BLOCO DE ANÚNCIO SEGURO -->
      <div class="ad-safe-slot" style="margin: 14px auto 18px; min-height:250px; background:#F8FAFC; border:1px dashed #CBD5E1; border-radius:12px; display:flex; flex-direction:column; align-items:center; justify-content:center; text-align:center; padding:10px;">
        <span class="ad-safe-label" style="font-size:10px; font-weight:700; color:#94A3B8; text-transform:uppercase; margin-bottom:6px;">Publicidade &bull; Espaço Patrocinado</span>
        <ins class="adsbygoogle"
             style="display:block; width:100%; max-width:336px; height:250px;"
             data-ad-client="ca-{PUB_ID}"
             data-ad-slot="auto"
             data-ad-format="auto"
             data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
      </div>

    </div>
  </section>

{FOOTER_HTML}

<script>
var urlParams = new URLSearchParams(window.location.search);
var targetPhone = urlParams.get('wpp') || '5511999999999';
var btn = document.getElementById('btnProprietarioWpp');
btn.setAttribute('href', 'https://wa.me/' + targetPhone + '?text=' + encodeURIComponent('Olá! Tenho um imóvel e quero vender em até 60 dias com renda garantida.'));

btn.addEventListener('click', function() {{
  if (window.fbq) {{
    fbq('track', 'Lead', {{ content_name: 'Proprietario Lead WhatsApp' }});
  }}
}});
</script>

<script src="../js/afiliados-config.js"></script>
<script src="../js/app.js"></script>
</body>
</html>
"""

# Escreve os arquivos
with open(os.path.join(TARGET_DIR, "index.html"), "w", encoding="utf-8") as f:
    f.write(index_html)

with open(os.path.join(TARGET_DIR, "comprar.html"), "w", encoding="utf-8") as f:
    f.write(comprar_html)

with open(os.path.join(TARGET_DIR, "proprietario.html"), "w", encoding="utf-8") as f:
    f.write(proprietario_html)

# Replica no Buzz 2.0
with open(os.path.join(r"C:\Users\mateu\Downloads\Projeto Dudu\Buzz 2.0\generate_simulador_imobiliario.py"), "w", encoding="utf-8") as f:
    with open(__file__, "r", encoding="utf-8") as src:
        f.write(src.read())

print("SUCESSO: Simulador Imobiliario Agressivo 2.0 Gerado!")

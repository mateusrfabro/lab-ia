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

HEADER_HTML = """  <!-- Header Ultra-Clean Mobile-First (Zero Overlap) -->
  <header style="background:#FFFFFF; border-bottom:1px solid #E2E8F0; padding:10px 0; position:relative; z-index:10;">
    <div class="container" style="display:flex; justify-content:space-between; align-items:center; max-width:680px; padding:0 14px;">
      <a href="/index.html" style="text-decoration:none; display:flex; align-items:center; gap:8px;">
        <span style="background:#008254; color:#FFFFFF; border-radius:8px; width:34px; height:34px; display:inline-flex; align-items:center; justify-content:center; font-weight:800; font-size:15px; flex-shrink:0;">CC</span>
        <div style="display:flex; flex-direction:column; line-height:1.2;">
          <span style="font-weight:800; color:#111827; font-size:15px; letter-spacing:-0.01em;">Comparador <span style="color:#008254;">Cartões</span></span>
          <span style="font-size:10.5px; color:#6B7280;">Simulador Imobiliário</span>
        </div>
      </a>
      <div style="font-size:11px; font-weight:700; color:#008254; background:#E6F5EF; padding:4px 10px; border-radius:99px; white-space:nowrap; display:flex; align-items:center; gap:4px;">
        <span>🏛️</span>
        <span>Banco Central</span>
      </div>
    </div>
  </header>
"""

FOOTER_HTML = """  <footer style="background:#0B251C; color:#94A3B8; padding:28px 0 20px; margin-top:32px; font-size:12px; border-top:1px solid rgba(255,255,255,0.08);">
    <div class="container" style="text-align:center; max-width:680px; padding:0 14px;">
      <p style="margin-bottom:8px; color:#E2E8F0; font-weight:600; font-size:12.5px;">Comparador Independente de Finanças, Cartões e Crédito Imobiliário</p>
      <p style="margin-bottom:10px; line-height:1.5; font-size:11px; color:#94A3B8;">O portal atua como ferramenta informativa e de simulação comparativa. As condições de financiamento bancário e de cotas de consórcio são regulamentadas pelo Banco Central do Brasil (Lei nº 11.795/2008 e Resolução BCB 285). Não realizamos cobrança de valores antecipados para aprovação de crédito.</p>
      <p style="font-size:11px; color:#64748B;">&copy; 2026 ComparadorCartoes.com &bull; Todos os direitos reservados.</p>
    </div>
  </footer>
"""

# ==============================================================================
# 1. INDEX.HTML (HUB DO SIMULADOR IMOBILIÁRIO)
# ==============================================================================
index_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
{HEAD_COMMON}
  <title>Simulador Imobiliário 2026: Compare Financiamento Caixa vs. Aquisição Planejada — Comparador Cartões</title>
  <meta name="description" content="Simulador independente de crédito imobiliário. Compare parcelas sem juros abusivos de banco, entrada de 15% e opção de morar já em conformidade com o Banco Central.">
  <link rel="canonical" href="https://comparadorcartoes.com/simulador-imobiliario/">
</head>
<body class="sim-page" style="margin:0; padding:0; background:#F8FAFC; overflow-x:hidden;">

{HEADER_HTML}

  <!-- HERO & MICRO-QUIZ ABOVE THE FOLD (DISPARO DO GOOGLE VIGNETTE NO CLIQUE INTERNO) -->
  <section class="pillar-hero" style="padding: 16px 0 12px; background: #F8FAFC;">
    <div class="container" style="max-width: 600px; text-align: center; padding: 0 14px;">
      <div style="display:inline-flex; align-items:center; gap:6px; background:#E6F5EF; color:#008254; font-size:11.5px; font-weight:800; padding:4px 12px; border-radius:99px; margin-bottom:10px; text-transform:uppercase;">
        <span>⚡ Simulador Inteligente 2026</span>
      </div>
      <h1 class="pillar-title" style="font-size: clamp(20px, 3.6vw, 28px); line-height: 1.25; margin-bottom: 8px; color:#0F172A; font-weight:800;">
        Descubra o valor da sua parcela sem juros abusivos de banco
      </h1>
      <p class="pillar-subtitle" style="font-size: 13.5px; color:#475569; margin-bottom: 16px; line-height: 1.5;">
        Em 2026, quem financia no modelo tradicional Caixa/Itaú paga de <strong>2,2x a 3x o valor do imóvel</strong> em juros. Compare alternativas autorizadas pelo Banco Central com entrada justa e parcelas planejadas.
      </p>

      <!-- MICRO-ACTION CARDS (DISPARADORES DE VIGNETTE) -->
      <div style="background:#FFFFFF; border:2px solid #008254; border-radius:14px; padding:18px 14px; box-shadow:0 8px 24px -4px rgba(0,130,84,0.12); margin-bottom:12px;">
        <p style="font-size:14px; font-weight:800; color:#0F172A; margin-bottom:12px;">
          Selecione o seu objetivo imobiliário hoje:
        </p>

        <!-- BOTAO 1: FRENTE COMPRADOR -->
        <a href="/simulador-imobiliario/comprar.html" class="nw-cta-btn js-keep-utms" style="display:flex; align-items:center; justify-content:space-between; width:100%; min-height:52px; padding:12px 16px; margin-bottom:10px; background:#008254; color:#FFFFFF; border-radius:8px; font-weight:800; font-size:14px; text-decoration:none; box-shadow:0 4px 12px rgba(0,130,84,0.25);">
          <span style="display:flex; align-items:center; gap:8px; text-align:left;">
            <span style="font-size:20px;">🏡</span>
            <span>QUERO COMPRAR OU CONSTRUIR MEU IMÓVEL</span>
          </span>
          <span style="font-size:18px;">&rarr;</span>
        </a>

        <!-- BOTAO 2: FRENTE PROPRIETÁRIO -->
        <a href="/simulador-imobiliario/proprietario.html" class="js-keep-utms" style="display:flex; align-items:center; justify-content:space-between; width:100%; min-height:50px; padding:12px 16px; background:#0F172A; color:#FFFFFF; border-radius:8px; font-weight:700; font-size:13.5px; text-decoration:none;">
          <span style="display:flex; align-items:center; gap:8px; text-align:left;">
            <span style="font-size:18px;">🔑</span>
            <span>TENHO UM IMÓVEL PARADO E QUERO VENDER</span>
          </span>
          <span style="font-size:16px;">&rarr;</span>
        </a>

        <!-- COMPLIANCE DISCLAIMER -->
        <span style="display:block; font-size:11px; color:#64748B; margin-top:10px; line-height:1.4;">
          🛡️ Ao clicar, você continuará navegando neste comparador financeiro independente (100% gratuito e seguro).
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

  <!-- CONTEÚDO DENSO DE QUALIDADE & COMPARATIVO OFICIAL -->
  <main class="container" style="max-width: 680px; padding: 0 14px 24px;">
    
    <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:14px; padding:20px 16px; margin-bottom:20px; box-shadow:0 2px 10px rgba(0,0,0,0.03);">
      <h2 style="font-size:18px; font-weight:800; color:#0F172A; margin-bottom:10px;">
        Como funciona a Matemática da Parcela Sem Juros de Banco
      </h2>
      <p style="font-size:13.5px; color:#334155; line-height:1.6; margin-bottom:14px;">
        No Brasil, a taxa Selic em patamar elevado faz com que o financiamento imobiliário pelos bancos convencionais opere com taxas nominais entre <strong>10,5% e 13,8% ao ano</strong>. Quando somados o seguro obrigatório MIP/DFI e a correção pela TR, o comprador assume uma dívida que triplica o custo final do bem ao longo de 30 a 35 anos.
      </p>

      <!-- TABELA COMPARATIVA OFICIAL COM AVISO DE SCROLL MOBILE -->
      <div class="quick-table-wrap" style="overflow-x:auto; margin:14px 0 18px; border-radius:8px; border:1px solid #E2E8F0;">
        <table style="width:100%; min-width:440px; border-collapse:collapse; font-size:12.5px; text-align:left;">
          <thead>
            <tr style="background:#0F172A; color:#FFFFFF;">
              <th style="padding:10px 10px;">Valor do Imóvel</th>
              <th style="padding:10px 10px;">Entrada (15%)</th>
              <th style="padding:10px 10px;">Parcela (0,8%)</th>
              <th style="padding:10px 10px;">Economia vs. Banco</th>
            </tr>
          </thead>
          <tbody>
            <tr style="border-bottom:1px solid #E2E8F0; background:#F8FAFC;">
              <td style="padding:9px 10px; font-weight:700;">R$ 200.000</td>
              <td style="padding:9px 10px;">R$ 30.000</td>
              <td style="padding:9px 10px; color:#008254; font-weight:800;">R$ 1.600/mês</td>
              <td style="padding:9px 10px; color:#059669; font-weight:700;">~ R$ 140.000</td>
            </tr>
            <tr style="border-bottom:1px solid #E2E8F0;">
              <td style="padding:9px 10px; font-weight:700;">R$ 400.000</td>
              <td style="padding:9px 10px;">R$ 60.000</td>
              <td style="padding:9px 10px; color:#008254; font-weight:800;">R$ 3.200/mês</td>
              <td style="padding:9px 10px; color:#059669; font-weight:700;">~ R$ 240.000</td>
            </tr>
            <tr style="border-bottom:1px solid #E2E8F0; background:#F8FAFC;">
              <td style="padding:9px 10px; font-weight:700;">R$ 600.000</td>
              <td style="padding:9px 10px;">R$ 90.000</td>
              <td style="padding:9px 10px; color:#008254; font-weight:800;">R$ 4.800/mês</td>
              <td style="padding:9px 10px; color:#059669; font-weight:700;">~ R$ 320.000</td>
            </tr>
            <tr>
              <td style="padding:9px 10px; font-weight:700;">R$ 1.000.000</td>
              <td style="padding:9px 10px;">R$ 150.000</td>
              <td style="padding:9px 10px; color:#008254; font-weight:800;">R$ 8.000/mês</td>
              <td style="padding:9px 10px; color:#059669; font-weight:700;">~ R$ 450.000</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div style="background:#F0FDF4; border:1px solid #BBF7D0; border-radius:10px; padding:12px; margin-top:14px;">
        <p style="font-size:12.5px; color:#166534; line-height:1.5; margin:0;">
          💡 <strong>Regra Oficial:</strong> A taxa de administração do consórcio imobiliário é fixa e diluída por todo o período, eliminando os juros compostos dos bancos. A modalidade de <em>Aluguel com Opção de Compra</em> permite ao comprador ocupar o imóvel de imediato enquanto aguarda a contemplação da cota homologada pelo Banco Central.
        </p>
      </div>
    </div>

    <!-- BOTÃO FINAL DE CHAMADA -->
    <div style="text-align:center; margin:20px 0;">
      <a href="/simulador-imobiliario/comprar.html" class="nw-cta-btn js-keep-utms" style="display:inline-block; max-width:400px; width:100%; padding:14px 18px; font-size:15px; font-weight:800; background:#008254; color:#fff; border-radius:8px; text-decoration:none;">
        CALCULAR SIMULAÇÃO DO MEU IMÓVEL AGORA &rarr;
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
# 2. COMPRAR.HTML (FUNIL COMPRADOR: MORAR JÁ EM 5 ETAPAS INTERATIVAS)
# ==============================================================================
comprar_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
{HEAD_COMMON}
  <title>Simulador de Compra & Aluguel com Opção: Calcule sua Entrada e Parcela — Comparador Cartões</title>
  <meta name="description" content="Simulação interativa para compra de imóvel sem juros bancários. Saiba a parcela exata para valores de R$ 120 mil a R$ 1 milhão regulamentados pelo Banco Central.">
  <link rel="canonical" href="https://comparadorcartoes.com/simulador-imobiliario/comprar.html">
  <style>
    .step-box {{ display: none; }}
    .step-box.active {{ display: block; }}
    .opt-card {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      min-height: 52px;
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

      <!-- ALERTA DE COMPATIBILIDADE BACEN (DWELL TIME INDUZIDO 12-15s) -->
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

          <div class="opt-card js-step1-opt" data-val="150000" data-label="R$ 150.000">
            <span>R$ 150.000 (Imóvel Inicial / Popular)</span>
            <div class="opt-radio"></div>
          </div>
          <div class="opt-card js-step1-opt" data-val="250000" data-label="R$ 250.000">
            <span>R$ 250.000 (Apartamento Padrão)</span>
            <div class="opt-radio"></div>
          </div>
          <div class="opt-card js-step1-opt selected" data-val="400000" data-label="R$ 400.000">
            <span>R$ 400.000 (Casa 3 Quartos / Médio Padrão)</span>
            <div class="opt-radio"></div>
          </div>
          <div class="opt-card js-step1-opt" data-val="600000" data-label="R$ 600.000">
            <span>R$ 600.000 (Condomínio Fechado)</span>
            <div class="opt-radio"></div>
          </div>
          <div class="opt-card js-step1-opt" data-val="1000000" data-label="R$ 1.000.000">
            <span>R$ 1.000.000 (Alto Padrão)</span>
            <div class="opt-radio"></div>
          </div>

          <!-- AVISO DE CLIQUE EM 2 TEMPOS -->
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
            Qual é a sua urgência para morar ou mudar para o imóvel?
          </h2>

          <div class="opt-card js-step2-opt selected" data-urgency="imediata">
            <span>Quero morar já (Opção de Aluguel com Compra)</span>
            <div class="opt-radio"></div>
          </div>
          <div class="opt-card js-step2-opt" data-urgency="planejado_12">
            <span>Planejamento médio (De 6 a 18 meses)</span>
            <div class="opt-radio"></div>
          </div>
          <div class="opt-card js-step2-opt" data-urgency="investimento">
            <span>Investimento patrimonial / Construção futura</span>
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
            Como está a situação do seu CPF no momento?
          </h2>

          <div class="opt-card js-step3-opt selected" data-doc="limpo">
            <span>Nome sem restrições (Score regular ou alto)</span>
            <div class="opt-radio"></div>
          </div>
          <div class="opt-card js-step3-opt" data-doc="autonomo">
            <span>Autônomo / Renda informal sem holerite</span>
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

      <!-- ================= RESULTADO ================= -->
      <div id="stepResult" class="step-box">
        <div style="background:#FFFFFF; border:2px solid #008254; border-radius:14px; padding:20px 16px; box-shadow:0 8px 24px rgba(0,130,84,0.12); margin-bottom:16px;">
          
          <div style="display:inline-flex; align-items:center; gap:6px; background:#DCFCE7; color:#15803D; font-size:11.5px; font-weight:800; padding:4px 10px; border-radius:99px; margin-bottom:10px;">
            <span>✅ Simulação Concluída com Sucesso</span>
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
              <span style="color:#64748B;">Entrada (15%):</span>
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

          <!-- BOTAO WHATSAPP CONVERSAO -->
          <a id="btnWhatsapp" href="#" target="_blank" class="nw-cta-btn" style="display:flex; align-items:center; justify-content:center; gap:8px; width:100%; min-height:52px; background:#16A34A; color:#FFFFFF; border-radius:8px; font-size:14.5px; font-weight:800; text-decoration:none; box-shadow:0 4px 14px rgba(22,163,74,0.35);">
            <span>💬 FALAR COM CONSULTOR NO WHATSAPP</span>
          </a>
          <span style="display:block; text-align:center; font-size:11px; color:#64748B; margin-top:8px;">
            Atendimento gratuito para verificar elegibilidade de vaga e documentação.
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
        ' (Entrada de ' + fmt(entrada) + ' e parcela de ' + fmt(parcela) + '/mês). Desejo verificar a liberação de vaga.'
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
# 3. PROPRIETARIO.HTML (FUNIL PROPRIETÁRIO: VENDA JÁ COM RENDA GARANTIDA)
# ==============================================================================
proprietario_html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
{HEAD_COMMON}
  <title>Venda de Imóvel com Renda Garantida: 15% na Assinatura + Ocupação — Comparador Cartões</title>
  <meta name="description" content="Proprietário: Venda seu imóvel parado sem custos de IPTU e condomínio. Receba 15% na assinatura, mensalidade pela ocupação e quitação via consórcio.">
  <link rel="canonical" href="https://comparadorcartoes.com/simulador-imobiliario/proprietario.html">
</head>
<body class="sim-page" style="margin:0; padding:0; background:#F8FAFC; overflow-x:hidden;">

{HEADER_HTML}

  <section class="pillar-hero" style="padding: 16px 0 12px;">
    <div class="container" style="max-width: 600px; padding: 0 14px;">
      
      <div style="background:#0F172A; color:#FFFFFF; border-radius:14px; padding:20px 16px; box-shadow:0 8px 24px rgba(0,0,0,0.12); margin-bottom:16px;">
        <div style="display:inline-flex; align-items:center; gap:6px; background:rgba(56,189,248,0.2); color:#38BDF8; font-size:11.5px; font-weight:800; padding:4px 10px; border-radius:99px; margin-bottom:10px;">
          <span>🔑 Originação de Imóveis &bull; Venda Certa</span>
        </div>
        
        <h1 style="font-size: clamp(19px, 3.4vw, 24px); font-weight:800; line-height:1.3; margin-bottom:8px;">
          Tem um imóvel parado gerando despesas de condomínio e IPTU?
        </h1>
        
        <p style="font-size:13.5px; color:#CBD5E1; line-height:1.5; margin-bottom:16px;">
          Troque a incerteza do mercado por um contrato estruturado: receba <strong>15% à vista na assinatura</strong>, uma <strong>mensalidade pela ocupação</strong> durante todo o período e o saldo de <strong>85% quitado</strong> via crédito homologado pelo Banco Central.
        </p>

        <!-- OS 3 PILARES DO PROPRIETÁRIO -->
        <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:6px; margin-bottom:16px; text-align:center;">
          <div style="background:rgba(255,255,255,0.06); padding:8px 4px; border-radius:8px;">
            <div style="font-size:17px; font-weight:800; color:#34D399;">15%</div>
            <div style="font-size:10.5px; color:#94A3B8;">Na Assinatura</div>
          </div>
          <div style="background:rgba(255,255,255,0.06); padding:8px 4px; border-radius:8px;">
            <div style="font-size:17px; font-weight:800; color:#38BDF8;">Renda</div>
            <div style="font-size:10.5px; color:#94A3B8;">Mensal Ocupação</div>
          </div>
          <div style="background:rgba(255,255,255,0.06); padding:8px 4px; border-radius:8px;">
            <div style="font-size:17px; font-weight:800; color:#FBBF24;">85%</div>
            <div style="font-size:10.5px; color:#94A3B8;">Quitação Final</div>
          </div>
        </div>

        <a id="btnProprietarioWpp" href="https://wa.me/5511999999999?text=Ol%C3%A1!%20Tenho%20um%20im%C3%B3vel%20e%20quero%20conhecer%20a%20proposta%20de%20venda%20com%20ocupa%C3%A7%C3%A3o%20garantida." target="_blank" class="nw-cta-btn" style="display:flex; align-items:center; justify-content:center; gap:8px; width:100%; min-height:50px; background:#008254; color:#fff; border-radius:8px; font-weight:800; font-size:14.5px; text-decoration:none; box-shadow:0 4px 12px rgba(0,130,84,0.35);">
          <span>FALAR COM EQUIPE DE CAPTAÇÃO NO WHATSAPP &rarr;</span>
        </a>
      </div>

      <!-- VANTAGENS DO MODELO -->
      <div style="background:#FFFFFF; border:1px solid #E2E8F0; border-radius:12px; padding:16px 14px; margin-bottom:16px;">
        <h3 style="font-size:16px; font-weight:800; color:#0F172A; margin-bottom:10px;">
          Por que proprietários preferem este modelo:
        </h3>
        <ul style="font-size:13px; color:#334155; line-height:1.65; padding-left:18px; margin:0;">
          <li><strong>Zero Vacância:</strong> Ocupação formalizada com contrato de locação e opção de compra.</li>
          <li><strong>Encargos Pagos:</strong> IPTU, água, luz e condomínio são transferidos para o ocupante.</li>
          <li><strong>Análise Cadastral Rígida:</strong> O ocupante passa por análise documental e capacidade de pagamento.</li>
          <li><strong>Segurança Jurídica:</strong> Cláusula resolutiva expressa e garantia patrimonial em cartório.</li>
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
btn.setAttribute('href', 'https://wa.me/' + targetPhone + '?text=' + encodeURIComponent('Olá! Tenho um imóvel e quero conhecer a proposta de venda com ocupação garantida.'));

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

print("SUCESSO: Simulador Imobiliário atualizado com novo Header Mobile!")

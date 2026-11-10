import os

pub_root = r'C:\Users\mateu\Projects\portal-eua\public'
ca_pub = 'ca-pub-4612410097892333'

DYNAMIC_PIXEL_AND_UTM_SCRIPT = """
<script>
/* === 1. DYNAMIC MULTI-PIXEL TRACKER (?fb=PIXEL_ID&tt=TT_ID&aw=AW_ID&gl=LABEL&lead=1) === */
(function(){
  var p = new URLSearchParams(window.location.search),
      fb  = p.get('fb'),
      aw  = p.get('aw'),
      gl  = p.get('gl'),
      gL  = p.get('gL'),
      tt  = p.get('tt'),
      lead = p.get('lead') === '1';

  /* META (Facebook Ads) */
  if (fb) {
    (function(f,b,e,v,n,t,s){
      if(f.fbq)return;n=f.fbq=function(){n.callMethod?
      n.callMethod.apply(n,arguments):n.queue.push(arguments)};
      if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
      n.queue=[];t=b.createElement(e);t.async=!0;
      t.src=v;s=b.getElementsByTagName(e)[0];
      s.parentNode.insertBefore(t,s)}(window, document,'script',
      'https://connect.facebook.net/en_US/fbevents.js'));
    fbq('init', fb);
    fbq('trackSingle', fb, 'PageView');
    fbq('trackSingle', fb, 'ViewContent');
    if (lead) fbq('trackSingle', fb, 'Lead');
  }

  /* GOOGLE ADS */
  if (aw) {
    window.dataLayer = window.dataLayer || [];
    function gtag(){ dataLayer.push(arguments); }
    if (!window.gtag) {
      window.gtag = gtag;
      gtag('js', new Date());
      var s = document.createElement('script');
      s.async = 1;
      s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(aw);
      document.head.appendChild(s);
    }
    gtag('config', aw, { send_page_view: false });
    if (gl) gtag('event', 'conversion', { 'send_to': aw + '/' + gl });
    if (lead && gL) gtag('event', 'conversion', { 'send_to': aw + '/' + gL });
  }

  /* TIKTOK ADS */
  if (tt) {
    !function (w, d, t) {
      w.TiktokAnalyticsObject = t;
      var ttq = w[t] = w[t] || [];
      ttq.methods = ["page","track","identify","instances","debug","on","off","once","ready","alias","group","enableCookie","disableCookie","holdConsent","revokeConsent","grantConsent"];
      ttq.setAndDefer = function(target, m){ target[m] = function(){ target.push([m].concat(Array.prototype.slice.call(arguments, 0))); }; };
      ttq.methods.forEach(function(m){ ttq.setAndDefer(ttq, m); });
      ttq.load = function(e){
        var r = "https://analytics.tiktok.com/i18n/pixel/events.js";
        var sc = d.createElement("script"); sc.type = "text/javascript"; sc.async = !0; sc.src = r + "?sdkid=" + e + "&lib=" + t;
        var fs = d.getElementsByTagName("script")[0]; fs.parentNode.insertBefore(sc, fs);
      };
      ttq.load(tt);
      ttq.page();
      ttq.track('ViewContent');
      if (lead) ttq.track('SubmitForm');
    }(window, document, 'ttq');
  }
})();

/* === 2. AUTOMATIC UTM & PIXEL PARAMETER PROPAGATOR ACROSS FUNNEL STEPS === */
(function () {
  var params = new URLSearchParams(window.location.search);
  var utmParams = [];
  params.forEach(function(value, key) {
    if (key.indexOf('utm_') === 0 || key.indexOf('fb') === 0 || key.indexOf('pixel') === 0 || key.indexOf('tt') === 0 || key.indexOf('aw') === 0 || key.indexOf('gl') === 0 || key.indexOf('gL') === 0) {
      utmParams.push(encodeURIComponent(key) + '=' + encodeURIComponent(value));
    }
  });
  if (!utmParams.length) return;
  function applyUtms() {
    document.querySelectorAll('a[href]').forEach(function(link) {
      var href = link.getAttribute('href');
      if (!href || href.indexOf('#') === 0 || href.indexOf('mailto:') === 0 || href.indexOf('tel:') === 0) return;
      try {
        var url = new URL(href, window.location.origin);
        utmParams.forEach(function(param) {
          var kv = param.split('=');
          if (!url.searchParams.has(kv[0])) url.searchParams.set(kv[0], decodeURIComponent(kv[1]));
        });
        link.setAttribute('href', url.pathname + url.search + url.hash);
      } catch(e) {}
    });
  }
  if (document.readyState === 'complete') applyUtms();
  else window.addEventListener('load', applyUtms);
})();
</script>
"""

FUNNEL_STYLE = """
  <style>
    * { box-sizing: border-box; }
    body { margin: 0; background: #f3eee3; color: #181512; font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; line-height: 1.55; }
    .mdp-header { background: #181512; color: #f3eee3; padding: 14px 20px; border-bottom: 3px solid #9e2a2b; }
    .mdp-header-inner { max-width: 680px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; }
    .mdp-brand { color: #f3eee3; text-decoration: none; font-size: 20px; font-weight: 800; letter-spacing: -0.02em; }
    .mdp-brand em { font-style: italic; color: #eab308; font-weight: 700; }
    .mdp-nav a { color: #cbd5e1; text-decoration: none; font-size: 13px; margin-left: 14px; font-weight: 600; }
    .csc-wrap { max-width: 640px; margin: 22px auto 60px; padding: 0 16px; }
    .csc-card { background: #ffffff; border: 1px solid #d6cfc2; border-radius: 14px; padding: 24px 20px; box-shadow: 0 8px 24px rgba(0,0,0,0.06); }
    .csc-badge { display: inline-block; background: #fef3c7; color: #92400e; font-size: 11px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.05em; padding: 4px 10px; border-radius: 99px; margin-bottom: 10px; }
    .csc-title { font-size: 24px; font-weight: 800; color: #0f172a; line-height: 1.25; margin: 0 0 12px; }
    .csc-lead { font-size: 15px; color: #334155; line-height: 1.6; margin-bottom: 18px; }
    .csc-ad-slot { margin: 18px 0; text-align: center; min-height: 250px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #faf8f5; border: 1px dashed #cbd5e1; border-radius: 10px; padding: 8px; }
    .csc-ad-label { font-size: 10px; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
    .csc-btn-stack { display: flex; flex-direction: column; gap: 12px; margin: 20px 0; }
    .csc-cta-btn { display: flex; align-items: center; justify-content: space-between; width: 100%; background: #1e40af; color: #ffffff !important; font-size: 15px; font-weight: 800; text-transform: uppercase; padding: 16px 20px; border-radius: 12px; text-decoration: none; border: none; cursor: pointer; box-shadow: 0 4px 12px rgba(30, 64, 175, 0.25); transition: transform 0.15s ease, background 0.15s ease; text-align: left; }
    .csc-cta-btn:hover { background: #1e3a8a; transform: translateY(-2px); }
    .csc-cta-btn.green { background: #059669; box-shadow: 0 4px 12px rgba(5, 150, 105, 0.25); }
    .csc-cta-btn.green:hover { background: #047857; }
    .csc-cta-arrow { font-size: 20px; font-weight: 900; margin-left: 10px; }
    .csc-quiz-box { background: #f8fafc; border: 2px solid #cbd5e1; border-radius: 14px; padding: 20px; margin: 18px 0; }
    .csc-q-title { font-size: 17px; font-weight: 800; color: #0f172a; margin: 0 0 12px; }
    .csc-q-opt { display: block; width: 100%; text-align: left; background: #ffffff; border: 2px solid #cbd5e1; border-radius: 10px; padding: 13px 16px; margin-bottom: 10px; font-size: 15px; font-weight: 700; color: #1e293b; cursor: pointer; transition: all 0.15s; }
    .csc-q-opt:hover { border-color: #2563eb; background: #eff6ff; }
    .csc-modal-backdrop { position: fixed; inset: 0; background: rgba(15, 23, 42, 0.78); display: none; align-items: center; justify-content: center; z-index: 9999; padding: 16px; }
    .csc-modal-backdrop.active { display: flex; }
    .csc-modal { background: #ffffff; max-width: 420px; width: 100%; border-radius: 16px; padding: 28px 22px; text-align: center; box-shadow: 0 20px 40px rgba(0,0,0,0.3); }
    .csc-spinner { width: 48px; height: 48px; border: 5px solid #e2e8f0; border-top-color: #f59e0b; border-radius: 50%; animation: cscSpin 0.9s linear infinite; margin: 0 auto 16px; }
    @keyframes cscSpin { to { transform: rotate(360deg); } }
    .mdp-footer { max-width: 640px; margin: 0 auto 40px; padding: 0 16px; text-align: center; font-size: 12px; color: #64748b; }
    .mdp-footer a { color: #475569; }
  </style>
"""

# 1. Credit Cards Funnel P1 (/us-credit-cards-csc/index.html)
p1_cards = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>2026 U.S. Cash-Back &amp; 0% Intro APR Credit Cards Guide | My Dollar Pilot</title>
  <meta name="description" content="Compare 2026 U.S. no-annual-fee cash-back credit cards, 0% intro APR balance transfer options, and soft-pull pre-qualification guidelines.">
  <meta name="robots" content="noindex, nofollow">
  <meta name="google-adsense-account" content="{ca_pub}">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ca_pub}" crossorigin="anonymous"></script>
  {DYNAMIC_PIXEL_AND_UTM_SCRIPT}
  {FUNNEL_STYLE}
</head>
<body>
  <header class="mdp-header">
    <div class="mdp-header-inner">
      <a href="/" class="mdp-brand">My Dollar <em>Pilot</em></a>
      <nav class="mdp-nav">
        <a href="/credit/">Credit</a>
        <a href="/calculators/">Calculators</a>
        <a href="/about/">About</a>
      </nav>
    </div>
  </header>

  <main class="csc-wrap">
    <article class="csc-card">
      <span class="csc-badge">U.S. Consumer Credit Desk • 2026 Guide</span>
      <h1 class="csc-title">How to Qualify for $0-Annual-Fee Cash-Back &amp; 0% Intro APR Cards in the U.S.</h1>
      <p class="csc-lead">With average U.S. credit card interest rates above 21% APR according to Federal Reserve G.19 data, matching your credit tier to a 0% Intro APR or 2%–5% cash-back card can save over $1,400 per year.</p>

      <!-- AD SLOT #1: TOP ABOVE QUIZ & BUTTONS -->
      <div id="mdp_top_slot" class="csc-ad-slot">
        <span class="csc-ad-label">Advertisement</span>
        <ins class="adsbygoogle" style="display:block; width:100%; min-height:250px;" data-ad-client="{ca_pub}" data-ad-format="rectangle" data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
      </div>

      <!-- INTERACTIVE 3-STEP QUIZ -->
      <div class="csc-quiz-box" id="cscQuizBox">
        <div id="qStep1">
          <p style="font-size:12px; font-weight:800; color:#1e40af; text-transform:uppercase; margin:0 0 6px;">Step 1 of 3 • Card Priority</p>
          <h2 class="csc-q-title">1. Which card benefit is your top priority for 2026?</h2>
          <button class="csc-q-opt" onclick="nextQ(2)">➡️ 2% to 5% Cash Back on Groceries, Gas &amp; Bills</button>
          <button class="csc-q-opt" onclick="nextQ(2)">➡️ 0% Intro APR for 15–21 Months (Balance Transfer)</button>
          <button class="csc-q-opt" onclick="nextQ(2)">➡️ Credit Building / No Annual Fee ($0/yr)</button>
        </div>
        <div id="qStep2" style="display:none;">
          <p style="font-size:12px; font-weight:800; color:#1e40af; text-transform:uppercase; margin:0 0 6px;">Step 2 of 3 • FICO Score Tier</p>
          <h2 class="csc-q-title">2. What is your estimated FICO credit score range?</h2>
          <button class="csc-q-opt" onclick="nextQ(3)">➡️ Good to Excellent (670 – 850)</button>
          <button class="csc-q-opt" onclick="nextQ(3)">➡️ Fair / Average (580 – 669)</button>
          <button class="csc-q-opt" onclick="nextQ(3)">➡️ Building or Rebuilding Credit (&lt; 580)</button>
        </div>
        <div id="qStep3" style="display:none;">
          <p style="font-size:12px; font-weight:800; color:#1e40af; text-transform:uppercase; margin:0 0 6px;">Step 3 of 3 • Soft-Pull Check</p>
          <h2 class="csc-q-title">3. Do you want to check eligibility via soft pull (no impact to credit score)?</h2>
          <button class="csc-q-opt" onclick="triggerPreloader('/us-credit-cards-results/?lead=1#goog_rewarded')">➡️ Yes, show soft-pull pre-qualification options</button>
          <button class="csc-q-opt" onclick="triggerPreloader('/us-credit-cards-results/?lead=1#goog_rewarded')">➡️ Compare all 2026 card categories &amp; limits</button>
        </div>
      </div>

      <!-- STACKED HIGH-INTENT BUTTONS (FORMONEY P1 -> P2 PATTERN) -->
      <div class="csc-btn-stack">
        <a id="btn-reward01" href="/us-credit-cards-results/?lead=1#goog_rewarded" class="csc-cta-btn">
          <span>CONTINUE TO SEE THE CARDS &amp; LIMITS</span>
          <span class="csc-cta-arrow">&rarr;</span>
        </a>
        <a id="btn-reward02" href="/us-credit-cards-results/?lead=1#goog_rewarded" class="csc-cta-btn green">
          <span>CHECK IF YOU QUALIFY (SOFT CREDIT PULL)</span>
          <span class="csc-cta-arrow">&rarr;</span>
        </a>
        <a id="btn-reward03" href="/us-credit-cards-results/?lead=1#goog_rewarded" class="csc-cta-btn">
          <span>COMPARE 0% INTRO APR &amp; CASH-BACK TIERS</span>
          <span class="csc-cta-arrow">&rarr;</span>
        </a>
      </div>

      <!-- AD SLOT #2: BELOW BUTTONS -->
      <div id="mdp_content_1_slot" class="csc-ad-slot">
        <span class="csc-ad-label">Advertisement</span>
        <ins class="adsbygoogle" style="display:block; width:100%; min-height:250px;" data-ad-client="{ca_pub}" data-ad-format="rectangle" data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
      </div>

      <h2 style="font-size:20px; font-weight:800; color:#0f172a; margin:22px 0 10px;">How Soft-Pull Credit Pre-Qualification Works</h2>
      <p class="csc-lead">Most major U.S. banks offer pre-qualification tools that run a soft inquiry on your Equifax, Experian, or TransUnion profile. A soft pull lets you view estimated APRs and credit limits before submitting a formal application, with zero effect on your FICO score.</p>

      <!-- AD SLOT #3: BOTTOM -->
      <div id="mdp_content_2_slot" class="csc-ad-slot">
        <span class="csc-ad-label">Advertisement</span>
        <ins class="adsbygoogle" style="display:block; width:100%; min-height:250px;" data-ad-client="{ca_pub}" data-ad-format="rectangle" data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
      </div>

      <div class="csc-btn-stack">
        <a id="btn-reward04" href="/us-credit-cards-results/?lead=1#goog_rewarded" class="csc-cta-btn green">
          <span>VIEW 2026 APPROVAL REQUIREMENTS &amp; CARDS</span>
          <span class="csc-cta-arrow">&rarr;</span>
        </a>
      </div>
    </article>
  </main>

  <!-- PRE-LOADER MODAL GATE -->
  <div class="csc-modal-backdrop" id="cscModal">
    <div class="csc-modal">
      <div id="modalLoadingState">
        <div class="csc-spinner"></div>
        <h3 id="modalPhrase" style="font-size:19px; font-weight:800; color:#0f172a; margin:0 0 6px;">Analysing your information...</h3>
        <p style="font-size:14px; color:#64748b; margin:0;">Comparing 2026 U.S. card tiers and APR criteria</p>
      </div>
      <div id="modalReadyState" style="display:none;">
        <div style="width:48px; height:48px; border-radius:50%; background:#dcfce7; color:#059669; display:flex; align-items:center; justify-content:center; font-size:24px; font-weight:900; margin:0 auto 14px;">✓</div>
        <h3 style="font-size:21px; font-weight:800; color:#0f172a; margin:0 0 8px;">Alright, we've found the result.</h3>
        <p style="font-size:14px; color:#475569; margin:0 0 18px;">Click below to view the complete 2026 credit card comparison and payoff calculators.</p>
        <a id="modalContinueBtn" href="/us-credit-cards-results/?lead=1#goog_rewarded" class="csc-cta-btn" style="justify-content:center; background:#2e2eb8;">
          <span>CONTINUE TO RESULTS &rarr;</span>
        </a>
      </div>
    </div>
  </div>

  <footer class="mdp-footer">
    <p>&copy; 2026 My Dollar Pilot. General educational information, not individualized financial advice. • <a href="/privacy/">Privacy Policy</a> • <a href="/disclaimer/">Disclaimer</a> • <a href="/how-we-make-money/">Advertising Disclosure</a></p>
  </footer>

  <script>
    function nextQ(step) {{
      document.getElementById('qStep1').style.display = 'none';
      document.getElementById('qStep2').style.display = 'none';
      document.getElementById('qStep3').style.display = 'none';
      document.getElementById('qStep' + step).style.display = 'block';
    }}
    function triggerPreloader(targetHref) {{
      var modal = document.getElementById('cscModal');
      var phrase = document.getElementById('modalPhrase');
      var loading = document.getElementById('modalLoadingState');
      var ready = document.getElementById('modalReadyState');
      var btn = document.getElementById('modalContinueBtn');
      var search = window.location.search;
      if (search && search.length > 1) {{
        var extra = search.substring(1);
        targetHref = targetHref.replace('?lead=1', '?lead=1&' + extra);
      }}
      btn.setAttribute('href', targetHref);
      modal.classList.add('active');
      setTimeout(function() {{ phrase.textContent = 'Comparing data...'; }}, 750);
      setTimeout(function() {{
        loading.style.display = 'none';
        ready.style.display = 'block';
      }}, 1500);
    }}
  </script>
</body>
</html>
"""

# 2. Credit Cards Funnel P2 (/us-credit-cards-results/index.html)
p2_cards = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>2026 U.S. Credit Card Categories &amp; Pre-Qualification Steps | My Dollar Pilot</title>
  <meta name="description" content="Review the top 2026 U.S. cash-back, 0% intro APR, and credit-builder card categories and calculate your interest savings.">
  <meta name="robots" content="noindex, nofollow">
  <meta name="google-adsense-account" content="{ca_pub}">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ca_pub}" crossorigin="anonymous"></script>
  {DYNAMIC_PIXEL_AND_UTM_SCRIPT}
  {FUNNEL_STYLE}
</head>
<body>
  <header class="mdp-header">
    <div class="mdp-header-inner">
      <a href="/" class="mdp-brand">My Dollar <em>Pilot</em></a>
      <nav class="mdp-nav">
        <a href="/credit/">Credit</a>
        <a href="/calculators/">Calculators</a>
        <a href="/about/">About</a>
      </nav>
    </div>
  </header>

  <main class="csc-wrap">
    <article class="csc-card">
      <span class="csc-badge">Step 2 of 2 • U.S. Card Comparison Results</span>
      <h1 class="csc-title">What Credit Cards Can You Get Approved For in 2026?</h1>
      <p class="csc-lead">Based on your selection, review the three main U.S. credit card categories below and run your exact numbers in our non-incentivized payoff and APR calculators.</p>

      <!-- P2 AD SLOT #1: TOP -->
      <div id="p2_top_slot" class="csc-ad-slot">
        <span class="csc-ad-label">Advertisement</span>
        <ins class="adsbygoogle" style="display:block; width:100%; min-height:250px;" data-ad-client="{ca_pub}" data-ad-format="rectangle" data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
      </div>

      <div style="border:2px solid #059669; background:#f0fdf4; border-radius:12px; padding:18px; margin:18px 0;">
        <span style="font-size:11px; font-weight:800; color:#059669; text-transform:uppercase;">Option 1 • 0% Intro APR &amp; Cash-Back Cards (670+ FICO)</span>
        <h2 style="font-size:19px; font-weight:800; color:#0f172a; margin:6px 0;">No-Annual-Fee 2%–5% Cash-Back &amp; Balance Transfer Cards</h2>
        <p style="font-size:14px; color:#334155; margin:0 0 12px;">Compare how a 15-to-21-month 0% Intro APR balance transfer stacks up against standard 21%+ credit card interest rates.</p>
        <a href="/calculators/credit-card-payoff/" class="csc-cta-btn green" style="justify-content:center;">
          <span>OPEN CREDIT CARD PAYOFF CALCULATOR &rarr;</span>
        </a>
      </div>

      <!-- P2 AD SLOT #2: MID -->
      <div id="p2_content_1_slot" class="csc-ad-slot">
        <span class="csc-ad-label">Advertisement</span>
        <ins class="adsbygoogle" style="display:block; width:100%; min-height:250px;" data-ad-client="{ca_pub}" data-ad-format="rectangle" data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
      </div>

      <div style="border:2px solid #1e40af; background:#eff6ff; border-radius:12px; padding:18px; margin:18px 0;">
        <span style="font-size:11px; font-weight:800; color:#1e40af; text-transform:uppercase;">Option 2 • Understanding Credit Card APR &amp; Minimum Payments</span>
        <h2 style="font-size:19px; font-weight:800; color:#0f172a; margin:6px 0;">How Issuers Calculate Your Monthly Interest &amp; Grace Period</h2>
        <p style="font-size:14px; color:#334155; margin:0 0 12px;">See the exact CFPB and Federal Reserve rules governing credit card grace periods, trailing interest, and balance transfer fees.</p>
        <a href="/guides/credit-card-balance-transfer/" class="csc-cta-btn" style="justify-content:center;">
          <span>READ 0% BALANCE TRANSFER &amp; APR GUIDE &rarr;</span>
        </a>
      </div>

      <!-- P2 AD SLOT #3: BOTTOM -->
      <div id="p2_content_2_slot" class="csc-ad-slot">
        <span class="csc-ad-label">Advertisement</span>
        <ins class="adsbygoogle" style="display:block; width:100%; min-height:250px;" data-ad-client="{ca_pub}" data-ad-format="rectangle" data-full-width-responsive="true"></ins>
        <script>(adsbygoogle = window.adsbygoogle || []).push({{}});</script>
      </div>

      <div style="border:1px solid #cbd5e1; background:#f8fafc; border-radius:12px; padding:18px; margin:18px 0;">
        <h3 style="font-size:17px; font-weight:800; color:#0f172a; margin:0 0 8px;">Compare Auto Loan &amp; High-Yield Savings Rates</h3>
        <p style="font-size:14px; color:#475569; margin:0 0 12px;">Looking to finance a vehicle or park emergency cash in an FDIC-insured High-Yield Savings Account? Use our live calculators below.</p>
        <a href="/calculators/auto-loan/" class="csc-cta-btn" style="background:#334155; justify-content:center;">
          <span>COMPARE AUTO LOAN MONTHLY PAYMENTS &rarr;</span>
        </a>
      </div>
    </article>
  </main>

  <footer class="mdp-footer">
    <p>&copy; 2026 My Dollar Pilot. General educational information, not individualized financial advice. • <a href="/privacy/">Privacy Policy</a> • <a href="/disclaimer/">Disclaimer</a> • <a href="/how-we-make-money/">Advertising Disclosure</a></p>
  </footer>
</body>
</html>
"""

for folder, content in [
    ('us-credit-cards-csc', p1_cards),
    ('us-credit-cards-results', p2_cards),
]:
    target_dir = os.path.join(pub_root, folder)
    os.makedirs(target_dir, exist_ok=True)
    with open(os.path.join(target_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(content)

print("Created /us-credit-cards-csc/ and /us-credit-cards-results/ in portal-eua/public!")

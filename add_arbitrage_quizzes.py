import os
import zipfile
import urllib.request
import urllib.parse
import base64

base = r'C:\Users\mateu\Projects\lab-ia\staging_rewardedtasks_br'
pub_id = 'pub-3266587888704229'
ca_pub = f'ca-{pub_id}'

# 1. US English Eligibility Micro-Quiz (Ready for US Paid Traffic -> CPA SOI / Media.net / AdSense)
us_quiz_html = f"""<!DOCTYPE html>
<html lang="en-US">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>2026 US Rewards & Cashback Eligibility Finder — RewardedTasks</title>
  <meta name="description" content="Answer 3 quick questions to match your profile with verified 2026 US cash-back apps, paid market research panels, and zero-fee financial tools.">
  <link rel="canonical" href="https://rewardedtasks.com/us-rewards.html">
  <link rel="stylesheet" href="/css/style.css">
  <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={ca_pub}" crossorigin="anonymous"></script>
  <style>
    .quiz-card {{ max-width: 680px; margin: 36px auto; background: #fff; border: 1px solid #e2e8f0; border-radius: 16px; padding: 32px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.06); }}
    .quiz-step {{ display: none; }}
    .quiz-step.active {{ display: block; }}
    .quiz-progress {{ height: 8px; background: #e2e8f0; border-radius: 99px; overflow: hidden; margin-bottom: 24px; }}
    .quiz-progress-bar {{ height: 100%; background: #10b981; width: 33%; transition: width 0.3s ease; }}
    .quiz-btn {{ display: block; width: 100%; text-align: left; padding: 16px 20px; margin-bottom: 14px; background: #f8fafc; border: 2px solid #cbd5e1; border-radius: 12px; font-size: 16px; font-weight: 700; color: #0f172a; cursor: pointer; transition: all 0.2s; }}
    .quiz-btn:hover {{ border-color: #10b981; background: #ecfdf5; transform: translateY(-1px); }}
    .offer-box {{ border: 2px solid #10b981; background: #f0fdf4; border-radius: 12px; padding: 20px; margin-bottom: 18px; }}
    .offer-cta {{ display: inline-block; width: 100%; text-align: center; background: #10b981; color: #fff !important; font-weight: 800; padding: 14px 20px; border-radius: 10px; margin-top: 12px; font-size: 16px; text-decoration: none; }}
  </style>
</head>
<body>
  <header class="site-header">
    <div class="container header-inner">
      <div class="logo-area">
        <a href="/" style="display:flex; align-items:center; gap:12px;">
          <div class="logo-badge">RT</div>
          <div class="logo-text">Rewarded<span>Tasks</span> <small style="font-size:12px; font-weight:600; color:#10b981; border:1px solid #10b981; padding:2px 6px; border-radius:4px; margin-left:4px;">US EDITION</small></div>
        </a>
      </div>
      <nav class="main-nav">
        <a href="/">Home</a>
        <a href="/sobre.html">About</a>
        <a href="/privacidade.html">Privacy</a>
        <a href="/contato.html" class="btn-nav">Contact</a>
      </nav>
    </div>
  </header>

  <main class="container" style="padding: 20px 16px 60px;">
    <div class="quiz-card">
      <span class="category-tag">2026 Interactive Finder</span>
      <h1 style="font-size: 26px; font-weight: 800; color: #0f172a; margin: 10px 0 12px;">Find Verified US Cash-Back & Micro-Task Platforms for Your Profile</h1>
      <p style="font-size: 15px; color: #475569; margin-bottom: 20px;">Answer 3 quick questions below (takes 15 seconds) to see which verified platforms match your device and payout preference.</p>

      <div class="quiz-progress">
        <div class="quiz-progress-bar" id="qBar"></div>
      </div>

      <!-- STEP 1 -->
      <div class="quiz-step active" id="step1">
        <h2 style="font-size: 19px; font-weight: 700; margin-bottom: 16px;">1. Which device do you primarily use?</h2>
        <button class="quiz-btn" onclick="nextStep(2, 66)">📱 Android Smartphone</button>
        <button class="quiz-btn" onclick="nextStep(2, 66)">🍎 iPhone / iOS Device</button>
        <button class="quiz-btn" onclick="nextStep(2, 66)">💻 Desktop / Laptop Computer</button>
      </div>

      <!-- STEP 2 -->
      <div class="quiz-step" id="step2">
        <h2 style="font-size: 19px; font-weight: 700; margin-bottom: 16px;">2. What is your preferred payout method?</h2>
        <button class="quiz-btn" onclick="nextStep(3, 90)">💵 PayPal Cash / Direct Bank Deposit</button>
        <button class="quiz-btn" onclick="nextStep(3, 90)">🎁 Amazon / Visa Prepaid Gift Cards</button>
        <button class="quiz-btn" onclick="nextStep(3, 90)">💳 Cash-Back on Everyday Shopping & Credit</button>
      </div>

      <!-- STEP 3 -->
      <div class="quiz-step" id="step3">
        <h2 style="font-size: 19px; font-weight: 700; margin-bottom: 16px;">3. How much spare time do you have per day?</h2>
        <button class="quiz-btn" onclick="nextStep(4, 100)">⏱️ 15 to 30 minutes a day</button>
        <button class="quiz-btn" onclick="nextStep(4, 100)">⚡ 30 to 60 minutes a day</button>
        <button class="quiz-btn" onclick="nextStep(4, 100)">🚀 1+ hour a day (Remote Freelance & Surveys)</button>
      </div>

      <!-- STEP 4: RESULTS -->
      <div class="quiz-step" id="step4">
        <h2 style="font-size: 22px; font-weight: 800; color: #059669; margin-bottom: 12px;">✓ 3 Verified Matches Found for Your Profile</h2>
        <p style="font-size: 14px; color: #475569; margin-bottom: 20px;">Based on your answers, here are our highest-rated platforms and complete editorial guides:</p>

        <div class="offer-box">
          <span style="font-size:12px; font-weight:800; color:#059669; text-transform:uppercase;">Match #1 • Instant Payouts & Market Research</span>
          <h3 style="font-size:18px; font-weight:800; margin:6px 0;">Top 7 Verified Reward & Survey Apps (2026 Guide)</h3>
          <p style="font-size:14px; color:#334155; margin:0;">Compare Google Opinion Rewards, AttaPoll, YouGov, and Toluna minimum payout thresholds and safety rules.</p>
          <a href="/artigos/melhores-aplicativos-renda-extra-2026.html" class="offer-cta">Read Full Guide & Compare Platforms &rarr;</a>
        </div>

        <div class="offer-box" style="border-color:#0284c7; background:#f0f9ff;">
          <span style="font-size:12px; font-weight:800; color:#0284c7; text-transform:uppercase;">Match #2 • Zero-Fee Cashback Credit Cards</span>
          <h3 style="font-size:18px; font-weight:800; margin:6px 0;">Best No-Annual-Fee Cashback Cards & Credit Score Tips</h3>
          <p style="font-size:14px; color:#334155; margin:0;">See how to earn 1% to 5% cash back on groceries and bills while building your credit score safely.</p>
          <a href="/artigos/melhores-cartoes-de-credito-sem-anuidade-com-cashback.html" class="offer-cta" style="background:#0284c7;">Compare Cash-Back Cards &rarr;</a>
        </div>

        <div class="offer-box" style="border-color:#4f46e5; background:#eef2ff;">
          <span style="font-size:12px; font-weight:800; color:#4f46e5; text-transform:uppercase;">Match #3 • Remote Freelance Platforms</span>
          <h3 style="font-size:18px; font-weight:800; margin:6px 0;">Verified Work-From-Home & Freelance Marketplaces</h3>
          <p style="font-size:14px; color:#334155; margin:0;">Step-by-step guide to escrow-protected freelance platforms paying in USD.</p>
          <a href="/artigos/trabalho-remoto-melhores-sites-para-freelancers-iniciantes.html" class="offer-cta" style="background:#4f46e5;">Explore Remote Work Guide &rarr;</a>
        </div>
      </div>
    </div>
  </main>

  <script>
    function nextStep(stepNum, pct) {{
      document.querySelectorAll('.quiz-step').forEach(function(el) {{ el.classList.remove('active'); }});
      document.getElementById('step' + stepNum).classList.add('active');
      document.getElementById('qBar').style.width = pct + '%';
      window.scrollTo({{ top: 0, behavior: 'smooth' }});
    }}
  </script>
</body>
</html>
"""

with open(os.path.join(base, 'us-rewards.html'), 'w', encoding='utf-8') as f:
    f.write(us_quiz_html)

# Repackage ZIP and update dpaste command
zip_path = r'C:\Users\mateu\Projects\lab-ia\pacotes-prontos-hostinger\PACOTE-2-REWARDEDTASKS-ADSENSE-BR.zip'
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(base):
        for file in files:
            full_path = os.path.join(root, file)
            arcname = os.path.relpath(full_path, base)
            zipf.write(full_path, arcname)

print("Created us-rewards.html and repackaged ZIP!")

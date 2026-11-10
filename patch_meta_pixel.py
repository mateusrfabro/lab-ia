import os

buzz2_dir = r"C:\Users\mateu\Downloads\Projeto Dudu\Buzz 2.0"

# 1. Update build_buzz2_pages.py
pages_py_path = os.path.join(buzz2_dir, "build_buzz2_pages.py")
with open(pages_py_path, "r", encoding="utf-8") as f:
    text = f.read()

pixel_js_addition = """
  // ============================================================================
  // META PIXEL (1510786527551026) FUNNEL & OUTBOUND CONVERSION TRACKING
  // ============================================================================
  try {
    var pName = window.location.pathname.toLowerCase();
    if (window.fbq) {
      if (pName.indexOf('/simulador/etapa-1') !== -1) {
        fbq('track', 'ViewContent', { content_name: 'Simulador Etapa 1', content_category: 'Quiz' });
        fbq('trackCustom', 'QuizStep1');
      } else if (pName.indexOf('/simulador/etapa-2') !== -1) {
        fbq('trackCustom', 'QuizStep2');
      } else if (pName.indexOf('/simulador/etapa-3') !== -1) {
        fbq('trackCustom', 'QuizStep3');
      } else if (pName.indexOf('/simulador/analise') !== -1) {
        fbq('trackCustom', 'QuizAnalyzing');
      } else if (pName.indexOf('/simulador/resultado') !== -1) {
        fbq('track', 'Lead', { content_name: 'Simulador Resultado Final', content_category: 'Conversao' });
        fbq('trackCustom', 'QuizComplete');
      }
    }

    document.addEventListener('click', function(e) {
      var btn = e.target.closest('.nw-cta-btn, .btn-quiz, .nw-table-cta, a[target="_blank"]');
      if (btn && window.fbq) {
        var cardEl = btn.closest('.nw-card, tr, .hero-micro-quiz, .sim-question-card');
        var cardTitle = '';
        if (cardEl) {
          var tEl = cardEl.querySelector('.nw-card-title, strong, h1, h2, h3, h4');
          if (tEl) cardTitle = tEl.textContent.trim();
        }
        fbq('track', 'InitiateCheckout', {
          content_name: cardTitle || btn.textContent.trim(),
          content_category: 'Afiliado Cartao'
        });
      }
    });
  } catch (err) {
    console.warn('Pixel tracking notice:', err);
  }
"""

target_end_iife = "  }\n})();\n\"\"\""
replacement_end_iife = "  }" + pixel_js_addition + "\n})();\n\"\"\""

if target_end_iife in text:
    text = text.replace(target_end_iife, replacement_end_iife, 1)
    with open(pages_py_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("build_buzz2_pages.py atualizado com sucesso!")
else:
    print("AVISO: target_end_iife não encontrado em build_buzz2_pages.py")

# 2. Update generate_all_html.py with Meta Pixel <head> tag
html_py_path = os.path.join(buzz2_dir, "generate_all_html.py")
with open(html_py_path, "r", encoding="utf-8") as f:
    html_py = f.read()

pixel_head_tag = """  <!-- Meta Pixel Code -->
  <script>
  !function(f,b,e,v,n,t,s)
  {{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?
  n.callMethod.apply(n,arguments):n.queue.push(arguments)}};
  if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
  n.queue=[];t=b.createElement(e);t.async=!0;
  t.src=v;s=b.getElementsByTagName(e)[0];
  s.parentNode.insertBefore(t,s)}}(window, document,'script',
  'https://connect.facebook.net/en_US/fbevents.js');
  fbq('init', '1510786527551026');
  fbq('track', 'PageView');
  </script>
  <noscript><img height="1" width="1" style="display:none"
  src="https://www.facebook.com/tr?id=1510786527551026&ev=PageView&noscript=1"
  /></noscript>
  <!-- End Meta Pixel Code -->
"""

adsense_tag = '<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-{PUB_ID}" crossorigin="anonymous"></script>'
replacement_head = adsense_tag + "\n" + pixel_head_tag

if adsense_tag in html_py and "1510786527551026" not in html_py:
    html_py = html_py.replace(adsense_tag, replacement_head, 1)
    with open(html_py_path, "w", encoding="utf-8") as f:
        f.write(html_py)
    print("generate_all_html.py atualizado com a tag Meta Pixel!")
else:
    print("AVISO: generate_all_html.py já tem o pixel ou adsense_tag não bateu")

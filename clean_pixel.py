import re

clean_pixel_block = """  <!-- Meta Pixel Code (Aguardando Pixel Novo do Dudu) -->
  <script>
    window.META_PIXEL_ID = ""; // O Dudu vai preencher com o Pixel NOVO
    if (window.META_PIXEL_ID && window.META_PIXEL_ID.trim() !== '') {
      !function(f,b,e,v,n,t,s)
      {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
      n.callMethod.apply(n,arguments):n.queue.push(arguments)};
      if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
      n.queue=[];t=b.createElement(e);t.async=!0;
      t.src=v;s=b.getElementsByTagName(e)[0];
      s.parentNode.insertBefore(t,s)}(window, document,'script',
      'https://connect.facebook.net/en_US/fbevents.js');
      fbq('init', window.META_PIXEL_ID);
      fbq('track', 'PageView');
    }
  </script>"""

pattern = re.compile(r"<!-- Meta Pixel Code.*?<\/noscript>", re.DOTALL)

for fname in [r'C:\Users\mateu\Projects\lab-ia\staging_spotify\offer.html', r'C:\Users\mateu\Projects\lab-ia\staging_spotify\chat.html']:
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = pattern.sub(clean_pixel_block, content)
    
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Atualizado com bloco de pixel seguro:", fname)

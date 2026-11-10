import os

base = r'C:\Users\mateu\Projects\lab-ia\staging_rewardedtasks_br'

home_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>RewardedTasks Brasil — Guia de Aplicativos, Renda Extra e Finanças</title>
  <meta name="description" content="O maior portal brasileiro sobre aplicativos de tarefas, educação financeira, economia digital e segurança na internet. Dicas práticas e análises 100% verificadas.">
  <link rel="canonical" href="https://rewardedtasks.com/">
  <link rel="stylesheet" href="/css/style.css">
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%2310b981'><path d='M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5'/></svg>">
  
  <!-- Schema.org WebSite & Organization -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "RewardedTasks Brasil",
    "url": "https://rewardedtasks.com/",
    "potentialAction": {
      "@type": "SearchAction",
      "target": "https://rewardedtasks.com/?s={search_term_string}",
      "query-input": "required name=search_term_string"
    }
  }
  </script>
  <!-- Google AdSense Placeholder Script -->
  <!-- <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX" crossorigin="anonymous"></script> -->
</head>
<body>

  <!-- Header -->
  <header class="site-header">
    <div class="container header-inner">
      <div class="logo-area">
        <a href="/" style="display:flex; align-items:center; gap:12px;">
          <div class="logo-badge">RT</div>
          <div class="logo-text">Rewarded<span>Tasks</span> <small style="font-size:12px; font-weight:600; color:#10b981; border:1px solid #10b981; padding:2px 6px; border-radius:4px; margin-left:4px;">BRASIL</small></div>
        </a>
      </div>
      <nav class="main-nav">
        <a href="/" class="active">Início</a>
        <a href="/artigos/melhores-aplicativos-renda-extra-2026.html">Apps & Renda Extra</a>
        <a href="/artigos/como-organizar-financas-pessoais-planilha-gratis.html">Finanças</a>
        <a href="/artigos/seguranca-digital-como-identificar-golpes-na-internet.html">Segurança</a>
        <a href="/sobre.html">Quem Somos</a>
        <a href="/contato.html" class="btn-nav">Contato</a>
      </nav>
      <button class="mobile-toggle" aria-label="Abrir Menu">☰</button>
    </div>
  </header>

  <!-- Top Ad Slot -->
  <div class="container">
    <div class="ad-slot leaderboard">
      <span>Espaço Publicitário - Google AdSense (728x90 / 320x100)</span>
    </div>
  </div>

  <!-- Hero Featured Section -->
  <section class="hero-section">
    <div class="container">
      <div class="hero-grid">
        <!-- Main Featured Card -->
        <a href="/artigos/melhores-aplicativos-renda-extra-2026.html" class="featured-card">
          <div class="featured-img-wrap">
            <img src="https://images.unsplash.com/photo-1559526324-4b87b5e36e44?auto=format&fit=crop&w=1200&q=80" alt="Melhores Aplicativos Renda Extra 2026">
          </div>
          <div class="featured-content">
            <span class="category-tag">Destaque da Semana</span>
            <h2 class="featured-title">Os 7 Melhores Aplicativos Confiáveis para Fazer Renda Extra no Celular em 2026</h2>
            <p class="featured-desc">Passamos 30 dias testando dezenas de ferramentas móveis. Veja quais plataformas realmente pagam via PIX e PayPal e aprenda a fugir dos golpes mais comuns.</p>
            <div class="meta-info">
              <span>Por Lucas Silveira</span>
              <span class="dot"></span>
              <span>15 Jan 2026</span>
              <span class="dot"></span>
              <span>7 min de leitura</span>
            </div>
          </div>
        </a>

        <!-- Secondary Side Posts -->
        <div class="hero-secondary">
          <a href="/artigos/como-organizar-financas-pessoais-planilha-gratis.html" class="side-post-card">
            <div class="side-post-img">
              <img src="https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?auto=format&fit=crop&w=400&q=80" alt="Organização Financeira">
            </div>
            <div class="side-post-info">
              <span class="category-tag" style="font-size:10px; margin-bottom:6px;">Finanças Pessoais</span>
              <h3 class="side-post-title">Guia Prático: Como Organizar suas Finanças Pessoais do Zero e Começar a Poupar</h3>
              <div class="meta-info" style="font-size:11px;">
                <span>22 Jan 2026</span>
                <span class="dot"></span>
                <span>8 min</span>
              </div>
            </div>
          </a>

          <a href="/artigos/seguranca-digital-como-identificar-golpes-na-internet.html" class="side-post-card">
            <div class="side-post-img">
              <img src="https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=400&q=80" alt="Segurança Digital">
            </div>
            <div class="side-post-info">
              <span class="category-tag" style="font-size:10px; margin-bottom:6px; background:#fee2e2; color:#b91c1c;">Alerta de Segurança</span>
              <h3 class="side-post-title">Segurança Digital: 5 Sinais Cruciais para Identificar e Evitar Golpes na Internet</h3>
              <div class="meta-info" style="font-size:11px;">
                <span>28 Jan 2026</span>
                <span class="dot"></span>
                <span>6 min</span>
              </div>
            </div>
          </a>
        </div>
      </div>
    </div>
  </section>

  <!-- Mid Ad Slot -->
  <div class="container">
    <div class="ad-slot leaderboard">
      <span>Espaço Publicitário - Google AdSense (In-Feed Responsive)</span>
    </div>
  </div>

  <!-- Main Content & Sidebar -->
  <main class="main-layout">
    <div class="container layout-grid">
      <!-- Latest Articles -->
      <section>
        <div class="section-header">
          <h2 class="section-title">Últimas Publicações</h2>
          <span style="font-size:13px; font-weight:600; color:#10b981;">Atualizado Diariamente</span>
        </div>

        <div class="articles-grid">
          <!-- Article Card 1 -->
          <a href="/artigos/plataformas-pesquisas-remuneradas-valem-a-pena.html" class="article-card">
            <div class="article-thumb">
              <img src="https://images.unsplash.com/photo-1434626881859-194d67b2b86f?auto=format&fit=crop&w=600&q=80" alt="Pesquisas Remuneradas">
            </div>
            <div class="article-body">
              <span class="category-tag">Apps & Renda Extra</span>
              <h3 class="article-title">Pesquisas Remuneradas na Internet Valem a Pena? Testamos as Principais</h3>
              <p class="article-excerpt">Separamos o mito da realidade sobre ganhos reais respondendo questionários de mercado online.</p>
              <div class="meta-info">
                <span>02 Fev 2026</span>
                <span class="dot"></span>
                <span>7 min</span>
              </div>
            </div>
          </a>

          <!-- Article Card 2 -->
          <a href="/artigos/trabalho-remoto-melhores-sites-para-freelancers-iniciantes.html" class="article-card">
            <div class="article-thumb">
              <img src="https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=600&q=80" alt="Trabalho Remoto">
            </div>
            <div class="article-body">
              <span class="category-tag">Carreira & Renda</span>
              <h3 class="article-title">Trabalho Remoto em 2026: Os Melhores Sites para Freelancers Iniciantes</h3>
              <p class="article-excerpt">Onde encontrar projetos rápidos de redação, design, suporte e edição de vídeo recebendo em reais e dólares.</p>
              <div class="meta-info">
                <span>05 Fev 2026</span>
                <span class="dot"></span>
                <span>8 min</span>
              </div>
            </div>
          </a>

          <!-- Article Card 3 -->
          <a href="/artigos/melhores-cartoes-de-credito-sem-anuidade-com-cashback.html" class="article-card">
            <div class="article-thumb">
              <img src="https://images.unsplash.com/photo-1556742049-0a67e5572293?auto=format&fit=crop&w=600&q=80" alt="Cartões de Crédito">
            </div>
            <div class="article-body">
              <span class="category-tag">Finanças Pessoais</span>
              <h3 class="article-title">Comparativo: Os Melhores Cartões de Crédito Sem Anuidade com Cashback</h3>
              <p class="article-excerpt">Análise prática dos cartões digitais que devolvem dinheiro de verdade na conta sem pegadinhas contratuais.</p>
              <div class="meta-info">
                <span>08 Fev 2026</span>
                <span class="dot"></span>
                <span>6 min</span>
              </div>
            </div>
          </a>

          <!-- Article Card 4 (Re-featured) -->
          <a href="/artigos/como-organizar-financas-pessoais-planilha-gratis.html" class="article-card">
            <div class="article-thumb">
              <img src="https://images.unsplash.com/photo-1579621970563-ebec7560ff3e?auto=format&fit=crop&w=600&q=80" alt="Regra 50-30-20">
            </div>
            <div class="article-body">
              <span class="category-tag">Educação Financeira</span>
              <h3 class="article-title">Como Aplicar a Regra 50-30-20 no Salário Mínimo e Fazer Sobrar Dinheiro</h3>
              <p class="article-excerpt">A fórmula de Harvard adaptada para a realidade do consumidor brasileiro com dicas práticas de corte inteligente.</p>
              <div class="meta-info">
                <span>22 Jan 2026</span>
                <span class="dot"></span>
                <span>8 min</span>
              </div>
            </div>
          </a>
        </div>
      </section>

      <!-- Sidebar -->
      <aside class="sidebar-widgets">
        <!-- Sidebar Ad Slot -->
        <div class="ad-slot sidebar">
          <span>Espaço Publicitário - Google AdSense (300x250 / 300x600)</span>
        </div>

        <!-- Newsletter Widget -->
        <div class="widget widget-newsletter">
          <h3 class="widget-title">Boletim Semanal</h3>
          <p>Receba as melhores dicas de apps, renda extra e finanças diretamente no seu e-mail.</p>
          <form>
            <input type="email" placeholder="Seu melhor e-mail" required>
            <button type="submit">Quero Receber Dicas</button>
          </form>
        </div>

        <!-- About Portal Widget -->
        <div class="widget">
          <h3 class="widget-title">Sobre o Portal</h3>
          <p style="font-size:14px; line-height:1.6; color:#475569; margin-bottom:12px;">
            O <strong>RewardedTasks Brasil</strong> é um veículo editorial independente focado em educação digital, aplicativos e economia doméstica inteligente.
          </p>
          <a href="/sobre.html" style="color:#10b981; font-weight:700; font-size:13px;">Saiba mais sobre nós &rarr;</a>
        </div>

        <!-- Categories Widget -->
        <div class="widget">
          <h3 class="widget-title">Categorias</h3>
          <ul class="category-list">
            <li><a href="/artigos/melhores-aplicativos-renda-extra-2026.html">Apps & Renda Extra</a> <span class="count">8</span></li>
            <li><a href="/artigos/como-organizar-financas-pessoais-planilha-gratis.html">Finanças Pessoais</a> <span class="count">6</span></li>
            <li><a href="/artigos/seguranca-digital-como-identificar-golpes-na-internet.html">Segurança Digital</a> <span class="count">4</span></li>
            <li><a href="/artigos/trabalho-remoto-melhores-sites-para-freelancers-iniciantes.html">Trabalho Remoto</a> <span class="count">5</span></li>
          </ul>
        </div>
      </aside>
    </div>
  </main>

  <!-- Footer -->
  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-col">
          <div class="logo-area" style="margin-bottom:16px;">
            <div class="logo-badge">RT</div>
            <div class="logo-text" style="color:#fff;">Rewarded<span style="color:#10b981;">Tasks</span></div>
          </div>
          <p style="line-height:1.6; font-size:14px; margin-bottom:16px;">
            O portal brasileiro de referência em educação financeira, aplicativos de produtividade, microtarefas seguras e economia digital inteligente.
          </p>
          <p style="font-size:13px; color:#64748b;">CNPJ: 48.912.304/0001-82 • São Paulo - SP</p>
        </div>
        <div class="footer-col">
          <h4>Editorias</h4>
          <ul>
            <li><a href="/artigos/melhores-aplicativos-renda-extra-2026.html">Apps & Renda Extra</a></li>
            <li><a href="/artigos/como-organizar-financas-pessoais-planilha-gratis.html">Finanças Pessoais</a></li>
            <li><a href="/artigos/seguranca-digital-como-identificar-golpes-na-internet.html">Segurança na Web</a></li>
            <li><a href="/artigos/trabalho-remoto-melhores-sites-para-freelancers-iniciantes.html">Trabalho Remoto</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Institucional</h4>
          <ul>
            <li><a href="/sobre.html">Quem Somos</a></li>
            <li><a href="/contato.html">Fale Conosco</a></li>
            <li><a href="/privacidade.html">Política de Privacidade</a></li>
            <li><a href="/termos.html">Termos de Uso</a></li>
            <li><a href="/aviso-legal.html">Aviso Legal</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Transparência</h4>
          <p style="font-size:13px; line-height:1.6; color:#94a3b8; margin-bottom:12px;">
            Nosso conteúdo é puramente informativo e educacional. Não realizamos consultoria de investimentos nem garantimos promessas de lucros rápidos.
          </p>
          <div style="background:#1e293b; padding:10px 14px; border-radius:8px; font-size:12px; color:#10b981; font-weight:600;">
            ✓ Conteúdo Auditado e Conforme LGPD
          </div>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; <span class="current-year">2026</span> RewardedTasks Brasil. Todos os direitos reservados.</p>
        <p>Desenvolvido para máxima velocidade e conformidade com o Google AdSense.</p>
      </div>
    </div>
  </footer>

  <script src="/js/main.js"></script>
</body>
</html>
"""

with open(os.path.join(base, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(home_html)
print('Created index.html')

# SITEMAP.XML
sitemap_xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://rewardedtasks.com/</loc>
    <lastmod>2026-02-10</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://rewardedtasks.com/artigos/melhores-aplicativos-renda-extra-2026.html</loc>
    <lastmod>2026-02-10</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://rewardedtasks.com/artigos/como-organizar-financas-pessoais-planilha-gratis.html</loc>
    <lastmod>2026-02-10</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>
  <url>
    <loc>https://rewardedtasks.com/artigos/seguranca-digital-como-identificar-golpes-na-internet.html</loc>
    <lastmod>2026-02-10</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://rewardedtasks.com/artigos/plataformas-pesquisas-remuneradas-valem-a-pena.html</loc>
    <lastmod>2026-02-10</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://rewardedtasks.com/artigos/trabalho-remoto-melhores-sites-para-freelancers-iniciantes.html</loc>
    <lastmod>2026-02-10</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://rewardedtasks.com/artigos/melhores-cartoes-de-credito-sem-anuidade-com-cashback.html</loc>
    <lastmod>2026-02-10</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
  <url>
    <loc>https://rewardedtasks.com/sobre.html</loc>
    <lastmod>2026-02-10</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>
  <url>
    <loc>https://rewardedtasks.com/contato.html</loc>
    <lastmod>2026-02-10</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.5</priority>
  </url>
  <url>
    <loc>https://rewardedtasks.com/privacidade.html</loc>
    <lastmod>2026-02-10</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.3</priority>
  </url>
  <url>
    <loc>https://rewardedtasks.com/termos.html</loc>
    <lastmod>2026-02-10</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.3</priority>
  </url>
  <url>
    <loc>https://rewardedtasks.com/aviso-legal.html</loc>
    <lastmod>2026-02-10</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.3</priority>
  </url>
</urlset>
"""

with open(os.path.join(base, 'sitemap.xml'), 'w', encoding='utf-8') as f:
    f.write(sitemap_xml)
print('Created sitemap.xml')

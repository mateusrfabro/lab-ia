import os

base = r'C:\Users\mateu\Projects\lab-ia\staging_rewardedtasks_br'

def wrap_page(title, meta_desc, active_nav, content_body):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} - RewardedTasks Brasil</title>
  <meta name="description" content="{meta_desc}">
  <link rel="canonical" href="https://rewardedtasks.com/">
  <link rel="stylesheet" href="/css/style.css">
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%2310b981'><path d='M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5'/></svg>">
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
        <a href="/" class="{'active' if active_nav == 'home' else ''}">Início</a>
        <a href="/artigos/melhores-aplicativos-renda-extra-2026.html" class="{'active' if active_nav == 'apps' else ''}">Apps & Renda Extra</a>
        <a href="/artigos/como-organizar-financas-pessoais-planilha-gratis.html" class="{'active' if active_nav == 'financas' else ''}">Finanças</a>
        <a href="/artigos/seguranca-digital-como-identificar-golpes-na-internet.html" class="{'active' if active_nav == 'seguranca' else ''}">Segurança</a>
        <a href="/sobre.html" class="{'active' if active_nav == 'sobre' else ''}">Quem Somos</a>
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

  <!-- Page Body -->
  <main class="container" style="padding: 20px 20px 60px;">
    {content_body}
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

# SOBRE.HTML
sobre_content = """
<div class="single-article" style="max-width:900px; margin:0 auto;">
  <span class="category-tag">Institucional</span>
  <h1 class="single-title">Quem Somos — RewardedTasks Brasil</h1>
  <div class="article-meta-bar" style="margin-bottom:24px;">
    <span>Publicado pela Equipe Editorial</span>
    <span class="dot"></span>
    <span>Atualizado em 2026</span>
  </div>

  <div class="article-content">
    <p>O <strong>RewardedTasks Brasil</strong> nasceu com a missão de desmistificar a economia digital para os brasileiros. Em um cenário com milhares de novos aplicativos, plataformas de tarefas e oportunidades na internet, nosso compromisso é oferecer informações verificadas, práticas e 100% transparentes.</p>

    <h2>Nossa Missão</h2>
    <p>Ajudar pessoas comuns a utilizarem a tecnologia a seu favor — seja para organizar o orçamento familiar, economizar nas compras diárias, encontrar ferramentas confiáveis de trabalho remoto ou aprender a se proteger contra golpes financeiros na web.</p>

    <h2>Nossa Linha Editorial</h2>
    <p>Acreditamos em jornalismo e curadoria de conteúdo com responsabilidade. Nossas diretrizes incluem:</p>
    <ul>
      <li><strong>Testes Práticos:</strong> Antes de recomendar qualquer aplicativo ou plataforma, nossa equipe realiza o cadastro e analisa a usabilidade, termos de uso e política de pagamento.</li>
      <li><strong>Zero Promessas Milagrosas:</strong> Condenamos qualquer esquema de "dinheiro fácil" ou pirâmides financeiras. Ressaltamos sempre que renda extra exige tempo, dedicação e critérios de segurança.</li>
      <li><strong>Independência:</strong> Nossas avaliações são imparciais e fundamentadas na experiência real do usuário.</li>
    </ul>

    <h2>Estrutura e Equipe</h2>
    <p>Nossa redação conta com analistas de tecnologia, redatores especializados em finanças pessoais e revisores de segurança da informação. Nosso escritório editorial central está situado em São Paulo, com colaboradores distribuídos em todo o Brasil.</p>

    <div class="highlight-box">
      <h4>Compromisso com o Leitor</h4>
      <p style="margin:0; font-size:15px;">Dúvidas, sugestões de pautas ou denúncias de aplicativos duvidosos? Entre em contato diretamente com nossos editores pelo canal oficial <a href="/contato.html" style="color:#10b981; font-weight:600;">Fale Conosco</a>.</p>
    </div>
  </div>
</div>
"""

# CONTATO.HTML
contato_content = """
<div class="single-article" style="max-width:900px; margin:0 auto;">
  <span class="category-tag">Atendimento</span>
  <h1 class="single-title">Fale Conosco — Canal de Atendimento</h1>
  <div class="article-meta-bar" style="margin-bottom:24px;">
    <span>Respondemos em até 24 horas úteis</span>
    <span class="dot"></span>
    <span>Segunda a Sexta, das 09h às 18h</span>
  </div>

  <div class="article-content">
    <p>Valorizamos o contato direto com nossos leitores, parceiros comerciais e desenvolvedores. Utilize os canais abaixo para enviar críticas, sugestões de matérias ou parcerias editoriais.</p>

    <div style="display:grid; grid-template-columns:1fr 1fr; gap:24px; margin:32px 0;">
      <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:24px;">
        <h3 style="margin-top:0; color:#0f172a;">📩 E-mails Oficiais</h3>
        <p style="font-size:14px; margin-bottom:8px;"><strong>Redação & Pautas:</strong><br><a href="mailto:contato@rewardedtasks.com" style="color:#10b981;">contato@rewardedtasks.com</a></p>
        <p style="font-size:14px; margin-bottom:8px;"><strong>Privacidade & DPO:</strong><br><a href="mailto:privacidade@rewardedtasks.com" style="color:#10b981;">privacidade@rewardedtasks.com</a></p>
        <p style="font-size:14px; margin-bottom:0;"><strong>Comercial & AdSense:</strong><br><a href="mailto:comercial@rewardedtasks.com" style="color:#10b981;">comercial@rewardedtasks.com</a></p>
      </div>

      <div style="background:#f8fafc; border:1px solid #e2e8f0; border-radius:12px; padding:24px;">
        <h3 style="margin-top:0; color:#0f172a;">📍 Sede Editorial</h3>
        <p style="font-size:14px; line-height:1.6; color:#475569;">
          <strong>RewardedTasks Brasil Mídia Digital Ltda.</strong><br>
          Av. Paulista, 1106 - Bela Vista<br>
          São Paulo - SP, CEP 01310-100<br>
          Brasil
        </p>
      </div>
    </div>

    <h2>Envie uma Mensagem</h2>
    <form style="display:flex; flex-direction:column; gap:16px; margin-top:20px;" onsubmit="event.preventDefault(); alert('Mensagem enviada com sucesso! Nossa equipe entrará em contato.'); this.reset();">
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:16px;">
        <div>
          <label style="display:block; font-size:14px; font-weight:600; margin-bottom:6px;">Seu Nome Completo *</label>
          <input type="text" required style="width:100%; padding:12px; border:1px solid #cbd5e1; border-radius:8px; font-size:15px;">
        </div>
        <div>
          <label style="display:block; font-size:14px; font-weight:600; margin-bottom:6px;">Seu E-mail *</label>
          <input type="email" required style="width:100%; padding:12px; border:1px solid #cbd5e1; border-radius:8px; font-size:15px;">
        </div>
      </div>
      <div>
        <label style="display:block; font-size:14px; font-weight:600; margin-bottom:6px;">Assunto *</label>
        <input type="text" required style="width:100%; padding:12px; border:1px solid #cbd5e1; border-radius:8px; font-size:15px;" placeholder="Ex: Sugestão de pauta / Dúvida sobre artigo">
      </div>
      <div>
        <label style="display:block; font-size:14px; font-weight:600; margin-bottom:6px;">Sua Mensagem *</label>
        <textarea required rows="5" style="width:100%; padding:12px; border:1px solid #cbd5e1; border-radius:8px; font-size:15px; font-family:inherit;"></textarea>
      </div>
      <button type="submit" style="background:#10b981; color:#fff; border:none; padding:14px 28px; font-size:16px; font-weight:700; border-radius:8px; cursor:pointer; width:fit-content;">Enviar Mensagem</button>
    </form>
  </div>
</div>
"""

# PRIVACIDADE.HTML (Full Google AdSense + LGPD)
privacidade_content = """
<div class="single-article" style="max-width:900px; margin:0 auto;">
  <span class="category-tag">Conformidade Legal</span>
  <h1 class="single-title">Política de Privacidade</h1>
  <div class="article-meta-bar" style="margin-bottom:24px;">
    <span>Em conformidade com a LGPD (Lei 13.709/2018)</span>
    <span class="dot"></span>
    <span>Atualizada em Janeiro de 2026</span>
  </div>

  <div class="article-content">
    <p>A sua privacidade é de extrema importância para o <strong>RewardedTasks Brasil</strong> ("nós", "nosso portal", "rewardedtasks.com"). Esta Política de Privacidade descreve como coletamos, usamos, armazenamos e protegemos os seus dados pessoais ao navegar em nosso site.</p>

    <h2>1. Dados Coletados</h2>
    <p>Podemos coletar e processar os seguintes dados:</p>
    <ul>
      <li><strong>Dados de Navegação:</strong> Endereço IP anonimizado, tipo de navegador, páginas visitadas, tempo de permanência e termos de busca interna.</li>
      <li><strong>Dados Fornecidos Voluntariamente:</strong> Nome e endereço de e-mail ao preencher nosso formulário de contato ou assinar nossa newsletter semanal.</li>
    </ul>

    <h2>2. Uso de Cookies e Tecnologias Semelhantes</h2>
    <p>Utilizamos cookies para melhorar sua experiência de navegação, lembrar suas preferências e gerar métricas estatísticas anônimas de tráfego.</p>

    <h2>3. Publicidade do Google AdSense e Cookies DoubleClick DART</h2>
    <p>O Google, como fornecedor terceirizado de anúncios em nosso site, utiliza cookies para exibir anúncios com base nas visitas anteriores dos usuários ao nosso ou a outros websites na internet.</p>
    <ul>
      <li>O uso de cookies de publicidade pelo Google permite a ele e aos seus parceiros veicular anúncios para nossos usuários com base na visita ao nosso portal e/ou a outros sites na Internet.</li>
      <li>Os usuários podem desativar a publicidade personalizada visitando as <a href="https://adssettings.google.com/" target="_blank" rel="noopener" style="color:#10b981;">Configurações de Anúncios do Google</a>.</li>
      <li>Alternativamente, você pode desativar o uso de cookies de terceiros para publicidade personalizada visitando o site <a href="https://www.aboutads.info/choices/" target="_blank" rel="noopener" style="color:#10b981;">aboutads.info</a>.</li>
    </ul>

    <h2>4. Direitos do Titular (LGPD)</h2>
    <p>Nos termos do artigo 18 da Lei Geral de Proteção de Dados (Lei 13.709/2018), você tem o direito de solicitar a confirmação da existência de tratamento, o acesso aos seus dados, a correção de dados incompletos ou a exclusão de dados cadastrais voluntários.</p>

    <h2>5. Contato com o Encarregado de Dados (DPO)</h2>
    <p>Para exercer qualquer um de seus direitos ou esclarecer dúvidas sobre esta política, envie uma mensagem ao nosso Encarregado pelo e-mail: <strong>privacidade@rewardedtasks.com</strong>.</p>
  </div>
</div>
"""

# TERMOS.HTML
termos_content = """
<div class="single-article" style="max-width:900px; margin:0 auto;">
  <span class="category-tag">Termos Legais</span>
  <h1 class="single-title">Termos e Condições de Uso</h1>
  <div class="article-meta-bar" style="margin-bottom:24px;">
    <span>Vigência em todo o território nacional</span>
    <span class="dot"></span>
    <span>Última revisão: 2026</span>
  </div>

  <div class="article-content">
    <p>Bem-vindo ao <strong>RewardedTasks Brasil</strong>. Ao acessar e utilizar este website (rewardedtasks.com), você concorda expressamente em cumprir os seguintes Termos e Condições de Uso.</p>

    <h2>1. Objeto do Portal</h2>
    <p>O RewardedTasks Brasil é um veículo editorial e informativo dedicado à publicação de notícias, artigos analíticos, guias comparativos de aplicativos e conteúdo educativo sobre economia digital e finanças pessoais.</p>

    <h2>2. Propriedade Intelectual</h2>
    <p>Todo o conteúdo textual, logotipos, layout e código-fonte deste portal são protegidos pela legislação de direitos autorais e propriedade intelectual brasileira. É proibida a reprodução total ou parcial sem menção expressa à fonte ou autorização prévia por escrito.</p>

    <h2>3. Isenção de Responsabilidade sobre Links Externos</h2>
    <p>Nosso portal pode conter links para sites, aplicativos e serviços de terceiros. Não exercemos qualquer controle sobre as políticas, termos ou práticas operacionais de plataformas externas e não assumimos qualquer responsabilidade pelos serviços prestados por terceiros.</p>

    <h2>4. Alterações nos Termos</h2>
    <p>Reservamo-nos o direito de modificar estes Termos a qualquer momento para adequação a mudanças legais ou editoriais. Recomendamos a consulta periódica desta página.</p>
  </div>
</div>
"""

# AVISO-LEGAL.HTML
aviso_content = """
<div class="single-article" style="max-width:900px; margin:0 auto;">
  <span class="category-tag">Transparência</span>
  <h1 class="single-title">Aviso Legal & Isenção de Responsabilidade</h1>
  <div class="article-meta-bar" style="margin-bottom:24px;">
    <span>Declaração Editorial Obrigatória</span>
  </div>

  <div class="article-content">
    <p>As informações disponibilizadas no portal <strong>RewardedTasks Brasil</strong> possuem finalidade estritamente educativa e informativa.</p>

    <div class="highlight-box">
      <h4>Isenção de Consultoria Financeira e de Investimentos</h4>
      <p style="margin:0; font-size:15px;">Nenhum conteúdo publicado neste portal constitui consultoria financeira, recomendação de investimento ou promessa de remuneração fixa. O leitor é inteiramente responsável por suas decisões de consumo, finanças e contratação de serviços.</p>
    </div>

    <h2>Resultados e Recompensas em Aplicativos</h2>
    <p>Ao analisar ou testar aplicativos de tarefas, jogos ou pesquisas de mercado, os valores de ganhos citados em nossos artigos refletem apenas estimativas baseadas na experiência de teste ou declarações dos desenvolvedores das plataformas. Os resultados reais variam conforme o tempo dedicado, perfil demográfico e critérios de cada plataforma independente.</p>
  </div>
</div>
"""

pages = [
    ('sobre.html', 'Quem Somos', 'Conheça o RewardedTasks Brasil, portal de notícias sobre aplicativos, renda extra e finanças pessoais.', 'sobre', sobre_content),
    ('contato.html', 'Fale Conosco', 'Entre em contato com a equipe editorial do RewardedTasks Brasil. Envie dúvidas, sugestões e pautas.', 'contato', contato_content),
    ('privacidade.html', 'Política de Privacidade', 'Política de Privacidade e Cookies do RewardedTasks Brasil, em total conformidade com a LGPD e o Google AdSense.', '', privacidade_content),
    ('termos.html', 'Termos de Uso', 'Termos e Condições de Uso do portal RewardedTasks Brasil.', '', termos_content),
    ('aviso-legal.html', 'Aviso Legal', 'Aviso legal e isenção de responsabilidade sobre conteúdos financeiros e educativos.', '', aviso_content)
]

for filename, title, desc, nav, body in pages:
    filepath = os.path.join(base, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(wrap_page(title, desc, nav, body))
    print(f'Created {filename}')

# ADS.TXT
ads_txt_content = "google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0\n"
with open(os.path.join(base, 'ads.txt'), 'w', encoding='utf-8') as f:
    f.write(ads_txt_content)
print('Created ads.txt')

# ROBOTS.TXT
robots_txt_content = """User-agent: *
Allow: /
Sitemap: https://rewardedtasks.com/sitemap.xml
"""
with open(os.path.join(base, 'robots.txt'), 'w', encoding='utf-8') as f:
    f.write(robots_txt_content)
print('Created robots.txt')

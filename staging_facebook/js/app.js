// =============================================================================
// REWARDED VIDEOS - LÓGICA DO FUNIL (GLOBAL BLACK FRIDAY EDITION)
// =============================================================================

let currentStep = 0;
let currentBalance = CONFIG.initialBalance;
let activeVideoElement = null;
let autoAdvanceTimer = null;
let isVslVideoInited = false;
let userComments = [];
let isPostLiked = false;
let toastTimeout = null;
let hasShownTutorial = false;

// Obter textos do idioma atual
function t(key) {
  const lang = CONFIG.language || "en";
  return (CONFIG.i18n[lang] && CONFIG.i18n[lang][key]) || CONFIG.i18n.en[key] || "";
}

// Formatação monetária
function formatMoney(amount) {
  if (CONFIG.currencySymbol === "R$") {
    return "R$ " + amount.toFixed(2).replace(".", ",");
  }
  return "$" + amount.toFixed(2);
}

// Animação de contagem suave do saldo
function animateBalance(targetAmount, duration = 1200) {
  const startAmount = currentBalance;
  const startTime = performance.now();
  const balanceEl = document.getElementById("header-balance");

  function update(now) {
    const elapsed = now - startTime;
    const progress = Math.min(elapsed / duration, 1);
    const ease = 1 - Math.pow(1 - progress, 3);
    const displayed = startAmount + (targetAmount - startAmount) * ease;
    
    if (balanceEl) {
      balanceEl.textContent = formatMoney(displayed);
    }

    if (progress < 1) {
      requestAnimationFrame(update);
    } else {
      currentBalance = targetAmount;
      if (balanceEl) {
        balanceEl.textContent = formatMoney(targetAmount);
      }
    }
  }

  requestAnimationFrame(update);
}

// Inicialização
document.addEventListener("DOMContentLoaded", () => {
  initTracking();
  applyLocalization();
  renderStoriesBar();
  userComments = [...CONFIG.comments];
  goToStep(0);
  startWelcomeTimer();
  startLivePayoutTicker();
  setupExitIntent();

  const welcomeBtn = document.querySelector("#step-welcome button.pulse-btn") || document.getElementById("welcome-btn-text");
  if (welcomeBtn) {
    const btnParent = welcomeBtn.closest("button") || welcomeBtn;
    btnParent.addEventListener("click", (e) => {
      e.preventDefault();
      goToStep(1);
    });
  }
});

// Cronômetro de Urgência da Tela de Entrada (04:59)
let welcomeSecondsLeft = 299;
let welcomeTimerInterval = null;

function startWelcomeTimer() {
  if (welcomeTimerInterval) clearInterval(welcomeTimerInterval);
  const timerEl = document.getElementById("welcome-timer");
  if (!timerEl) return;

  function update() {
    if (welcomeSecondsLeft <= 0) {
      timerEl.textContent = "00:00";
      clearInterval(welcomeTimerInterval);
      return;
    }
    const mins = Math.floor(welcomeSecondsLeft / 60);
    const secs = welcomeSecondsLeft % 60;
    timerEl.textContent = `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
    welcomeSecondsLeft--;
  }

  update();
  welcomeTimerInterval = setInterval(update, 1000);
}

// Aplica textos de acordo com o idioma
function applyLocalization() {
  const initialText = formatMoney(CONFIG.initialBalance);
  
  const welcomeTag = document.getElementById("welcome-tag");
  if (welcomeTag) welcomeTag.textContent = t("welcomeTag");

  const welcomeTitle = document.getElementById("welcome-title");
  if (welcomeTitle) welcomeTitle.textContent = t("welcomeTitle");

  const welcomeDesc = document.getElementById("welcome-desc");
  if (welcomeDesc) welcomeDesc.textContent = t("welcomeDesc");

  const welcomeBadge = document.getElementById("welcome-reward-badge");
  if (welcomeBadge) {
    welcomeBadge.textContent = CONFIG.language === "pt" 
      ? `Você já ganhou ${initialText}!` 
      : `You've already earned ${initialText}!`;
  }

  const welcomeReserveNote = document.getElementById("welcome-reserve-note");
  if (welcomeReserveNote) {
    welcomeReserveNote.textContent = CONFIG.language === "pt"
      ? `Seu bônus de ${initialText} está reservado até o cronômetro zerar.`
      : `Your ${initialText} initial bonus is reserved until the timer expires.`;
  }

  const welcomeLiveAuditors = document.getElementById("welcome-live-auditors");
  if (welcomeLiveAuditors) welcomeLiveAuditors.textContent = t("welcomeLiveAuditors");

  const welcomeSpotsLabel = document.getElementById("welcome-spots-label");
  if (welcomeSpotsLabel) welcomeSpotsLabel.textContent = t("welcomeSpotsLabel");

  const welcomeSpotsLeft = document.getElementById("welcome-spots-left");
  if (welcomeSpotsLeft) welcomeSpotsLeft.textContent = t("welcomeSpotsLeft");

  const welcomeGuarantee = document.getElementById("welcome-guarantee");
  if (welcomeGuarantee) welcomeGuarantee.textContent = t("welcomeGuarantee");

  const welcomeNote = document.getElementById("welcome-note");
  if (welcomeNote) welcomeNote.textContent = t("welcomeNote");

  const welcomeBtnText = document.getElementById("welcome-btn-text");
  if (welcomeBtnText) welcomeBtnText.textContent = t("welcomeBtn");

  const headerBalance = document.getElementById("header-balance");
  if (headerBalance) headerBalance.textContent = initialText;

  // Tutorial Modal texts
  const tutTitle = document.getElementById("tutorial-title");
  if (tutTitle) tutTitle.textContent = t("tutorialTitle");
  const tutText = document.getElementById("tutorial-text");
  if (tutText) tutText.textContent = t("tutorialText");
  const tutBtn = document.getElementById("tutorial-btn");
  if (tutBtn) tutBtn.textContent = t("tutorialBtn");

  // VSL & Conversion Modals
  const vslModalTitle = document.getElementById("modal-vsl-title");
  if (vslModalTitle) vslModalTitle.textContent = t("vslRuleTitle");
  const vslModalBtn = document.getElementById("modal-vsl-btn");
  if (vslModalBtn) vslModalBtn.textContent = t("vslRuleBtn");

  const exitTitle = document.getElementById("modal-exit-title");
  if (exitTitle) exitTitle.textContent = t("exitTitle");
  const exitBtnLeave = document.getElementById("modal-exit-btn-leave");
  if (exitBtnLeave) exitBtnLeave.textContent = t("exitBtnLeave");

  const pushApp = document.getElementById("push-app-name");
  if (pushApp) pushApp.textContent = t("pushApp") || "Facebook Wallet";

  const btnEn = document.getElementById("lang-btn-en");
  const btnPt = document.getElementById("lang-btn-pt");
  if (btnEn && btnPt) {
    if (CONFIG.language === "en") {
      btnEn.classList.add("bg-neutral-800", "text-white");
      btnEn.classList.remove("text-neutral-400");
      btnPt.classList.remove("bg-neutral-800", "text-white");
      btnPt.classList.add("text-neutral-400");
    } else {
      btnPt.classList.add("bg-neutral-800", "text-white");
      btnPt.classList.remove("text-neutral-400");
      btnEn.classList.remove("bg-neutral-800", "text-white");
      btnEn.classList.add("text-neutral-400");
    }
  }
}

// Alternar idioma
function switchLanguage(lang) {
  try { SoundFX.playClick(); } catch (e) {}
  CONFIG.language = lang;
  payoutQueue = [];
  lastPayoutName = "";
  if (lang === "pt") {
    CONFIG.currencySymbol = "R$";
    CONFIG.initialBalance = 48.50;
    currentBalance = 48.50;
  } else {
    CONFIG.currencySymbol = "$";
    CONFIG.initialBalance = 32.27;
    currentBalance = 32.27;
  }
  applyLocalization();
  if (currentStep >= 1 && currentStep <= CONFIG.tasks.length) {
    renderInstagramFeedPost(currentStep - 1);
  } else if (currentStep > CONFIG.tasks.length) {
    renderMetaVslStep();
  }
}

// Renderiza os Stories com logos vetoriais garantidas (Samsung, Apple, Nike, etc.)
function renderStoriesBar() {
  const container = document.getElementById("stories-carousel");
  if (!container) return;

  container.innerHTML = CONFIG.stories.map(s => {
    const logoSrc = CONFIG.brandLogos[s.brandKey] || s.avatar;
    return `
      <div onclick="handleStoryClick('${s.displayName}')" class="flex flex-col items-center gap-1 flex-shrink-0 cursor-pointer">
        <div class="story-ring-gradient relative">
          <div class="story-inner bg-white">
            <img src="${logoSrc}" class="w-full h-full object-contain p-1" alt="${s.displayName}">
          </div>
          ${s.isLive ? '<span class="live-badge absolute -bottom-1 left-1/2 -translate-x-1/2">((•))</span>' : ''}
        </div>
        <span class="text-[11px] text-neutral-800 font-normal truncate max-w-[68px]">${s.username}</span>
      </div>
    `;
  }).join("");
}

// Notificação ao tentar abrir Story durante a avaliação
function handleStoryClick(name) {
  SoundFX.playClick();
  showToast(t("storyAlert"));
}

function showToast(message) {
  const toast = document.getEleme// Navegação entre Etapas Ultra-Blindada
function goToStep(stepIndex) {
  try {
    if (window.SoundFX && typeof SoundFX.playClick === "function") {
      SoundFX.playClick();
    }
  } catch (e) {}

  if (activeVideoElement) {
    try { activeVideoElement.pause(); } catch (e) {}
    activeVideoElement = null;
  }

  if (evalTimerInterval) {
    clearInterval(evalTimerInterval);
    evalTimerInterval = null;
  }

  const stepWelcome = document.getElementById("step-welcome");
  const stepTask = document.getElementById("step-task");
  const stepVsl = document.getElementById("step-vsl");

  if (stepWelcome) stepWelcome.classList.remove("active");
  if (stepTask) stepTask.classList.remove("active");
  if (stepVsl) stepVsl.classList.remove("active");

  currentStep = stepIndex;

  const instaHeader = document.getElementById("instagram-header");
  const storiesSection = document.getElementById("stories-section");
  const bottomNav = document.getElementById("instagram-bottom-nav");

  if (stepIndex === 0) {
    if (stepWelcome) stepWelcome.classList.add("active");
    if (instaHeader) instaHeader.classList.add("hidden");
    if (storiesSection) storiesSection.classList.add("hidden");
    if (bottomNav) bottomNav.classList.add("hidden");
  } else if (stepIndex >= 1 && stepIndex <= (window.CONFIG && CONFIG.tasks ? CONFIG.tasks.length : 3)) {
    if (instaHeader) instaHeader.classList.remove("hidden");
    if (storiesSection) storiesSection.classList.add("hidden");
    if (bottomNav) bottomNav.classList.add("hidden");

    try {
      renderInstagramFeedPost(stepIndex - 1);
    } catch (err) {
      console.error("Error in renderInstagramFeedPost:", err);
    }

    if (stepTask) stepTask.classList.add("active");
    window.scrollTo({ top: 0, behavior: "smooth" });

    // Exibe pop-up tutorial apenas no 1º vídeo
    if (stepIndex === 1) {
      try { trackEvent('ViewContent'); } catch (e) {}
      if (!hasShownTutorial) {
        hasShownTutorial = true;
        setTimeout(() => {
          openTutorialModal();
        }, 400);
      }
    }
  } else {
    try { trackEvent('ViewContent'); } catch (e) {}
    if (instaHeader) instaHeader.classList.remove("hidden");
    if (storiesSection) storiesSection.classList.add("hidden");
    if (bottomNav) bottomNav.classList.add("hidden");

    if (stepVsl) stepVsl.classList.add("active");
    window.scrollTo({ top: 0, behavior: "smooth" });

    try {
      renderMetaVslStep();
    } catch (err) {
      console.error("Error in renderMetaVslStep:", err);
    }
  }
}
window.goToStep = goToStep;
      stepVsl.style.setProperty("display", "block", "important");
      stepVsl.classList.add("active");
    }
    window.scrollTo({ top: 0, behavior: "smooth" });

    try {
      renderMetaVslStep();
    } catch (err) {
      console.error("Error in renderMetaVslStep:", err);
    }
  }
}
window.goToStep = goToStep;

// Pop-up tutorial explicativo no primeiro vídeo
function openTutorialModal() {
  const modal = document.getElementById("modal-tutorial");
  if (modal) {
    modal.classList.add("open");
  }
}

function closeTutorialModal() {
  SoundFX.playClick();
  const modal = document.getElementById("modal-tutorial");
  if (modal) {
    modal.classList.remove("open");
  }
  // Tenta dar play no vídeo caso estivesse pausado
  if (activeVideoElement) {
    activeVideoElement.play().catch(() => {});
  }
}

// Atualiza a Barra de Progresso Segmentada das Tarefas
function updateTaskProgressBar(index) {
  const stepText = document.getElementById("task-progress-step-text");
  const pctText = document.getElementById("task-progress-pct");
  const seg1 = document.getElementById("prog-seg-1");
  const seg2 = document.getElementById("prog-seg-2");
  const seg3 = document.getElementById("prog-seg-3");

  if (index === 0) {
    if (stepText) stepText.textContent = t("progressStep1");
    if (pctText) pctText.textContent = "33%";
    if (seg1) seg1.className = "h-1.5 rounded-full flex-1 bg-gradient-to-r from-emerald-500 to-teal-500 transition-all duration-300";
    if (seg2) seg2.className = "h-1.5 rounded-full flex-1 bg-neutral-200 transition-all duration-300";
    if (seg3) seg3.className = "h-1.5 rounded-full flex-1 bg-neutral-200 transition-all duration-300";
  } else if (index === 1) {
    if (stepText) stepText.textContent = t("progressStep2");
    if (pctText) pctText.textContent = "66%";
    if (seg1) seg1.className = "h-1.5 rounded-full flex-1 bg-gradient-to-r from-emerald-500 to-teal-500 transition-all duration-300";
    if (seg2) seg2.className = "h-1.5 rounded-full flex-1 bg-gradient-to-r from-emerald-500 to-teal-500 transition-all duration-300";
    if (seg3) seg3.className = "h-1.5 rounded-full flex-1 bg-neutral-200 transition-all duration-300";
  } else if (index === 2) {
    if (stepText) stepText.textContent = t("progressStep3");
    if (pctText) pctText.textContent = "99%";
    if (seg1) seg1.className = "h-1.5 rounded-full flex-1 bg-gradient-to-r from-emerald-500 to-teal-500 transition-all duration-300";
    if (seg2) seg2.className = "h-1.5 rounded-full flex-1 bg-gradient-to-r from-emerald-500 to-teal-500 transition-all duration-300";
    if (seg3) seg3.className = "h-1.5 rounded-full flex-1 bg-gradient-to-r from-emerald-500 to-teal-500 transition-all duration-300";
  }
}

// Renderiza o Post no Feed do Instagram com Desbloqueio Temporizado (1º: 3s, 2º: 7s, 3º: 10s)
function renderInstagramFeedPost(index) {
  updateTaskProgressBar(index);
  const task = CONFIG.tasks[index];
  const container = document.getElementById("task-card-container");
  isPostLiked = false;

  const captionText = CONFIG.language === "pt" ? task.captionPt : task.caption;
  const questionText = CONFIG.language === "pt" ? task.questionPt : task.question;
  const logoSrc = CONFIG.brandLogos[task.brandKey] || task.avatar;
  const reactionsMap = ["36,8 mil", "4.736", "12.5 mil"];
  const commentsMap = ["735 comments  1.401 shares", "232 comments  54 shares", "432 comments  127 shares"];

  container.innerHTML = `
    <article class="bg-white border-b border-neutral-200 pb-4 flex-1 flex flex-col justify-between">
      
      <div>
        <!-- Cabeçalho do Post do Facebook -->
        <div class="flex items-center justify-between px-3 py-2.5 bg-white">
          <div class="flex items-center gap-2.5">
            <div class="w-10 h-10 rounded-full bg-white border border-neutral-200 flex items-center justify-center p-1 overflow-hidden shadow-xs">
              <img src="${logoSrc}" class="w-full h-full object-contain" alt="${task.displayName}">
            </div>
            <div>
              <div class="flex items-center gap-1">
                <span class="font-bold text-sm text-neutral-900 leading-tight">${task.displayName}</span>
                <svg class="w-3.5 h-3.5 text-[#1877F2] fill-current" viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
              </div>
              <div class="flex items-center gap-1 text-[11px] text-neutral-500 font-normal">
                <span>Sponsored</span>
                <span>•</span>
                <span class="text-[10px]">🌐</span>
              </div>
            </div>
          </div>

          <button class="text-neutral-400 hover:text-neutral-700 px-1 font-bold text-lg">
            •••
          </button>
        </div>

        <!-- Texto da Publicação -->
        <div class="px-3 pb-2.5 text-xs sm:text-sm text-neutral-800 leading-snug">
          ${captionText}
        </div>

        <!-- Foto da Publicação -->
        <div class="w-full bg-neutral-100 overflow-hidden aspect-[4/3] flex items-center justify-center">
          <img src="${task.posterUrl}" class="w-full h-full object-cover" alt="${task.displayName} Photo">
        </div>

        <!-- Linha de Reações do Facebook -->
        <div class="px-3 py-2 flex items-center justify-between text-neutral-500 text-xs border-b border-neutral-100">
          <div class="flex items-center gap-1.5">
            <span class="inline-flex items-center -space-x-1">
              <span class="w-4 h-4 rounded-full bg-[#1877F2] text-white flex items-center justify-center text-[9px]">👍</span>
              <span class="w-4 h-4 rounded-full bg-[#FA3E3E] text-white flex items-center justify-center text-[9px]">❤️</span>
              <span class="w-4 h-4 rounded-full bg-[#F7B125] text-white flex items-center justify-center text-[9px]">😲</span>
            </span>
            <span class="font-medium text-neutral-600 text-xs">${reactionsMap[index] || task.likes}</span>
          </div>
          <div class="text-[11px] text-neutral-500 flex items-center gap-2">
            <span>${commentsMap[index] || "232 comments"}</span>
          </div>
        </div>

        <!-- Barra de Ações Like / Comment / Share -->
        <div class="px-4 py-2 flex items-center justify-around border-b border-neutral-200/80 text-xs font-semibold text-neutral-600">
          <button class="flex items-center gap-1.5 hover:text-neutral-900 py-0.5">
            <span>👍</span> <span>Like</span>
          </button>
          <button class="flex items-center gap-1.5 hover:text-neutral-900 py-0.5">
            <span>💬</span> <span>Comment</span>
          </button>
          <button class="flex items-center gap-1.5 hover:text-neutral-900 py-0.5">
            <span>↗</span> <span>Share</span>
          </button>
        </div>

        <!-- Seção da Pergunta e Avaliação -->
        <div class="p-4 bg-white text-center">
          <span class="text-[11px] text-neutral-400 font-medium block mb-1">
            Answer the question:
          </span>
          <h3 class="text-sm sm:text-base font-extrabold text-neutral-900 mb-4">
            ${questionText}
          </h3>

          <div class="grid grid-cols-2 gap-3 max-w-xs mx-auto">
            <button onclick="handleVote(false)" class="flex items-center justify-center gap-1.5 py-3 px-3 rounded-xl font-bold text-xs sm:text-sm bg-[#D93025] hover:bg-[#c5221f] active:scale-95 text-white transition shadow-sm">
              <span>👎</span>
              <span>Not relevant</span>
            </button>

            <button onclick="handleVote(true)" class="flex items-center justify-center gap-1.5 py-3 px-3 rounded-xl font-bold text-xs sm:text-sm bg-[#1E8E3E] hover:bg-[#188038] active:scale-95 text-white transition shadow-sm">
              <span>👍</span>
              <span>Relevant</span>
            </button>
          </div>
        </div>

      </div>

    </article>
  `;
}

function startEvalUnlockCountdown(delaySeconds) {
  if (evalTimerInterval) clearInterval(evalTimerInterval);

  let secondsRemaining = delaySeconds;
  const timerBadge = document.getElementById("eval-countdown-timer");

  if (timerBadge) timerBadge.textContent = `${secondsRemaining.toString().padStart(2, "0")}s`;

  evalTimerInterval = setInterval(() => {
    secondsRemaining--;
    if (timerBadge) {
      timerBadge.textContent = `${Math.max(0, secondsRemaining).toString().padStart(2, "0")}s`;
    }

    if (secondsRemaining <= 0) {
      clearInterval(evalTimerInterval);
      evalTimerInterval = null;

      // Abre o pop-up sobrepondo o vídeo
      const popup = document.getElementById("video-eval-popup");
      if (popup) {
        popup.classList.remove("hidden");
        try { SoundFX.playPop(); } catch (e) {}
      }

      // Atualiza a barra informativa abaixo para indicar que está aguardando escolha no vídeo
      const icon = document.getElementById("eval-status-icon");
      if (icon) {
        icon.className = "w-8 h-8 rounded-full bg-emerald-500 flex items-center justify-center text-white flex-shrink-0 shadow-sm";
        icon.innerHTML = '<svg class="w-4 h-4 fill-none stroke-current" stroke-width="2.5" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"></polyline></svg>';
      }
      const title = document.getElementById("eval-status-title");
      if (title) {
        title.textContent = CONFIG.language === "pt" ? "Responda no vídeo acima 👆" : "Answer on the video above 👆";
      }
      const timerContainer = document.getElementById("eval-timer-badge-container");
      if (timerContainer) {
        timerContainer.innerHTML = `<span class="text-emerald-700 font-extrabold text-[11px]">${CONFIG.language === "pt" ? "Liberado" : "Ready"}</span>`;
      }
    }
  }, 1000);
}

// Alternar Curtida no Post
function togglePostLike(btn) {
  SoundFX.playClick();
  const heart = document.getElementById("post-heart-svg");
  isPostLiked = !isPostLiked;

  if (isPostLiked) {
    heart.classList.remove("fill-none");
    heart.classList.add("fill-[#ED4956]", "stroke-[#ED4956]");
  } else {
    heart.classList.remove("fill-[#ED4956]", "stroke-[#ED4956]");
    heart.classList.add("fill-none");
  }
}

// Alternar Áudio no Vídeo
function toggleVideoSound() {
  if (!activeVideoElement) return;
  activeVideoElement.muted = !activeVideoElement.muted;
  const iconSvg = document.getElementById("sound-icon-svg");
  
  if (activeVideoElement.muted) {
    iconSvg.innerHTML = '<path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4L9.91 6.09 12 8.18V4z"/>';
  } else {
    iconSvg.innerHTML = '<path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>';
  }
}

// Processa o voto da tarefa
function handleVote(isPositive) {
  if (evalTimerInterval) {
    clearInterval(evalTimerInterval);
    evalTimerInterval = null;
  }
  const currentTask = CONFIG.tasks[currentStep - 1];
  const rewardAmount = currentTask.reward;
  const newTotal = currentBalance + rewardAmount;

  SoundFX.playCash();

  document.getElementById("modal-reward-title").textContent = t("rewardTitle");
  document.getElementById("modal-reward-desc").textContent = t("rewardDesc");
  document.getElementById("modal-reward-amount").textContent = `+${formatMoney(rewardAmount)}`;
  document.getElementById("modal-reward-btn").textContent = t("rewardContinue");

  const modal = document.getElementById("modal-reward");
  modal.querySelectorAll(".anim-circle, .anim-check, .anim-fade-1, .anim-fade-2, .anim-fade-3, .anim-fade-4").forEach(el => {
    el.style.animation = "none";
    void el.offsetWidth;
    el.style.animation = "";
  });

  modal.classList.add("open");
  animateBalance(newTotal, 1400);

  if (autoAdvanceTimer) clearTimeout(autoAdvanceTimer);
  autoAdvanceTimer = setTimeout(() => {
    closeRewardModalAndAdvance();
  }, 4500);
}

function closeRewardModalAndAdvance() {
  if (autoAdvanceTimer) {
    clearTimeout(autoAdvanceTimer);
    autoAdvanceTimer = null;
  }
  document.getElementById("modal-reward").classList.remove("open");
  goToStep(currentStep + 1);
}

// Tela de Saque & VSL Oficial
function renderMetaVslStep() {
  const finalFormatted = formatMoney(currentBalance);
  
  const vslBalanceEl = document.getElementById("vsl-final-balance");
  if (vslBalanceEl) vslBalanceEl.textContent = finalFormatted;

  const headerBalanceEl = document.getElementById("header-balance");
  if (headerBalanceEl) headerBalanceEl.textContent = finalFormatted;

  const vslPrefix = document.getElementById("vsl-timer-prefix");
  if (vslPrefix) vslPrefix.textContent = t("vslTimerPrefix");

  const vslSuffix = document.getElementById("vsl-timer-suffix");
  if (vslSuffix) vslSuffix.textContent = t("vslTimerSuffix");

  const vslTag = document.getElementById("vsl-notice-tag");
  if (vslTag) vslTag.textContent = t("vslNoticeTag");

  const vslDesc = document.getElementById("vsl-notice-desc");
  if (vslDesc) vslDesc.textContent = t("vslNoticeDesc");

  const vslBtn = document.getElementById("vsl-withdraw-btn");
  if (vslBtn) vslBtn.textContent = t("vslWithdrawBtn");

  const vslSub = document.getElementById("vsl-withdraw-sub");
  if (vslSub) vslSub.textContent = t("vslWithdrawSub");

  const commTitle = document.getElementById("comments-title");
  if (commTitle) commTitle.textContent = t("commentsTitle");

  const commLive = document.getElementById("comments-live-tag");
  if (commLive) commLive.textContent = t("liveTag");

  renderComments();

  if (!isVslVideoInited) {
    initVslPlayer();
  }

  // Notificação Push Estilo iOS / Instagram (Topo)
  try {
    triggerVslPushNotification(finalFormatted);
  } catch (err) {
    console.error("Push notification error:", err);
  }

  // Pop-up Obrigatório de Regra de Saque (Assistir ao vídeo completo para liberar saldo)
  setTimeout(() => {
    try {
      openVslInstructionModal(finalFormatted);
    } catch (err) {
      console.error("VSL modal error:", err);
    }
  }, 450);
}

function initVslPlayer() {
  isVslVideoInited = true;
  const container = document.getElementById("vsl-player-container");
  if (!container) return;
  container.innerHTML = "";

  if (CONFIG.vsl.playerType === "vturb" && CONFIG.vsl.vturbScriptUrl && !CONFIG.vsl.vturbPlayerId.includes("SEU-ID")) {
    const player = document.createElement("vturb-smartplayer");
    player.id = CONFIG.vsl.vturbPlayerId;
    player.style.cssText = "display:block;margin:0 auto;width:100%;max-width:430px;";
    player.innerHTML = '<div class="vturb-player-placeholder" style="position:relative;width:100%;padding:125% 0 0;background-color:black;"></div>';
    container.appendChild(player);

    const script = document.createElement("script");
    script.src = CONFIG.vsl.vturbScriptUrl;
    script.async = true;
    document.head.appendChild(script);
  } else {
    container.innerHTML = `
      <div class="relative w-full aspect-video rounded-xl overflow-hidden bg-black shadow-md">
        <video id="vsl-html5-player" playsinline controls class="w-full h-full object-cover">
          <source src="${CONFIG.vsl.fallbackVideoUrl}" type="video/mp4">
        </video>
      </div>
    `;
  }

  // Garante que qualquer link de CTA gerado dentro do player Vturb vá para o checkout com todas as UTMs
  setInterval(() => {
    if (!CONFIG.vsl.checkoutUrl) return;
    const targetUrl = getCheckoutUrlWithUtms();
    function fixRoot(root) {
      try {
        (root || document).querySelectorAll('a[href]').forEach(function(a){
          if (a.href !== targetUrl) {
            a.href = targetUrl;
            a.addEventListener("click", () => {
              trackEvent('InitiateCheckout');
            }, { once: true });
          }
        });
      } catch(e){}
    }
    document.querySelectorAll("vturb-smartplayer").forEach((el) => {
      if (el.shadowRoot) fixRoot(el.shadowRoot);
      if (el.querySelectorAll) {
        el.querySelectorAll("*").forEach((c) => { if (c.shadowRoot) fixRoot(c.shadowRoot); });
      }
    });
  }, 800);
}

function renderComments() {
  const list = document.getElementById("comments-container");
  if (!list) return;
  list.innerHTML = "";

  userComments.forEach((c, idx) => {
    const contentText = CONFIG.language === "pt" ? (c.contentPt || c.content) : c.content;
    const item = document.createElement("div");
    item.className = "flex gap-2.5 text-left py-2 border-b border-neutral-100 last:border-0";
    item.innerHTML = `
      <img src="${c.avatar}" class="w-8 h-8 rounded-full object-cover flex-shrink-0" alt="${c.username}">
      <div class="flex-1 min-w-0">
        <p class="text-xs text-neutral-800 leading-snug">
          <span class="font-bold text-neutral-900 mr-1.5">${c.username}</span>
          ${contentText}
        </p>
        <div class="flex items-center gap-3 mt-1 text-[11px] text-neutral-400 font-medium">
          <span>${c.time}</span>
          <button onclick="toggleCommentLike(${idx}, this)" class="hover:text-neutral-700 transition-colors">Like (${c.likes})</button>
          <span class="text-emerald-600 font-semibold">• Payout Confirmed</span>
        </div>
      </div>
      <button onclick="toggleCommentHeart(this)" class="self-center p-1 text-neutral-300 hover:text-[#ED4956]">
        <svg class="w-3.5 h-3.5 fill-current" viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
      </button>
    `;
    list.appendChild(item);
  });
}

function toggleCommentLike(idx, btn) {
  userComments[idx].likes += 1;
  btn.textContent = `Liked (${userComments[idx].likes})`;
  btn.classList.add("text-emerald-600", "font-bold");
  SoundFX.playClick();
}

function toggleCommentHeart(btn) {
  btn.classList.toggle("text-[#ED4956]");
  btn.classList.toggle("text-neutral-300");
  SoundFX.playClick();
}

function handleAddComment(e) {
  e.preventDefault();
  const input = document.getElementById("new-comment-input");
  const text = input.value.trim();
  if (!text) return;

  userComments.unshift({
    avatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&h=100&fit=crop&crop=faces",
    username: "you_official",
    time: "just now",
    content: text,
    contentPt: text,
    likes: 1
  });

  input.value = "";
  renderComments();
  SoundFX.playClick();
}

function openCheckoutModal() {
  SoundFX.playClick();
  document.getElementById("modal-checkout-title").textContent = t("modalCheckoutTitle");
  document.getElementById("modal-checkout-desc").textContent = t("modalCheckoutDesc");
  document.getElementById("checkout-name-label").textContent = t("fullNameLabel");
  document.getElementById("checkout-email-label").textContent = t("emailLabel");
  document.getElementById("modal-checkout-submit").textContent = t("submitCheckoutBtn");
  document.getElementById("modal-ssl-secure").textContent = t("sslSecure");
  document.getElementById("modal-checkout").classList.add("open");
}

function closeCheckoutModal() {
  document.getElementById("modal-checkout").classList.remove("open");
}

function getCheckoutUrlWithUtms() {
  try {
    const url = new URL(CONFIG.vsl.checkoutUrl);
    const currentParams = new URLSearchParams(window.location.search);
    currentParams.forEach((val, key) => {
      url.searchParams.set(key, val);
    });
    return url.toString();
  } catch (e) {
    return CONFIG.vsl.checkoutUrl;
  }
}

// Rastreamento Meta Pixel & Utmify
function initTracking() {
  const urlParams = new URLSearchParams(window.location.search);
  const pixelId = (CONFIG.tracking && CONFIG.tracking.metaPixelId) || urlParams.get("pixel");

  if (pixelId && pixelId !== "SEU_PIXEL_AQUI") {
    !function(f,b,e,v,n,t,s)
    {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
    n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
    n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];
    s.parentNode.insertBefore(t,s)}(window, document,'script',
    'https://connect.facebook.net/en_US/fbevents.js');
    
    fbq('init', pixelId);
    fbq('track', 'PageView');
  }

  // Utmify Pixel ID se fornecido
  const utmifyId = (CONFIG.tracking && CONFIG.tracking.utmifyPixelId) || urlParams.get("utmify");
  if (utmifyId) {
    window.pixelId = utmifyId;
    const utmifyScript = document.createElement("script");
    utmifyScript.src = "https://cdn.utmify.com.br/scripts/pixel/pixel.js";
    utmifyScript.async = true;
    document.head.appendChild(utmifyScript);
  }
}

function trackEvent(eventName, params = {}) {
  try {
    if (window.fbq) {
      window.fbq('track', eventName, params);
    }
  } catch (e) {}
}

function submitCheckout(e) {
  e.preventDefault();
  hasSubmittedCheckout = true;
  trackEvent('InitiateCheckout');
  const name = document.getElementById("checkout-name").value;
  const email = document.getElementById("checkout-email").value;

  try {
    const targetUrl = new URL(getCheckoutUrlWithUtms());
    if (name) targetUrl.searchParams.set("name", name);
    if (email) targetUrl.searchParams.set("email", email);
    window.location.href = targetUrl.toString();
  } catch (err) {
    window.location.href = CONFIG.vsl.checkoutUrl;
  }
}

// =============================================================================
// CONVERSION BOOSTERS: LIVE PAYOUTS, PUSH NOTIFICATION, VSL RULE & EXIT INTENT
// =============================================================================

// 1. Notificações Flutuantes de Saques em Tempo Real (Social Proof Ticker Sem Repetição)
let livePayoutInterval = null;
let livePayoutHideTimeout = null;
let payoutQueue = [];
let lastPayoutName = "";

function shuffleArray(array) {
  const arr = [...array];
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

function getNextUniquePayout(lang) {
  const payouts = (CONFIG.livePayouts && CONFIG.livePayouts[lang]) || (CONFIG.livePayouts && CONFIG.livePayouts.en) || [];
  if (!payouts.length) return null;

  // Se a fila estiver vazia ou terminando, embaralha uma nova rodada garantindo que o primeiro nome não seja igual ao último exibido
  if (!payoutQueue.length) {
    let fresh = shuffleArray(payouts);
    if (fresh.length > 1 && fresh[0].name === lastPayoutName) {
      const temp = fresh[0];
      fresh[0] = fresh[fresh.length - 1];
      fresh[fresh.length - 1] = temp;
    }
    payoutQueue = fresh;
  }

  const nextItem = payoutQueue.shift();
  lastPayoutName = nextItem.name;
  return nextItem;
}

function startLivePayoutTicker() {
  if (livePayoutInterval) clearInterval(livePayoutInterval);
  payoutQueue = [];
  lastPayoutName = "";
  
  const toast = document.getElementById("live-payout-toast");
  if (!toast) return;

  function showNextPayout() {
    // Se estiver na tela da VSL, não exibe notificações de saque para manter 100% de foco no vídeo
    if (currentStep > CONFIG.tasks.length) return;

    // Evita sobreposição caso a notificação push da VSL esteja ativa
    const push = document.getElementById("vsl-push-notification");
    if (push && push.classList.contains("show")) return;

    const lang = CONFIG.language || "en";
    const item = getNextUniquePayout(lang);
    if (!item) return;
    
    const nameEl = document.getElementById("live-payout-name");
    const locEl = document.getElementById("live-payout-loc");
    const amtEl = document.getElementById("live-payout-amount");
    const timeEl = document.getElementById("live-payout-time");
    const actEl = document.getElementById("live-payout-action-text");

    if (nameEl) nameEl.textContent = item.name;
    if (locEl) locEl.textContent = `(${item.location})`;
    if (amtEl) amtEl.textContent = item.amount;
    if (timeEl) timeEl.textContent = item.time;
    if (actEl) actEl.textContent = lang === "pt" ? "sacou via Pix " : "withdrew ";

    toast.classList.add("show");

    if (livePayoutHideTimeout) clearTimeout(livePayoutHideTimeout);
    livePayoutHideTimeout = setTimeout(() => {
      toast.classList.remove("show");
    }, 4200);
  }

  // Primeiro disparo após 3 segundos
  setTimeout(showNextPayout, 3000);
  // Intervalo contínuo a cada 11 segundos
  livePayoutInterval = setInterval(showNextPayout, 11000);
}

function dismissLivePayout() {
  const toast = document.getElementById("live-payout-toast");
  if (toast) toast.classList.remove("show");
}

// 2. Notificação Push Estilo iOS / Instagram (Topo - VSL Step 4)
let pushNotificationTimeout = null;

function triggerVslPushNotification(balanceText) {
  const push = document.getElementById("vsl-push-notification");
  if (!push) return;

  const pushApp = document.getElementById("push-app-name");
  const pushTitle = document.getElementById("push-title");
  const pushDesc = document.getElementById("push-desc");

  if (pushApp) pushApp.textContent = t("pushApp") || "Facebook Wallet";
  if (pushTitle) pushTitle.textContent = (t("pushTitle") || "Pending Payout: {balance}").replace("{balance}", balanceText);
  if (pushDesc) pushDesc.textContent = t("pushDesc") || "Your withdrawal authorization is waiting. Complete the security video to release funds.";

  try { SoundFX.playPop(); } catch (e) {}
  push.classList.add("show");

  if (pushNotificationTimeout) clearTimeout(pushNotificationTimeout);
  pushNotificationTimeout = setTimeout(() => {
    dismissPushNotification();
  }, 6500);
}

function dismissPushNotification() {
  const push = document.getElementById("vsl-push-notification");
  if (push) push.classList.remove("show");
}

// 3. Pop-up Obrigatório de Regra de Saque da VSL
function openVslInstructionModal(balanceText) {
  const modal = document.getElementById("modal-vsl-instruction");
  if (!modal) return;

  const titleEl = document.getElementById("modal-vsl-title");
  const descEl = document.getElementById("modal-vsl-desc");
  const btnEl = document.getElementById("modal-vsl-btn");

  if (titleEl) titleEl.textContent = t("vslRuleTitle");
  if (btnEl) btnEl.textContent = t("vslRuleBtn");
  if (descEl) {
    const rawText = t("vslRuleText");
    descEl.innerHTML = rawText.replace("{balance}", `<span class="font-extrabold text-emerald-600">${balanceText}</span>`);
  }

  try { SoundFX.playPop(); } catch (e) {}
  modal.classList.add("open");
}

function closeVslInstructionModal() {
  try { SoundFX.playClick(); } catch (e) {}
  const modal = document.getElementById("modal-vsl-instruction");
  if (modal) modal.classList.remove("open");
}

// 4. Pop-up de Retenção de Saída (Exit-Intent Anti-Abandono)
let hasTriggeredExitIntent = false;
let hasSubmittedCheckout = false;

function setupExitIntent() {
  try {
    history.pushState({ page: "rewarded_tasks" }, "", window.location.href);
  } catch (err) {}

  window.addEventListener("popstate", () => {
    // Não dispara na etapa da VSL para não atrapalhar quem está assistindo ao vídeo
    if (currentStep > CONFIG.tasks.length) return;

    if (!hasTriggeredExitIntent && !hasSubmittedCheckout && currentStep > 0) {
      hasTriggeredExitIntent = true;
      try {
        history.pushState({ page: "rewarded_tasks" }, "", window.location.href);
      } catch (err) {}
      showExitIntentModal();
    }
  });

  document.addEventListener("mouseleave", (e) => {
    // Não dispara na etapa da VSL para não atrapalhar quem está assistindo ao vídeo
    if (currentStep > CONFIG.tasks.length) return;

    if (e.clientY <= 15 && !hasTriggeredExitIntent && !hasSubmittedCheckout && currentStep > 0) {
      hasTriggeredExitIntent = true;
      showExitIntentModal();
    }
  });
}

function showExitIntentModal() {
  // Não exibe na tela da VSL
  if (currentStep > CONFIG.tasks.length) return;

  const modal = document.getElementById("modal-exit-intent");
  if (!modal) return;

  const titleEl = document.getElementById("modal-exit-title");
  const descEl = document.getElementById("modal-exit-desc");
  const btnStay = document.getElementById("modal-exit-btn-stay");
  const btnLeave = document.getElementById("modal-exit-btn-leave");
  const balanceText = formatMoney(currentBalance);

  if (titleEl) titleEl.textContent = t("exitTitle");
  if (btnStay) btnStay.textContent = (t("exitBtnStay") || "KEEP MY {balance} & RELEASE PAYOUT").replace("{balance}", balanceText);
  if (btnLeave) btnLeave.textContent = t("exitBtnLeave");
  if (descEl) {
    const raw = t("exitText") || "Your accumulated balance of {balance} is reserved in your name. If you leave this page now, your balance will be CANCELLED!";
    descEl.innerHTML = raw.replace("{balance}", `<span class="font-black text-emerald-600">${balanceText}</span>`);
  }

  try { SoundFX.playPop(); } catch (e) {}
  modal.classList.add("open");
}

function closeExitIntentModal() {
  try { SoundFX.playClick(); } catch (e) {}
  const modal = document.getElementById("modal-exit-intent");
  if (modal) modal.classList.remove("open");

  if (currentStep > CONFIG.tasks.length) {
    const vslContainer = document.getElementById("step-vsl");
    if (vslContainer) {
      vslContainer.scrollIntoView({ behavior: "smooth" });
    }
  }
}

function confirmLeavePage() {
  const modal = document.getElementById("modal-exit-intent");
  if (modal) modal.classList.remove("open");
}

/**
 * FitBuddy - Frontend Application Controller
 * Handles tab transitions, dynamic calculations, AJAX requests to FastAPI backend,
 * and conversational AI Coach messaging.
 */

document.addEventListener('DOMContentLoaded', () => {
  initTabs();
  initPresetButtons();
  initProfileForm();
  initPlanGenerators();
  initCoachChat();
});

// Toast notification helper
function showToast(message, type = 'info') {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = 'toast';
  
  let icon = '⚡';
  if (type === 'success') icon = '✅';
  if (type === 'warning') icon = '⚠️';
  if (type === 'error') icon = '❌';

  toast.innerHTML = `<span>${icon}</span> <span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transition = 'opacity 0.4s ease';
    setTimeout(() => toast.remove(), 400);
  }, 4000);
}

// High-precision Markdown to HTML renderer using marked.js
function renderMarkdown(md) {
  if (!md) return '';
  if (typeof marked !== 'undefined' && typeof marked.parse === 'function') {
    return marked.parse(md, { breaks: true, gfm: true });
  }
  return md.replace(/\n/g, '<br>');
}

// Tab navigation
function initTabs() {
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabPanes = document.querySelectorAll('.tab-pane');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.getAttribute('data-tab');

      tabBtns.forEach(b => b.classList.remove('active'));
      tabPanes.forEach(p => p.classList.remove('active'));

      btn.classList.add('active');
      const targetPane = document.getElementById(target);
      if (targetPane) targetPane.classList.add('active');
    });
  });
}

// Preset personas
function initPresetButtons() {
  const chips = document.querySelectorAll('.preset-chip');
  chips.forEach(chip => {
    chip.addEventListener('click', async () => {
      const presetName = chip.getAttribute('data-preset');
      chips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');

      try {
        const response = await fetch(`/api/preset/${encodeURIComponent(presetName)}`, { method: 'POST' });
        const data = await response.json();
        if (data.success) {
          updateFormFields(data.profile);
          updateMetricsDisplay(data.metrics);
          showToast(`Applied preset: ${presetName}`, 'success');
        }
      } catch (err) {
        showToast('Error applying preset', 'error');
      }
    });
  });
}

// Update form input values
function updateFormFields(p) {
  if (!p) return;
  const setVal = (id, val) => {
    const el = document.getElementById(id);
    if (el) el.value = val;
  };

  setVal('inputAge', p.age);
  setVal('selectGender', p.gender);
  setVal('inputHeight', p.height_cm);
  setVal('inputWeight', p.weight_kg);
  setVal('inputTargetWeight', p.target_weight_kg);
  setVal('selectGoal', p.goal);
  setVal('selectActivity', p.activity_level);
  setVal('selectExperience', p.experience);
  setVal('selectEquipment', p.equipment);
  setVal('inputDays', p.days_per_week);
  setVal('inputDuration', p.session_duration_mins);
  setVal('selectDiet', p.diet_type);
  setVal('inputAllergies', p.allergies || 'None');
  setVal('inputInjuries', p.injuries || 'None');

  // Update slider display badges
  const daysBadge = document.getElementById('daysBadge');
  if (daysBadge) daysBadge.textContent = `${p.days_per_week} Days`;
  const durBadge = document.getElementById('durationBadge');
  if (durBadge) durBadge.textContent = `${p.session_duration_mins} Mins`;
}

// Update calculated metrics on dashboard
function updateMetricsDisplay(m) {
  if (!m) return;
  const setText = (id, text) => {
    const el = document.getElementById(id);
    if (el) el.textContent = text;
  };

  setText('statBmi', m.bmi);
  setText('statBmiCat', m.bmi_category);
  setText('statBmr', `${m.bmr} kcal`);
  setText('statTdee', `${m.tdee} kcal`);
  setText('statTargetCals', m.target_calories);
  setText('statCalMode', m.calorie_mode);
  setText('statHydration', `${m.hydration_l} L`);

  const macros = m.macros || {};
  setText('macroProtein', `${macros.protein_g}g (${macros.protein_pct}%)`);
  setText('macroCarbs', `${macros.carbs_g}g (${macros.carbs_pct}%)`);
  setText('macroFat', `${macros.fat_g}g (${macros.fat_pct}%)`);

  // Animate progress bars
  const pBar = document.getElementById('barProtein');
  if (pBar) pBar.style.width = `${macros.protein_pct || 30}%`;
  const cBar = document.getElementById('barCarbs');
  if (cBar) cBar.style.width = `${macros.carbs_pct || 40}%`;
  const fBar = document.getElementById('barFats');
  if (fBar) fBar.style.width = `${macros.fat_pct || 30}%`;
}

// Profile submission & dynamic updates
function initProfileForm() {
  const form = document.getElementById('profileForm');
  if (!form) return;

  const daysInput = document.getElementById('inputDays');
  if (daysInput) {
    daysInput.addEventListener('input', (e) => {
      const badge = document.getElementById('daysBadge');
      if (badge) badge.textContent = `${e.target.value} Days`;
    });
  }

  const durInput = document.getElementById('inputDuration');
  if (durInput) {
    durInput.addEventListener('input', (e) => {
      const badge = document.getElementById('durationBadge');
      if (badge) badge.textContent = `${e.target.value} Mins`;
    });
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = new FormData(form);

    try {
      const response = await fetch('/api/profile', {
        method: 'POST',
        body: formData
      });
      const data = await response.json();
      if (data.success) {
        updateMetricsDisplay(data.metrics);
        showToast('Health biometrics recalculated & saved to SQLite!', 'success');
      }
    } catch (err) {
      showToast('Error saving profile data', 'error');
    }
  });
}

// Workout & Nutrition plan generators
function initPlanGenerators() {
  const btnGenWorkout = document.getElementById('btnGenWorkout');
  const btnDemoWorkout = document.getElementById('btnDemoWorkout');
  const workoutDisplay = document.getElementById('workoutDisplay');

  const btnGenMeal = document.getElementById('btnGenMeal');
  const btnDemoMeal = document.getElementById('btnDemoMeal');
  const mealDisplay = document.getElementById('mealDisplay');

  const getApiKey = () => {
    const input = document.getElementById('navApiKey');
    return input ? input.value.trim() : '';
  };

  if (btnGenWorkout) {
    btnGenWorkout.addEventListener('click', async () => {
      btnGenWorkout.disabled = true;
      btnGenWorkout.innerHTML = '⏳ Formulating Split...';
      try {
        const response = await fetch('/api/workout/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ api_key: getApiKey(), is_demo: false })
        });
        const data = await response.json();
        if (data.success) {
          workoutDisplay.innerHTML = renderMarkdown(data.content);
          showToast(data.message || 'Workout plan generated!', 'success');
        }
      } catch (err) {
        showToast('Error generating workout plan', 'error');
      } finally {
        btnGenWorkout.disabled = false;
        btnGenWorkout.innerHTML = '⚡ Generate AI Workout Split';
      }
    });
  }

  if (btnDemoWorkout) {
    btnDemoWorkout.addEventListener('click', async () => {
      try {
        const response = await fetch('/api/workout/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ is_demo: true })
        });
        const data = await response.json();
        if (data.success) {
          workoutDisplay.innerHTML = renderMarkdown(data.content);
          showToast('Loaded demo workout plan!', 'info');
        }
      } catch (err) {
        showToast('Error loading demo plan', 'error');
      }
    });
  }

  if (btnGenMeal) {
    btnGenMeal.addEventListener('click', async () => {
      btnGenMeal.disabled = true;
      btnGenMeal.innerHTML = '⏳ Formulating Blueprint...';
      try {
        const response = await fetch('/api/meal/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ api_key: getApiKey(), is_demo: false })
        });
        const data = await response.json();
        if (data.success) {
          mealDisplay.innerHTML = renderMarkdown(data.content);
          showToast(data.message || 'Nutrition blueprint generated!', 'success');
        }
      } catch (err) {
        showToast('Error generating meal plan', 'error');
      } finally {
        btnGenMeal.disabled = false;
        btnGenMeal.innerHTML = '⚡ Generate AI Nutrition Plan';
      }
    });
  }

  if (btnDemoMeal) {
    btnDemoMeal.addEventListener('click', async () => {
      try {
        const response = await fetch('/api/meal/generate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ is_demo: true })
        });
        const data = await response.json();
        if (data.success) {
          mealDisplay.innerHTML = renderMarkdown(data.content);
          showToast('Loaded demo meal plan!', 'info');
        }
      } catch (err) {
        showToast('Error loading demo meal plan', 'error');
      }
    });
  }
}

// FitBuddy AI Coach Chat
function initCoachChat() {
  const chatMessages = document.getElementById('chatMessages');
  const chatForm = document.getElementById('chatForm');
  const chatInput = document.getElementById('chatInput');
  const promptChips = document.querySelectorAll('.prompt-chip');

  const scrollToBottom = () => {
    if (chatMessages) chatMessages.scrollTop = chatMessages.scrollHeight;
  };

  const appendMessage = (role, text) => {
    if (!chatMessages) return;
    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${role}`;
    bubble.innerHTML = renderMarkdown(text);
    chatMessages.appendChild(bubble);
    scrollToBottom();
  };

  const getApiKey = () => {
    const input = document.getElementById('navApiKey');
    return input ? input.value.trim() : '';
  };

  const sendQuery = async (query) => {
    if (!query || !query.trim()) return;
    appendMessage('user', query);
    if (chatInput) chatInput.value = '';

    // Typing indicator
    const typingBubble = document.createElement('div');
    typingBubble.className = 'chat-bubble assistant';
    typingBubble.innerHTML = '<i>FitBuddy AI Coach is formulating advice...</i>';
    chatMessages.appendChild(typingBubble);
    scrollToBottom();

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: query,
          api_key: getApiKey()
        })
      });
      const data = await response.json();
      typingBubble.remove();
      if (data.success) {
        appendMessage('assistant', data.answer);
      } else {
        appendMessage('assistant', data.answer || 'Error contacting Coach.');
      }
    } catch (err) {
      typingBubble.remove();
      appendMessage('assistant', '⚠️ Could not connect to FitBuddy Coach server.');
    }
  };

  if (chatForm && chatInput) {
    chatForm.addEventListener('submit', (e) => {
      e.preventDefault();
      sendQuery(chatInput.value);
    });
  }

  promptChips.forEach(chip => {
    chip.addEventListener('click', () => {
      const promptText = chip.getAttribute('data-prompt');
      sendQuery(promptText);
    });
  });

  scrollToBottom();
}

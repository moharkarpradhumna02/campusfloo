import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update WAYZEN Speech Bubble HTML
bubble_old = '''  <!-- Cute Speech Bubble Popping Out -->
  <div id="wayzenSpeechBubble" class="fixed bottom-24 right-6 z-[9990] max-w-xs glass-panel speech-bubble-tail p-3.5 rounded-2xl border border-brand-cyan/40 shadow-2xl animate-pop-in transition-all cursor-pointer" onclick="toggleWayzenChat()">
    <div class="flex items-start justify-between gap-2">
      <div class="flex items-center gap-1.5 text-brand-cyan font-black text-[11px]">
        <span class="animate-bounce">🤖</span>
        <span>WAYZEN AI</span>
      </div>
      <button onclick="event.stopPropagation(); closeWayzenBubble();" class="text-zinc-400 hover:text-white text-xs">×</button>
    </div>
    <p id="wayzenBubbleText" class="text-xs text-white mt-1 leading-snug font-medium">
      👋 Oye hero! 8:30 AM class ke liye late ho raha hai? Bus ka ETA puch le! 🚌
    </p>
  </div>'''

bubble_new = '''  <!-- WAYZEN AI Speech Bubble -->
  <div id="wayzenSpeechBubble" class="fixed bottom-24 right-6 z-[9990] max-w-xs bg-white border-2 border-black p-3.5 rounded-2xl shadow-2xl animate-pop-in transition-all cursor-pointer" onclick="toggleWayzenChat()">
    <div class="flex items-start justify-between gap-2">
      <div class="flex items-center gap-1.5 text-black font-black text-xs">
        <span class="animate-bounce">🤖</span>
        <span>WAYZEN AI</span>
      </div>
      <button onclick="event.stopPropagation(); closeWayzenBubble();" class="text-zinc-600 hover:text-black font-bold text-sm">✕</button>
    </div>
    <p id="wayzenBubbleText" class="text-xs text-black font-bold mt-1.5 leading-snug">
      👋 Oye hero! 8:30 AM class ke liye late ho raha hai? Bus ka ETA puch le! 🚌
    </p>
  </div>'''

if bubble_old in content:
    content = content.replace(bubble_old, bubble_new)
    print("[PASS] Replaced wayzenSpeechBubble")
else:
    print("[WARN] wayzenSpeechBubble exact match not found, using regex...")
    content = re.sub(r'<!-- Cute Speech Bubble Popping Out -->[\s\S]*?<p id="wayzenBubbleText"[\s\S]*?</div>', bubble_new, content, count=1)

# 2. Update WAYZEN Chat Modal Header & Chips & Input
modal_header_old = '''    <!-- Header -->
    <div class="p-4 border-b border-white/10 flex items-center justify-between bg-zinc-50 shrink-0">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-brand-cyan to-brand-purple flex items-center justify-center text-xl shadow-lg shadow-brand-cyan/20 shrink-0">
          🤖
        </div>
        <div>
          <div class="flex items-center gap-1.5">
            <h3 class="text-sm font-black text-white">WAYZEN</h3>
            <span class="text-[9px] font-mono px-2 py-0.5 rounded-full bg-brand-cyan/20 text-brand-cyan font-bold border border-brand-cyan/30">AI Buddy</span>
          </div>
          <p class="text-[10px] text-zinc-400">Speaks English + Hinglish • 24/7 Active</p>
        </div>
      </div>
      <div class="flex items-center gap-1.5">
        <button onclick="toggleHinglishMode()" id="wayzenHinglishToggle" class="px-2 py-1 rounded-lg bg-brand-cyan/20 text-brand-cyan text-[10px] font-bold border border-brand-cyan/40" title="Toggle Hinglish">
          🇮🇳 Hinglish
        </button>
        <button onclick="toggleWayzenSound()" id="wayzenSoundBtn" class="p-1.5 rounded-lg text-zinc-400 hover:text-white hover:bg-white/10" title="Sound Effects">
          🔊
        </button>
        <button onclick="toggleWayzenChat()" class="p-1.5 rounded-lg text-zinc-400 hover:text-white hover:bg-white/10">
          <i data-lucide="x" class="w-4 h-4"></i>
        </button>
      </div>
    </div>

    <!-- Quick Action Chips -->
    <div class="p-2 border-b border-white/5 bg-black/30 flex items-center gap-1.5 overflow-x-auto text-[11px] font-semibold text-zinc-300 shrink-0">
      <button onclick="sendWayzenPrompt('Next bus kab aayegi?')" class="px-2.5 py-1 rounded-xl bg-zinc-50 hover:bg-white/15 whitespace-nowrap border border-zinc-200">🚏 Next Bus?</button>
      <button onclick="sendWayzenPrompt('Auto bula do')" class="px-2.5 py-1 rounded-xl bg-zinc-50 hover:bg-white/15 whitespace-nowrap border border-zinc-200">🛺 Auto Bulao</button>
      <button onclick="sendWayzenPrompt('Mera wallet balance kitna hai?')" class="px-2.5 py-1 rounded-xl bg-zinc-50 hover:bg-white/15 whitespace-nowrap border border-zinc-200">💳 Wallet?</button>
      <button onclick="sendWayzenPrompt('Driver OTP do')" class="px-2.5 py-1 rounded-xl bg-zinc-50 hover:bg-white/15 whitespace-nowrap border border-zinc-200">🔢 Driver OTP</button>
      <button onclick="sendWayzenPrompt('Koi discount coupon hai?')" class="px-2.5 py-1 rounded-xl bg-zinc-50 hover:bg-white/15 whitespace-nowrap border border-zinc-200">🎟️ 10% Off</button>
      <button onclick="sendWayzenPrompt('Ek campus joke sunao!')" class="px-2.5 py-1 rounded-xl bg-zinc-50 hover:bg-white/15 whitespace-nowrap border border-zinc-200">😂 Joke Sunao</button>
      <button onclick="sendWayzenPrompt('Library kaise jau?')" class="px-2.5 py-1 rounded-xl bg-zinc-50 hover:bg-white/15 whitespace-nowrap border border-zinc-200">📍 Library Route</button>
    </div>'''

modal_header_new = '''    <!-- Header -->
    <div class="p-4 border-b border-zinc-200 flex items-center justify-between bg-white shrink-0">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-2xl bg-black text-white flex items-center justify-center text-xl shadow-md shrink-0">
          🤖
        </div>
        <div>
          <div class="flex items-center gap-1.5">
            <h3 class="text-base font-black text-black">WAYZEN</h3>
            <span class="text-[10px] font-mono px-2 py-0.5 rounded-full bg-zinc-100 text-black font-black border border-zinc-300">AI Buddy</span>
          </div>
          <p class="text-[11px] text-zinc-600 font-semibold">Speaks English + Hinglish • 24/7 Active</p>
        </div>
      </div>
      <div class="flex items-center gap-1.5">
        <button onclick="toggleHinglishMode()" id="wayzenHinglishToggle" class="px-2.5 py-1 rounded-lg bg-black text-white text-[11px] font-bold border border-black" title="Toggle Hinglish">
          🇮🇳 Hinglish
        </button>
        <button onclick="toggleWayzenSound()" id="wayzenSoundBtn" class="p-1.5 rounded-lg text-black hover:bg-zinc-100 border border-zinc-200" title="Sound Effects">
          🔊
        </button>
        <button onclick="toggleWayzenChat()" class="p-1.5 rounded-lg text-black hover:bg-zinc-100 border border-zinc-200">
          <i data-lucide="x" class="w-4 h-4"></i>
        </button>
      </div>
    </div>

    <!-- Quick Action Chips -->
    <div class="p-2.5 border-b border-zinc-200 bg-zinc-100 flex items-center gap-2 overflow-x-auto text-xs shrink-0">
      <button onclick="sendWayzenPrompt('Next bus kab aayegi?')" class="px-3 py-1.5 rounded-xl bg-white hover:bg-black hover:text-white text-black font-extrabold text-xs border border-zinc-300 shadow-sm transition-all whitespace-nowrap">🚏 Next Bus?</button>
      <button onclick="sendWayzenPrompt('Auto bula do')" class="px-3 py-1.5 rounded-xl bg-white hover:bg-black hover:text-white text-black font-extrabold text-xs border border-zinc-300 shadow-sm transition-all whitespace-nowrap">🛺 Auto Bulao</button>
      <button onclick="sendWayzenPrompt('Mera wallet balance kitna hai?')" class="px-3 py-1.5 rounded-xl bg-white hover:bg-black hover:text-white text-black font-extrabold text-xs border border-zinc-300 shadow-sm transition-all whitespace-nowrap">💳 Wallet?</button>
      <button onclick="sendWayzenPrompt('Driver OTP do')" class="px-3 py-1.5 rounded-xl bg-white hover:bg-black hover:text-white text-black font-extrabold text-xs border border-zinc-300 shadow-sm transition-all whitespace-nowrap">🔢 Driver OTP</button>
      <button onclick="sendWayzenPrompt('Koi discount coupon hai?')" class="px-3 py-1.5 rounded-xl bg-white hover:bg-black hover:text-white text-black font-extrabold text-xs border border-zinc-300 shadow-sm transition-all whitespace-nowrap">🎟️ 10% Off</button>
      <button onclick="sendWayzenPrompt('Ek campus joke sunao!')" class="px-3 py-1.5 rounded-xl bg-white hover:bg-black hover:text-white text-black font-extrabold text-xs border border-zinc-300 shadow-sm transition-all whitespace-nowrap">😂 Joke Sunao</button>
      <button onclick="sendWayzenPrompt('Library kaise jau?')" class="px-3 py-1.5 rounded-xl bg-white hover:bg-black hover:text-white text-black font-extrabold text-xs border border-zinc-300 shadow-sm transition-all whitespace-nowrap">📍 Library Route</button>
    </div>'''

if modal_header_old in content:
    content = content.replace(modal_header_old, modal_header_new)
    print("[PASS] Replaced modal_header")
else:
    print("[WARN] modal_header exact match not found!")

# 3. Update Input Bar in WAYZEN Chat Modal
input_bar_old = '''    <!-- Input Bar -->
    <div class="p-3 border-t border-white/10 bg-[#000000] flex items-center gap-2 shrink-0">
      <input type="text" id="wayzenInput" placeholder="Puchho WAYZEN se (Hindi / English / Hinglish)..." onkeydown="if(event.key==='Enter') sendWayzenMessage()" class="glass-input flex-1 px-4 py-2.5 rounded-xl text-xs font-semibold text-white">
      <button onclick="sendWayzenMessage()" class="btn-gradient p-2.5 rounded-xl text-black font-bold">
        <i data-lucide="send" class="w-4 h-4"></i>
      </button>
    </div>'''

input_bar_new = '''    <!-- Input Bar -->
    <div class="p-3.5 border-t border-zinc-200 bg-white flex items-center gap-2 shrink-0">
      <input type="text" id="wayzenInput" placeholder="Puchho WAYZEN se (Hindi / English / Hinglish)..." onkeydown="if(event.key==='Enter') sendWayzenMessage()" class="bg-zinc-100 border border-zinc-300 flex-1 px-4 py-2.5 rounded-xl text-xs font-bold text-black placeholder:text-zinc-500 focus:outline-none focus:border-black">
      <button onclick="sendWayzenMessage()" class="p-2.5 rounded-xl bg-black text-white hover:bg-zinc-800 font-bold transition-all shadow-md">
        <i data-lucide="send" class="w-4 h-4"></i>
      </button>
    </div>'''

if input_bar_old in content:
    content = content.replace(input_bar_old, input_bar_new)
    print("[PASS] Replaced input_bar")
else:
    print("[WARN] input_bar exact match not found!")

# 4. Update renderWayzenMessages to have BOLD black text
render_wayzen_old = '''function renderWayzenMessages() {
      const container = document.getElementById('wayzenChatMessages');
      if (!container) return;
      container.innerHTML = wayzenChatLog.map(m => `
        <div class="flex flex-col ${m.sender === 'user' ? 'items-end' : 'items-start'}">
          <div class="max-w-[85%] p-3.5 rounded-2xl ${
            m.sender === 'user' 
              ? 'bg-gradient-to-r from-brand-cyan to-brand-purple text-black font-semibold rounded-br-none shadow-md' 
              : 'glass-panel text-white rounded-bl-none border border-brand-cyan/25 shadow-md'
          }">
            <p class="leading-relaxed">${m.text}</p>
            ${m.actionBtn ? `
              <div class="pt-2">
                <button onclick="${m.actionBtn.onclick}" class="px-3 py-1.5 rounded-xl bg-brand-cyan/20 border border-brand-cyan/40 text-brand-cyan hover:bg-brand-cyan hover:text-black font-extrabold text-[11px] transition-all">
                  ${m.actionBtn.label}
                </button>
              </div>
            ` : ''}
          </div>
          <span class="text-[9px] text-zinc-500 mt-1 px-1 flex items-center gap-1">
            ${m.sender === 'user' ? 'You' : '🤖 WAYZEN AI'}
          </span>
        </div>
      `).join('');
      container.scrollTop = container.scrollHeight;
    }'''

render_wayzen_new = '''function renderWayzenMessages() {
      const container = document.getElementById('wayzenChatMessages');
      if (!container) return;
      container.innerHTML = wayzenChatLog.map(m => `
        <div class="flex flex-col ${m.sender === 'user' ? 'items-end' : 'items-start'}">
          <div class="max-w-[85%] p-4 rounded-2xl ${
            m.sender === 'user' 
              ? 'bg-black text-white font-bold rounded-br-none shadow-md' 
              : 'bg-white border-2 border-black text-black font-bold rounded-bl-none shadow-md'
          }">
            <p class="leading-relaxed font-bold text-black text-sm">${m.text}</p>
            ${m.actionBtn ? `
              <div class="pt-2.5">
                <button onclick="${m.actionBtn.onclick}" class="px-3.5 py-2 rounded-xl bg-black text-white hover:bg-zinc-800 font-black text-xs shadow-md transition-all">
                  ${m.actionBtn.label}
                </button>
              </div>
            ` : ''}
          </div>
          <span class="text-[10px] text-zinc-600 font-extrabold mt-1 px-1 flex items-center gap-1">
            ${m.sender === 'user' ? 'You' : '🤖 WAYZEN AI'}
          </span>
        </div>
      `).join('');
      container.scrollTop = container.scrollHeight;
    }'''

if render_wayzen_old in content:
    content = content.replace(render_wayzen_old, render_wayzen_new)
    print("[PASS] Replaced renderWayzenMessages")
else:
    print("[WARN] renderWayzenMessages exact match not found!")

# 5. Update Category Filter HTML
cat_filter_old = '''        <!-- Vehicle Category Filter Bar -->
        <div class="grid grid-cols-4 p-1 rounded-xl bg-black/40 border border-zinc-200 text-[11px] font-extrabold text-zinc-400">
          <button data-type="all" onclick="filterFleetCategory('all', this)" class="fleet-cat-btn py-1 rounded-lg bg-white/15 text-brand-cyan shadow-sm">All</button>
          <button data-type="bus" onclick="filterFleetCategory('bus', this)" class="fleet-cat-btn py-1 rounded-lg hover:text-white">🚌 Shuttles</button>
          <button data-type="auto" onclick="filterFleetCategory('auto', this)" class="fleet-cat-btn py-1 rounded-lg hover:text-white">🛺 Autos</button>
          <button data-type="ev" onclick="filterFleetCategory('ev', this)" class="fleet-cat-btn py-1 rounded-lg hover:text-white">⚡ EVs</button>
        </div>'''

cat_filter_new = '''        <!-- Vehicle Category Filter Bar -->
        <div class="grid grid-cols-4 gap-1.5 p-1.5 rounded-2xl bg-zinc-100 border border-zinc-200 text-xs font-bold">
          <button data-type="all" onclick="filterFleetCategory('all', this)" class="fleet-cat-btn py-2 rounded-xl bg-black text-white shadow-sm font-black transition-all flex items-center justify-center">All</button>
          <button data-type="bus" onclick="filterFleetCategory('bus', this)" class="fleet-cat-btn py-2 rounded-xl text-zinc-700 hover:text-black font-extrabold transition-all flex items-center justify-center gap-1">🚌 Shuttles</button>
          <button data-type="auto" onclick="filterFleetCategory('auto', this)" class="fleet-cat-btn py-2 rounded-xl text-zinc-700 hover:text-black font-extrabold transition-all flex items-center justify-center gap-1">🛺 Autos</button>
          <button data-type="ev" onclick="filterFleetCategory('ev', this)" class="fleet-cat-btn py-2 rounded-xl text-zinc-700 hover:text-black font-extrabold transition-all flex items-center justify-center gap-1">⚡ EVs</button>
        </div>'''

if cat_filter_old in content:
    content = content.replace(cat_filter_old, cat_filter_new)
    print("[PASS] Replaced cat_filter HTML")
else:
    print("[WARN] cat_filter HTML exact match not found!")

# 6. Update filterFleetCategory function
filter_fn_old = '''function filterFleetCategory(cat, btn) {
      currentFilterType = cat;
      document.querySelectorAll('.fleet-cat-btn').forEach(b => {
        b.className = 'fleet-cat-btn py-1.5 rounded-xl hover:text-white';
      });
      if (btn) btn.className = 'fleet-cat-btn py-1.5 rounded-xl bg-white/15 text-brand-cyan shadow-sm';
      renderFleetList();
    }'''

filter_fn_new = '''function filterFleetCategory(cat, btn) {
      currentFilterType = cat;
      document.querySelectorAll('.fleet-cat-btn').forEach(b => {
        b.className = 'fleet-cat-btn py-2 rounded-xl text-zinc-700 hover:text-black font-extrabold transition-all flex items-center justify-center gap-1';
      });
      if (btn) btn.className = 'fleet-cat-btn py-2 rounded-xl bg-black text-white shadow-sm font-black transition-all flex items-center justify-center gap-1';
      renderFleetList();
    }'''

if filter_fn_old in content:
    content = content.replace(filter_fn_old, filter_fn_new)
    print("[PASS] Replaced filterFleetCategory function")
else:
    print("[WARN] filterFleetCategory function exact match not found!")

# 7. Update fleetSectionTitle HTML
sec_title_old = '''        <!-- Fleet Section Heading -->
        <div class="flex items-center justify-between text-xs font-bold text-zinc-400 px-1 pt-1">
          <span id="fleetSectionTitle" class="text-white font-black text-xs flex items-center gap-1.5">
            🟢 Active Moving Shuttles (8)
          </span>
          <span id="fleetSectionSub" class="text-[10px] text-brand-cyan font-mono">
            Real-time GPS • Cruise 18 km/h
          </span>
        </div>'''

sec_title_new = '''        <!-- Fleet Section Heading -->
        <div class="flex items-center justify-between text-xs font-bold text-zinc-700 px-1 pt-1">
          <span id="fleetSectionTitle" class="text-black font-black text-xs flex items-center gap-1.5">
            🚍 Active Moving Shuttles (8)
          </span>
          <span id="fleetSectionSub" class="text-[10px] text-zinc-700 font-mono font-bold">
            Real-time GPS • Cruise 18 km/h
          </span>
        </div>'''

if sec_title_old in content:
    content = content.replace(sec_title_old, sec_title_new)
    print("[PASS] Replaced fleetSectionTitle HTML")
else:
    print("[WARN] fleetSectionTitle HTML exact match not found!")

# 8. Update setFleetViewMode
viewmode_old = '''      if (mode === 'moving') {
        if (btnMoving) btnMoving.className = 'py-2 rounded-xl bg-black text-white font-black shadow-md flex items-center justify-center gap-1.5 transition-all';
        if (btnParked) btnParked.className = 'py-2 rounded-xl text-zinc-400 hover:text-white font-bold flex items-center justify-center gap-1.5 transition-all';
        if (secTitle) secTitle.innerHTML = '🟢 Active Moving Shuttles (8)';
        if (secSub) secSub.textContent = 'Real-time GPS • Cruise 18 km/h';
      } else {
        if (btnMoving) btnMoving.className = 'py-2 rounded-xl text-zinc-400 hover:text-white font-bold flex items-center justify-center gap-1.5 transition-all';
        if (btnParked) btnParked.className = 'py-2 rounded-xl bg-black text-white font-black shadow-md flex items-center justify-center gap-1.5 transition-all';
        if (secTitle) secTitle.innerHTML = '🅿️ Scheduled & Parked Fleet (4)';
        if (secSub) secSub.textContent = 'Fixed Bay Departure Times';
      }'''

viewmode_new = '''      if (mode === 'moving') {
        if (btnMoving) btnMoving.className = 'py-2 rounded-xl bg-black text-white font-black shadow-md flex items-center justify-center gap-1.5 transition-all';
        if (btnParked) btnParked.className = 'py-2 rounded-xl text-zinc-700 hover:text-black font-extrabold flex items-center justify-center gap-1.5 transition-all';
        if (secTitle) secTitle.innerHTML = '🚍 Active Moving Shuttles (8)';
        if (secSub) secSub.textContent = 'Real-time GPS • Cruise 18 km/h';
      } else {
        if (btnMoving) btnMoving.className = 'py-2 rounded-xl text-zinc-700 hover:text-black font-extrabold flex items-center justify-center gap-1.5 transition-all';
        if (btnParked) btnParked.className = 'py-2 rounded-xl bg-black text-white font-black shadow-md flex items-center justify-center gap-1.5 transition-all';
        if (secTitle) secTitle.innerHTML = '🅿️ Scheduled & Parked Fleet (4)';
        if (secSub) secSub.textContent = 'Fixed Bay Departure Times';
      }'''

if viewmode_old in content:
    content = content.replace(viewmode_old, viewmode_new)
    print("[PASS] Replaced setFleetViewMode")
else:
    print("[WARN] setFleetViewMode exact match not found!")

# 9. Update moving vehicle card HTML inside renderFleetList()
# Find the exact moving vehicle card template in renderFleetList()
moving_card_match = re.search(r'container\.innerHTML = filtered\.map\(v => \{([\s\S]*?)\}\)\.join\(\'\'\);', content)
if moving_card_match:
    old_moving_block = moving_card_match.group(0)
    new_moving_block = '''container.innerHTML = filtered.map(v => {
        const isSelected = v.id === selectedVehicleId;
        const etaMin = Math.max(1, Math.round(v.s / 800));
        const occupancyPct = Math.round((v.occupiedSeats / v.totalSeats) * 100);
        const seatBadgeClass = v.availableSeats > 2 ? 'bg-zinc-100 text-black border border-zinc-300 font-extrabold' : (v.availableSeats > 0 ? 'bg-zinc-200 text-black border border-zinc-300 font-extrabold' : 'bg-zinc-800 text-white border border-black font-extrabold');

        return `
          <div onclick="selectVehicle('${v.id}')" class="p-4 rounded-2xl glass-card cursor-pointer border ${isSelected ? 'border-black ring-2 ring-black shadow-lg' : 'border-zinc-200 shadow-sm'} bg-white text-black hover:border-black space-y-3 transition-all">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <div class="w-11 h-11 rounded-2xl bg-zinc-100 border border-zinc-200 flex items-center justify-center text-2xl shadow-sm">
                  ${v.icon}
                </div>
                <div>
                  <h4 class="text-sm font-black text-[#DC2626]">${v.name}</h4>
                  <p class="text-[11px] text-black font-black uppercase tracking-wider">${v.typeName}</p>
                  <p class="text-[11px] text-zinc-700 font-mono font-bold">${v.plate} • 👨‍✈️ ${v.driver} (★ ${v.rating})</p>
                </div>
              </div>
              <div class="text-right">
                <span class="text-xs font-black text-black block">${etaMin} min ETA</span>
                <p class="text-[10px] text-zinc-600 font-mono font-bold">${v.speed} km/h • ${v.battery}% 🔋</p>
              </div>
            </div>

            <!-- Live Upcoming Block Stops & Precise Time Calculation -->
            <div class="p-2.5 rounded-xl bg-zinc-100 border border-zinc-200 space-y-1.5">
              <div class="flex items-center justify-between text-[11px]">
                <span class="text-black font-extrabold">⏱️ Upcoming Block Arrival Timetable:</span>
                <span class="text-black font-mono font-black">~18 km/h</span>
              </div>
              <div class="space-y-1">
                ${(() => {
                  const upcoming = getVehicleUpcomingStops(v);
                  if (!upcoming || upcoming.length === 0) return '<p class="text-[11px] text-zinc-600 font-bold">Cruising campus loop</p>';
                  return upcoming.map((u, i) => `
                    <div class="flex items-center justify-between ${i === 0 ? 'text-black font-black text-xs' : 'text-zinc-700 font-bold text-[11px]'}">
                      <span class="flex items-center gap-1.5 truncate max-w-[180px]">
                        <span>${u.icon}</span>
                        <span class="truncate">${u.name}</span>
                      </span>
                      <span class="${i === 0 ? 'text-[#DC2626] font-black' : 'text-zinc-800 font-bold'} font-mono whitespace-nowrap">
                        ${u.mins} min (${u.timeStr})
                      </span>
                    </div>
                  `).join('');
                })()}
              </div>
            </div>

            <!-- Seat Occupancy Meter -->
            <div class="space-y-1.5 bg-zinc-100 p-2.5 rounded-xl border border-zinc-200">
              <div class="flex items-center justify-between text-[11px]">
                <span class="text-zinc-800 font-extrabold">Available Seats:</span>
                <span class="font-mono font-black px-2.5 py-0.5 rounded-full border ${seatBadgeClass}">
                  💺 ${v.availableSeats} of ${v.totalSeats} free
                </span>
              </div>
              <div class="w-full h-2 rounded-full bg-zinc-300 overflow-hidden">
                <div class="h-full rounded-full bg-black" style="width: ${occupancyPct}%"></div>
              </div>
            </div>

            <!-- Action buttons -->
            <div class="flex items-center justify-between pt-1 border-t border-zinc-200 text-xs">
              <span class="text-zinc-700 font-extrabold">Fare: <strong class="text-black font-mono font-black text-sm">₹${v.fare}</strong></span>
              <div class="flex items-center gap-1.5">
                <button onclick="event.stopPropagation(); openDriverChat('${v.id}')" class="px-3 py-1.5 rounded-xl bg-zinc-100 hover:bg-zinc-200 text-black font-extrabold border border-zinc-300 flex items-center gap-1 transition-all">
                  💬 Chat
                </button>
                <button onclick="event.stopPropagation(); openSeatLayoutModal('${v.id}')" class="px-3 py-1.5 rounded-xl bg-zinc-100 hover:bg-zinc-200 text-black font-extrabold border border-zinc-300 flex items-center gap-1 transition-all">
                  💺 Seats
                </button>
                <button onclick="event.stopPropagation(); bookSpecificVehicle('${v.id}')" class="px-4 py-1.5 rounded-xl bg-black hover:bg-zinc-800 text-white font-black shadow-md flex items-center gap-1 transition-all">
                  ⚡ Book
                </button>
              </div>
            </div>
          </div>
        `;
      }).join('');'''
    content = content.replace(old_moving_block, new_moving_block)
    print("[PASS] Replaced moving vehicle card template in renderFleetList")
else:
    print("[WARN] moving_card_match not found!")

# 10. Ensure initCampusMap is called on DOMContentLoaded
dom_old = '''window.addEventListener('DOMContentLoaded', () => {
      updateUserAccountPill();
      updateWalletDisplay();
      startSimulationEngine();'''

dom_new = '''window.addEventListener('DOMContentLoaded', () => {
      updateUserAccountPill();
      updateWalletDisplay();
      if (!map) {
        initCampusMap();
      }
      startSimulationEngine();'''

if dom_old in content:
    content = content.replace(dom_old, dom_new)
    print("[PASS] Added initCampusMap to DOMContentLoaded")
else:
    print("[WARN] dom_old exact match not found!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated index.html successfully.")

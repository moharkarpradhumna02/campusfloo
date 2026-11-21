import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# =========================================================================
# 1. FIX initCampusMap() TO RESTORE ALL RUNNING VEHICLES ON MAP
# =========================================================================
init_start = text.find('function initCampusMap() {')
init_end = text.find('let currentMapTileLayers = [];', init_start)

new_init_map = '''function initCampusMap() {
      if (map) return;
      map = L.map('campusMap', { zoomControl: false }).setView([31.2540, 75.7055], 16);

      // Student Map Tap to Share Live Location
      map.on('click', e => {
        if (isLocationPickerActive) {
          setStudentLiveLocation(e.latlng.lat, e.latlng.lng);
          toggleLocationPickerMode(false);
        }
      });
      setMapTheme('dark');

      // Draw all 4 Multi-Transit Routes on LPU Roads
      Object.keys(LPU_ROUTES).forEach(k => {
        const r = LPU_ROUTES[k];
        const poly = L.polyline(r.coords, {
          color: r.color,
          weight: 4.5,
          opacity: 0.85,
          dashArray: k === 'route_emerald' ? '6, 6' : (k === 'route_amber' ? '4, 4' : null),
          lineCap: 'round'
        }).addTo(map);

        poly.bindTooltip(`<span class="font-bold text-xs">${r.name} (${r.code})</span>`, { sticky: true });
        routePolylineLayers[k] = poly;
      });

      routePolylineLayer = routePolylineLayers.route_purple;

      // 1. Campus Landmark & Stop Markers
      LPU_STOPS.forEach(stop => {
        const icon = L.divIcon({
          className: 'pulse-marker-icon',
          html: `
            <div class="relative group cursor-pointer flex items-center justify-center">
              <div class="w-7 h-7 rounded-xl bg-white border border-black text-xs flex items-center justify-center shadow-md hover:scale-125 transition-transform">
                <span>${stop.icon || '📍'}</span>
              </div>
              <div class="absolute -bottom-6 left-1/2 -translate-x-1/2 whitespace-nowrap px-2 py-0.5 rounded-md bg-black text-white border border-zinc-700 text-[9px] font-black pointer-events-none hidden group-hover:block z-30">
                ${stop.name}
              </div>
            </div>
          `,
          iconSize: [28, 28],
          iconAnchor: [14, 14]
        });

        const marker = L.marker([stop.lat, stop.lng], { icon }).addTo(map);
        marker.bindPopup(`
          <div class="p-3 text-xs font-sans space-y-1.5 min-w-[240px]">
            <div class="flex items-center gap-2 border-b border-zinc-200 pb-1.5">
              <span class="text-xl">${stop.icon || '📍'}</span>
              <div>
                <strong class="text-black font-black text-sm block">${stop.name}</strong>
                <span class="text-[11px] font-mono text-black font-extrabold block">Code: ${stop.code}</span>
              </div>
            </div>
            <p class="text-[12px] text-zinc-700 font-semibold leading-snug">${stop.desc}</p>
            <div class="pt-1.5 flex items-center justify-between text-[10px] font-mono text-black border-t border-zinc-200">
              <span class="font-bold">● LPU Active Station</span>
              <button onclick="filterByStop('${stop.id}')" class="text-black underline font-black">Find Shuttles →</button>
            </div>
          </div>
        `);
        stopMarkers.push(marker);
      });

      // Fit map smoothly to the road loop
      if (routePolylineLayer) {
        setTimeout(() => map.fitBounds(routePolylineLayer.getBounds().pad(0.08)), 200);
      }

      // 2. Active Running Fleet Markers (All 8 Moving Vehicles)
      FLEET.forEach(v => {
        const pos = getCoordOnRoute(v.routeId, v.s);
        const icon = L.divIcon({
          className: 'pulse-marker-icon',
          html: `
            <div class="relative group cursor-pointer flex items-center justify-center" onclick="selectVehicle('${v.id}')">
              <div class="w-10 h-10 rounded-2xl bg-white border-2 border-black text-sm flex items-center justify-center shadow-xl hover:scale-125 transition-transform" style="box-shadow: 0 4px 14px rgba(0,0,0,0.3);">
                <span class="text-base leading-none select-none">${v.icon}</span>
                <div class="bus-heading-needle" id="needle_${v.id}" style="transform: rotate(${pos.heading}deg)"></div>
              </div>
              <div class="absolute -top-7 left-1/2 -translate-x-1/2 whitespace-nowrap px-2 py-0.5 rounded-full bg-black text-white border border-zinc-700 text-[9px] font-black shadow-xl flex items-center gap-1 z-20 pointer-events-none">
                <span>${v.category === 'auto' ? 'Auto' : (v.category === 'ev' ? 'EV' : 'Bus')}</span>
                <span class="w-1 h-1 rounded-full bg-zinc-500"></span>
                <span class="font-mono text-white">💺 ${v.availableSeats}</span>
              </div>
            </div>
          `,
          iconSize: [40, 40],
          iconAnchor: [20, 20]
        });

        const m = L.marker([pos.lat, pos.lng], { icon }).addTo(map);

        const etaMin = Math.max(1, Math.round(v.s / 800));
        const occupancyPct = Math.round((v.occupiedSeats / v.totalSeats) * 100);

        const popupContent = `
          <div class="p-3.5 space-y-2.5 min-w-[270px] text-xs font-sans">
            <div class="flex items-center justify-between border-b border-zinc-200 pb-2">
              <div class="flex items-center gap-2">
                <span class="text-2xl">${v.icon}</span>
                <div>
                  <h4 class="font-black text-black text-sm tracking-tight">${v.name}</h4>
                  <span class="text-[10px] font-bold text-zinc-600 uppercase tracking-wider">${v.typeName}</span>
                </div>
              </div>
              <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-zinc-100 text-black border border-zinc-300 font-bold">
                💺 ${v.availableSeats} Free
              </span>
            </div>

            <div class="space-y-1">
              <div class="flex items-center justify-between text-[10px] font-bold text-zinc-700">
                <span>Seats Occupancy: <strong>${v.occupiedSeats} / ${v.totalSeats}</strong></span>
                <span class="text-black font-mono font-bold">${occupancyPct}% Full</span>
              </div>
              <div class="w-full h-2 rounded-full bg-zinc-200 overflow-hidden">
                <div class="h-full rounded-full ${occupancyPct > 85 ? 'bg-zinc-500' : 'bg-black'}" style="width: ${occupancyPct}%"></div>
              </div>
            </div>

            <!-- Live Upcoming Blocks & Clock Arrival Time in Popup -->
            <div class="p-2 rounded-xl bg-zinc-50 border border-zinc-200 space-y-1">
              <div class="flex items-center justify-between text-[10px]">
                <span class="text-zinc-700 font-bold">⏱️ Upcoming Block Arrival:</span>
                <span class="text-black font-mono font-bold">${v.speed} km/h cruise</span>
              </div>
              <div class="space-y-0.5">
                ${(() => {
                  const upcoming = getVehicleUpcomingStops(v);
                  if (!upcoming || upcoming.length === 0) return '<p class="text-[10px] text-zinc-400">Cruising campus loop</p>';
                  return upcoming.map((u, i) => `
                    <div class="flex items-center justify-between ${i === 0 ? 'text-black font-black text-[11px]' : 'text-zinc-600 text-[10px]'}">
                      <span class="flex items-center gap-1.5 truncate max-w-[170px]">
                        <span>${u.icon}</span>
                        <span class="truncate">${u.name}</span>
                      </span>
                      <span class="${i === 0 ? 'text-black font-extrabold' : 'text-zinc-500'} font-mono whitespace-nowrap">
                        ${u.mins} min (${u.timeStr})
                      </span>
                    </div>
                  `).join('');
                })()}
              </div>
            </div>

            <div class="p-2 rounded-xl bg-zinc-50 border border-zinc-200 flex items-center justify-between text-[11px]">
              <div>
                <p class="font-bold text-black flex items-center gap-1.5">
                  <span>👨‍✈️ ${v.driver}</span>
                  <span class="text-black font-mono text-[10px]">★ ${v.rating}</span>
                </p>
                <p class="text-[10px] text-zinc-600 font-mono font-semibold">${v.plate} • ${v.phone}</p>
              </div>
              <button onclick="callDriver('${v.phone}', '${v.driver}')" class="px-2.5 py-1 rounded-lg bg-zinc-100 text-black hover:bg-zinc-200 border border-zinc-300 font-bold flex items-center gap-1" title="Call Driver">
                📞 Call
              </button>
            </div>

            <div class="grid grid-cols-2 gap-1.5 pt-1">
              <button onclick="openDriverChat('${v.id}')" class="btn !py-2 px-2.5 rounded-xl bg-black hover:bg-zinc-800 text-white font-black text-[11px] flex items-center justify-center gap-1 shadow-sm">
                💬 Chat Driver
              </button>
              <button onclick="openSeatLayoutModal('${v.id}')" class="btn !py-2 px-2.5 rounded-xl bg-zinc-100 hover:bg-zinc-200 text-black border border-zinc-300 font-black text-[11px] flex items-center justify-center gap-1 shadow-sm">
                💺 View Seats
              </button>
            </div>
          </div>
        `;

        m.bindPopup(popupContent, { maxWidth: 320 });
        m.on('click', () => selectVehicle(v.id));
        vehicleMarkers[v.id] = m;
      });

      // 3. Render Parked & Scheduled Standby Fleet on Map
      PARKED_FLEET.forEach(pv => {
        const icon = L.divIcon({
          className: 'pulse-marker-icon',
          html: `
            <div class="relative group cursor-pointer flex items-center justify-center" onclick="selectParkedVehicle('${pv.id}')">
              <div class="w-10 h-10 rounded-2xl bg-zinc-900 border-2 border-black text-sm flex items-center justify-center shadow-xl hover:scale-125 transition-transform" style="box-shadow: 0 4px 14px rgba(0,0,0,0.35);">
                <span class="text-base leading-none select-none">${pv.icon}</span>
              </div>
              <div class="absolute -top-7 left-1/2 -translate-x-1/2 whitespace-nowrap px-2 py-0.5 rounded-full bg-black text-white border border-zinc-700 text-[9px] font-mono font-bold shadow-xl flex items-center gap-1 z-20 pointer-events-none">
                <span>🅿️ ${pv.name.split(' ')[0]}</span>
                <span class="w-1 h-1 rounded-full bg-zinc-500"></span>
                <span class="font-mono">💺 ${pv.availableSeats}</span>
              </div>
            </div>
          `,
          iconSize: [40, 40],
          iconAnchor: [20, 20]
        });

        const m = L.marker([pv.lat, pv.lng], { icon }).addTo(map);
        parkedMarkers[pv.id] = m;
        updateParkedMarkerPopup(pv.id);
      });
    }

    '''

text = text[:init_start] + new_init_map + text[init_end:]

# =========================================================================
# 2. FIX FILTER BAR SEGMENTED CONTROL (HTML & JS)
# =========================================================================
old_filter_pattern = r'<div class="grid grid-cols-4 gap-1 p-1 bg-zinc-50[^"]*">[\s\S]*?</div>\s*<!-- Compact System Delay Status Banner -->'
new_filter_bar = '''<div class="grid grid-cols-4 gap-1.5 p-1.5 bg-zinc-100 rounded-2xl border border-zinc-200 text-xs font-bold text-zinc-700">
          <button data-type="all" onclick="filterFleetCategory('all', this)" class="fleet-cat-btn py-1.5 rounded-xl bg-black text-white shadow-sm font-black">All</button>
          <button data-type="bus" onclick="filterFleetCategory('bus', this)" class="fleet-cat-btn py-1.5 rounded-xl text-zinc-700 hover:text-black font-extrabold transition-all">🚌 Shuttles</button>
          <button data-type="auto" onclick="filterFleetCategory('auto', this)" class="fleet-cat-btn py-1.5 rounded-xl text-zinc-700 hover:text-black font-extrabold transition-all">🛺 Autos</button>
          <button data-type="ev" onclick="filterFleetCategory('ev', this)" class="fleet-cat-btn py-1.5 rounded-xl text-zinc-700 hover:text-black font-extrabold transition-all">⚡ EVs</button>
        </div>

        <!-- Compact System Delay Status Banner -->'''

text = re.sub(old_filter_pattern, new_filter_bar, text)

# JS filterFleetCategory
old_filter_func = r'function filterFleetCategory\(cat, btn\) \{[\s\S]*?renderFleetList\(\);\s*\}'
new_filter_func = '''function filterFleetCategory(cat, btn) {
      currentFilterType = cat;
      document.querySelectorAll('.fleet-cat-btn').forEach(b => {
        b.className = 'fleet-cat-btn py-1.5 rounded-xl text-zinc-700 hover:text-black font-extrabold transition-all';
      });
      if (btn) {
        btn.className = 'fleet-cat-btn py-1.5 rounded-xl bg-black text-white shadow-sm font-black transition-all';
      }
      renderFleetList();
    }'''
text = re.sub(old_filter_func, new_filter_func, text)

# =========================================================================
# 3. FIX WAYZEN AI: MAKE BOT TEXT BOLD, HEADER BLACK, CHIPS CRISP
# =========================================================================
# WAYZEN header title & subtitles
text = text.replace(
    '<h3 class="text-sm font-black text-white">WAYZEN</h3>',
    '<h3 class="text-base font-black text-black">WAYZEN</h3>'
)
text = text.replace(
    '<span class="text-[9px] font-mono px-2 py-0.5 rounded-full bg-brand-cyan/20 text-brand-cyan font-bold border border-brand-cyan/30">AI Buddy</span>',
    '<span class="text-[10px] font-mono px-2.5 py-0.5 rounded-full bg-zinc-100 text-black font-black border border-zinc-300">AI Buddy</span>'
)
text = text.replace(
    '<p class="text-[10px] text-zinc-400">Speaks English + Hinglish • 24/7 Active</p>',
    '<p class="text-[11px] text-zinc-600 font-bold">Speaks English + Hinglish • 24/7 Active</p>'
)
text = text.replace(
    '<button onclick="toggleHinglishMode()" id="wayzenHinglishToggle" class="px-2 py-1 rounded-lg bg-brand-cyan/20 text-brand-cyan text-[10px] font-bold border border-brand-cyan/40" title="Toggle Hinglish">',
    '<button onclick="toggleHinglishMode()" id="wayzenHinglishToggle" class="px-2.5 py-1 rounded-xl bg-zinc-100 text-black text-[11px] font-black border border-zinc-300" title="Toggle Hinglish">'
)

# WAYZEN quick action chips
old_wayzen_chips = text[text.find('<!-- Quick Action Chips -->'):text.find('<!-- Chat Messages Stream -->')]
new_wayzen_chips = '''<!-- Quick Action Chips -->
    <div class="p-2.5 border-b border-zinc-200 bg-zinc-100 flex items-center gap-2 overflow-x-auto text-xs font-bold text-zinc-800 shrink-0">
      <button onclick="sendWayzenPrompt('Next bus kab aayegi?')" class="px-3 py-1.5 rounded-xl bg-white hover:bg-zinc-200 text-black font-extrabold text-xs whitespace-nowrap border border-zinc-300 shadow-sm transition-all">🚏 Next Bus?</button>
      <button onclick="sendWayzenPrompt('Auto bula do')" class="px-3 py-1.5 rounded-xl bg-white hover:bg-zinc-200 text-black font-extrabold text-xs whitespace-nowrap border border-zinc-300 shadow-sm transition-all">🛺 Auto Bulao</button>
      <button onclick="sendWayzenPrompt('Mera wallet balance kitna hai?')" class="px-3 py-1.5 rounded-xl bg-white hover:bg-zinc-200 text-black font-extrabold text-xs whitespace-nowrap border border-zinc-300 shadow-sm transition-all">💳 Wallet?</button>
      <button onclick="sendWayzenPrompt('Mera ride verification OTP kya hai?')" class="px-3 py-1.5 rounded-xl bg-white hover:bg-zinc-200 text-black font-extrabold text-xs whitespace-nowrap border border-zinc-300 shadow-sm transition-all">🔢 Driver OTP</button>
    </div>

    '''
text = text.replace(old_wayzen_chips, new_wayzen_chips)

# WAYZEN speech bubble (Screenshot 1)
old_speech_bubble = text[text.find('id="wayzenSpeechBubble"'):text.find('<!-- Cute Floating Button -->')]
new_speech_bubble = '''id="wayzenSpeechBubble" class="hidden fixed bottom-24 right-6 z-[9990] max-w-xs p-3.5 rounded-2xl bg-white border border-zinc-300 shadow-2xl animate-pop-in cursor-pointer" onclick="toggleWayzenChat()">
    <div class="flex items-center justify-between gap-2 border-b border-zinc-200 pb-1.5">
      <div class="flex items-center gap-1.5 text-black font-black text-xs">
        <span class="animate-bounce">🤖</span>
        <span>WAYZEN AI</span>
      </div>
      <button onclick="event.stopPropagation(); closeWayzenBubble();" class="text-zinc-400 hover:text-black font-black text-sm">✕</button>
    </div>
    <p id="wayzenBubbleText" class="text-xs text-black mt-2 leading-relaxed font-black">
      👋 Oye hero! 8:30 AM class ke liye late ho raha hai? Bus ka ETA puch le! 🚌
    </p>
  </div>

  '''
text = text.replace(old_speech_bubble, new_speech_bubble)

# WAYZEN chat messages renderer: make bot text BOLD, crystal clear black
old_render_wayzen = text[text.find('function renderWayzenMessages() {'):text.find('function sendWayzenPrompt(text) {')]
new_render_wayzen = '''function renderWayzenMessages() {
      const container = document.getElementById('wayzenChatMessages');
      if (!container) return;
      container.innerHTML = wayzenChatLog.map(m => `
        <div class="flex flex-col ${m.sender === 'user' ? 'items-end' : 'items-start'}">
          <div class="max-w-[85%] p-3.5 rounded-2xl ${
            m.sender === 'user' 
              ? 'bg-black text-white font-bold rounded-br-none shadow-md' 
              : 'bg-zinc-50 text-black font-extrabold rounded-bl-none border border-zinc-200 shadow-sm text-sm'
          }">
            <p class="leading-relaxed font-bold text-black text-sm">${m.text}</p>
            ${m.actionBtn ? `
              <div class="pt-2.5">
                <button onclick="${m.actionBtn.onclick}" class="btn !py-2 px-3 rounded-xl bg-black hover:bg-zinc-800 text-white font-black text-xs transition-all shadow-md">
                  ${m.actionBtn.label}
                </button>
              </div>
            ` : ''}
          </div>
          <span class="text-[10px] font-bold text-zinc-600 mt-1 px-1 flex items-center gap-1">
            ${m.sender === 'user' ? '👤 You' : '🤖 WAYZEN AI'}
          </span>
        </div>
      `).join('');
      container.scrollTop = container.scrollHeight;
    }

    '''
text = text.replace(old_render_wayzen, new_render_wayzen)

# Ensure WAYZEN input text is black and high contrast
text = text.replace(
    'class="w-full pl-4 pr-10 py-2.5 rounded-xl bg-zinc-50 border border-zinc-200 text-xs font-semibold text-white focus:outline-none focus:border-brand-cyan"',
    'class="w-full pl-4 pr-10 py-3 rounded-xl bg-zinc-50 border border-zinc-300 text-xs font-bold text-black focus:outline-none focus:border-black"'
)

# Vehicle card name in moving fleet list
text = text.replace(
    '<h4 class="text-xs font-black text-[#DC2626]">${v.name}</h4>',
    '<h4 class="text-sm font-black text-black tracking-tight">${v.name}</h4>'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("fix_everything_perfect.py completed successfully!")

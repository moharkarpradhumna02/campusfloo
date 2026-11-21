import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Fix sidebarTransitPassCard (Screenshot 1 & 10)
old_sidebar_card = text[text.find('id="sidebarTransitPassCard"'):text.find('<!-- Fleet Section Heading -->')]
new_sidebar_card = '''id="sidebarTransitPassCard" class="p-4 rounded-2xl bg-black text-white border border-zinc-800 shadow-xl relative overflow-hidden">
          <div class="flex items-center justify-between mb-3">
            <div class="flex items-center gap-2.5">
              <div class="w-8 h-8 rounded-xl bg-zinc-800 border border-zinc-700 flex items-center justify-center text-white font-black">
                <i data-lucide="wallet" class="w-4 h-4 text-white"></i>
              </div>
              <div>
                <p class="text-[9px] font-black uppercase tracking-wider text-zinc-400">Campus Smart Pass</p>
                <p class="text-sm font-black text-white truncate max-w-[150px]" id="sidebarPassName">Student</p>
              </div>
            </div>
            <span class="text-[10px] font-mono px-2.5 py-0.5 rounded-full bg-zinc-800 text-white border border-zinc-700 font-bold flex items-center gap-1.5">
              <span class="w-1.5 h-1.5 rounded-full bg-white animate-pulse"></span> Active
            </span>
          </div>
          <div class="flex items-end justify-between pt-1 border-t border-zinc-800/80">
            <div>
              <p class="text-[9px] text-zinc-400 uppercase font-bold tracking-wider">Wallet Balance</p>
              <p class="text-2xl font-black text-white font-mono" id="sidebarPassBalance">₹ 240.00</p>
              <p class="text-[10px] text-zinc-400 font-mono" id="sidebarPassId">STU-2024-8891</p>
            </div>
            <div class="flex items-center gap-2">
              <button onclick="openWalletModal()" class="px-3 py-2 rounded-xl bg-white hover:bg-zinc-200 text-black font-extrabold text-xs transition-all flex items-center gap-1 shadow-md">
                <i data-lucide="plus" class="w-3.5 h-3.5"></i> Top-Up
              </button>
              <button onclick="openWalletModal(); filterWalletHistory('all')" class="px-3 py-2 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-white font-bold text-xs transition-all border border-zinc-700">
                History
              </button>
            </div>
          </div>
        </div>

        '''
text = text.replace(old_sidebar_card, new_sidebar_card)

# In walletModal's hologram card
text = text.replace(
    '<span class="text-brand-cyan text-sm font-black tracking-widest uppercase">Campus Flow Pass</span>',
    '<span class="text-white text-sm font-black tracking-widest uppercase">Campus Flow Pass</span>'
)
text = text.replace(
    '<i data-lucide="wifi" class="w-5 h-5 text-brand-cyan rotate-90"></i>',
    '<i data-lucide="wifi" class="w-5 h-5 text-white rotate-90"></i>'
)

# 2. Fix Filter Segmented Control (Screenshots 2 & 4)
old_filter_html = '''        <div class="grid grid-cols-4 gap-1 p-1 bg-zinc-50 rounded-xl border border-zinc-200 text-xs font-bold text-zinc-400">
          <button data-type="all" onclick="filterFleetCategory('all', this)" class="fleet-cat-btn py-1 rounded-lg bg-white/15 text-brand-cyan shadow-sm">All</button>
          <button data-type="bus" onclick="filterFleetCategory('bus', this)" class="fleet-cat-btn py-1 rounded-lg hover:text-white">🚌 Shuttles</button>
          <button data-type="auto" onclick="filterFleetCategory('auto', this)" class="fleet-cat-btn py-1 rounded-lg hover:text-white">🛺 Autos</button>
          <button data-type="ev" onclick="filterFleetCategory('ev', this)" class="fleet-cat-btn py-1 rounded-lg hover:text-white">⚡ EVs</button>
        </div>'''

new_filter_html = '''        <div class="grid grid-cols-4 gap-1 p-1.5 bg-zinc-100 rounded-2xl border border-zinc-200 text-xs font-bold text-zinc-700">
          <button data-type="all" onclick="filterFleetCategory('all', this)" class="fleet-cat-btn py-1.5 rounded-xl bg-black text-white shadow-sm font-black">All</button>
          <button data-type="bus" onclick="filterFleetCategory('bus', this)" class="fleet-cat-btn py-1.5 rounded-xl text-zinc-700 hover:text-black font-extrabold">🚌 Shuttles</button>
          <button data-type="auto" onclick="filterFleetCategory('auto', this)" class="fleet-cat-btn py-1.5 rounded-xl text-zinc-700 hover:text-black font-extrabold">🛺 Autos</button>
          <button data-type="ev" onclick="filterFleetCategory('ev', this)" class="fleet-cat-btn py-1.5 rounded-xl text-zinc-700 hover:text-black font-extrabold">⚡ EVs</button>
        </div>'''
text = text.replace(old_filter_html, new_filter_html)

# In JS filterFleetCategory
old_filter_js = '''    function filterFleetCategory(cat, btn) {
      currentFilterType = cat;
      document.querySelectorAll('.fleet-cat-btn').forEach(b => {
        b.className = 'fleet-cat-btn py-1.5 rounded-xl hover:text-white';
      });
      if (btn) btn.className = 'fleet-cat-btn py-1.5 rounded-xl bg-white/15 text-white shadow-sm font-black';
      renderFleetList();
    }'''

new_filter_js = '''    function filterFleetCategory(cat, btn) {
      currentFilterType = cat;
      document.querySelectorAll('.fleet-cat-btn').forEach(b => {
        b.className = 'fleet-cat-btn py-1.5 rounded-xl text-zinc-700 hover:text-black font-extrabold transition-all';
      });
      if (btn) btn.className = 'fleet-cat-btn py-1.5 rounded-xl bg-black text-white shadow-sm font-black transition-all';
      renderFleetList();
    }'''
text = text.replace(old_filter_js, new_filter_js)

# 3. Fix Vehicle Markers on Map (Screenshot 8)
# Replace moving vehicle icon HTML
old_v_icon_pattern = r"const icon = L\.divIcon\(\{\s*className:\s*'pulse-marker-icon',\s*html:\s*`\s*<div class=\"relative group cursor-pointer\" onclick=\"selectVehicle\('\$\{v\.id\}'\)\">\s*<div class=\"bus-marker-3d\" style=\"background:\$\{v\.color\};\">\s*<span class=\"text-sm font-black\">\$\{v\.icon\}</span>\s*<div class=\"bus-heading-needle\" id=\"needle_\$\{v\.id\}\" style=\"transform: rotate\(\$\{pos\.heading\}deg\)\"></div>\s*</div>\s*<div class=\"absolute -top-7 left-1/2 -translate-x-1/2 whitespace-nowrap px-2 py-0\.5 rounded-full bg-\[#0A0A0A\]/95 backdrop-blur-md border border-white/20 text-\[9px\] font-black shadow-xl flex items-center gap-1 z-20 pointer-events-none\">\s*<span class=\"text-brand-cyan\">\$\{v\.category === 'auto' \? 'Auto' : \(v\.category === 'ev' \? 'EV' : 'Bus'\)\}</span>\s*<span class=\"w-1 h-1 rounded-full bg-zinc-500\"></span>\s*<span style=\"color:\$\{seatColor\};\" class=\"font-mono\">💺 \$\{v\.availableSeats\} free</span>\s*</div>\s*</div>\s*`,\s*iconSize:\s*\[36, 36\],\s*iconAnchor:\s*\[18, 18\]\s*\}\);"

new_v_icon = """const icon = L.divIcon({
          className: 'pulse-marker-icon',
          html: `
            <div class="relative group cursor-pointer flex items-center justify-center" onclick="selectVehicle('${v.id}')">
              <div class="w-10 h-10 rounded-2xl bg-white border-2 border-black text-sm flex items-center justify-center shadow-xl hover:scale-125 transition-transform" style="box-shadow: 0 4px 14px rgba(0,0,0,0.3);">
                <span class="text-base leading-none select-none">${v.icon}</span>
                <div class="bus-heading-needle" id="needle_${v.id}" style="transform: rotate(${pos.heading}deg)"></div>
              </div>
              <div class="absolute -top-7 left-1/2 -translate-x-1/2 whitespace-nowrap px-2 py-0.5 rounded-full bg-black text-white border border-zinc-700 text-[9px] font-black shadow-xl flex items-center gap-1 z-20 pointer-events-none">
                <span class="text-white">${v.category === 'auto' ? 'Auto' : (v.category === 'ev' ? 'EV' : 'Bus')}</span>
                <span class="w-1 h-1 rounded-full bg-zinc-500"></span>
                <span class="font-mono text-white">💺 ${v.availableSeats}</span>
              </div>
            </div>
          `,
          iconSize: [40, 40],
          iconAnchor: [20, 20]
        });"""

text = re.sub(old_v_icon_pattern, new_v_icon, text)

# Replace parked vehicle icon HTML
old_pv_icon_pattern = r"<div class=\"w-9 h-9 rounded-2xl bg-\[#0f172a\] border-2 border-black text-sm flex items-center justify-center shadow-lg hover:scale-125 transition-transform\" style=\"box-shadow: 0 4px 12px rgba\(0, 0, 0, 0\.35\);\">"
new_pv_icon = """<div class="w-10 h-10 rounded-2xl bg-zinc-900 border-2 border-black text-sm flex items-center justify-center shadow-xl hover:scale-125 transition-transform" style="box-shadow: 0 4px 14px rgba(0,0,0,0.35);">"""
text = text.replace(old_pv_icon_pattern, new_pv_icon)

# 4. Fix Moving Vehicle Popup Content (Screenshot 6)
text = text.replace(
    '<div class="flex items-center justify-between text-[10px] font-semibold text-zinc-300">',
    '<div class="flex items-center justify-between text-[10px] font-bold text-zinc-700">'
)
text = text.replace(
    '<p class="font-bold text-white flex items-center gap-1.5">\n                  <span>👨‍✈️ ${v.driver}</span>',
    '<p class="font-bold text-black flex items-center gap-1.5">\n                  <span>👨‍✈️ ${v.driver}</span>'
)
text = text.replace(
    '<p class="text-[10px] text-zinc-400 font-mono">${v.plate} • ${v.phone}</p>',
    '<p class="text-[10px] text-zinc-600 font-mono font-semibold">${v.plate} • ${v.phone}</p>'
)
text = text.replace(
    '<span class="text-zinc-400 font-bold">⏱️ Upcoming Block Arrival:</span>',
    '<span class="text-zinc-700 font-bold">⏱️ Upcoming Block Arrival:</span>'
)
text = text.replace(
    '<span class="text-brand-cyan font-mono font-bold">${v.speed} km/h cruise</span>',
    '<span class="text-black font-mono font-bold">${v.speed} km/h cruise</span>'
)
text = text.replace(
    'py-1.5 px-2 rounded-xl bg-gradient-to-r from-brand-cyan to-brand-purple text-black font-black text-[11px] flex items-center justify-center gap-1 hover:opacity-90 shadow-sm',
    'btn !py-2 px-2.5 rounded-xl bg-black hover:bg-zinc-800 text-white font-black text-[11px] flex items-center justify-center gap-1 shadow-sm'
)
text = text.replace(
    'py-1.5 px-2 rounded-xl bg-white/10 hover:bg-white/20 text-white font-bold text-[11px] flex items-center justify-center gap-1 border border-zinc-200',
    'btn !py-2 px-2.5 rounded-xl bg-zinc-100 hover:bg-zinc-200 text-black border border-zinc-300 font-black text-[11px] flex items-center justify-center gap-1 shadow-sm'
)

# 5. Fix Parked Vehicle Popup (similar contrast fixes)
text = text.replace(
    '<p class="font-bold text-white">👨‍✈️ ${pv.driver} (★ ${pv.rating})</p>',
    '<p class="font-bold text-black">👨‍✈️ ${pv.driver} (★ ${pv.rating})</p>'
)
text = text.replace(
    '<p class="text-zinc-300">🅿️ <strong>Stationed:</strong> ${pv.parkedAt}</p>',
    '<p class="text-zinc-700">🅿️ <strong>Stationed:</strong> ${pv.parkedAt}</p>'
)
text = text.replace(
    '<p class="text-brand-cyan">🎯 <strong>Dest:</strong> ${pv.destination}</p>',
    '<p class="text-black">🎯 <strong>Dest:</strong> ${pv.destination}</p>'
)
text = text.replace(
    '<span class="text-zinc-300">Seats Remaining:</span>',
    '<span class="text-zinc-700 font-bold">Seats Remaining:</span>'
)
text = text.replace(
    '<span class="\'text-black font-black\' font-mono text-xs">',
    '<span class="text-black font-black font-mono text-xs">'
)

# 6. Fix Map Stop Marker Popup (Screenshot 5)
text = text.replace(
    '<strong class="text-white font-black text-xs">${stop.name}</strong>',
    '<strong class="text-black font-black text-sm">${stop.name}</strong>'
)
text = text.replace(
    '<span class="text-[10px] font-mono text-brand-cyan font-bold block">Code: ${stop.code}</span>',
    '<span class="text-[11px] font-mono text-black font-extrabold block">Code: ${stop.code}</span>'
)
text = text.replace(
    '<p class="text-[11px] text-zinc-300 leading-snug">${stop.desc}</p>',
    '<p class="text-[12px] text-zinc-700 font-semibold leading-snug">${stop.desc}</p>'
)
text = text.replace(
    '<button onclick="filterByStop(\'${stop.id}\')" class="text-brand-cyan underline font-bold">Find Shuttles →</button>',
    '<button onclick="filterByStop(\'${stop.id}\')" class="text-black underline font-black">Find Shuttles →</button>'
)

# 7. Fix Live Location HUD & Popup (Screenshot 3)
text = text.replace(
    '<button onclick="shareLocationToChat()" class="py-1 px-2 rounded-lg bg-purple-500/20 text-purple-300 font-bold text-[10px] border border-purple-500/30">',
    '<button onclick="shareLocationToChat()" class="btn !py-1 px-2.5 rounded-lg bg-zinc-100 hover:bg-zinc-200 text-black border border-zinc-300 font-extrabold text-[10px]">'
)
text = text.replace(
    '<button onclick="requestPickupAtMySpot()" class="py-1 px-2 rounded-lg bg-brand-cyan text-black font-black text-[10px]">',
    '<button onclick="requestPickupAtMySpot()" class="btn !py-1 px-2.5 rounded-lg bg-black hover:bg-zinc-800 text-white font-black text-[10px] shadow-sm">'
)
text = text.replace(
    '<strong class="text-white block font-black">Your Live Location</strong>',
    '<strong class="text-black block font-black">Your Live Location</strong>'
)
text = text.replace(
    '<strong class="text-white text-xs block font-black">My Live Location</strong>',
    '<strong class="text-black text-xs block font-black">My Live Location</strong>'
)
text = text.replace(
    '<p class="text-[10px] text-zinc-300 font-mono">Coordinates: ${lat.toFixed(5)}, ${lng.toFixed(5)}</p>',
    '<p class="text-[10px] text-zinc-700 font-mono font-bold">Coordinates: ${lat.toFixed(5)}, ${lng.toFixed(5)}</p>'
)
text = text.replace(
    '<p class="text-zinc-400 text-[10px] font-mono" id="hudCoordinatesText">GPS: 31.2555, 75.7038</p>',
    '<p class="text-zinc-700 text-[10px] font-mono font-bold" id="hudCoordinatesText">GPS: 31.2555, 75.7038</p>'
)
text = text.replace(
    'class="py-1.5 px-2 rounded-xl bg-purple-500/20 text-purple-300 hover:bg-purple-500/30 border border-purple-500/30 font-bold text-[11px] flex items-center justify-center gap-1 transition-all"',
    'class="btn !py-2 px-3 rounded-xl bg-zinc-100 hover:bg-zinc-200 border border-zinc-300 text-black font-extrabold text-[11px] flex items-center justify-center gap-1 transition-all"'
)
text = text.replace(
    'class="py-1.5 px-2 rounded-xl bg-brand-cyan text-black font-black text-[11px] hover:opacity-90 flex items-center justify-center gap-1 shadow-sm transition-all"',
    'class="btn !py-2 px-3 rounded-xl bg-black hover:bg-zinc-800 text-white font-black text-[11px] shadow-sm flex items-center justify-center gap-1 transition-all"'
)

# 8. Fix Fares & Passes Modal (Screenshot 7)
old_fares_modal = text[text.find('id="farePassesModal"'):text.find('<!-- ================= MODAL 5: H4 STRESS TEST SIMULATOR ================= -->')]
new_fares_modal = '''id="farePassesModal" class="fixed inset-0 z-[1000] bg-black/75 backdrop-blur-md hidden place-items-center p-4">
    <div class="glass-panel w-full max-w-md p-6 rounded-3xl border border-zinc-200 space-y-5 animate-pop-in bg-white text-black">
      <div class="flex items-center justify-between border-b border-zinc-200 pb-3">
        <h3 class="text-lg font-black text-black">University Transit Passes</h3>
        <button onclick="closeModal('farePassesModal')" class="p-1.5 rounded-xl text-zinc-400 hover:text-black hover:bg-zinc-100 transition-all"><i data-lucide="x" class="w-5 h-5"></i></button>
      </div>
      <div class="space-y-3 text-xs">
        <div class="p-4 rounded-2xl bg-zinc-50 border border-zinc-200 flex justify-between items-center hover:border-black transition-all">
          <div>
            <p class="font-black text-black text-sm">Single Ride (Bus / Auto)</p>
            <p class="text-zinc-600 text-[11px] font-medium">Valid 45 mins across campus</p>
          </div>
          <span class="text-base font-black text-black font-mono">₹15</span>
        </div>
        <div class="p-4 rounded-2xl bg-zinc-50 border border-zinc-200 flex justify-between items-center hover:border-black transition-all">
          <div>
            <p class="font-black text-black text-sm">Daily Unlimited Pass</p>
            <p class="text-zinc-600 text-[11px] font-medium">Unlimited rides on all Shuttles & EVs</p>
          </div>
          <span class="text-base font-black text-black font-mono">₹40</span>
        </div>
        <div class="p-4 rounded-2xl bg-zinc-50 border border-zinc-200 flex justify-between items-center hover:border-black transition-all">
          <div>
            <p class="font-black text-black text-sm">Semester Pass (4 Months)</p>
            <p class="text-zinc-600 text-[11px] font-medium">Includes all routes + priority booking</p>
          </div>
          <span class="text-base font-black text-black font-mono">₹999</span>
        </div>
      </div>
      <button onclick="closeModal('farePassesModal'); openPaymentAndBookingModal();" class="btn w-full !py-3.5 bg-black hover:bg-zinc-800 text-white font-black text-sm shadow-md">
        Buy Pass Now →
      </button>
    </div>
  </div>

  '''
text = text.replace(old_fares_modal, new_fares_modal)

# 9. Fix Seat Layout Modal (Screenshot 9)
text = text.replace(
    '<h3 class="text-sm font-black text-white" id="seatModalVehicleName">Shuttle #1</h3>',
    '<h3 class="text-base font-black text-black" id="seatModalVehicleName">Shuttle #1</h3>'
)
text = text.replace(
    '<span class="text-[10px] font-mono px-2 py-0.5 rounded bg-brand-cyan/20 text-brand-cyan font-bold" id="seatModalVehiclePlate">PB 08 BX 9021</span>',
    '<span class="text-[10px] font-mono px-2 py-0.5 rounded bg-zinc-200 text-black font-bold" id="seatModalVehiclePlate">PB 08 BX 9021</span>'
)
text = text.replace(
    '<p class="text-[11px] text-zinc-400" id="seatModalVehicleType">50-Seater Campus Shuttle • Driver: Rajesh Sharma (★ 4.9)</p>',
    '<p class="text-[11px] text-zinc-600 font-semibold" id="seatModalVehicleType">50-Seater Campus Shuttle • Driver: Rajesh Sharma (★ 4.9)</p>'
)
text = text.replace(
    '<p class="font-bold text-white" id="selectedSeatLabel">Click an available green seat to select</p>',
    '<p class="font-bold text-black" id="selectedSeatLabel">Click an available seat to select</p>'
)
text = text.replace(
    '<p class="text-[10px] text-zinc-400" id="selectedSeatSubtitle">Window or aisle seats available with live USB charging</p>',
    '<p class="text-[10px] text-zinc-600" id="selectedSeatSubtitle">Window or aisle seats available with live USB charging</p>'
)
text = text.replace(
    'document.getElementById(\'selectedSeatLabel\').textContent = \'Click an available green seat to select\';',
    'document.getElementById(\'selectedSeatLabel\').textContent = \'Click an available seat to select\';'
)
text = text.replace(
    '<span class="text-brand-cyan font-bold font-mono" id="seatModalFareText">Fare: ₹15</span>',
    '<span class="text-black font-black font-mono" id="seatModalFareText">Fare: ₹15</span>'
)
text = text.replace(
    '<span class="text-zinc-400 font-bold" id="seatModalStatsText">8 of 50 Seats Free</span>',
    '<span class="text-black font-extrabold" id="seatModalStatsText">8 of 50 Seats Free</span>'
)
text = text.replace(
    'class="px-4 py-2.5 rounded-xl bg-white/10 hover:bg-white/20 text-white font-bold text-xs flex items-center gap-1.5 border border-zinc-200"',
    'class="btn !py-2.5 px-4 rounded-xl bg-zinc-100 hover:bg-zinc-200 text-black font-bold text-xs flex items-center gap-1.5 border border-zinc-300 shadow-sm"'
)

# Seat layout inner cabin container
text = text.replace(
    'id="seatGridContainer" class="p-4 rounded-2xl bg-[#080c1d] border border-zinc-200 space-y-3"',
    'id="seatGridContainer" class="p-4 rounded-2xl bg-zinc-50 border border-zinc-200 space-y-3"'
)
text = text.replace(
    'class="p-3 rounded-2xl bg-black/40 border border-zinc-200 flex items-center justify-between text-xs"',
    'class="p-3 rounded-2xl bg-zinc-100 border border-zinc-200 flex items-center justify-between text-xs"'
)

# Seat button styles inside renderSeatGrid
text = re.sub(
    r"\$\{v\.availableSeats >= 1 \? 'bg-zinc-100 border-emerald-500 text-zinc-800 hover:scale-105' : 'bg-rose-500/20 border-rose-500/40 text-rose-400 cursor-not-allowed'\}",
    "${v.availableSeats >= 1 ? 'bg-white hover:bg-zinc-100 text-black border-2 border-black font-black shadow-sm' : 'bg-zinc-200/60 text-zinc-400 border border-zinc-200 opacity-60 cursor-not-allowed'}",
    text
)
text = re.sub(
    r"\$\{v\.availableSeats >= 2 \? 'bg-zinc-100 border-emerald-500 text-zinc-800 hover:scale-105' : 'bg-rose-500/20 border-rose-500/40 text-rose-400 cursor-not-allowed'\}",
    "${v.availableSeats >= 2 ? 'bg-white hover:bg-zinc-100 text-black border-2 border-black font-black shadow-sm' : 'bg-zinc-200/60 text-zinc-400 border border-zinc-200 opacity-60 cursor-not-allowed'}",
    text
)
text = re.sub(
    r"\$\{v\.availableSeats >= 3 \? 'bg-zinc-100 border-emerald-500 text-zinc-800 hover:scale-105' : 'bg-rose-500/20 border-rose-500/40 text-rose-400 cursor-not-allowed'\}",
    "${v.availableSeats >= 3 ? 'bg-white hover:bg-zinc-100 text-black border-2 border-black font-black shadow-sm' : 'bg-zinc-200/60 text-zinc-400 border border-zinc-200 opacity-60 cursor-not-allowed'}",
    text
)
text = re.sub(
    r"\$\{isFree \? 'bg-zinc-100 border-emerald-500 text-zinc-800 hover:scale-105' : 'bg-rose-500/20 border-rose-500/40 text-rose-400 cursor-not-allowed'\}",
    "${isFree ? 'bg-white hover:bg-zinc-100 text-black border-2 border-black font-black shadow-sm' : 'bg-zinc-200/60 text-zinc-400 border border-zinc-200 opacity-60 cursor-not-allowed'}",
    text
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("fix_contrast_and_markers.py executed successfully.")

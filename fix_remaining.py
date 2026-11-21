with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Replace Vehicle Category Filters HTML
cat_filter_old = '''        <!-- Vehicle Category Filters -->
        <div class="grid grid-cols-4 p-1 rounded-xl bg-black/40 border border-zinc-200 text-[11px] font-extrabold text-zinc-400">
          <button data-type="all" onclick="filterFleetCategory('all', this)" class="fleet-cat-btn py-1 rounded-lg bg-white/15 text-brand-cyan shadow-sm">All</button>
          <button data-type="bus" onclick="filterFleetCategory('bus', this)" class="fleet-cat-btn py-1 rounded-lg hover:text-white">🚌 Shuttles</button>
          <button data-type="auto" onclick="filterFleetCategory('auto', this)" class="fleet-cat-btn py-1 rounded-lg hover:text-white">🛺 Autos</button>
          <button data-type="ev" onclick="filterFleetCategory('ev', this)" class="fleet-cat-btn py-1 rounded-lg hover:text-white">⚡ EVs</button>
        </div>'''

cat_filter_new = '''        <!-- Vehicle Category Filters -->
        <div class="grid grid-cols-4 gap-1.5 p-1.5 rounded-2xl bg-zinc-100 border border-zinc-200 text-xs font-bold">
          <button data-type="all" onclick="filterFleetCategory('all', this)" class="fleet-cat-btn py-2 rounded-xl bg-black text-white shadow-sm font-black transition-all flex items-center justify-center">All</button>
          <button data-type="bus" onclick="filterFleetCategory('bus', this)" class="fleet-cat-btn py-2 rounded-xl text-zinc-700 hover:text-black font-extrabold transition-all flex items-center justify-center gap-1">🚌 Shuttles</button>
          <button data-type="auto" onclick="filterFleetCategory('auto', this)" class="fleet-cat-btn py-2 rounded-xl text-zinc-700 hover:text-black font-extrabold transition-all flex items-center justify-center gap-1">🛺 Autos</button>
          <button data-type="ev" onclick="filterFleetCategory('ev', this)" class="fleet-cat-btn py-2 rounded-xl text-zinc-700 hover:text-black font-extrabold transition-all flex items-center justify-center gap-1">⚡ EVs</button>
        </div>'''

if cat_filter_old in c:
    c = c.replace(cat_filter_old, cat_filter_new)
    print("[PASS] Fixed Category Filter HTML")
else:
    print("[FAIL] Category Filter HTML old text not matched")

# 2. Replace setFleetViewMode
viewmode_old = '''function setFleetViewMode(mode) {
      currentFleetViewMode = mode;
      const btnMoving = document.getElementById('btnFleetMoving');
      const btnParked = document.getElementById('btnFleetParked');
      const secTitle = document.getElementById('fleetSectionTitle');
      const secSub = document.getElementById('fleetSectionSub');

      if (mode === 'moving') {
        if (btnMoving) btnMoving.className = 'py-2 rounded-xl bg-black text-white font-black shadow-md flex items-center justify-center gap-1.5 transition-all';
        if (btnParked) btnParked.className = 'py-2 rounded-xl text-zinc-400 hover:text-white font-bold flex items-center justify-center gap-1.5 transition-all';
        if (secTitle) secTitle.innerHTML = '🟢 Active Moving Shuttles (8)';
        if (secSub) secSub.textContent = 'Real-time GPS • Cruise 18 km/h';
      } else {
        if (btnMoving) btnMoving.className = 'py-2 rounded-xl text-zinc-400 hover:text-white font-bold flex items-center justify-center gap-1.5 transition-all';
        if (btnParked) btnParked.className = 'py-2 rounded-xl bg-black text-white font-black shadow-md flex items-center justify-center gap-1.5 transition-all';
        if (secTitle) secTitle.innerHTML = '🅿️ Scheduled & Parked Shuttles (4)';
        if (secSub) secSub.textContent = 'Campus Standby • Pick Seat & Board';
      }
      renderFleetList();
    }'''

viewmode_new = '''function setFleetViewMode(mode) {
      currentFleetViewMode = mode;
      const btnMoving = document.getElementById('btnFleetMoving');
      const btnParked = document.getElementById('btnFleetParked');
      const secTitle = document.getElementById('fleetSectionTitle');
      const secSub = document.getElementById('fleetSectionSub');

      if (mode === 'moving') {
        if (btnMoving) btnMoving.className = 'py-2 rounded-xl bg-black text-white font-black shadow-md flex items-center justify-center gap-1.5 transition-all';
        if (btnParked) btnParked.className = 'py-2 rounded-xl text-zinc-700 hover:text-black font-extrabold flex items-center justify-center gap-1.5 transition-all';
        if (secTitle) secTitle.innerHTML = '🚍 Active Moving Shuttles (8)';
        if (secSub) secSub.textContent = 'Real-time GPS • Cruise 18 km/h';
      } else {
        if (btnMoving) btnMoving.className = 'py-2 rounded-xl text-zinc-700 hover:text-black font-extrabold flex items-center justify-center gap-1.5 transition-all';
        if (btnParked) btnParked.className = 'py-2 rounded-xl bg-black text-white font-black shadow-md flex items-center justify-center gap-1.5 transition-all';
        if (secTitle) secTitle.innerHTML = '🅿️ Scheduled & Parked Fleet (4)';
        if (secSub) secSub.textContent = 'Campus Standby • Pick Seat & Board';
      }
      renderFleetList();
    }'''

if viewmode_old in c:
    c = c.replace(viewmode_old, viewmode_new)
    print("[PASS] Fixed setFleetViewMode")
else:
    print("[FAIL] setFleetViewMode old text not matched")

# 3. Clean Driver Auth Login Page styling (high contrast black & white)
c = c.replace('class="w-full bg-[#1A1A1A] border border-white/20 text-white rounded-xl px-4 py-3 text-xs', 'class="w-full bg-zinc-100 border border-zinc-300 text-black font-extrabold rounded-xl px-4 py-3 text-xs focus:border-black focus:outline-none')
c = c.replace('class="w-full bg-zinc-700 border border-zinc-600 text-white', 'class="w-full bg-zinc-100 border border-zinc-300 text-black font-extrabold')

# 4. Clean bottom navbar buttons: remove yellow and green tints
c = c.replace('class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-emerald-500/20 text-emerald-400', 'class="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-zinc-100 text-black font-black border border-zinc-200')
c = c.replace('text-amber-400', 'text-black')
c = c.replace('text-yellow-400', 'text-black')
c = c.replace('text-emerald-400', 'text-black')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Remaining updates saved.")

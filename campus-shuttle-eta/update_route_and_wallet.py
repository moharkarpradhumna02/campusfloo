import json

with open('campus-shuttle-eta/data/routes/campus_route.geojson') as f:
    geojson_data = json.load(f)

# Convert [lon, lat] -> [lat, lon] with 6 decimal places
leaflet_coords = [[round(p[1], 6), round(p[0], 6)] for p in geojson_data['features'][0]['geometry']['coordinates']]
coords_js_str = 'const CAMPUS_ROUTE_COORDS = ' + json.dumps(leaflet_coords) + ';'

with open('build_full_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Top Navbar Wallet button to have id="navWalletBtn" and class="hidden ..."
old_nav_wallet = '''        <!-- Wallet Button with Live Balance -->
        <button onclick="openWalletModal()" class="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-gradient-to-r from-brand-cyan/15 to-brand-purple/15 hover:from-brand-cyan/25 hover:to-brand-purple/25 border border-brand-cyan/30 text-xs font-bold text-white transition-all shadow-sm">
          <span class="text-brand-cyan">💳</span>
          <span class="hidden sm:inline text-zinc-300">Wallet:</span>
          <span id="navWalletBalance" class="text-brand-cyan font-black">₹240.00</span>
        </button>'''

new_nav_wallet = '''        <!-- Wallet Button with Live Balance (Visible only after login) -->
        <button id="navWalletBtn" onclick="openWalletModal()" class="hidden inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-gradient-to-r from-brand-cyan/15 to-brand-purple/15 hover:from-brand-cyan/25 hover:to-brand-purple/25 border border-brand-cyan/30 text-xs font-bold text-white transition-all shadow-sm">
          <span class="text-brand-cyan">💳</span>
          <span class="hidden sm:inline text-zinc-300">Wallet:</span>
          <span id="navWalletBalance" class="text-brand-cyan font-black">₹240.00</span>
        </button>'''

if old_nav_wallet in content:
    content = content.replace(old_nav_wallet, new_nav_wallet)
    print("Updated top navbar wallet button to be hidden by default!")
else:
    print("Warning: old_nav_wallet not matched directly, checking normalized")

# 2. Update Hero promo banner wallet button to have id="heroPromoWalletBtn" and class="hidden ..."
old_promo_wallet = '''              <button onclick="openWalletModal()" class="w-full sm:w-auto px-3 py-2 rounded-xl bg-white/10 text-white font-extrabold text-xs hover:bg-white/20 transition-all border border-white/15">
                💳 Wallet
              </button>'''

new_promo_wallet = '''              <button id="heroPromoWalletBtn" onclick="openWalletModal()" class="hidden w-full sm:w-auto px-3 py-2 rounded-xl bg-white/10 text-white font-extrabold text-xs hover:bg-white/20 transition-all border border-white/15">
                💳 Wallet
              </button>'''

if old_promo_wallet in content:
    content = content.replace(old_promo_wallet, new_promo_wallet)
    print("Updated hero promo wallet button to be hidden by default!")

# 3. Replace STOPS with the realistic campus road stops
old_stops_str = '''    const STOPS = [
      { id: 'stop_main_gate', name: 'Main Gate & Metro Link', lat: 31.2530, lng: 75.7000 },
      { id: 'stop_admin', name: 'Admin Block & Registrar', lat: 31.2555, lng: 75.7040 },
      { id: 'stop_library', name: 'Central Library & Law Quad', lat: 31.2585, lng: 75.7085 },
      { id: 'stop_hostel_boys', name: 'Boys Hostel Quad (BH 1-4)', lat: 31.2615, lng: 75.7130 },
      { id: 'stop_innov_hub', name: 'Innovation Hub & Robotics Labs', lat: 31.2590, lng: 75.7160 },
      { id: 'stop_sports_complex', name: 'Olympic Sports Complex & Gym', lat: 31.2550, lng: 75.7180 },
      { id: 'stop_food_court', name: 'Food Court & Student Activity', lat: 31.2520, lng: 75.7145 },
      { id: 'stop_hostel_girls', name: 'Girls Hostel Complex (GH 1-3)', lat: 31.2490, lng: 75.7090 },
      { id: 'stop_hospital', name: 'University Hospital & Biotech', lat: 31.2505, lng: 75.7035 }
    ];'''

new_stops_str = '''    const STOPS = [
      { id: 'stop_main_gate', name: 'Main Gate & Metro Hub', code: 'MG', lat: 31.2503, lng: 75.7022, desc: 'Main Campus Gate & City Transit Interchange' },
      { id: 'stop_admin', name: 'Admin Block & Registrar', code: 'AB', lat: 31.2528, lng: 75.7017, desc: 'Central Administration, Dean Office & Student Helpdesk' },
      { id: 'stop_library', name: 'Central Library & Quad', code: 'CL', lat: 31.2553, lng: 75.7022, desc: 'Central Library, Law Building & Digital Archives' },
      { id: 'stop_hostels', name: 'Hostel Quadrangle (BH & GH)', code: 'HQ', lat: 31.2583, lng: 75.7032, desc: 'Campus Residences & Common Student Hall' },
      { id: 'stop_innov_hub', name: 'Innovation Hub & Labs', code: 'IH', lat: 31.2593, lng: 75.7067, desc: 'Engineering Wings, Incubation & AI Research Labs' },
      { id: 'stop_sports_complex', name: 'Sports Arena & Stadium', code: 'SC', lat: 31.2568, lng: 75.7097, desc: 'Olympic Sports Arena, Gym & Swimming Pool' },
      { id: 'stop_food_court', name: 'Student Activity & Food Court', code: 'FC', lat: 31.2538, lng: 75.7092, desc: 'Cafeteria, Open Amphitheater & Stationery' },
      { id: 'stop_medical', name: 'Medical Center & Pharmacy', code: 'MC', lat: 31.2510, lng: 75.7072, desc: '24/7 Campus Health Center & Emergency Care' }
    ];'''

if old_stops_str in content:
    content = content.replace(old_stops_str, new_stops_str)
    print("Replaced STOPS with accurate road stops!")

# 4. Replace CAMPUS_ROUTE_COORDS with the 121 precise road coordinates from GeoJSON
old_route_str = '''    // Campus Route Coordinates
    const CAMPUS_ROUTE_COORDS = [
      [31.2530, 75.7000], [31.2555, 75.7040], [31.2585, 75.7085],
      [31.2615, 75.7130], [31.2590, 75.7160], [31.2550, 75.7180],
      [31.2520, 75.7145], [31.2490, 75.7090], [31.2505, 75.7035],
      [31.2530, 75.7000]
    ];'''

new_route_str = f'''    // Campus Road Network Polyline (121 road-aligned coordinates from campus_route.geojson)
    {coords_js_str}'''

if old_route_str in content:
    content = content.replace(old_route_str, new_route_str)
    print("Replaced CAMPUS_ROUTE_COORDS with 121 smooth road-aligned coordinates!")

# 5. Update initial map view & recenter in initCampusMap() and recenterCampusMap()
old_map_init = "map = L.map('campusMap', { zoomControl: false }).setView([31.2550, 75.7090], 15);"
new_map_init = "map = L.map('campusMap', { zoomControl: false }).setView([31.2548, 75.7058], 16);"
if old_map_init in content:
    content = content.replace(old_map_init, new_map_init)

old_recenter = "if (map) map.setView([31.2550, 75.7090], 15);"
new_recenter = "if (map && routePolylineLayer) { map.fitBounds(routePolylineLayer.getBounds().pad(0.08)); } else if (map) { map.setView([31.2548, 75.7058], 16); }"
if old_recenter in content:
    content = content.replace(old_recenter, new_recenter)

# 6. Update stop markers in initCampusMap() to render rich stop popups with stop.code & stop.desc
old_stop_markers = '''      // Stop Markers
      STOPS.forEach(stop => {
        const icon = L.divIcon({
          className: 'pulse-marker-icon',
          html: `<div class="w-4 h-4 rounded-full bg-brand-cyan border-2 border-black shadow-[0_0_12px_#00f0ff] animate-ping"></div>`,
          iconSize: [16, 16]
        });
        const marker = L.marker([stop.lat, stop.lng], { icon }).addTo(map);
        marker.bindPopup(`<strong class="text-xs">${stop.name}</strong><br><span class="text-[10px] text-zinc-400">Stop ID: ${stop.id}</span>`);
        stopMarkers.push(marker);
      });'''

new_stop_markers = '''      // Stop Markers aligned on campus road curbs
      STOPS.forEach(stop => {
        const icon = L.divIcon({
          className: 'pulse-marker-icon',
          html: `
            <div class="relative group cursor-pointer">
              <div class="w-4 h-4 rounded-full bg-brand-cyan border-2 border-black shadow-[0_0_12px_#00f0ff] animate-ping"></div>
              <div class="w-3.5 h-3.5 rounded-full bg-brand-cyan border-2 border-white absolute top-0 left-0 shadow-md"></div>
              <div class="absolute -bottom-6 left-1/2 -translate-x-1/2 whitespace-nowrap px-1.5 py-0.5 rounded-md bg-black/90 border border-white/20 text-[9px] font-bold text-zinc-300 pointer-events-none hidden group-hover:block z-30">
                ${stop.name}
              </div>
            </div>
          `,
          iconSize: [16, 16],
          iconAnchor: [8, 8]
        });
        const marker = L.marker([stop.lat, stop.lng], { icon }).addTo(map);
        marker.bindPopup(`
          <div class="p-2.5 text-xs font-sans space-y-1 min-w-[210px]">
            <div class="flex items-center gap-1.5 border-b border-white/10 pb-1.5">
              <span class="text-base">🚏</span>
              <div>
                <strong class="text-white font-bold text-xs">${stop.name}</strong>
                <span class="text-[10px] font-mono text-brand-cyan font-bold block">Stop Code: ${stop.code}</span>
              </div>
            </div>
            <p class="text-[10px] text-zinc-400 pt-0.5">${stop.desc}</p>
            <div class="pt-1 flex items-center justify-between text-[10px] font-mono text-emerald-400 border-t border-white/5">
              <span>● Live Station</span>
              <span>Shuttle: ~2-3 min</span>
            </div>
          </div>
        `);
        stopMarkers.push(marker);
      });

      // Fit map smoothly to the road loop
      if (routePolylineLayer) {
        setTimeout(() => map.fitBounds(routePolylineLayer.getBounds().pad(0.08)), 200);
      }'''

if old_stop_markers in content:
    content = content.replace(old_stop_markers, new_stop_markers)
    print("Enhanced stop markers on road curbs!")

# 7. Update updateUserAccountPill to toggle visibility of wallet buttons based on auth state
old_pill_func = '''    function updateUserAccountPill() {
      const saved = localStorage.getItem('cf_user');
      if (saved) {
        try { 
          currentUser = JSON.parse(saved); 
          const entered = document.getElementById('suFullName') ? document.getElementById('suFullName').value.trim() : '';
          if (entered) currentUser.name = entered;
        } catch(e) {}
      }
      const pill = document.getElementById('userAccountPill');
      if (pill) {
        if (currentUser && currentUser.name) {
          pill.textContent = `👤 ${currentUser.name.trim()}`;
        } else {
          pill.textContent = 'Sign Up / Login';
        }
      }
    }'''

new_pill_func = '''    function updateUserAccountPill() {
      const saved = localStorage.getItem('cf_user');
      if (saved) {
        try { 
          currentUser = JSON.parse(saved); 
          const entered = document.getElementById('suFullName') ? document.getElementById('suFullName').value.trim() : '';
          if (entered) currentUser.name = entered;
        } catch(e) {}
      }
      const pill = document.getElementById('userAccountPill');
      const navWallet = document.getElementById('navWalletBtn');
      const heroPromoWallet = document.getElementById('heroPromoWalletBtn');
      const sidePass = document.getElementById('sidebarTransitPassCard');

      if (currentUser && currentUser.name) {
        if (pill) pill.textContent = `👤 ${currentUser.name.trim()}`;
        if (navWallet) navWallet.classList.remove('hidden');
        if (heroPromoWallet) heroPromoWallet.classList.remove('hidden');
        if (sidePass) sidePass.classList.remove('hidden');
      } else {
        if (pill) pill.textContent = 'Sign Up / Login';
        if (navWallet) navWallet.classList.add('hidden');
        if (heroPromoWallet) heroPromoWallet.classList.add('hidden');
        if (sidePass) sidePass.classList.add('hidden');
      }
    }'''

if old_pill_func in content:
    content = content.replace(old_pill_func, new_pill_func)
    print("Updated updateUserAccountPill() to dynamically show wallet only when authenticated!")

# 8. Also update FLEET initial positions along the 2885m road loop so they are evenly spread
old_fleet_spacing = "s: 200, icon: '🚌', color: '#00f0ff', delay: 0 },\n      { id: 'auto_2', category: 'auto', typeName: '3-Seater Campus Auto', name: 'Auto #2 (Hostel Quad)', plate: 'PB 08 CA 1201', driver: 'Vikram Singh', phone: '+91 98140-55672', totalSeats: 3, occupiedSeats: 2, availableSeats: 1, fare: 30, rating: 4.8, speed: 32, battery: 92, s: 1200,"
new_fleet_spacing = "s: 150, icon: '🚌', color: '#00f0ff', delay: 0 },\n      { id: 'auto_2', category: 'auto', typeName: '3-Seater Campus Auto', name: 'Auto #2 (Hostel Quad)', plate: 'PB 08 CA 1201', driver: 'Vikram Singh', phone: '+91 98140-55672', totalSeats: 3, occupiedSeats: 2, availableSeats: 1, fare: 30, rating: 4.8, speed: 32, battery: 92, s: 500,"
if old_fleet_spacing in content:
    content = content.replace(old_fleet_spacing, new_fleet_spacing)

with open('build_full_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved all updates to build_full_app.py!")

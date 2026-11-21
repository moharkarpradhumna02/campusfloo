import re

with open('build_full_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Leaflet dark popup styles to <style>
style_addition = '''
    /* Leaflet Dark HUD Popup Styling */
    .leaflet-popup-content-wrapper {
      background: rgba(11, 15, 30, 0.96) !important;
      backdrop-filter: blur(24px) !important;
      -webkit-backdrop-filter: blur(24px) !important;
      border: 1px solid rgba(0, 240, 255, 0.35) !important;
      border-radius: 20px !important;
      color: #f1f5f9 !important;
      box-shadow: 0 20px 45px rgba(0, 0, 0, 0.75), 0 0 20px rgba(0, 240, 255, 0.25) !important;
      padding: 0 !important;
      overflow: hidden;
    }
    .leaflet-popup-content {
      margin: 0 !important;
      line-height: 1.4 !important;
    }
    .leaflet-popup-tip {
      background: rgba(11, 15, 30, 0.96) !important;
      border: 1px solid rgba(0, 240, 255, 0.35) !important;
    }
    .leaflet-container a.leaflet-popup-close-button {
      color: #94a3b8 !important;
      padding: 8px 10px !important;
      font-size: 16px !important;
    }
    .leaflet-container a.leaflet-popup-close-button:hover {
      color: #00f0ff !important;
    }
'''

if '/* Leaflet Dark HUD Popup Styling */' not in content:
    content = content.replace('/* Custom Leaflet Markers */', style_addition + '\n    /* Custom Leaflet Markers */')
    print("Added Leaflet dark popup CSS!")

# 2. Update FLEET definition with rich seat & vehicle type metadata
old_fleet_str = '''    // Simulation Fleet
    let FLEET = [
      { id: 'bus_1', category: 'bus', name: 'Shuttle #1 (Outer Loop)', plate: 'PB 08 BX 9021', driver: 'Rajesh Sharma', phone: '+91 98765-43210', capacity: '42/50', speed: 28, battery: 84, s: 200, icon: '🚌', color: '#00f0ff', delay: 0 },
      { id: 'auto_2', category: 'auto', name: 'Auto #2 (Hostel Quad)', plate: 'PB 08 CA 1201', driver: 'Vikram Singh', phone: '+91 98140-55672', capacity: '2/3', speed: 32, battery: 92, s: 1200, icon: '🛺', color: '#10b981', delay: 0 },
      { id: 'ev_3', category: 'ev', name: 'Eco EV #3 (Green Cart)', plate: 'PB 08 EV 0044', driver: 'Suresh Yadav', phone: '+91 94170-88321', capacity: '5/6', speed: 20, battery: 78, s: 2200, icon: '⚡', color: '#f59e0b', delay: 0 },
      { id: 'bus_4', category: 'bus', name: 'Express #4 (Metro Link)', plate: 'PB 08 BX 9410', driver: 'Amit Patel', phone: '+91 99882-11490', capacity: '35/50', speed: 30, battery: 65, s: 3100, icon: '🚌', color: '#a855f7', delay: 0 },
      { id: 'auto_5', category: 'auto', name: 'Auto #5 (Sports Complex)', plate: 'PB 08 CA 3381', driver: 'Priya Verma', phone: '+91 98721-66710', capacity: '1/3', speed: 31, battery: 88, s: 800, icon: '🛺', color: '#10b981', delay: 0 },
      { id: 'ev_6', category: 'ev', name: 'Eco EV #6 (Medical Cart)', plate: 'PB 08 EV 0092', driver: 'Sunita Gupta', phone: '+91 94630-11220', capacity: '4/6', speed: 18, battery: 95, s: 1800, icon: '⚡', color: '#f59e0b', delay: 0 },
      { id: 'bus_7', category: 'bus', name: 'Shuttle #7 (Library Express)', plate: 'PB 08 BX 8812', driver: 'Ramesh Kumar', phone: '+91 98155-77441', capacity: '48/50', speed: 26, battery: 54, s: 2600, icon: '🚌', color: '#00f0ff', delay: 0 },
      { id: 'auto_8', category: 'auto', name: 'Auto #8 (Innovation Hub)', plate: 'PB 08 CA 5509', driver: 'Deepak Sharma', phone: '+91 98788-33219', capacity: '0/3', speed: 33, battery: 90, s: 3600, icon: '🛺', color: '#10b981', delay: 0 }
    ];'''

new_fleet_str = '''    // Simulation Fleet with Real-time Seat Occupancy & Vehicle Types
    let FLEET = [
      { id: 'bus_1', category: 'bus', typeName: '50-Seater Campus Shuttle', name: 'Shuttle #1 (Outer Loop)', plate: 'PB 08 BX 9021', driver: 'Rajesh Sharma', phone: '+91 98765-43210', totalSeats: 50, occupiedSeats: 42, availableSeats: 8, fare: 15, rating: 4.9, speed: 28, battery: 84, s: 200, icon: '🚌', color: '#00f0ff', delay: 0 },
      { id: 'auto_2', category: 'auto', typeName: '3-Seater Campus Auto', name: 'Auto #2 (Hostel Quad)', plate: 'PB 08 CA 1201', driver: 'Vikram Singh', phone: '+91 98140-55672', totalSeats: 3, occupiedSeats: 2, availableSeats: 1, fare: 30, rating: 4.8, speed: 32, battery: 92, s: 1200, icon: '🛺', color: '#10b981', delay: 0 },
      { id: 'ev_3', category: 'ev', typeName: '6-Seater Eco EV Cart', name: 'Eco EV #3 (Green Cart)', plate: 'PB 08 EV 0044', driver: 'Suresh Yadav', phone: '+91 94170-88321', totalSeats: 6, occupiedSeats: 5, availableSeats: 1, fare: 10, rating: 4.9, speed: 20, battery: 78, s: 2200, icon: '⚡', color: '#f59e0b', delay: 0 },
      { id: 'bus_4', category: 'bus', typeName: '50-Seater Express Bus', name: 'Express #4 (Metro Link)', plate: 'PB 08 BX 9410', driver: 'Amit Patel', phone: '+91 99882-11490', totalSeats: 50, occupiedSeats: 35, availableSeats: 15, fare: 15, rating: 4.7, speed: 30, battery: 65, s: 3100, icon: '🚌', color: '#a855f7', delay: 0 },
      { id: 'auto_5', category: 'auto', typeName: '3-Seater Campus Auto', name: 'Auto #5 (Sports Complex)', plate: 'PB 08 CA 3381', driver: 'Priya Verma', phone: '+91 98721-66710', totalSeats: 3, occupiedSeats: 1, availableSeats: 2, fare: 30, rating: 5.0, speed: 31, battery: 88, s: 800, icon: '🛺', color: '#10b981', delay: 0 },
      { id: 'ev_6', category: 'ev', typeName: '6-Seater Medical Cart', name: 'Eco EV #6 (Medical Cart)', plate: 'PB 08 EV 0092', driver: 'Sunita Gupta', phone: '+91 94630-11220', totalSeats: 6, occupiedSeats: 4, availableSeats: 2, fare: 10, rating: 4.9, speed: 18, battery: 95, s: 1800, icon: '⚡', color: '#f59e0b', delay: 0 },
      { id: 'bus_7', category: 'bus', typeName: '50-Seater AC Shuttle', name: 'Shuttle #7 (Library Express)', plate: 'PB 08 BX 8812', driver: 'Ramesh Kumar', phone: '+91 98155-77441', totalSeats: 50, occupiedSeats: 48, availableSeats: 2, fare: 15, rating: 4.8, speed: 26, battery: 54, s: 2600, icon: '🚌', color: '#00f0ff', delay: 0 },
      { id: 'auto_8', category: 'auto', typeName: '3-Seater Campus Auto', name: 'Auto #8 (Innovation Hub)', plate: 'PB 08 CA 5509', driver: 'Deepak Sharma', phone: '+91 98788-33219', totalSeats: 3, occupiedSeats: 0, availableSeats: 3, fare: 30, rating: 4.9, speed: 33, battery: 90, s: 3600, icon: '🛺', color: '#10b981', delay: 0 }
    ];'''

if old_fleet_str in content:
    content = content.replace(old_fleet_str, new_fleet_str)
    print("Updated FLEET metadata!")
else:
    print("Warning: old_fleet_str not found directly, checking regex")

# 3. Insert Interactive Seat Layout Modal right before driverChatModal
seat_modal_html = '''  <!-- ================= SEAT LAYOUT & RESERVATION MODAL ================= -->
  <div id="seatLayoutModal" class="fixed inset-0 z-[1060] bg-black/85 backdrop-blur-md hidden place-items-center p-4">
    <div class="glass-panel w-full max-w-xl rounded-3xl border border-white/15 overflow-hidden shadow-2xl animate-pop-in flex flex-col max-h-[90vh]">
      
      <!-- Header -->
      <div class="p-4 border-b border-white/10 flex items-center justify-between bg-white/5 shrink-0">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-brand-cyan to-brand-purple text-black flex items-center justify-center text-xl font-black" id="seatModalVehicleIcon">
            🚌
          </div>
          <div>
            <div class="flex items-center gap-2">
              <h3 class="text-sm font-black text-white" id="seatModalVehicleName">Shuttle #1</h3>
              <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-brand-cyan/20 text-brand-cyan font-bold" id="seatModalVehiclePlate">PB 08 BX 9021</span>
            </div>
            <p class="text-[11px] text-zinc-400" id="seatModalVehicleType">50-Seater Campus Shuttle • Driver: Rajesh Sharma (★ 4.9)</p>
          </div>
        </div>
        <button onclick="closeModal('seatLayoutModal')" class="p-2 rounded-xl text-zinc-400 hover:text-white hover:bg-white/10">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <!-- Live Seat Legend & Stats -->
      <div class="p-3 bg-gradient-to-r from-[#0d1226] via-[#10193a] to-[#0d1226] border-b border-white/10 flex flex-wrap items-center justify-between gap-3 text-xs shrink-0">
        <div class="flex items-center gap-4">
          <div class="flex items-center gap-1.5">
            <span class="w-3.5 h-3.5 rounded-lg bg-emerald-500/20 border border-emerald-500 text-emerald-400 flex items-center justify-center text-[9px]">✓</span>
            <span class="text-zinc-300">Available</span>
          </div>
          <div class="flex items-center gap-1.5">
            <span class="w-3.5 h-3.5 rounded-lg bg-rose-500/20 border border-rose-500/40 text-rose-400 flex items-center justify-center text-[9px]">✕</span>
            <span class="text-zinc-400">Booked</span>
          </div>
          <div class="flex items-center gap-1.5">
            <span class="w-3.5 h-3.5 rounded-lg bg-brand-cyan border border-brand-cyan text-black flex items-center justify-center text-[9px] font-bold">★</span>
            <span class="text-brand-cyan font-bold">Selected</span>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-zinc-400 font-bold" id="seatModalStatsText">8 of 50 Seats Free</span>
          <span class="text-brand-cyan font-bold font-mono" id="seatModalFareText">Fare: ₹15</span>
        </div>
      </div>

      <!-- Vehicle Cabin Grid (Scrollable) -->
      <div class="flex-1 overflow-y-auto p-5 space-y-4">
        
        <!-- Driver Cabin Indicator -->
        <div class="p-3 rounded-2xl bg-black/40 border border-white/10 flex items-center justify-between text-xs">
          <div class="flex items-center gap-2 text-zinc-400">
            <span class="text-lg">🛞</span>
            <span class="font-bold">Driver Cabin (Front)</span>
          </div>
          <div class="flex items-center gap-2 text-emerald-400 font-mono text-[11px]">
            <span>🚪 Entry / Exit Door</span>
          </div>
        </div>

        <!-- Seats Grid Container -->
        <div id="seatGridContainer" class="p-4 rounded-2xl bg-[#080c1d] border border-white/10 space-y-3">
          <!-- Rendered dynamically -->
        </div>

        <!-- Selected Seat Banner -->
        <div id="seatSelectionBanner" class="p-3 rounded-2xl bg-brand-cyan/10 border border-brand-cyan/30 flex items-center justify-between text-xs">
          <div class="flex items-center gap-2">
            <span class="text-lg">💺</span>
            <div>
              <p class="font-bold text-white" id="selectedSeatLabel">Click an available green seat to select</p>
              <p class="text-[10px] text-zinc-400" id="selectedSeatSubtitle">Window or aisle seats available with live USB charging</p>
            </div>
          </div>
          <span class="text-sm font-black text-brand-cyan font-mono" id="selectedSeatPrice"></span>
        </div>

      </div>

      <!-- Footer Buttons -->
      <div class="p-4 border-t border-white/10 bg-white/5 flex items-center justify-between gap-3 shrink-0">
        <button onclick="openDriverChat(currentSeatModalVehicleId)" class="px-4 py-2.5 rounded-xl bg-white/10 hover:bg-white/20 text-white font-bold text-xs flex items-center gap-1.5 border border-white/15">
          💬 Ask Driver About Seat / Luggage
        </button>
        <button id="btnConfirmSeatBooking" onclick="confirmSeatBooking()" class="px-5 py-2.5 rounded-xl btn-gradient text-black font-black text-xs uppercase tracking-wider flex items-center gap-2 shadow-lg shadow-brand-cyan/20">
          <span>Confirm Seat & Ride</span>
          <i data-lucide="arrow-right" class="w-4 h-4"></i>
        </button>
      </div>

    </div>
  </div>

'''

if 'id="seatLayoutModal"' not in content:
    content = content.replace('<!-- ================= MODAL 3: DRIVER CHAT & OTP SECURITY ================= -->', seat_modal_html + '  <!-- ================= MODAL 3: DRIVER CHAT & OTP SECURITY ================= -->')
    print("Added seatLayoutModal HTML!")

# 4. Enhance driverChatModal Header to include Phone Call button
old_chat_header = '''        <button onclick="closeModal('driverChatModal')" class="p-2 rounded-xl text-zinc-400 hover:text-white hover:bg-white/10">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>'''

new_chat_header = '''        <div class="flex items-center gap-2">
          <button id="btnCallDriverModal" onclick="callCurrentDriver()" class="px-3 py-1.5 rounded-xl bg-emerald-500/20 text-emerald-400 hover:bg-emerald-500/30 border border-emerald-500/30 font-bold text-xs flex items-center gap-1.5 transition-all">
            <span>📞 Call</span>
          </button>
          <button onclick="closeModal('driverChatModal')" class="p-2 rounded-xl text-zinc-400 hover:text-white hover:bg-white/10">
            <i data-lucide="x" class="w-5 h-5"></i>
          </button>
        </div>'''

if old_chat_header in content and 'callCurrentDriver' not in content:
    content = content.replace(old_chat_header, new_chat_header)
    print("Enhanced driverChatModal header with Call button!")

# 5. Enhance map markers in initCampusMap()
old_map_marker_block = '''      FLEET.forEach(v => {
        const pos = getCoordAtDistance(v.s);
        const icon = L.divIcon({
          className: 'pulse-marker-icon',
          html: `
            <div class="bus-marker-3d" style="background:${v.color};">
              <span class="text-sm">${v.icon}</span>
              <div class="bus-heading-needle" id="needle_${v.id}" style="transform: rotate(${pos.heading}deg)"></div>
            </div>
          `,
          iconSize: [38, 38],
          iconAnchor: [19, 19]
        });
        const m = L.marker([pos.lat, pos.lng], { icon }).addTo(map);
        m.on('click', () => selectVehicle(v.id));
        vehicleMarkers[v.id] = m;
      });'''

new_map_marker_block = '''      FLEET.forEach(v => {
        const pos = getCoordAtDistance(v.s);
        const seatColor = v.availableSeats > 2 ? '#10b981' : (v.availableSeats > 0 ? '#f59e0b' : '#ef4444');
        const icon = L.divIcon({
          className: 'pulse-marker-icon',
          html: `
            <div class="relative group cursor-pointer" onclick="selectVehicle('${v.id}')">
              <div class="bus-marker-3d" style="background:${v.color};">
                <span class="text-sm font-black">${v.icon}</span>
                <div class="bus-heading-needle" id="needle_${v.id}" style="transform: rotate(${pos.heading}deg)"></div>
              </div>
              <div class="absolute -top-7 left-1/2 -translate-x-1/2 whitespace-nowrap px-2 py-0.5 rounded-full bg-[#080c1e]/95 backdrop-blur-md border border-white/20 text-[9px] font-black shadow-xl flex items-center gap-1 z-20 pointer-events-none">
                <span class="text-brand-cyan">${v.category === 'auto' ? 'Auto' : (v.category === 'ev' ? 'EV' : 'Bus')}</span>
                <span class="w-1 h-1 rounded-full bg-zinc-500"></span>
                <span style="color:${seatColor};" class="font-mono">💺 ${v.availableSeats} free</span>
              </div>
            </div>
          `,
          iconSize: [42, 42],
          iconAnchor: [21, 21]
        });
        const m = L.marker([pos.lat, pos.lng], { icon }).addTo(map);

        // Bind interactive dark HUD popup
        const occupancyPct = Math.round((v.occupiedSeats / v.totalSeats) * 100);
        const popupContent = `
          <div class="p-3.5 space-y-2.5 min-w-[250px] text-xs font-sans">
            <div class="flex items-center justify-between border-b border-white/10 pb-2">
              <div class="flex items-center gap-2">
                <span class="text-2xl">${v.icon}</span>
                <div>
                  <h4 class="font-black text-white text-xs">${v.name}</h4>
                  <span class="text-[10px] font-bold text-brand-cyan uppercase tracking-wider">${v.typeName}</span>
                </div>
              </div>
              <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full ${v.availableSeats > 2 ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : (v.availableSeats > 0 ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' : 'bg-rose-500/20 text-rose-400 border border-rose-500/30')}">
                💺 ${v.availableSeats} Free
              </span>
            </div>

            <div class="space-y-1">
              <div class="flex items-center justify-between text-[10px] font-semibold text-zinc-300">
                <span>Seats Occupancy: <strong>${v.occupiedSeats} / ${v.totalSeats}</strong></span>
                <span class="${occupancyPct > 85 ? 'text-amber-400' : 'text-emerald-400'} font-mono">${occupancyPct}% Full</span>
              </div>
              <div class="w-full h-2 rounded-full bg-white/10 overflow-hidden">
                <div class="h-full rounded-full ${occupancyPct > 85 ? 'bg-amber-400' : 'bg-brand-cyan'}" style="width: ${occupancyPct}%"></div>
              </div>
            </div>

            <div class="p-2 rounded-xl bg-white/5 border border-white/10 flex items-center justify-between text-[11px]">
              <div>
                <p class="font-bold text-white flex items-center gap-1.5">
                  <span>👨‍✈️ ${v.driver}</span>
                  <span class="text-amber-400 font-mono text-[10px]">★ ${v.rating}</span>
                </p>
                <p class="text-[10px] text-zinc-400 font-mono">${v.plate} • ${v.phone}</p>
              </div>
              <button onclick="callDriver('${v.phone}', '${v.driver}')" class="px-2 py-1 rounded-lg bg-emerald-500/20 text-emerald-400 hover:bg-emerald-500/30 font-bold flex items-center gap-1" title="Call Driver">
                📞 Call
              </button>
            </div>

            <div class="grid grid-cols-2 gap-1.5 pt-1">
              <button onclick="openDriverChat('${v.id}')" class="py-1.5 px-2 rounded-xl bg-gradient-to-r from-brand-cyan to-brand-purple text-black font-black text-[11px] flex items-center justify-center gap-1 hover:opacity-90 shadow-sm">
                💬 Chat Driver
              </button>
              <button onclick="openSeatLayoutModal('${v.id}')" class="py-1.5 px-2 rounded-xl bg-white/10 hover:bg-white/20 text-white font-bold text-[11px] flex items-center justify-center gap-1 border border-white/15">
                💺 View Seats
              </button>
            </div>
          </div>
        `;

        m.bindPopup(popupContent, { maxWidth: 300 });
        m.on('click', () => selectVehicle(v.id));
        vehicleMarkers[v.id] = m;
      });'''

if old_map_marker_block in content:
    content = content.replace(old_map_marker_block, new_map_marker_block)
    print("Enhanced initCampusMap() marker badges and popups!")

# 6. Update renderFleetList() in sidebar
old_render_fleet = '''      container.innerHTML = filtered.map(v => {
        const isSelected = v.id === selectedVehicleId;
        const etaMin = Math.max(1, Math.round(v.s / 800));
        return `
          <div onclick="selectVehicle('${v.id}')" class="p-3.5 rounded-2xl glass-card cursor-pointer border ${isSelected ? 'border-brand-cyan bg-brand-cyan/10' : 'border-white/10'} hover:border-white/30 space-y-2">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2.5">
                <span class="text-xl">${v.icon}</span>
                <div>
                  <h4 class="text-xs font-black text-white">${v.name}</h4>
                  <p class="text-[10px] text-zinc-400 font-mono">${v.plate} • Driver: ${v.driver}</p>
                </div>
              </div>
              <div class="text-right">
                <span class="text-xs font-black text-brand-cyan">${etaMin} min ETA</span>
                <p class="text-[9px] text-zinc-400">${v.speed} km/h • ${v.battery}% 🔋</p>
              </div>
            </div>
            <div class="flex items-center justify-between pt-1 border-t border-white/5 text-[11px]">
              <span class="text-zinc-400">Seats: <strong class="text-white">${v.capacity}</strong></span>
              <div class="flex items-center gap-1.5">
                <button onclick="event.stopPropagation(); openDriverChat()" class="px-2 py-0.5 rounded-lg bg-white/10 hover:bg-white/20 text-white font-bold">
                  💬 Chat
                </button>
                <button onclick="event.stopPropagation(); openPaymentAndBookingModal()" class="px-2 py-0.5 rounded-lg bg-brand-cyan/20 text-brand-cyan hover:bg-brand-cyan hover:text-black font-bold">
                  Book (₹${v.category === 'auto' ? '30' : '15'})
                </button>
              </div>
            </div>
          </div>
        `;
      }).join('');'''

new_render_fleet = '''      container.innerHTML = filtered.map(v => {
        const isSelected = v.id === selectedVehicleId;
        const etaMin = Math.max(1, Math.round(v.s / 800));
        const occupancyPct = Math.round((v.occupiedSeats / v.totalSeats) * 100);
        const seatBadgeClass = v.availableSeats > 2 ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30' : (v.availableSeats > 0 ? 'bg-amber-500/20 text-amber-400 border-amber-500/30' : 'bg-rose-500/20 text-rose-400 border-rose-500/30');

        return `
          <div onclick="selectVehicle('${v.id}')" class="p-3.5 rounded-2xl glass-card cursor-pointer border ${isSelected ? 'border-brand-cyan bg-brand-cyan/15 ring-1 ring-brand-cyan/40' : 'border-white/10'} hover:border-white/30 space-y-2.5 transition-all">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2.5">
                <span class="text-2xl">${v.icon}</span>
                <div>
                  <h4 class="text-xs font-black text-white">${v.name}</h4>
                  <p class="text-[10px] text-brand-cyan font-bold uppercase tracking-wider">${v.typeName}</p>
                  <p class="text-[10px] text-zinc-400 font-mono">${v.plate} • 👨‍✈️ ${v.driver} (★ ${v.rating})</p>
                </div>
              </div>
              <div class="text-right">
                <span class="text-xs font-black text-brand-cyan">${etaMin} min ETA</span>
                <p class="text-[9px] text-zinc-400">${v.speed} km/h • ${v.battery}% 🔋</p>
              </div>
            </div>

            <!-- Seat Occupancy Meter -->
            <div class="space-y-1 bg-black/30 p-2 rounded-xl border border-white/5">
              <div class="flex items-center justify-between text-[10px]">
                <span class="text-zinc-400">Available Seats:</span>
                <span class="font-mono font-bold px-2 py-0.5 rounded-full border ${seatBadgeClass}">
                  💺 ${v.availableSeats} of ${v.totalSeats} free
                </span>
              </div>
              <div class="w-full h-1.5 rounded-full bg-white/10 overflow-hidden">
                <div class="h-full rounded-full ${occupancyPct > 85 ? 'bg-amber-400' : 'bg-brand-cyan'}" style="width: ${occupancyPct}%"></div>
              </div>
            </div>

            <!-- Action buttons -->
            <div class="flex items-center justify-between pt-1 border-t border-white/5 text-[11px]">
              <span class="text-zinc-400 font-bold">Fare: <strong class="text-white font-mono">₹${v.fare}</strong></span>
              <div class="flex items-center gap-1.5">
                <button onclick="event.stopPropagation(); openDriverChat('${v.id}')" class="px-2.5 py-1 rounded-xl bg-gradient-to-r from-brand-cyan to-brand-purple text-black font-black hover:opacity-90 flex items-center gap-1 shadow-sm">
                  💬 Chat
                </button>
                <button onclick="event.stopPropagation(); openSeatLayoutModal('${v.id}')" class="px-2.5 py-1 rounded-xl bg-white/10 hover:bg-white/20 text-white font-bold border border-white/10 flex items-center gap-1">
                  💺 Seats
                </button>
                <button onclick="event.stopPropagation(); bookSpecificVehicle('${v.id}')" class="px-2.5 py-1 rounded-xl bg-brand-cyan/20 text-brand-cyan hover:bg-brand-cyan hover:text-black font-bold">
                  Book
                </button>
              </div>
            </div>
          </div>
        `;
      }).join('');'''

if old_render_fleet in content:
    content = content.replace(old_render_fleet, new_render_fleet)
    print("Enhanced renderFleetList() sidebar cards with seats and vehicle types!")

# 7. Add JavaScript functions for Seat Layout & enhanced Driver Chat
js_new_functions = '''
    // ================= SEAT LAYOUT & DRIVER CHAT EXTENSIONS =================
    let currentSeatModalVehicleId = 'bus_1';
    let selectedSeatNumber = null;

    function callDriver(phone, name) {
      playBeep(440, 'sine', 0.1);
      setTimeout(() => playBeep(580, 'sine', 0.15), 120);
      showToast(`📞 Dialing Driver ${name} (${phone})...`);
    }

    function callCurrentDriver() {
      const v = FLEET.find(x => x.id === selectedVehicleId) || FLEET[0];
      callDriver(v.phone, v.driver);
    }

    function bookSpecificVehicle(id) {
      selectedVehicleId = id;
      openPaymentAndBookingModal();
    }

    function openSeatLayoutModal(vehicleId) {
      currentSeatModalVehicleId = vehicleId || selectedVehicleId || 'bus_1';
      const v = FLEET.find(x => x.id === currentSeatModalVehicleId) || FLEET[0];
      selectedVehicleId = v.id;
      selectedSeatNumber = null;

      document.getElementById('seatModalVehicleIcon').textContent = v.icon;
      document.getElementById('seatModalVehicleName').textContent = v.name;
      document.getElementById('seatModalVehiclePlate').textContent = v.plate;
      document.getElementById('seatModalVehicleType').textContent = `${v.typeName} • Driver: ${v.driver} (★ ${v.rating})`;
      document.getElementById('seatModalStatsText').textContent = `${v.availableSeats} of ${v.totalSeats} Seats Free`;
      document.getElementById('seatModalFareText').textContent = `Fare: ₹${v.fare}`;

      document.getElementById('selectedSeatLabel').textContent = 'Click an available green seat to select';
      document.getElementById('selectedSeatSubtitle').textContent = 'Window or aisle seats available with live USB charging';
      document.getElementById('selectedSeatPrice').textContent = '';

      renderSeatGrid(v);
      openModal('seatLayoutModal');
    }

    function renderSeatGrid(v) {
      const container = document.getElementById('seatGridContainer');
      if (!container) return;

      if (v.category === 'auto') {
        // Auto Rickshaw Layout: 1 front driver + 3 rear seats
        container.innerHTML = `
          <div class="text-center text-[10px] text-zinc-400 font-bold uppercase tracking-wider mb-2">Auto Rickshaw Passenger Cabin</div>
          <div class="grid grid-cols-3 gap-3 max-w-sm mx-auto">
            <button onclick="pickSeat('Seat 1 (Window)', ${v.fare})" class="p-4 rounded-2xl border ${v.availableSeats >= 1 ? 'bg-emerald-500/20 border-emerald-500 text-emerald-300 hover:scale-105' : 'bg-rose-500/20 border-rose-500/40 text-rose-400 cursor-not-allowed'} font-bold text-center flex flex-col items-center gap-1 transition-all">
              <span class="text-xl">💺</span>
              <span class="text-xs font-black">Seat 1</span>
              <span class="text-[9px] text-zinc-400">Left Window</span>
            </button>
            <button onclick="pickSeat('Seat 2 (Center)', ${v.fare})" class="p-4 rounded-2xl border ${v.availableSeats >= 2 ? 'bg-emerald-500/20 border-emerald-500 text-emerald-300 hover:scale-105' : 'bg-rose-500/20 border-rose-500/40 text-rose-400 cursor-not-allowed'} font-bold text-center flex flex-col items-center gap-1 transition-all">
              <span class="text-xl">💺</span>
              <span class="text-xs font-black">Seat 2</span>
              <span class="text-[9px] text-zinc-400">Center</span>
            </button>
            <button onclick="pickSeat('Seat 3 (Window)', ${v.fare})" class="p-4 rounded-2xl border ${v.availableSeats >= 3 ? 'bg-emerald-500/20 border-emerald-500 text-emerald-300 hover:scale-105' : 'bg-rose-500/20 border-rose-500/40 text-rose-400 cursor-not-allowed'} font-bold text-center flex flex-col items-center gap-1 transition-all">
              <span class="text-xl">💺</span>
              <span class="text-xs font-black">Seat 3</span>
              <span class="text-[9px] text-zinc-400">Right Window</span>
            </button>
          </div>
        `;
      } else if (v.category === 'ev') {
        // Eco EV Cart: 2 rows of 3 seats
        container.innerHTML = `
          <div class="text-center text-[10px] text-zinc-400 font-bold uppercase tracking-wider mb-2">Eco Electric Shuttle Cart Seating</div>
          <div class="space-y-3 max-w-sm mx-auto">
            <div class="text-[10px] font-bold text-zinc-400">Row 1 (Front Facing)</div>
            <div class="grid grid-cols-3 gap-2">
              ${[1, 2, 3].map(n => {
                const isFree = n <= v.availableSeats;
                return `
                  <button onclick="${isFree ? `pickSeat('Seat ${n} (Row 1)', ${v.fare})` : ''}" class="p-3 rounded-xl border ${isFree ? 'bg-emerald-500/20 border-emerald-500 text-emerald-300 hover:scale-105' : 'bg-rose-500/20 border-rose-500/40 text-rose-400 cursor-not-allowed'} text-center font-bold flex flex-col items-center gap-1 transition-all">
                    <span>💺</span>
                    <span class="text-xs">S${n}</span>
                  </button>
                `;
              }).join('')}
            </div>
            <div class="text-[10px] font-bold text-zinc-400 pt-2">Row 2 (Rear Bench)</div>
            <div class="grid grid-cols-3 gap-2">
              ${[4, 5, 6].map(n => {
                const isFree = n <= v.availableSeats;
                return `
                  <button onclick="${isFree ? `pickSeat('Seat ${n} (Row 2)', ${v.fare})` : ''}" class="p-3 rounded-xl border ${isFree ? 'bg-emerald-500/20 border-emerald-500 text-emerald-300 hover:scale-105' : 'bg-rose-500/20 border-rose-500/40 text-rose-400 cursor-not-allowed'} text-center font-bold flex flex-col items-center gap-1 transition-all">
                    <span>💺</span>
                    <span class="text-xs">S${n}</span>
                  </button>
                `;
              }).join('')}
            </div>
          </div>
        `;
      } else {
        // 50-Seater Bus Layout: 8 rows of 2x2 with aisle
        let rowsHtml = '';
        const totalRows = 8;
        const freeCount = v.availableSeats;
        let freeAssigned = 0;

        for (let r = 1; r <= totalRows; r++) {
          const seatsInRow = ['A', 'B', 'C', 'D'];
          const buttons = seatsInRow.map((col, idx) => {
            const isFree = (r * 4 + idx) % 5 === 0 && freeAssigned < freeCount;
            if (isFree) freeAssigned++;
            const seatName = `${r}${col}`;
            const isWindow = col === 'A' || col === 'D';
            return `
              <button onclick="${isFree ? `pickSeat('Seat ${seatName} (${isWindow ? 'Window' : 'Aisle'})', ${v.fare})` : ''}" class="p-2 sm:p-2.5 rounded-xl border ${isFree ? 'bg-emerald-500/20 border-emerald-500 text-emerald-300 hover:scale-105 hover:bg-emerald-500/30' : 'bg-rose-500/15 border-rose-500/30 text-rose-400/70 cursor-not-allowed'} text-center font-bold flex flex-col items-center gap-0.5 transition-all text-xs">
                <span>💺</span>
                <span class="font-mono font-bold">${seatName}</span>
                <span class="text-[8px] text-zinc-400">${isWindow ? 'Win' : 'Ais'}</span>
              </button>
            `;
          });

          rowsHtml += `
            <div class="flex items-center justify-between gap-2">
              <div class="grid grid-cols-2 gap-2 flex-1">
                ${buttons[0]}
                ${buttons[1]}
              </div>
              <div class="w-8 text-center text-[10px] text-zinc-500 font-mono tracking-widest font-black">AISLE</div>
              <div class="grid grid-cols-2 gap-2 flex-1">
                ${buttons[2]}
                ${buttons[3]}
              </div>
            </div>
          `;
        }
        container.innerHTML = rowsHtml;
      }
    }

    function pickSeat(seatName, fare) {
      selectedSeatNumber = seatName;
      playBeep(520, 'sine', 0.08);

      document.getElementById('selectedSeatLabel').innerHTML = `✅ Selected: <strong class="text-brand-cyan">${seatName}</strong>`;
      document.getElementById('selectedSeatSubtitle').textContent = 'Seat reserved for you on this campus vehicle';
      document.getElementById('selectedSeatPrice').textContent = `₹${fare}`;
      showToast(`Selected ${seatName}! Click "Confirm Seat & Ride" below.`);
    }

    function confirmSeatBooking() {
      const v = FLEET.find(x => x.id === currentSeatModalVehicleId) || FLEET[0];
      const seat = selectedSeatNumber || `Seat 2A (${v.category === 'auto' ? 'Window' : 'Front'})`;

      closeModal('seatLayoutModal');
      activeOtpCode = Math.floor(1000 + Math.random() * 9000);

      // Deduct from wallet if balance is available
      if (walletBalance >= v.fare) {
        walletBalance -= v.fare;
        walletHistory.unshift({
          type: 'ride',
          title: `${v.name} (${seat})`,
          date: 'Just now',
          amount: -v.fare,
          method: 'Campus Smart Pass'
        });
        updateWalletDisplay();
      }

      showToast(`🎉 ${seat} reserved on ${v.name}! OTP: ${activeOtpCode}`);

      // Open driver chat directly with the reservation
      openDriverChat(v.id);
      driverChatHistory.push({
        sender: 'user',
        text: `Bhaiya, maine ${v.name} me ${seat} book kiya hai. Mera verification OTP ${activeOtpCode} hai.`
      });
      renderChatMessages();

      setTimeout(() => {
        driverChatHistory.push({
          sender: 'driver',
          text: `Haanji student ji! ${seat} maine reserve kar di hai. OTP ${activeOtpCode} confirm ho gaya. Main 2 minute me aapke stop par aa raha hoon!`
        });
        renderChatMessages();
        playBeep(600, 'sine', 0.1);
      }, 800);
    }
'''

if 'function openSeatLayoutModal' not in content:
    content = content.replace('// Driver Chat Modal', js_new_functions + '\n    // Driver Chat Modal')
    print("Added Seat Layout and Driver Call JavaScript functions!")

# 8. Upgrade openDriverChat() to accept vehicleId parameter and update dynamic details
old_open_chat = '''    // Driver Chat Modal
    function openDriverChat() {
      const v = FLEET.find(x => x.id === selectedVehicleId) || FLEET[1];
      document.getElementById('chatDriverName').textContent = v.driver;
      document.getElementById('chatPlate').textContent = v.plate;
      document.getElementById('chatVehicleType').textContent = `${v.name} • Rating: 4.9 ★`;
      document.getElementById('chatOtpDisplay').textContent = activeOtpCode;
      renderChatMessages();
      openModal('driverChatModal');
    }'''

new_open_chat = '''    // Driver Chat Modal
    function openDriverChat(vehicleId) {
      if (vehicleId) {
        selectedVehicleId = vehicleId;
      }
      const v = FLEET.find(x => x.id === selectedVehicleId) || FLEET[0];
      
      const dName = document.getElementById('chatDriverName');
      if (dName) dName.textContent = v.driver;
      const dPlate = document.getElementById('chatPlate');
      if (dPlate) dPlate.textContent = v.plate;
      const dType = document.getElementById('chatVehicleType');
      if (dType) dType.textContent = `${v.typeName} • 💺 ${v.availableSeats} Seats Free • Rating: ${v.rating} ★`;
      const otpDisplay = document.getElementById('chatOtpDisplay');
      if (otpDisplay) otpDisplay.textContent = activeOtpCode;

      // Set fresh driver greeting if history is empty
      if (!driverChatHistory || driverChatHistory.length <= 1) {
        driverChatHistory = [
          { sender: 'driver', text: `Namaste! Main <strong>${v.driver}</strong> (${v.name}). Meri gaadi me <strong>${v.availableSeats} seats</strong> abhi khali hain. Aap kahan wait kar rahe hain?` }
        ];
      }

      renderChatMessages();
      openModal('driverChatModal');
    }'''

if old_open_chat in content:
    content = content.replace(old_open_chat, new_open_chat)
    print("Upgraded openDriverChat() with vehicleId parameter and dynamic driver greeting!")

with open('build_full_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved all updates to build_full_app.py successfully!")

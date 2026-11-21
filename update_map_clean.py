with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

idx = text.find("function initCampusMap()")
idx_end = text.find("let currentMapTileLayers = [];", idx)

assert idx != -1, "initCampusMap not found"
assert idx_end != -1, "currentMapTileLayers not found"

new_init_map = """function initCampusMap() {
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

      // 1. LPU Campus Landmarks, Academic Blocks 1-36, Hostels & Parkings
      LPU_STOPS.forEach(stop => {
        const icon = L.divIcon({
          className: 'pulse-marker-icon',
          html: `
            <div class="relative group cursor-pointer flex items-center justify-center">
              <div class="w-7 h-7 rounded-xl bg-white border border-black text-xs flex items-center justify-center shadow-md hover:scale-125 transition-transform">
                <span>${stop.icon || '📍'}</span>
              </div>
              <div class="absolute -bottom-6 left-1/2 -translate-x-1/2 whitespace-nowrap px-1.5 py-0.5 rounded-md bg-black text-white border border-zinc-700 text-[9px] font-black pointer-events-none hidden group-hover:block z-30">
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

      // 2. Active Moving Fleet Markers (All 8 Moving Campus Vehicles)
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

    """

text = text[:idx] + new_init_map + text[idx_end:]

with open("index.html", "w", encoding="utf-8") as f:
    f.write(text)

print("update_map_clean.py succeeded!")

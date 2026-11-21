import re

with open('build_full_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Define the complete LPU setup
lpu_code = '''    // ================= LOVELY PROFESSIONAL UNIVERSITY (LPU) MULTI-ROUTE TRANSIT =================
    // 21 Verified Campus Landmarks, Blocks 1-36, Hostels BH 1-12, GH 1-7, UniMall, Unipolis & Parkings
    const LPU_STOPS = [
      // Primary Gate & Admin
      { id: 'lpu_main_gate', name: 'Main Gate (GT Road NH-44)', code: 'MG', cat: 'gate', icon: '⛩️', lat: 31.2485, lng: 75.7015, desc: 'Main University Entrance, Welcome Arch & Security Checkpoint' },
      { id: 'lpu_admission', name: 'Admission Block (Block 30)', code: 'AB-30', cat: 'admin', icon: '🏛️', lat: 31.2500, lng: 75.7032, desc: 'Division of Admissions, International Relations & Student Center' },
      
      // Central Student Hubs
      { id: 'lpu_unimall', name: 'UniMall Student Complex', code: 'UM', cat: 'mall', icon: '🛍️', lat: 31.2518, lng: 75.7042, desc: '5-Story Campus Mall: Food Courts, Banks, Stationery, Supermarket & Salon' },
      { id: 'lpu_unipolis', name: 'Unipolis Open Amphitheatre', code: 'UP', cat: 'landmark', icon: '🎪', lat: 31.2535, lng: 75.7040, desc: 'Iconic Covered Mega Arena & Campus Cultural Heart' },
      { id: 'lpu_library', name: 'Central Library (B.R. Mittal)', code: 'LIB', cat: 'library', icon: '📚', lat: 31.2555, lng: 75.7038, desc: '9-Story Resource Library, 24/7 Digital Archives & Quiet Reading Halls' },
      { id: 'lpu_robopark', name: 'Robopark & Innovation Arena', code: 'ROBO', cat: 'innov', icon: '🤖', lat: 31.2578, lng: 75.7065, desc: 'Robotics Center, Drone Arena, AI Labs & Electric Vehicle Prototyping' },

      // Sports & Fitness
      { id: 'lpu_cricket', name: 'International Cricket Stadium', code: 'CS', cat: 'sports', icon: '🏏', lat: 31.2530, lng: 75.7095, desc: 'ICC-Standard Turf Pitch, Pavilion & Floodlit Night Matches' },
      { id: 'lpu_indoor_sports', name: 'Indoor Sports Complex & Gym', code: 'ISC', cat: 'sports', icon: '🏊', lat: 31.2550, lng: 75.7100, desc: 'Olympic Swimming Pool, 12 Badminton Courts, Squash & High-Performance Gym' },

      // 4 Dedicated Campus Parkings
      { id: 'lpu_parking_1', name: 'Parking P1 (Main Gate & Visitors)', code: 'P1', cat: 'parking', icon: '🅿️', lat: 31.2492, lng: 75.7030, desc: 'Capacity: 350 Vehicles • EV Fast Charging Stations' },
      { id: 'lpu_parking_2', name: 'Parking P2 (UniMall Multilevel)', code: 'P2', cat: 'parking', icon: '🅿️', lat: 31.2520, lng: 75.7052, desc: 'Capacity: 500 Vehicles • Student 2-Wheelers & Day-Scholar Cars' },
      { id: 'lpu_parking_3', name: 'Parking P3 (Block 34 North Parking)', code: 'P3', cat: 'parking', icon: '🅿️', lat: 31.2575, lng: 75.7045, desc: 'Capacity: 300 Vehicles • Engineering Faculty & Tech Commuters' },
      { id: 'lpu_parking_4', name: 'Parking P4 (Sports Arena East)', code: 'P4', cat: 'parking', icon: '🅿️', lat: 31.2555, lng: 75.7115, desc: 'Capacity: 400 Vehicles • Tournament & Stadium Parking' },

      // Academic Block Clusters (Blocks 1 to 36)
      { id: 'lpu_blocks_1_5', name: 'Academic Blocks 1-5 (Polytechnic)', code: 'B1-5', cat: 'academic', icon: '🏫', lat: 31.2510, lng: 75.7018, desc: 'Blocks 1, 2, 3, 4, 5 — Diploma, Physics, Basic Chemistry & Electrical Labs' },
      { id: 'lpu_blocks_6_10', name: 'Academic Blocks 6-10 (Applied Sciences)', code: 'B6-10', cat: 'academic', icon: '🏫', lat: 31.2528, lng: 75.7022, desc: 'Blocks 6, 7, 8, 9, 10 — Mathematics, Humanities, Social Sciences & Languages' },
      { id: 'lpu_blocks_11_15', name: 'Academic Blocks 11-15 (Business & Law)', code: 'B11-15', cat: 'academic', icon: '🏫', lat: 31.2545, lng: 75.7025, desc: 'Blocks 11 to 15 — Mittal School of Business, Moot Court & Economics' },
      { id: 'lpu_blocks_16_24', name: 'Academic Blocks 16-24 (Design & Media)', code: 'B16-24', cat: 'academic', icon: '🏫', lat: 31.2562, lng: 75.7032, desc: 'Blocks 16 to 24 — Fashion Design Studios, Architecture & Film Making' },
      { id: 'lpu_blocks_25_29', name: 'Academic Blocks 25-29 (Agri & Biotech)', code: 'B25-29', cat: 'academic', icon: '🏫', lat: 31.2582, lng: 75.7042, desc: 'Blocks 25 to 29 — Agriculture Research Farms, Pharmacy & Bio-Tech Labs' },
      { id: 'lpu_blocks_31_36', name: 'Academic Blocks 31-36 (CSE & Tech Hub)', code: 'B31-36', cat: 'academic', icon: '💻', lat: 31.2568, lng: 75.7052, desc: 'Blocks 31 to 36 — School of CSE, Supercomputing, Data Science & Placement Hub' },

      // Hostels
      { id: 'lpu_girls_hostels', name: 'Girls Hostels Sector (GH 1 to GH 7)', code: 'GH1-7', cat: 'hostel_girls', icon: '🏡', lat: 31.2508, lng: 75.7068, desc: 'Residential Sector GH-1 to GH-7: Dedicated Dining, Salon & Strict Curfew Security' },
      { id: 'lpu_boys_hostels_1_6', name: 'Boys Hostels North (BH 1 to BH 6)', code: 'BH1-6', cat: 'hostel_boys', icon: '🏢', lat: 31.2592, lng: 75.7052, desc: 'Residential Towers BH-1, BH-2, BH-3, BH-4, BH-5, BH-6 along North Avenue' },
      { id: 'lpu_boys_hostels_7_12', name: 'Boys Hostels East (BH 7 to BH 12)', code: 'BH7-12', cat: 'hostel_boys', icon: '🏢', lat: 31.2572, lng: 75.7092, desc: 'Residential Towers BH-7, BH-8, BH-9, BH-10, BH-11, BH-12 near Sports Complex' }
    ];

    const STOPS = LPU_STOPS; // Backward compatibility

    // 4 Complex, Intersecting Transit Routes around LPU Roads
    const LPU_ROUTES = {
      route_purple: {
        id: 'route_purple',
        name: 'Ring Road & Hostels Loop',
        code: 'LINE-1',
        color: '#a855f7',
        coords: [
          [31.2485, 75.7015], [31.2492, 75.7030], [31.2500, 75.7032], [31.2508, 75.7068],
          [31.2520, 75.7080], [31.2530, 75.7095], [31.2550, 75.7100], [31.2555, 75.7115],
          [31.2570, 75.7105], [31.2572, 75.7092], [31.2585, 75.7075], [31.2578, 75.7065],
          [31.2592, 75.7052], [31.2582, 75.7042], [31.2562, 75.7032], [31.2545, 75.7025],
          [31.2528, 75.7022], [31.2510, 75.7018], [31.2485, 75.7015]
        ]
      },
      route_cyan: {
        id: 'route_cyan',
        name: 'Academic Core & Blocks 1-36',
        code: 'LINE-2',
        color: '#00f0ff',
        coords: [
          [31.2485, 75.7015], [31.2510, 75.7018], [31.2528, 75.7022], [31.2545, 75.7025],
          [31.2535, 75.7040], [31.2555, 75.7038], [31.2568, 75.7052], [31.2578, 75.7065],
          [31.2575, 75.7045], [31.2582, 75.7042], [31.2562, 75.7032], [31.2555, 75.7038],
          [31.2535, 75.7040], [31.2518, 75.7042], [31.2492, 75.7030], [31.2485, 75.7015]
        ]
      },
      route_emerald: {
        id: 'route_emerald',
        name: 'Auto Rapid Cross-Campus Connect',
        code: 'LINE-3',
        color: '#10b981',
        coords: [
          [31.2572, 75.7092], [31.2550, 75.7100], [31.2530, 75.7095], [31.2518, 75.7042],
          [31.2520, 75.7052], [31.2508, 75.7068], [31.2500, 75.7032], [31.2510, 75.7018],
          [31.2535, 75.7040], [31.2568, 75.7052], [31.2592, 75.7052], [31.2578, 75.7065],
          [31.2572, 75.7092]
        ]
      },
      route_amber: {
        id: 'route_amber',
        name: 'Eco EV Green Campus Circulator',
        code: 'LINE-4',
        color: '#f59e0b',
        coords: [
          [31.2578, 75.7065], [31.2568, 75.7052], [31.2555, 75.7038], [31.2535, 75.7040],
          [31.2518, 75.7042], [31.2508, 75.7068], [31.2530, 75.7095], [31.2550, 75.7100],
          [31.2555, 75.7115], [31.2570, 75.7105], [31.2578, 75.7065]
        ]
      }
    };

    const CAMPUS_ROUTE_COORDS = LPU_ROUTES.route_purple.coords;

    // Simulation Fleet with Real-time Seat Occupancy, Route Assignment & Independent Offsets
    let FLEET = [
      { id: 'bus_1', category: 'bus', routeId: 'route_purple', typeName: '50-Seater Campus Shuttle', name: 'Shuttle #1 (Ring Loop)', plate: 'PB 08 BX 9021', driver: 'Rajesh Sharma', phone: '+91 98765-43210', totalSeats: 50, occupiedSeats: 42, availableSeats: 8, fare: 15, rating: 4.9, speed: 28, battery: 84, s: 300, icon: '🚌', color: '#a855f7', delay: 0 },
      { id: 'auto_2', category: 'auto', routeId: 'route_emerald', typeName: '3-Seater Campus Auto', name: 'Auto #2 (Hostels ➔ UniMall)', plate: 'PB 08 CA 1201', driver: 'Vikram Singh', phone: '+91 98140-55672', totalSeats: 3, occupiedSeats: 2, availableSeats: 1, fare: 30, rating: 4.8, speed: 32, battery: 92, s: 200, icon: '🛺', color: '#10b981', delay: 0 },
      { id: 'ev_3', category: 'ev', routeId: 'route_amber', typeName: '6-Seater Eco EV Cart', name: 'Eco EV #3 (Robopark Circulator)', plate: 'PB 08 EV 0044', driver: 'Suresh Yadav', phone: '+91 94170-88321', totalSeats: 6, occupiedSeats: 5, availableSeats: 1, fare: 10, rating: 4.9, speed: 20, battery: 78, s: 400, icon: '⚡', color: '#f59e0b', delay: 0 },
      { id: 'bus_4', category: 'bus', routeId: 'route_cyan', typeName: '50-Seater Express Bus', name: 'Express #4 (Blocks 1-36 Core)', plate: 'PB 08 BX 9410', driver: 'Amit Patel', phone: '+91 99882-11490', totalSeats: 50, occupiedSeats: 35, availableSeats: 15, fare: 15, rating: 4.7, speed: 30, battery: 65, s: 800, icon: '🚌', color: '#00f0ff', delay: 0 },
      { id: 'auto_5', category: 'auto', routeId: 'route_emerald', typeName: '3-Seater Campus Auto', name: 'Auto #5 (Sports & Unipolis)', plate: 'PB 08 CA 3381', driver: 'Priya Verma', phone: '+91 98721-66710', totalSeats: 3, occupiedSeats: 1, availableSeats: 2, fare: 30, rating: 5.0, speed: 31, battery: 88, s: 1300, icon: '🛺', color: '#10b981', delay: 0 },
      { id: 'ev_6', category: 'ev', routeId: 'route_amber', typeName: '6-Seater Medical & Sports Cart', name: 'Eco EV #6 (Library Shuttle)', plate: 'PB 08 EV 0092', driver: 'Sunita Gupta', phone: '+91 94630-11220', totalSeats: 6, occupiedSeats: 4, availableSeats: 2, fare: 10, rating: 4.9, speed: 18, battery: 95, s: 1500, icon: '⚡', color: '#f59e0b', delay: 0 },
      { id: 'bus_7', category: 'bus', routeId: 'route_purple', typeName: '50-Seater AC Shuttle', name: 'Shuttle #7 (BH 1-12 & UniMall)', plate: 'PB 08 BX 8812', driver: 'Ramesh Kumar', phone: '+91 98155-77441', totalSeats: 50, occupiedSeats: 48, availableSeats: 2, fare: 15, rating: 4.8, speed: 26, battery: 54, s: 2100, icon: '🚌', color: '#a855f7', delay: 0 },
      { id: 'auto_8', category: 'auto', routeId: 'route_emerald', typeName: '3-Seater Campus Auto', name: 'Auto #8 (GH 1-7 & Admission)', plate: 'PB 08 CA 5509', driver: 'Deepak Sharma', phone: '+91 98788-33219', totalSeats: 3, occupiedSeats: 0, availableSeats: 3, fare: 30, rating: 4.9, speed: 33, battery: 90, s: 2500, icon: '🛺', color: '#10b981', delay: 0 }
    ];

    // Precompute Cumulative Distances for All Routes
    function haversineDist(c1, c2) {
      const R = 6371000;
      const dLat = (c2[0] - c1[0]) * Math.PI / 180;
      const dLng = (c2[1] - c1[1]) * Math.PI / 180;
      const a = Math.sin(dLat/2)**2 + Math.cos(c1[0]*Math.PI/180) * Math.cos(c2[0]*Math.PI/180) * Math.sin(dLng/2)**2;
      return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    }

    Object.keys(LPU_ROUTES).forEach(k => {
      const r = LPU_ROUTES[k];
      r.totalDist = 0;
      r.cumDistances = [0];
      for (let i = 0; i < r.coords.length - 1; i++) {
        const d = haversineDist(r.coords[i], r.coords[i+1]);
        r.totalDist += d;
        r.cumDistances.push(r.totalDist);
      }
    });

    let routeTotalDist = LPU_ROUTES.route_purple.totalDist;

    function getCoordOnRoute(routeId, dist) {
      const r = LPU_ROUTES[routeId] || LPU_ROUTES.route_purple;
      const d = (dist % r.totalDist + r.totalDist) % r.totalDist;
      for (let i = 0; i < r.cumDistances.length - 1; i++) {
        if (d >= r.cumDistances[i] && d <= r.cumDistances[i+1]) {
          const segDist = r.cumDistances[i+1] - r.cumDistances[i];
          const frac = segDist === 0 ? 0 : (d - r.cumDistances[i]) / segDist;
          const p1 = r.coords[i];
          const p2 = r.coords[i+1];
          const lat = p1[0] + (p2[0] - p1[0]) * frac;
          const lng = p1[1] + (p2[1] - p1[1]) * frac;
          const heading = Math.atan2(p2[1] - p1[1], p2[0] - p1[0]) * 180 / Math.PI;
          return { lat, lng, heading };
        }
      }
      return { lat: r.coords[0][0], lng: r.coords[0][1], heading: 0 };
    }

    function getCoordAtDistance(dist) {
      return getCoordOnRoute('route_purple', dist);
    }
'''

# Replace from `// Verified Campus Road Network Stops` or `const STOPS = [` to `// Initialize Campus Map`
stops_start = content.find('const STOPS = [')
if stops_start == -1:
    stops_start = content.find('const LPU_STOPS = [')

init_map_start = content.find('function initCampusMap() {')

if stops_start != -1 and init_map_start != -1:
    # replace between stops_start and init_map_start
    content = content[:stops_start] + lpu_code + '\n    ' + content[init_map_start:]
    print("Replaced Stops, Routes and FLEET with LPU Multi-Route system!")

# Update initCampusMap() to render all 4 routes, LPU landmarks with categories & route legend
old_init_map = '''    function initCampusMap() {
      if (map) return;
      map = L.map('campusMap', { zoomControl: false }).setView([31.2548, 75.7058], 16);
      setMapTheme('dark');

      routePolylineLayer = L.polyline(CAMPUS_ROUTE_COORDS, {
        color: '#00f0ff',
        weight: 5,
        opacity: 0.85,
        dashArray: '8, 8',
        lineCap: 'round'
      }).addTo(map);'''

new_init_map = '''    let routePolylineLayers = {};

    function initCampusMap() {
      if (map) return;
      map = L.map('campusMap', { zoomControl: false }).setView([31.2540, 75.7055], 16);
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

      routePolylineLayer = routePolylineLayers.route_purple;'''

if old_init_map in content:
    content = content.replace(old_init_map, new_init_map)
    print("Updated initCampusMap with 4 multi-route polylines!")

# Update stop markers rendering in initCampusMap() to handle categories & rich icons
old_stops_render = '''      // Stop Markers aligned on campus road curbs
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
      });'''

new_stops_render = '''      // LPU Campus Landmarks, Academic Blocks 1-36, Hostels & Parkings
      LPU_STOPS.forEach(stop => {
        const catColors = {
          gate: '#00f0ff',
          admin: '#a855f7',
          mall: '#f59e0b',
          landmark: '#6366f1',
          library: '#3b82f6',
          innov: '#06b6d4',
          sports: '#10b981',
          parking: '#eab308',
          academic: '#8b5cf6',
          hostel_girls: '#ec4899',
          hostel_boys: '#3b82f6'
        };
        const color = catColors[stop.cat] || '#00f0ff';

        const icon = L.divIcon({
          className: 'pulse-marker-icon',
          html: `
            <div class="relative group cursor-pointer">
              <div class="w-6 h-6 rounded-xl bg-[#0b0f22]/90 border border-white/30 text-xs flex items-center justify-center shadow-lg hover:scale-125 transition-transform" style="box-shadow: 0 0 10px ${color}66;">
                <span>${stop.icon || '📍'}</span>
              </div>
              <div class="absolute -bottom-6 left-1/2 -translate-x-1/2 whitespace-nowrap px-1.5 py-0.5 rounded-md bg-black/90 border border-white/20 text-[9px] font-black text-white pointer-events-none hidden group-hover:block z-30">
                ${stop.name}
              </div>
            </div>
          `,
          iconSize: [24, 24],
          iconAnchor: [12, 12]
        });

        const marker = L.marker([stop.lat, stop.lng], { icon }).addTo(map);
        marker.bindPopup(`
          <div class="p-3 text-xs font-sans space-y-1.5 min-w-[230px]">
            <div class="flex items-center gap-2 border-b border-white/10 pb-1.5">
              <span class="text-xl">${stop.icon || '📍'}</span>
              <div>
                <strong class="text-white font-black text-xs">${stop.name}</strong>
                <span class="text-[10px] font-mono text-brand-cyan font-bold block">Code: ${stop.code}</span>
              </div>
            </div>
            <p class="text-[11px] text-zinc-300 leading-snug">${stop.desc}</p>
            <div class="pt-1.5 flex items-center justify-between text-[10px] font-mono text-emerald-400 border-t border-white/10">
              <span>● LPU Active Station</span>
              <button onclick="filterByStop('${stop.id}')" class="text-brand-cyan underline font-bold">Find Shuttles →</button>
            </div>
          </div>
        `);
        stopMarkers.push(marker);
      });'''

if old_stops_render in content:
    content = content.replace(old_stops_render, new_stops_render)
    print("Updated LPU landmark markers rendering!")

# Update vehicle positioning in initCampusMap()
old_init_fleet = "const pos = getCoordAtDistance(v.s);"
new_init_fleet = "const pos = getCoordOnRoute(v.routeId, v.s);"
content = content.replace(old_init_fleet, new_init_fleet)

# Update simulation loop to advance each vehicle along its respective route
old_sim_loop = '''        FLEET.forEach(v => {
          v.s = (v.s + v.speed * dt * 2.5) % routeTotalDist;
          const pos = getCoordAtDistance(v.s);
          if (vehicleMarkers[v.id]) {
            vehicleMarkers[v.id].setLatLng([pos.lat, pos.lng]);
            const needle = document.getElementById(`needle_${v.id}`);
            if (needle) needle.style.transform = `rotate(${pos.heading}deg)`;
          }
        });'''

new_sim_loop = '''        FLEET.forEach(v => {
          const r = LPU_ROUTES[v.routeId] || LPU_ROUTES.route_purple;
          v.s = (v.s + v.speed * dt * 2.8) % r.totalDist;
          const pos = getCoordOnRoute(v.routeId, v.s);
          if (vehicleMarkers[v.id]) {
            vehicleMarkers[v.id].setLatLng([pos.lat, pos.lng]);
            const needle = document.getElementById(`needle_${v.id}`);
            if (needle) needle.style.transform = `rotate(${pos.heading}deg)`;
          }
        });'''

if old_sim_loop in content:
    content = content.replace(old_sim_loop, new_sim_loop)
    print("Updated simulation loop for multi-route independent vehicle movement!")

# Update selectVehicle() to use getCoordOnRoute
old_select_vehicle = '''    function selectVehicle(id) {
      selectedVehicleId = id;
      renderFleetList();
      const v = FLEET.find(x => x.id === id);
      if (v && map) {
        const pos = getCoordAtDistance(v.s);
        map.panTo([pos.lat, pos.lng], { animate: true, duration: 0.5 });
      }
    }'''

new_select_vehicle = '''    function selectVehicle(id) {
      selectedVehicleId = id;
      renderFleetList();
      const v = FLEET.find(x => x.id === id);
      if (v && map) {
        const pos = getCoordOnRoute(v.routeId, v.s);
        map.panTo([pos.lat, pos.lng], { animate: true, duration: 0.5 });
        if (vehicleMarkers[id]) vehicleMarkers[id].openPopup();
      }
    }'''

if old_select_vehicle in content:
    content = content.replace(old_select_vehicle, new_select_vehicle)
    print("Updated selectVehicle() to pan and open popup on the correct route!")

# Add filterByStop function
if 'function filterByStop' not in content:
    content = content.replace('function selectVehicle(id) {', '''function filterByStop(stopId) {
      const s = LPU_STOPS.find(x => x.id === stopId);
      if (!s) return;
      document.getElementById('transitSearchInput').value = s.code;
      renderFleetList();
      showToast(`Filtered routes for ${s.name} (${s.code})`);
    }

    function selectVehicle(id) {''')
    print("Added filterByStop function!")

with open('build_full_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated build_full_app.py successfully!")

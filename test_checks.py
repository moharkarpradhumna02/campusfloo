with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

checks = [
    ('FLEET.forEach in initCampusMap', 'vehicleMarkers[v.id] = m;'),
    ('PARKED_FLEET in initCampusMap', 'parkedMarkers[pv.id] = m;'),
    ('LPU_STOPS in initCampusMap', 'stopMarkers.push(marker);'),
    ('filterFleetCategory active class', 'fleet-cat-btn py-1.5 rounded-xl bg-black text-white shadow-sm font-black'),
    ('WAYZEN header title', '<h3 class="text-base font-black text-black">WAYZEN</h3>'),
    ('WAYZEN bold text in JS', '<p class="leading-relaxed font-bold text-black text-sm">${m.text}</p>')
]

for name, needle in checks:
    status = "PASS" if needle in text else "FAIL"
    print(f"[{status}] {name}")

import re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Remove "⚡ Demo Fill" button completely
demo_fill_btn = '''              <!-- Quick Demo Autofill Button from Reference -->
              <button type="button" onclick="autoFillDemoCredentials()" class="btn light !py-2 !px-3 text-xs" title="Instantly fill test credentials for hackathon evaluation">
                <span>⚡ Demo Fill</span>
              </button>'''

if demo_fill_btn in c:
    c = c.replace(demo_fill_btn, '')
    print("[PASS] Removed ⚡ Demo Fill button exact match")
else:
    c = re.sub(r'<!-- Quick Demo Autofill Button from Reference -->\s*<button[^>]*onclick="autoFillDemoCredentials\(\)"[^>]*>[\s\S]*?<span>⚡ Demo Fill</span>\s*</button>', '', c)
    print("[PASS] Removed ⚡ Demo Fill button via regex")

# 2. Fix CSS .btn so color: #fff does not have !important (prevents overriding black text buttons)
c = c.replace('color: #fff !important;\n      text-decoration: none;', 'color: #fff;\n      text-decoration: none;')
c = c.replace('color: #fff !important;', 'color: #fff;')
print("[PASS] Updated .btn CSS rule")

# 3. Fix "💬 Chat Driver" button in studentLocationMarker.bindPopup
old_loc_chat = '''          <div class="grid grid-cols-2 gap-1.5 pt-1">
            <button onclick="shareLocationToChat()" class="btn !py-1 px-2.5 rounded-lg bg-zinc-100 hover:bg-zinc-200 text-black border border-zinc-300 font-extrabold text-[10px]">
              💬 Chat Driver
            </button>
            <button onclick="requestPickupAtMySpot()" class="btn !py-1 px-2.5 rounded-lg bg-black hover:bg-zinc-800 text-white font-black text-[10px] shadow-sm">
              ⚡ Book Pickup
            </button>
          </div>'''

new_loc_chat = '''          <div class="grid grid-cols-2 gap-1.5 pt-1">
            <button onclick="shareLocationToChat()" class="py-2 px-2.5 rounded-xl bg-zinc-100 hover:bg-zinc-200 border border-zinc-300 text-black font-black text-xs flex items-center justify-center gap-1 shadow-sm transition-all" style="color: #000000 !important;">
              💬 <span class="font-black text-black">Chat Driver</span>
            </button>
            <button onclick="requestPickupAtMySpot()" class="py-2 px-2.5 rounded-xl bg-black hover:bg-zinc-800 text-white font-black text-xs flex items-center justify-center gap-1 shadow-sm transition-all" style="color: #ffffff !important;">
              ⚡ Book Pickup
            </button>
          </div>'''

if old_loc_chat in c:
    c = c.replace(old_loc_chat, new_loc_chat)
    print("[PASS] Replaced studentLocationMarker Chat Driver button")
else:
    print("[WARN] studentLocationMarker Chat Driver button exact match not found!")

# 4. Fix "💺 View Seats" in FLEET.forEach (Moving vehicle popup)
old_fleet_seats = '''            <div class="grid grid-cols-2 gap-2 pt-1 border-t border-zinc-200">
              <button onclick="openDriverChat('${v.id}')" class="btn !py-2 px-2.5 rounded-xl bg-black hover:bg-zinc-800 text-white font-black text-[11px] flex items-center justify-center gap-1 shadow-sm">
                💬 Chat Driver
              </button>
              <button onclick="openSeatLayoutModal('${v.id}')" class="btn !py-2 px-2.5 rounded-xl bg-zinc-100 hover:bg-zinc-200 text-black border border-zinc-300 font-black text-[11px] flex items-center justify-center gap-1 shadow-sm">
                💺 View Seats
              </button>
            </div>'''

new_fleet_seats = '''            <div class="grid grid-cols-2 gap-2 pt-1 border-t border-zinc-200">
              <button onclick="openDriverChat('${v.id}')" class="py-2 px-2.5 rounded-xl bg-black hover:bg-zinc-800 text-white font-black text-xs flex items-center justify-center gap-1 shadow-sm transition-all" style="color: #ffffff !important;">
                💬 <span class="font-black text-white">Chat Driver</span>
              </button>
              <button onclick="openSeatLayoutModal('${v.id}')" class="py-2 px-2.5 rounded-xl bg-zinc-100 hover:bg-zinc-200 border border-zinc-300 font-black text-xs flex items-center justify-center gap-1 shadow-sm transition-all" style="color: #000000 !important;">
                💺 <span class="font-black text-black">View Seats</span>
              </button>
            </div>'''

if old_fleet_seats in c:
    c = c.replace(old_fleet_seats, new_fleet_seats)
    print("[PASS] Replaced FLEET.forEach View Seats button")
else:
    print("[WARN] FLEET.forEach View Seats button exact match not found!")

# 5. Fix "💺 View Seats" in PARKED_FLEET.forEach and updateParkedMarkerPopup
old_parked_seats = '''          <div class="grid grid-cols-2 gap-1.5 pt-1">
            <button onclick="openSeatLayoutModal('${pv.id}')" class="py-2 px-2 rounded-xl bg-white/10 hover:bg-white/20 text-white font-bold text-[11px] flex items-center justify-center gap-1 border border-zinc-200">
              💺 View Seats
            </button>'''

new_parked_seats = '''          <div class="grid grid-cols-2 gap-1.5 pt-1">
            <button onclick="openSeatLayoutModal('${pv.id}')" class="py-2 px-2 rounded-xl bg-zinc-100 hover:bg-zinc-200 border border-zinc-300 font-black text-xs flex items-center justify-center gap-1 shadow-sm transition-all" style="color: #000000 !important;">
              💺 <span class="font-black text-black">View Seats</span>
            </button>'''

if old_parked_seats in c:
    c = c.replace(old_parked_seats, new_parked_seats)
    print("[PASS] Replaced PARKED_FLEET View Seats button")
else:
    print("[WARN] PARKED_FLEET View Seats button exact match not found!")

# 6. Fix "💺 Pick Seat" in renderFleetList for parked fleet
c = c.replace(
    'class="px-2.5 py-1.5 rounded-xl bg-purple-500/20 hover:bg-purple-500/30 text-purple-300 font-bold flex items-center gap-1 border border-purple-500/30" title="Choose Window or Aisle Seat">',
    'class="px-3 py-1.5 rounded-xl bg-zinc-100 hover:bg-zinc-200 border border-zinc-300 text-black font-black text-xs flex items-center gap-1 shadow-sm transition-all" style="color: #000000 !important;" title="Choose Window or Aisle Seat">'
)

# 7. Fix "💬 Chat Driver" in activeTripBanner
c = c.replace(
    'class="px-3 py-1 rounded-lg bg-black text-white text-black font-extrabold hover:bg-zinc-800"',
    'class="px-3.5 py-1.5 rounded-xl bg-zinc-100 hover:bg-zinc-200 border border-zinc-300 text-black font-black text-xs flex items-center gap-1" style="color: #000000 !important;"'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Updated index.html successfully.")

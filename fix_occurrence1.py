with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

target = '''            <div class="grid grid-cols-2 gap-1.5 pt-1">
              <button onclick="openDriverChat('${v.id}')" class="btn !py-2 px-2.5 rounded-xl bg-black hover:bg-zinc-800 text-white font-black text-[11px] flex items-center justify-center gap-1 shadow-sm">
                💬 Chat Driver
              </button>
              <button onclick="openSeatLayoutModal('${v.id}')" class="btn !py-2 px-2.5 rounded-xl bg-zinc-100 hover:bg-zinc-200 text-black border border-zinc-300 font-black text-[11px] flex items-center justify-center gap-1 shadow-sm">
                💺 View Seats
              </button>
            </div>'''

replacement = '''            <div class="grid grid-cols-2 gap-1.5 pt-1">
              <button onclick="openDriverChat('${v.id}')" class="py-2 px-2.5 rounded-xl bg-black hover:bg-zinc-800 text-white font-black text-xs flex items-center justify-center gap-1.5 shadow-sm transition-all" style="color: #ffffff !important;">
                💬 <span class="font-black text-white">Chat Driver</span>
              </button>
              <button onclick="openSeatLayoutModal('${v.id}')" class="py-2 px-2.5 rounded-xl bg-zinc-100 hover:bg-zinc-200 border border-zinc-300 text-black font-black text-xs flex items-center justify-center gap-1.5 shadow-sm transition-all" style="color: #000000 !important;">
                💺 <span class="font-black text-black">View Seats</span>
              </button>
            </div>'''

if target in c:
    c = c.replace(target, replacement)
    print("[PASS] Successfully updated Occurrence 1 (FLEET.forEach popup)")
else:
    print("[FAIL] Target not found")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Remove Route Legend Overlay
legend_snippet = '''      <!-- LPU Multi-Transit Route Legend Overlay -->
      <div class="absolute bottom-6 left-4 z-[400] glass-panel p-3 rounded-2xl border border-zinc-200 shadow-2xl max-w-xs space-y-2 text-xs backdrop-blur-xl hidden sm:block">
        <div class="flex items-center justify-between border-b border-white/10 pb-1.5">
          <span class="font-black text-white text-[11px] uppercase tracking-wider flex items-center gap-1.5">
            <span>🗺️</span> LPU Transit Network
          </span>
          <span class="text-[9px] font-mono text-brand-cyan bg-brand-cyan/15 px-1.5 py-0.5 rounded font-bold">4 Lines</span>
        </div>
        <div class="grid grid-cols-1 gap-1 text-[10px]">
          <div class="flex items-center gap-2">
            <span class="w-3 h-1.5 rounded-full bg-[#a855f7]"></span>
            <span class="text-zinc-300 font-bold">Line 1:</span>
            <span class="text-zinc-400 truncate">Ring Road & Hostels Loop (Buses)</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="w-3 h-1.5 rounded-full bg-[#00f0ff]"></span>
            <span class="text-zinc-300 font-bold">Line 2:</span>
            <span class="text-zinc-400 truncate">Academic Core & Blocks 1-36 (Express)</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="w-3 h-1.5 rounded-full bg-[#334155]"></span>
            <span class="text-zinc-300 font-bold">Line 3:</span>
            <span class="text-zinc-400 truncate">Rapid Cross-Connect (Autos)</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="w-3 h-1.5 rounded-full bg-[#1e293b]"></span>
            <span class="text-zinc-300 font-bold">Line 4:</span>
            <span class="text-zinc-400 truncate">Eco EV Green Circulator (EVs)</span>
          </div>
        </div>
      </div>'''

if legend_snippet in c:
    c = c.replace(legend_snippet, '')
    print("[PASS] Removed Route Legend Overlay snippet")
else:
    import re
    c = re.sub(r'<!-- LPU Multi-Transit Route Legend Overlay -->[\s\S]*?</div>\s*</div>\s*</div>', '', c, count=1)
    print("[PASS] Removed Route Legend Overlay via regex")

# 2. Remove 1x, 2x, 5x speed panel
warp_snippet = '''        <div class="glass-panel p-1 rounded-2xl flex items-center gap-1 text-xs font-bold text-zinc-400">
          <button onclick="setSimWarp(1, this)" class="warp-btn px-2.5 py-1 rounded-xl bg-white/15 text-brand-cyan">1x</button>
          <button onclick="setSimWarp(2, this)" class="warp-btn px-2.5 py-1 rounded-xl hover:text-white">2x</button>
          <button onclick="setSimWarp(5, this)" class="warp-btn px-2.5 py-1 rounded-xl hover:text-white">5x</button>
        </div>'''

if warp_snippet in c:
    c = c.replace(warp_snippet, '')
    print("[PASS] Removed 1x, 2x panel snippet")
else:
    import re
    c = re.sub(r'<div class="glass-panel p-1 rounded-2xl flex items-center gap-1 text-xs font-bold text-zinc-400">[\s\S]*?</div>', '', c, count=1)
    print("[PASS] Removed 1x, 2x panel via regex")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("index.html updated.")

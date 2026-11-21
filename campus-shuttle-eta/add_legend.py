with open('build_full_app.py', 'r', encoding='utf-8') as f:
    text = f.read()

legend_html = '''      <!-- LPU Multi-Transit Route Legend Overlay -->
      <div class="absolute bottom-6 left-4 z-[400] glass-panel p-3 rounded-2xl border border-white/15 shadow-2xl max-w-xs space-y-2 text-xs backdrop-blur-xl hidden sm:block">
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
            <span class="w-3 h-1.5 rounded-full bg-[#10b981]"></span>
            <span class="text-zinc-300 font-bold">Line 3:</span>
            <span class="text-zinc-400 truncate">Rapid Cross-Connect (Autos)</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="w-3 h-1.5 rounded-full bg-[#f59e0b]"></span>
            <span class="text-zinc-300 font-bold">Line 4:</span>
            <span class="text-zinc-400 truncate">Eco EV Green Circulator (EVs)</span>
          </div>
        </div>
      </div>'''

target = '<div id="campusMap" class="w-full h-full z-0"></div>'
if 'LPU Multi-Transit Route Legend Overlay' not in text:
    text = text.replace(target, target + '\n\n' + legend_html)
    with open('build_full_app.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Added LPU route legend overlay to map!')
else:
    print('Legend already present!')

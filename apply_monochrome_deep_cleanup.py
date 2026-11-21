import re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Parked Fleet template replacements (Screenshot 6)
c = c.replace(
    "${isSelected ? 'border-amber-400 bg-amber-500/15 ring-1 ring-amber-400/40' : 'border-amber-500/30 bg-amber-500/5'} hover:border-amber-400",
    "${isSelected ? 'border-black shadow-md ring-1 ring-black' : 'border-zinc-200 shadow-sm'} bg-white text-black hover:border-zinc-400"
)

c = c.replace(
    'bg-amber-500/20 border border-amber-500/40 flex items-center justify-center text-xl',
    'bg-zinc-100 border border-zinc-200 flex items-center justify-center text-xl'
)

c = c.replace(
    'bg-amber-500/20 text-amber-300 text-[9px] font-mono font-bold">🅿️ PARKED</span>',
    'bg-zinc-100 text-zinc-800 border border-zinc-300 text-[9px] font-mono font-bold">🅿️ PARKED</span>'
)

c = c.replace(
    'text-[10px] text-amber-300 font-bold uppercase tracking-wider',
    'text-[10px] text-zinc-600 font-bold uppercase tracking-wider'
)

c = c.replace(
    '<span class="text-xs font-black text-amber-400 font-mono">₹${pv.fare}</span>',
    '<span class="text-xs font-black text-black font-mono">₹${pv.fare}</span>'
)

c = c.replace(
    '<p class="text-[9px] text-emerald-400 font-bold">Scheduled</p>',
    '<p class="text-[9px] text-zinc-600 font-bold">Scheduled</p>'
)

c = c.replace(
    '<span class="text-amber-400 font-mono font-black">${pv.scheduledDeparture}</span>',
    '<span class="text-black font-mono font-black">${pv.scheduledDeparture}</span>'
)

c = c.replace(
    '<span class="text-brand-cyan font-bold text-right max-w-[180px]">${pv.destination}</span>',
    '<span class="text-black font-bold text-right max-w-[180px]">${pv.destination}</span>'
)

c = c.replace(
    '<span class="text-white font-bold">${pv.parkedAt}</span>',
    '<span class="text-black font-bold">${pv.parkedAt}</span>'
)

c = c.replace(
    'p-2.5 rounded-xl bg-black/40 border border-zinc-200 space-y-1.5 text-[11px]',
    'p-2.5 rounded-xl bg-zinc-50 border border-zinc-200 space-y-1.5 text-[11px]'
)

c = c.replace(
    'space-y-1.5 bg-black/50 p-2.5 rounded-xl border border-zinc-200',
    'space-y-1.5 bg-zinc-50 p-2.5 rounded-xl border border-zinc-200'
)

c = c.replace(
    '<span class="text-zinc-300 font-bold flex items-center gap-1">',
    '<span class="text-zinc-800 font-bold flex items-center gap-1">'
)

# Parked seat badge logic
c = re.sub(
    r"\$\{pv\.availableSeats > 2 \? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30' : \([^)]+\)\}",
    "${pv.availableSeats > 2 ? 'bg-zinc-100 text-black border-zinc-300 font-bold' : (pv.availableSeats > 0 ? 'bg-zinc-200 text-black border-zinc-300 font-bold' : 'bg-zinc-800 text-white border-black font-bold')}",
    c
)

c = c.replace(
    '🟢 ${pv.availableSeats} of ${pv.totalSeats} Free',
    '💺 ${pv.availableSeats} of ${pv.totalSeats} Free'
)

c = c.replace(
    "${occupancyPct > 85 ? 'bg-amber-400' : 'bg-emerald-400'}",
    "${occupancyPct > 85 ? 'bg-zinc-500' : 'bg-black'}"
)

c = c.replace(
    "${pv.availableSeats > 0 ? 'text-emerald-400 font-bold' : 'text-rose-400 font-bold'}",
    "${pv.availableSeats > 0 ? 'text-zinc-900 font-bold' : 'text-rose-600 font-bold'}"
)

c = c.replace(
    '<strong class="text-amber-400 font-mono">₹${pv.fare}</strong>',
    '<strong class="text-black font-mono font-bold">₹${pv.fare}</strong>'
)

c = c.replace(
    'bg-amber-400 hover:bg-amber-300 text-black font-black',
    'bg-black hover:bg-zinc-800 text-white font-black'
)

c = c.replace(
    'border border-amber-400/40 text-amber-300',
    'border border-zinc-300 text-black'
)

# 2. Moving Fleet template replacements (Screenshot 1)
c = re.sub(
    r"const seatBadgeClass = v\.availableSeats > 2 \? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30' : \([^)]+\);",
    "const seatBadgeClass = v.availableSeats > 2 ? 'bg-zinc-100 text-black border border-zinc-300 font-extrabold' : (v.availableSeats > 0 ? 'bg-zinc-200 text-black border border-zinc-300 font-extrabold' : 'bg-zinc-800 text-white border border-black font-extrabold');",
    c
)

c = c.replace(
    '<span class="${i === 0 ? \'text-emerald-400 font-bold\' : \'text-zinc-400\'} font-mono whitespace-nowrap">',
    '<span class="${i === 0 ? \'text-black font-extrabold\' : \'text-zinc-500\'} font-mono whitespace-nowrap">'
)

c = c.replace(
    '<div class="flex items-center justify-between ${i === 0 ? \'text-white font-bold text-[11px]\' : \'text-zinc-400 text-[10px]\'}">',
    '<div class="flex items-center justify-between ${i === 0 ? \'text-black font-black text-[11px]\' : \'text-zinc-600 text-[10px]\'}">'
)

c = c.replace(
    'class="p-2 rounded-xl bg-black/40 border border-zinc-200 space-y-1">',
    'class="p-2 rounded-xl bg-zinc-50 border border-zinc-200 space-y-1">'
)

c = c.replace(
    '<span class="text-zinc-400 font-bold">⏱️ Upcoming Block Arrival Timetable:</span>',
    '<span class="text-zinc-700 font-bold">⏱️ Upcoming Block Arrival Timetable:</span>'
)

c = c.replace(
    '<span class="text-brand-cyan font-mono font-bold">~18 km/h</span>',
    '<span class="text-black font-mono font-bold">~18 km/h</span>'
)

c = c.replace(
    'class="space-y-1 bg-black/30 p-2 rounded-xl border border-zinc-200">',
    'class="space-y-1 bg-zinc-50 p-2 rounded-xl border border-zinc-200">'
)

c = c.replace(
    "${occupancyPct > 85 ? 'bg-amber-400' : 'bg-brand-cyan'}",
    "${occupancyPct > 85 ? 'bg-zinc-500' : 'bg-black'}"
)

c = c.replace(
    "<strong class=\"text-white font-mono\">₹${v.fare}</strong>",
    "<strong class=\"text-black font-mono font-bold\">₹${v.fare}</strong>"
)

# 3. Dynamic Main Gate box in JS
c = c.replace(
    '<strong class="text-white text-xs block font-black">${p.vehicle}</strong>',
    '<strong class="text-black text-xs block font-black">${p.vehicle}</strong>'
)
c = c.replace(
    '<span class="text-[10px] text-brand-cyan font-semibold">${p.route}</span>',
    '<span class="text-[10px] text-zinc-500 font-semibold">${p.route}</span>'
)
c = c.replace(
    '<span class="text-xs font-black text-emerald-400 font-mono">₹${p.fare}</span>',
    '<span class="text-xs font-black text-black font-mono">₹${p.fare}</span>'
)
c = c.replace(
    '<span class="text-[10px] text-zinc-400 block">Arriving ${p.eta}</span>',
    '<span class="text-[10px] text-zinc-600 block">Arriving ${p.eta}</span>'
)
c = c.replace(
    '<span class="text-emerald-400 font-bold">● Boarding Ready</span>',
    '<span class="text-zinc-800 font-bold">● Boarding Ready</span>'
)

# 4. Map Popup & Marker Cleanups
c = c.replace(
    'border-2 border-amber-400 text-sm flex items-center justify-center shadow-lg hover:scale-125 transition-transform" style="box-shadow: 0 0 14px rgba(245, 158, 11, 0.6);"',
    'border-2 border-black text-sm flex items-center justify-center shadow-lg hover:scale-125 transition-transform" style="box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35);"'
)

c = c.replace(
    'text-[10px] font-bold text-amber-400 uppercase tracking-wider',
    'text-[10px] font-bold text-zinc-600 uppercase tracking-wider'
)

c = c.replace(
    'bg-amber-500/20 text-amber-300 border border-amber-500/30',
    'bg-zinc-100 text-black border border-zinc-300 font-bold'
)

c = c.replace(
    '<p class="text-amber-300">⏰ <strong>Departure:</strong> ${pv.scheduledDeparture}</p>',
    '<p class="text-zinc-800">⏰ <strong>Departure:</strong> ${pv.scheduledDeparture}</p>'
)

c = c.replace(
    "${pv.availableSeats > 2 ? 'text-emerald-400' : (pv.availableSeats > 0 ? 'text-amber-400' : 'text-rose-400')}",
    "'text-black font-black'"
)

# 5. Fullscreen Driver Cockpit Cleanup
c = c.replace('bg-emerald-500/15 border border-emerald-500/30 text-emerald-400', 'bg-zinc-100 border border-zinc-300 text-black')
c = c.replace('bg-emerald-500/20 text-emerald-400 border border-emerald-500/30', 'bg-zinc-100 text-black border border-zinc-300 font-bold')
c = c.replace('bg-amber-500/20 text-amber-400 border border-amber-500/30', 'bg-zinc-100 text-black border border-zinc-300 font-bold')
c = c.replace('bg-amber-500/10 border border-amber-500/25', 'bg-zinc-100 border border-zinc-200 text-black')
c = c.replace('bg-emerald-500/10 border border-emerald-500/25', 'bg-zinc-100 border border-zinc-200 text-black')
c = c.replace('bg-amber-500/10 border border-amber-500/30', 'bg-zinc-100 border border-zinc-200 text-black')
c = c.replace('bg-emerald-500/10 border border-emerald-500/30', 'bg-zinc-100 border border-zinc-200 text-black')
c = c.replace('text-emerald-400', 'text-black')
c = c.replace('text-emerald-300', 'text-zinc-800')
c = c.replace('text-amber-400', 'text-black')
c = c.replace('text-amber-300', 'text-zinc-800')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("apply_monochrome_deep_cleanup.py successfully executed.")

import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update :root variables
content = content.replace('--pulse: #06c167;', '--pulse: #0a0a0a;')
content = content.replace('--sun: #ee9559;', '--sun: #27272a;')

# 2. Update tailwind.config colors
content = re.sub(r"emerald:\s*'#06c167'", "emerald: '#18181b'", content)
content = re.sub(r"amber:\s*'#ee9559'", "amber: '#27272a'", content)
content = re.sub(r"pulse:\s*'#06c167'", "pulse: '#0a0a0a'", content)

# 3. Fix About Us section container and text (Screenshot 4)
# Make section light bg-white and text high contrast black
about_old = '<section id="aboutUsSection" class="py-20 px-4 sm:px-6 lg:px-8 border-t border-white/10 bg-[#0A0A0A] relative z-10">'
about_new = '<section id="aboutUsSection" class="py-20 px-4 sm:px-6 lg:px-8 border-t border-zinc-200 bg-white relative z-10">'
content = content.replace(about_old, about_new)

# In About Us heading
content = content.replace(
    'Revolutionizing University Transit with <span class="bg-gradient-to-r from-brand-cyan to-brand-purple bg-clip-text text-transparent">AI & Clean Energy</span>',
    'Revolutionizing University Transit with <span class="text-[#DC2626]">AI & Clean Energy</span>'
)

# 4. Fix Fleet Status Banner (Screenshot 1)
banner_old = '''<div id="fleetStatusBanner" class="py-1.5 px-2.5 rounded-lg text-[10px] font-bold flex items-center justify-between bg-emerald-500/10 border border-emerald-500/25 text-emerald-400">
          <div class="flex items-center gap-1.5">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-ping"></span>
            <span id="bannerStatusText">All campus transit on schedule</span>
          </div>
          <span class="font-mono uppercase bg-emerald-500/20 px-1.5 py-0.2 rounded text-[9px]">±2m Confirmed</span>
        </div>'''
banner_new = '''<div id="fleetStatusBanner" class="py-1.5 px-2.5 rounded-lg text-[10px] font-bold flex items-center justify-between bg-zinc-100 border border-zinc-300 text-zinc-900 shadow-sm">
          <div class="flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-black animate-ping"></span>
            <span id="bannerStatusText">All campus transit on schedule</span>
          </div>
          <span class="font-mono uppercase bg-zinc-200 text-zinc-800 px-1.5 py-0.5 rounded text-[9px] font-extrabold border border-zinc-300">±2m Confirmed</span>
        </div>'''
content = content.replace(banner_old, banner_new)

# Fix Moving Fleet Tab button icon and dot
content = content.replace(
    '<span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> 🟢 Moving Fleet (8)',
    '<span class="w-2 h-2 rounded-full bg-black"></span> 🚍 Moving Fleet (8)'
)

# 5. Fix Bottom Navigation Bar (Screenshots 1 & 6)
bottom_old = '''      <!-- Pinned Bottom Quick Actions -->
      <div class="p-3 border-t border-white/10 bg-black/50 shrink-0 flex items-center justify-between gap-2 text-xs font-bold z-20">
        <button onclick="openFarePassesModal()" class="flex-1 py-2 px-3 rounded-xl bg-zinc-50 hover:bg-white/10 border border-zinc-200 text-zinc-300 text-center flex items-center justify-center gap-1.5 transition-all">
          <i data-lucide="ticket" class="w-3.5 h-3.5 text-brand-cyan"></i>
          Fares & Passes
        </button>
        <button onclick="openDriverPortalModal()" class="flex-1 py-2 px-3 rounded-xl bg-emerald-500/15 hover:bg-emerald-500/25 border border-emerald-500/30 text-emerald-400 text-center flex items-center justify-center gap-1.5 transition-all">
          <span class="text-xs">👨‍✈️</span> Driver
        </button>
        <button onclick="openH4StressModal()" class="flex-1 py-2 px-3 rounded-xl bg-zinc-50 hover:bg-white/10 border border-zinc-200 text-amber-400 text-center flex items-center justify-center gap-1.5 transition-all">
          <i data-lucide="zap" class="w-3.5 h-3.5"></i>
          H4 Stress Test
        </button>
        <button onclick="toggleWayzenChat()" class="p-2 rounded-xl bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/30 text-purple-300 font-black transition-all" title="Chat with WAYZEN Route Advisor">
          🤖
        </button>
      </div>'''

bottom_new = '''      <!-- Pinned Bottom Quick Actions -->
      <div class="p-3 border-t border-zinc-200 bg-white shrink-0 flex items-center justify-between gap-2 text-xs font-bold z-20 shadow-lg">
        <button onclick="openFarePassesModal()" class="flex-1 py-2.5 px-3 rounded-xl bg-zinc-100 hover:bg-zinc-200 border border-zinc-300 text-black text-center flex items-center justify-center gap-1.5 transition-all font-bold">
          <i data-lucide="ticket" class="w-3.5 h-3.5 text-black"></i>
          <span>Fares & Passes</span>
        </button>
        <button onclick="openDriverPortalModal()" class="flex-1 py-2.5 px-3 rounded-xl bg-black hover:bg-zinc-800 text-white text-center flex items-center justify-center gap-1.5 transition-all font-extrabold shadow-sm">
          <span class="text-xs">👨‍✈️</span> <span>Driver</span>
        </button>
        <button onclick="openH4StressModal()" class="flex-1 py-2.5 px-3 rounded-xl bg-zinc-100 hover:bg-zinc-200 border border-zinc-300 text-black text-center flex items-center justify-center gap-1.5 transition-all font-bold">
          <i data-lucide="zap" class="w-3.5 h-3.5 text-black"></i>
          <span>H4 Stress Test</span>
        </button>
        <button onclick="toggleWayzenChat()" class="p-2.5 rounded-xl bg-zinc-100 hover:bg-zinc-200 border border-zinc-300 text-black font-black transition-all" title="Chat with WAYZEN Route Advisor">
          🤖
        </button>
      </div>'''
content = content.replace(bottom_old, bottom_new)

# 6. Fix Ride from Main Gate (Screenshot 5)
content = content.replace(
    'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-[9px] font-mono font-bold">● Active Hub</span>',
    'bg-zinc-100 text-zinc-900 border border-zinc-300 text-[9px] font-mono font-bold">● Active Hub</span>'
)
content = content.replace(
    '<span class="text-xs font-black text-emerald-400 font-mono">₹15</span>',
    '<span class="text-xs font-black text-black font-mono">₹15</span>'
)
content = content.replace(
    '<span class="text-emerald-400 font-bold">● Boarding Ready</span>',
    '<span class="text-zinc-800 font-bold">● Boarding Ready</span>'
)
content = content.replace(
    'class="w-full py-2.5 rounded-xl bg-gradient-to-r from-brand-cyan via-emerald-400 to-brand-purple text-black font-black text-xs hover:opacity-95 shadow-lg flex items-center justify-center gap-1.5 transition-all"',
    'class="btn w-full !py-3 bg-black hover:bg-zinc-800 text-white font-extrabold text-xs shadow-md flex items-center justify-center gap-1.5 transition-all"'
)

# 7. Fix Smart Pass Active Badges (Screenshots 1 & 5)
content = content.replace(
    'class="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-[9px] font-mono font-bold">● Active</span>',
    'class="px-2.5 py-0.5 rounded-full bg-white/20 text-white border border-white/30 text-[9px] font-mono font-bold">● Active</span>'
)

# 8. Fix Wallet Modal (Screenshot 2)
content = content.replace(
    '<span class="text-[11px] px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">Active</span>',
    '<span class="text-[10px] px-2.5 py-0.5 rounded-full bg-black text-white font-black border border-zinc-200">Active</span>'
)
content = content.replace(
    '<span class="text-[10px] text-emerald-400 font-bold">Zero Convenience Fee</span>',
    '<span class="text-[10px] text-zinc-500 font-bold">Zero Convenience Fee</span>'
)

# 9. Fix Driver Login Modal (Screenshot 3)
content = content.replace(
    'bg-gradient-to-tr from-emerald-400 via-teal-500 to-brand-cyan mx-auto flex items-center justify-center text-3xl shadow-xl shadow-emerald-500/25',
    'bg-black border border-zinc-200 mx-auto flex items-center justify-center text-3xl shadow-xl text-white'
)
content = content.replace(
    'class="w-full px-4 py-3 rounded-2xl bg-black/60 border border-zinc-200 text-xs font-bold text-emerald-300 focus:outline-none focus:border-emerald-400 cursor-pointer"',
    'class="w-full px-4 py-3 rounded-2xl bg-zinc-100 border border-zinc-300 text-xs font-bold text-black focus:outline-none focus:border-black cursor-pointer"'
)
content = content.replace(
    'class="w-full px-4 py-3 rounded-2xl bg-black/60 border border-zinc-200 text-xs font-mono font-semibold text-white focus:outline-none focus:border-emerald-400"',
    'class="w-full px-4 py-3 rounded-2xl bg-zinc-100 border border-zinc-300 text-xs font-mono font-semibold text-black focus:outline-none focus:border-black"'
)
content = content.replace(
    'class="w-full px-4 py-3 rounded-2xl bg-black/60 border border-zinc-200 text-sm font-mono tracking-widest text-center text-emerald-400 focus:outline-none focus:border-emerald-400"',
    'class="w-full px-4 py-3 rounded-2xl bg-zinc-100 border border-zinc-300 text-sm font-mono tracking-widest text-center text-black font-extrabold focus:outline-none focus:border-black"'
)

# 10. Fix Driver 1-Click login buttons (Screenshot 3 bottom)
content = re.sub(
    r'<strong class="text-white block text-\[11px\]">([^<]+)</strong>',
    r'<strong class="text-black block text-[11px] font-black">\1</strong>',
    content
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Step 1 basic replacements done.")

with open('build_full_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove the 3D Video Toggle button in top navbar
old_video_btn = '''        <!-- Background Video Toggle -->
        <button id="btnToggleBgVideo" onclick="toggleHeroBgVideo()" class="hidden lg:inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 text-[11px] font-bold text-zinc-300">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span id="btnToggleBgVideoText">🎥 3D Video</span>
        </button>'''

if old_video_btn in content:
    content = content.replace(old_video_btn, '')
    print("Removed 3D Video button from top navbar!")

# 2. Add 'Overview' link to Center Nav in Header
old_nav = '''      <!-- Center Links (Clean & Public) -->
      <nav class="hidden md:flex items-center gap-1 text-sm font-semibold text-zinc-300">
        <button onclick="showLandingPage(); window.scrollTo({top:0, behavior:'smooth'});" class="px-3.5 py-1.5 rounded-xl hover:text-white hover:bg-white/5 transition-colors font-bold">Home</button>
        <button onclick="scrollToLandingSection('aboutUsSection')" class="px-3.5 py-1.5 rounded-xl hover:text-white hover:bg-white/5 transition-colors font-bold">About Us</button>
        <button onclick="scrollToLandingSection('faqSection')" class="px-3.5 py-1.5 rounded-xl hover:text-white hover:bg-white/5 transition-colors font-bold">Q&A</button>
      </nav>'''

new_nav = '''      <!-- Center Links (Clean & Public) -->
      <nav class="hidden md:flex items-center gap-1 text-sm font-semibold text-zinc-300">
        <button onclick="showLandingPage(); window.scrollTo({top:0, behavior:'smooth'});" class="px-3.5 py-1.5 rounded-xl hover:text-white hover:bg-white/5 transition-colors font-bold">Home</button>
        <button onclick="scrollToLandingSection('systemOverviewSection')" class="px-3.5 py-1.5 rounded-xl hover:text-white hover:bg-white/5 transition-colors font-bold text-brand-cyan">Overview</button>
        <button onclick="scrollToLandingSection('aboutUsSection')" class="px-3.5 py-1.5 rounded-xl hover:text-white hover:bg-white/5 transition-colors font-bold">About Us</button>
        <button onclick="scrollToLandingSection('faqSection')" class="px-3.5 py-1.5 rounded-xl hover:text-white hover:bg-white/5 transition-colors font-bold">Q&A</button>
      </nav>'''

if old_nav in content:
    content = content.replace(old_nav, new_nav)
    print("Added Overview link to top nav!")

# 3. Replace the Hero Background Video with clean modern dark mesh background
old_hero_bg = '''      <!-- Video Background -->
      <div class="hero-video-container">
        <video id="heroBgVideo" autoplay loop muted playsinline class="bg-video">
          <source src="campus-flow-bg.mp4" type="video/mp4">
        </video>
        <!-- Dark gradient vignette overlay for perfect contrast -->
        <div class="absolute inset-0 bg-gradient-to-r from-[#05070e]/95 via-[#05070e]/75 to-[#05070e]/90 z-[1]"></div>
      </div>'''

new_hero_bg = '''      <!-- Clean High-Performance Tech Hero Background (Video Removed) -->
      <div class="absolute inset-0 pointer-events-none z-0">
        <div class="absolute inset-0 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(0,240,255,0.12),rgba(5,7,14,1))]"></div>
        <div class="absolute top-1/4 -left-40 w-96 h-96 bg-brand-cyan/15 rounded-full blur-[140px]"></div>
        <div class="absolute bottom-1/4 -right-40 w-96 h-96 bg-brand-purple/15 rounded-full blur-[140px]"></div>
        <div class="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)]"></div>
      </div>'''

if old_hero_bg in content:
    content = content.replace(old_hero_bg, new_hero_bg)
    print("Replaced video background with clean high-performance tech background!")

# 4. Insert systemOverviewSection right after landingHeroSection
overview_section_html = '''    <!-- ================= 2. SYSTEM OVERVIEW SECTION ================= -->
    <section id="systemOverviewSection" class="py-20 px-4 sm:px-6 lg:px-8 border-t border-white/10 bg-[#070914] relative z-10">
      <div class="max-w-7xl mx-auto space-y-14">
        
        <!-- Header -->
        <div class="text-center max-w-3xl mx-auto space-y-4">
          <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-brand-cyan/10 border border-brand-cyan/30 text-brand-cyan text-xs font-bold uppercase tracking-wider">
            <i data-lucide="layers" class="w-3.5 h-3.5"></i>
            Campus Flow Architecture & Mobility Ecosystem
          </div>
          <h2 class="text-3xl sm:text-5xl font-black text-white tracking-tight">
            The Complete Overview of <span class="bg-gradient-to-r from-brand-cyan via-brand-purple to-brand-violet bg-clip-text text-transparent">LPU Smart Transit</span>
          </h2>
          <p class="text-sm sm:text-base text-zinc-400 leading-relaxed">
            Engineered specifically for the 600-acre Lovely Professional University campus. Connecting 21 key hubs, Academic Blocks 1 to 36, and Hostels BH 1-12 & GH 1-7 with zero-delay predictability.
          </p>
        </div>

        <!-- 6 Core Capabilities Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          
          <!-- Card 1 -->
          <div class="glass-panel p-6 rounded-3xl border border-white/10 hover:border-brand-cyan/40 transition-all space-y-4 group">
            <div class="w-12 h-12 rounded-2xl bg-brand-cyan/15 border border-brand-cyan/30 text-brand-cyan flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">
              🛰️
            </div>
            <div class="space-y-1.5">
              <h3 class="text-base font-black text-white">AI Dead-Reckoning & Kalman Filter</h3>
              <p class="text-xs text-zinc-400 leading-relaxed">
                Cellular blind spots between dense high-rise academic blocks won't leave you stranded. Our dead-reckoning engine calculates kinematic positions at 60Hz even when satellite GPS drops.
              </p>
            </div>
            <div class="pt-2 text-[11px] font-mono font-bold text-brand-cyan flex items-center gap-1.5">
              <span>● ±2 Min Arrival Accuracy</span>
            </div>
          </div>

          <!-- Card 2 -->
          <div class="glass-panel p-6 rounded-3xl border border-white/10 hover:border-brand-purple/40 transition-all space-y-4 group">
            <div class="w-12 h-12 rounded-2xl bg-purple-500/15 border border-purple-500/30 text-purple-400 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">
              🗺️
            </div>
            <div class="space-y-1.5">
              <h3 class="text-base font-black text-white">4 Criss-Crossing Transit Lines</h3>
              <p class="text-xs text-zinc-400 leading-relaxed">
                No single slow loop. 4 independent colored lines connect Main Gate, UniMall, Unipolis, Central Library, Robopark, Girls Hostels GH 1-7, and Boys Hostels BH 1-12.
              </p>
            </div>
            <div class="pt-2 text-[11px] font-mono font-bold text-purple-400 flex items-center gap-1.5">
              <span>● Shuttles, Autos & Eco EVs</span>
            </div>
          </div>

          <!-- Card 3 -->
          <div class="glass-panel p-6 rounded-3xl border border-white/10 hover:border-emerald-500/40 transition-all space-y-4 group">
            <div class="w-12 h-12 rounded-2xl bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">
              💺
            </div>
            <div class="space-y-1.5">
              <h3 class="text-base font-black text-white">Live Seats & Cabin Layouts</h3>
              <p class="text-xs text-zinc-400 leading-relaxed">
                Know before you run! Real-time available seat counters (e.g. 8/50, 1/3) with interactive seat layout preview to reserve window or aisle seats with live charging ports.
              </p>
            </div>
            <div class="pt-2 text-[11px] font-mono font-bold text-emerald-400 flex items-center gap-1.5">
              <span>● Interactive Seat Selection</span>
            </div>
          </div>

          <!-- Card 4 -->
          <div class="glass-panel p-6 rounded-3xl border border-white/10 hover:border-amber-500/40 transition-all space-y-4 group">
            <div class="w-12 h-12 rounded-2xl bg-amber-500/15 border border-amber-500/30 text-amber-400 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">
              💬
            </div>
            <div class="space-y-1.5">
              <h3 class="text-base font-black text-white">Driver Chat & OTP Safety Gate</h3>
              <p class="text-xs text-zinc-400 leading-relaxed">
                Communicate directly with verified campus drivers in English or Hinglish. Every boarding is cryptographically matched with dynamic 4-digit student security OTP.
              </p>
            </div>
            <div class="pt-2 text-[11px] font-mono font-bold text-amber-400 flex items-center gap-1.5">
              <span>● 100% Verified Indian Drivers</span>
            </div>
          </div>

          <!-- Card 5 -->
          <div class="glass-panel p-6 rounded-3xl border border-white/10 hover:border-brand-cyan/40 transition-all space-y-4 group">
            <div class="w-12 h-12 rounded-2xl bg-brand-cyan/15 border border-brand-cyan/30 text-brand-cyan flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">
              💳
            </div>
            <div class="space-y-1.5">
              <h3 class="text-base font-black text-white">Campus Pass & UPI QR Wallet</h3>
              <p class="text-xs text-zinc-400 leading-relaxed">
                Zero-convenience fee wallet top-ups via Google Pay, PhonePe, or Cards. Pay in 1 second without loose cash change drama at UniMall, hostels, or the sports complex.
              </p>
            </div>
            <div class="pt-2 text-[11px] font-mono font-bold text-brand-cyan flex items-center gap-1.5">
              <span>● ₹240 Student Welcome Credit</span>
            </div>
          </div>

          <!-- Card 6 -->
          <div class="glass-panel p-6 rounded-3xl border border-white/10 hover:border-purple-500/40 transition-all space-y-4 group">
            <div class="w-12 h-12 rounded-2xl bg-purple-500/15 border border-purple-500/30 text-purple-400 flex items-center justify-center text-2xl group-hover:scale-110 transition-transform">
              🤖
            </div>
            <div class="space-y-1.5">
              <h3 class="text-base font-black text-white">WAYZEN AI Transit Companion</h3>
              <p class="text-xs text-zinc-400 leading-relaxed">
                Your 24/7 witty campus buddy speaking fluent Hinglish. Ask live vehicle ETAs, summon an auto rickshaw, check wallet balance, or find your examination room.
              </p>
            </div>
            <div class="pt-2 text-[11px] font-mono font-bold text-purple-400 flex items-center gap-1.5">
              <span>● 24/7 Voice & Chat Buddy</span>
            </div>
          </div>

        </div>

        <!-- Campus Transit Key Metrics Strip -->
        <div class="p-6 sm:p-8 rounded-3xl glass-panel border border-brand-cyan/20 bg-gradient-to-r from-brand-cyan/10 via-purple-950/20 to-black/60 shadow-2xl">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            <div class="space-y-1">
              <p class="text-3xl sm:text-4xl font-black text-brand-cyan font-mono">600+ Acres</p>
              <p class="text-xs text-zinc-400 font-bold uppercase tracking-wider">Campus Area Covered</p>
            </div>
            <div class="space-y-1">
              <p class="text-3xl sm:text-4xl font-black text-purple-400 font-mono">21 Hubs</p>
              <p class="text-xs text-zinc-400 font-bold uppercase tracking-wider">Blocks 1-36 & Hostels</p>
            </div>
            <div class="space-y-1">
              <p class="text-3xl sm:text-4xl font-black text-emerald-400 font-mono">±2 Mins</p>
              <p class="text-xs text-zinc-400 font-bold uppercase tracking-wider">ETA Accuracy</p>
            </div>
            <div class="space-y-1">
              <p class="text-3xl sm:text-4xl font-black text-amber-400 font-mono">99.8%</p>
              <p class="text-xs text-zinc-400 font-bold uppercase tracking-wider">On-Time Reliability</p>
            </div>
          </div>
        </div>

      </div>
    </section>

'''

if 'id="systemOverviewSection"' not in content:
    content = content.replace('<!-- ================= 2. ABOUT US PORTAL ================= -->', overview_section_html + '    <!-- ================= 3. ABOUT US PORTAL ================= -->')
    print("Inserted systemOverviewSection successfully!")

# 5. Clean up toggleHeroBgVideo JS function
old_toggle_func = '''    // Background Video Controls
    function toggleHeroBgVideo() {
      const vid = document.getElementById('heroBgVideo');
      const txt = document.getElementById('btnToggleBgVideoText');
      if (!vid) return;
      if (vid.paused) {
        vid.play();
        txt.textContent = '🎥 3D Video Active';
        showToast('Video Background resumed');
      } else {
        vid.pause();
        txt.textContent = '⏸ Video Paused';
        showToast('Video Background paused');
      }
    }'''

new_toggle_func = '''    function toggleHeroBgVideo() {
      // Clean modern background active
    }'''

if old_toggle_func in content:
    content = content.replace(old_toggle_func, new_toggle_func)
    print("Cleaned up toggleHeroBgVideo JS function!")

with open('build_full_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated build_full_app.py successfully!")

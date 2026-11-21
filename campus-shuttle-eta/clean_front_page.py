with open('build_full_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Clean Center Nav Links in Header
old_nav_center = '''      <!-- Center Links -->
      <nav class="hidden md:flex items-center gap-1 text-sm font-semibold text-zinc-300">
        <button onclick="showLandingPage(); window.scrollTo({top:0, behavior:'smooth'});" class="px-3 py-1.5 rounded-xl hover:text-white hover:bg-white/5 transition-colors">Home</button>
        <button onclick="scrollToLandingSection('aboutUsSection')" class="px-3 py-1.5 rounded-xl hover:text-white hover:bg-white/5 transition-colors">About Us</button>
        <button onclick="scrollToLandingSection('faqSection')" class="px-3 py-1.5 rounded-xl hover:text-white hover:bg-white/5 transition-colors">FAQ</button>
        <button onclick="scrollToLandingSection('happyStudentsSection')" class="px-3 py-1.5 rounded-xl hover:text-white hover:bg-white/5 transition-colors">Happy Students</button>
        <button onclick="launchTransportDashboard()" class="px-3 py-1.5 rounded-xl text-brand-purple hover:bg-brand-purple/10 transition-colors flex items-center gap-1.5">
          <i data-lucide="map" class="w-4 h-4"></i> Live Map
        </button>
        <button onclick="openFarePassesModal()" class="px-3 py-1.5 rounded-xl hover:text-white hover:bg-white/5 transition-colors">Fares</button>
      </nav>'''

new_nav_center = '''      <!-- Center Links (Clean & Public) -->
      <nav class="hidden md:flex items-center gap-1 text-sm font-semibold text-zinc-300">
        <button onclick="showLandingPage(); window.scrollTo({top:0, behavior:'smooth'});" class="px-3.5 py-1.5 rounded-xl hover:text-white hover:bg-white/5 transition-colors font-bold">Home</button>
        <button onclick="scrollToLandingSection('aboutUsSection')" class="px-3.5 py-1.5 rounded-xl hover:text-white hover:bg-white/5 transition-colors font-bold">About Us</button>
        <button onclick="scrollToLandingSection('faqSection')" class="px-3.5 py-1.5 rounded-xl hover:text-white hover:bg-white/5 transition-colors font-bold">Q&A</button>
      </nav>'''

if old_nav_center in content:
    content = content.replace(old_nav_center, new_nav_center)
    print("Cleaned Header Nav links!")

# 2. Remove the cluttered Promo / Wallet banner from the Hero section
old_hero_promo = '''          <!-- Promo Banner with Booking Action -->
          <div class="glass-panel p-3.5 rounded-2xl flex flex-col sm:flex-row items-center justify-between gap-3 border border-brand-cyan/20 bg-gradient-to-r from-brand-cyan/10 via-transparent to-brand-purple/10">
            <div class="flex items-center gap-2.5">
              <span class="text-xl">🎁</span>
              <div>
                <p class="text-xs font-black text-white">First Ride 100% Free • Coupon: <span class="text-brand-cyan">CAMPUS10</span> for 10% Off</p>
                <p class="text-[11px] text-zinc-400">Pay via Google Pay UPI QR, Smart Wallet, or Cash on Board with OTP</p>
              </div>
            </div>
            <div class="flex items-center gap-2 w-full sm:w-auto">
              <button onclick="openPaymentAndBookingModal()" class="w-full sm:w-auto px-4 py-2 rounded-xl bg-brand-cyan text-black font-extrabold text-xs hover:opacity-90 transition-all shadow-md">
                Book / Pay Now
              </button>
              <button id="heroPromoWalletBtn" onclick="openWalletModal()" class="hidden w-full sm:w-auto px-3 py-2 rounded-xl bg-white/10 text-white font-extrabold text-xs hover:bg-white/20 transition-all border border-white/15">
                💳 Wallet
              </button>
            </div>
          </div>'''

if old_hero_promo in content:
    content = content.replace(old_hero_promo, '')
    print("Removed cluttered promo / wallet banner from Hero section!")

# 3. Remove happyStudentsSection from the landing page
start_happy = content.find('<!-- ================= 4. UNIVERSITY HAPPY STUDENTS SHOWCASE ================= -->')
end_happy = content.find('<!-- ================= 5. CAMPUS FOOTER ================= -->')

if start_happy != -1 and end_happy != -1:
    content = content[:start_happy] + content[end_happy:]
    print("Removed happyStudentsSection from front page!")

# 4. Clean Footer Links (remove Campus Wallet and Stress Test from public front page footer)
old_footer_links = '''        <div class="flex flex-wrap items-center justify-center gap-6 text-xs font-semibold text-zinc-300">
          <button onclick="showLandingPage(); window.scrollTo({top:0, behavior:'smooth'});" class="hover:text-brand-cyan">Home</button>
          <button onclick="scrollToLandingSection('aboutUsSection')" class="hover:text-brand-cyan">About Us</button>
          <button onclick="scrollToLandingSection('faqSection')" class="hover:text-brand-cyan">FAQ</button>
          <button onclick="openWalletModal()" class="hover:text-brand-cyan">Campus Wallet</button>
          <button onclick="launchTransportDashboard()" class="hover:text-brand-cyan">Live Map</button>
          <button onclick="toggleWayzenChat()" class="hover:text-brand-cyan">WAYZEN AI</button>
          <button onclick="openH4StressModal()" class="hover:text-brand-amber">Stress Test (H4)</button>
        </div>'''

new_footer_links = '''        <div class="flex flex-wrap items-center justify-center gap-6 text-xs font-semibold text-zinc-300">
          <button onclick="showLandingPage(); window.scrollTo({top:0, behavior:'smooth'});" class="hover:text-brand-cyan">Home</button>
          <button onclick="scrollToLandingSection('aboutUsSection')" class="hover:text-brand-cyan">About Us</button>
          <button onclick="scrollToLandingSection('faqSection')" class="hover:text-brand-cyan">Q&A</button>
          <button onclick="handleGuestDirectAccess()" class="hover:text-brand-cyan">Guest Access</button>
        </div>'''

if old_footer_links in content:
    content = content.replace(old_footer_links, new_footer_links)
    print("Cleaned public footer links!")

# 5. Add Fares button into the Dashboard Sidebar Search bar
old_dash_search = '''          <button onclick="openWalletModal()" title="Campus Wallet" class="p-2.5 rounded-xl bg-purple-500/20 text-purple-300 border border-purple-500/30 hover:bg-purple-500/30 font-bold">
            <i data-lucide="wallet" class="w-4 h-4"></i>
          </button>
          <button onclick="openPaymentAndBookingModal()" title="Book / Pay Pass" class="p-2.5 rounded-xl bg-brand-cyan text-black hover:opacity-90 font-bold shadow-md">
            <i data-lucide="credit-card" class="w-4 h-4"></i>
          </button>'''

new_dash_search = '''          <button onclick="openWalletModal()" title="Campus Wallet" class="p-2.5 rounded-xl bg-purple-500/20 text-purple-300 border border-purple-500/30 hover:bg-purple-500/30 font-bold">
            <i data-lucide="wallet" class="w-4 h-4"></i>
          </button>
          <button onclick="openFarePassesModal()" title="Student Transit Fares & Passes" class="p-2.5 rounded-xl bg-amber-500/20 text-amber-300 border border-amber-500/30 hover:bg-amber-500/30 font-bold">
            <i data-lucide="ticket" class="w-4 h-4"></i>
          </button>
          <button onclick="openPaymentAndBookingModal()" title="Book / Pay Pass" class="p-2.5 rounded-xl bg-brand-cyan text-black hover:opacity-90 font-bold shadow-md">
            <i data-lucide="credit-card" class="w-4 h-4"></i>
          </button>'''

if old_dash_search in content:
    content = content.replace(old_dash_search, new_dash_search)
    print("Added Fares & Passes button inside Dashboard sidebar!")

with open('build_full_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated clean build_full_app.py!")

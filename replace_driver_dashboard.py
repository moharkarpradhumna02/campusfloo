import re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx1 = c.find('id="driverFullScreenDashboard"')
idx1 = c.rfind('<section', 0, idx1)
idx2 = c.find('<!-- ================= MODAL: FARES & PASSES ================= -->', idx1)

new_driver_dashboard_html = '''<section id="driverFullScreenDashboard" class="hidden flex-1 flex flex-col h-[calc(100vh-72px)] bg-[#F4F4F5] overflow-hidden">
    
    <!-- Top Cockpit Control Header -->
    <header class="p-4 border-b border-zinc-800 bg-[#0B0F19] text-white flex flex-wrap items-center justify-between gap-3 shrink-0 z-20 shadow-md">
      <!-- Left: Identity & Status -->
      <div class="flex items-center gap-3">
        <div class="relative">
          <div class="w-12 h-12 rounded-2xl bg-zinc-800 border border-zinc-700 flex items-center justify-center text-2xl shadow-md">
            <span id="fsDriverIcon">👨‍✈️</span>
          </div>
          <span id="fsDriverStatusDot" class="w-3.5 h-3.5 rounded-full bg-emerald-500 absolute -bottom-0.5 -right-0.5 border-2 border-[#0B0F19] animate-pulse"></span>
        </div>
        <div>
          <div class="flex items-center gap-2">
            <h3 class="text-sm sm:text-base font-black text-white" id="fsDriverName">Rajesh Sharma</h3>
            <span class="px-2.5 py-0.5 rounded-full bg-emerald-950 text-emerald-300 text-[10px] font-mono font-bold border border-emerald-700">VERIFIED PILOT</span>
          </div>
          <p class="text-xs text-zinc-300 font-mono font-bold" id="fsDriverVehicle">PB 08 BX 9021 • Shuttle #1 (Ring Loop)</p>
        </div>
      </div>

      <!-- Center: Switch Vehicle Profile Dropdown (High Contrast) -->
      <div class="hidden md:flex items-center gap-2 bg-zinc-800/90 px-3 py-1.5 rounded-2xl border border-zinc-700">
        <span class="text-[11px] font-black text-zinc-200 uppercase tracking-wider">Assigned Vehicle:</span>
        <select id="fsDriverSelectDropdown" onchange="switchDriverProfile(this.value)" class="bg-white text-black font-black text-xs rounded-xl border-2 border-zinc-300 px-3 py-2 shadow-sm focus:border-black cursor-pointer">
          <option value="bus_1">🚌 Shuttle #1 — Rajesh Sharma (PB 08 BX 9021 • Ring Loop)</option>
          <option value="auto_2">🛺 Auto #2 — Vikram Singh (PB 08 CA 1201 • Hostels Sprint)</option>
          <option value="ev_3">⚡ Eco EV #3 — Suresh Yadav (PB 08 EV 0044 • UniMall Direct)</option>
          <option value="bus_4">🚌 Express #4 — Amit Patel (PB 08 BX 9410 • Blocks 1-36 Core)</option>
          <option value="auto_5">🛺 Priya Verma — Auto #5 (PB 08 CA 3381)</option>
          <option value="ev_6">⚡ Eco EV #6 — Sunita Gupta (PB 08 EV 0092)</option>
          <option value="bus_7">🚌 Shuttle #7 — Ramesh Kumar (PB 08 BX 8812)</option>
          <option value="auto_8">🛺 Deepak Sharma — Auto #8 (PB 08 CA 5509)</option>
          <option value="parked_bus_9">🅿️ Shuttle #9 — Harpreet Singh (P1 Standby)</option>
          <option value="parked_ev_10">🅿️ Eco EV #10 — Karan Verma (P2 UniMall)</option>
          <option value="parked_auto_11">🅿️ Auto #11 — Manjit Kumar (P3 Block 34)</option>
          <option value="parked_bus_12">🅿️ Shuttle #12 — Satnam Singh (P4 Sports)</option>
        </select>
      </div>

      <!-- Right: Duty Toggle, View Map & Logout -->
      <div class="flex items-center gap-2">
        <button onclick="toggleDriverDutyStatus()" id="fsDriverDutyBtn" class="px-4 py-2 rounded-xl bg-emerald-500 hover:bg-emerald-600 text-black font-black text-xs flex items-center gap-1.5 shadow-md transition-all">
          <span class="w-2.5 h-2.5 rounded-full bg-black animate-ping"></span>
          <span id="fsDriverDutyBtnText">🟢 ON DUTY</span>
        </button>
        <button onclick="launchTransportDashboard()" class="px-3.5 py-2 rounded-xl bg-zinc-800 hover:bg-zinc-700 text-white border border-zinc-600 text-xs font-black flex items-center gap-1.5 transition-all" title="View Full Campus Map">
          <span>🗺️ Map View</span>
        </button>
        <button onclick="logoutDriver()" class="px-3.5 py-2 rounded-xl bg-rose-950/70 hover:bg-rose-900 border border-rose-700 text-rose-300 text-xs font-black flex items-center gap-1.5 transition-all" title="Logout Driver">
          <span>🚪 Logout</span>
        </button>
      </div>
    </header>

    <!-- Segmented Navigation Tabs (Light High-Contrast) -->
    <div class="grid grid-cols-4 border-b border-zinc-300 bg-zinc-200 text-xs font-bold text-zinc-700 shrink-0">
      <button onclick="setDriverTab('pickups')" id="tabBtnPickups" class="py-3.5 text-center bg-black text-white font-black shadow-md border-b-2 border-black flex items-center justify-center gap-2 transition-all">
        <span>📍</span> <span>Passenger Pickups (<span id="driverPickupCount" class="font-mono font-black">3</span>)</span>
      </button>
      <button onclick="setDriverTab('chats')" id="tabBtnChats" class="py-3.5 text-center text-zinc-700 hover:text-black hover:bg-zinc-300 font-extrabold flex items-center justify-center gap-2 transition-all">
        <span>💬</span> <span>Passenger Chats & GPS</span>
      </button>
      <button onclick="setDriverTab('payments')" id="tabBtnPayments" class="py-3.5 text-center text-zinc-700 hover:text-black hover:bg-zinc-300 font-extrabold flex items-center justify-center gap-2 transition-all">
        <span>💰</span> <span>Fares & Payment Ledger</span>
      </button>
      <button onclick="setDriverTab('insights')" id="tabBtnInsights" class="py-3.5 text-center text-zinc-700 hover:text-black hover:bg-zinc-300 font-extrabold flex items-center justify-center gap-2 transition-all">
        <span>💡</span> <span>AI Insights & Telemetry</span>
      </button>
    </div>

    <!-- Main Full-Screen Body Container -->
    <div class="flex-1 overflow-y-auto p-4 sm:p-6 custom-scrollbar bg-[#F4F4F5]">
      
      <!-- PANE 1: PASSENGER PICKUPS & CUSTOMER PROFILES -->
      <div id="paneDriverPickups" class="space-y-4">
        <!-- Summary Banner with 4 Executive Metrics -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <div class="p-4 rounded-2xl bg-white border-2 border-zinc-300 shadow-sm space-y-1 text-black">
            <span class="text-[11px] text-zinc-500 font-black uppercase tracking-wider">Total in Queue</span>
            <p class="text-2xl font-black text-black font-mono" id="statQueueTotal">3 Passengers</p>
          </div>
          <div class="p-4 rounded-2xl bg-white border-2 border-zinc-300 shadow-sm space-y-1 text-black">
            <span class="text-[11px] text-amber-800 font-black uppercase tracking-wider">Waiting at Stops</span>
            <p class="text-2xl font-black text-amber-600 font-mono" id="statQueueWaiting">2 Waiting</p>
          </div>
          <div class="p-4 rounded-2xl bg-white border-2 border-zinc-300 shadow-sm space-y-1 text-black">
            <span class="text-[11px] text-emerald-800 font-black uppercase tracking-wider">On Board</span>
            <p class="text-2xl font-black text-emerald-600 font-mono" id="statQueueBoarded">1 Boarded</p>
          </div>
          <div class="p-4 rounded-2xl bg-white border-2 border-zinc-300 shadow-sm space-y-1 text-black">
            <span class="text-[11px] text-zinc-500 font-black uppercase tracking-wider">Total Trip Fare</span>
            <p class="text-2xl font-black text-black font-mono" id="statQueueFare">₹45.00</p>
          </div>
        </div>

        <!-- Passenger Cards Container -->
        <div class="space-y-3.5" id="driverPassengerListContainer">
          <!-- Rendered dynamically by JS -->
        </div>
      </div>

      <!-- PANE 2: PASSENGER CHATS & LIVE GPS LOCATION STREAM -->
      <div id="paneDriverChats" class="hidden space-y-4">
        <div class="p-4 rounded-2xl bg-white border-2 border-zinc-300 text-black flex items-center justify-between shadow-sm">
          <div class="flex items-center gap-3">
            <span class="text-2xl">📡</span>
            <div>
              <h4 class="text-sm font-black text-black">Live Student Two-Way Comms Center</h4>
              <p class="text-xs text-zinc-600 font-bold">Incoming live GPS location pings and passenger queries appear here in real time</p>
            </div>
          </div>
          <span class="px-3 py-1 rounded-full bg-emerald-100 text-emerald-900 border border-emerald-300 font-black text-xs font-mono flex items-center gap-1.5">
            <span class="w-2 h-2 rounded-full bg-emerald-600 animate-ping"></span> Live Connected
          </span>
        </div>

        <!-- Chat Messages Box -->
        <div class="p-4 rounded-2xl bg-white border-2 border-zinc-300 h-[380px] overflow-y-auto space-y-3 custom-scrollbar text-black shadow-inner" id="driverPortalChatStream">
          <!-- Rendered dynamically -->
        </div>

        <!-- Quick Canned Replies for Driver -->
        <div class="space-y-2">
          <span class="text-xs font-black text-black uppercase tracking-wider">⚡ 1-Tap Quick Driver Replies:</span>
          <div class="flex flex-wrap gap-2">
            <button onclick="sendDriverQuickReply('🚗 Haanji, bas 2 minute me aapke spot par aa raha hoon!')" class="px-3.5 py-2 rounded-xl bg-white hover:bg-zinc-200 text-black text-xs font-black border border-zinc-300 shadow-sm transition-all">
              ⚡ 2 min me aa raha hoon
            </button>
            <button onclick="sendDriverQuickReply('⛩️ Main Gate shelter par boarding open hai, jaldi aa jaiye!')" class="px-3.5 py-2 rounded-xl bg-white hover:bg-zinc-200 text-black text-xs font-black border border-zinc-300 shadow-sm transition-all">
              ⛩️ Main Gate par boarding open hai
            </button>
            <button onclick="sendDriverQuickReply('✅ OTP verified, aapka luggage safe hai!')" class="px-3.5 py-2 rounded-xl bg-white hover:bg-zinc-200 text-black text-xs font-black border border-zinc-300 shadow-sm transition-all">
              ✅ OTP verified
            </button>
            <button onclick="sendDriverQuickReply('⚠️ 5 minute ka traffic delay hai Block 34 cross par')" class="px-3.5 py-2 rounded-xl bg-white hover:bg-zinc-200 text-black text-xs font-black border border-zinc-300 shadow-sm transition-all">
              ⚠️ 5 min delay
            </button>
          </div>
        </div>
      </div>

      <!-- PANE 3: FARES & PAYMENT LEDGER -->
      <div id="paneDriverPayments" class="hidden space-y-4">
        <!-- Revenue Cards -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <div class="p-4 rounded-2xl bg-white border-2 border-zinc-300 text-black space-y-1 shadow-sm">
            <span class="text-[11px] text-zinc-500 font-black uppercase tracking-wider">Today's Earnings</span>
            <p class="text-2xl font-black text-black font-mono" id="statTodayRevenue">₹ 1,420.00</p>
            <span class="text-xs text-zinc-600 font-bold block">28 Completed Rides</span>
          </div>
          <div class="p-4 rounded-2xl bg-white border-2 border-zinc-300 text-black space-y-1 shadow-sm">
            <span class="text-[11px] text-zinc-500 font-black uppercase tracking-wider">Pass Auto-Deduct</span>
            <p class="text-2xl font-black text-black font-mono">₹ 1,120.00</p>
            <span class="text-xs text-zinc-600 font-bold block">22 Smart Pass Swipes</span>
          </div>
          <div class="p-4 rounded-2xl bg-white border-2 border-zinc-300 text-black space-y-1 shadow-sm">
            <span class="text-[11px] text-zinc-500 font-black uppercase tracking-wider">UPI QR Payments</span>
            <p class="text-2xl font-black text-black font-mono">₹ 255.00</p>
            <span class="text-xs text-zinc-600 font-bold block">6 Verified GPay/PhonePe</span>
          </div>
          <div class="p-4 rounded-2xl bg-white border-2 border-zinc-300 text-black space-y-1 shadow-sm">
            <span class="text-[11px] text-amber-800 font-black uppercase tracking-wider">Pending Cash</span>
            <p class="text-2xl font-black text-amber-600 font-mono" id="statPendingCash">₹ 45.00</p>
            <span class="text-xs text-zinc-600 font-bold block">2 Cash to Collect</span>
          </div>
        </div>

        <!-- Payment Transactions Table (High Contrast) -->
        <div class="rounded-2xl border-2 border-zinc-300 bg-white overflow-hidden shadow-sm">
          <div class="p-4 border-b border-zinc-200 flex items-center justify-between bg-zinc-50">
            <div class="flex items-center gap-2">
              <span class="text-base">🧾</span>
              <h4 class="text-xs font-black text-black">Live Passenger Fare Collection Ledger</h4>
            </div>
            <span class="text-xs text-zinc-600 font-mono font-bold">Auto-audited via Smart Transit Contract</span>
          </div>
          <div class="overflow-x-auto">
            <table class="w-full text-left text-xs font-sans">
              <thead class="bg-zinc-100 border-b border-zinc-200 text-black font-black uppercase text-[10px]">
                <tr>
                  <th class="p-3.5">Student Passenger</th>
                  <th class="p-3.5">Route & Trip</th>
                  <th class="p-3.5">Fare</th>
                  <th class="p-3.5">Payment Method</th>
                  <th class="p-3.5">Status</th>
                  <th class="p-3.5 text-right">Receipt</th>
                </tr>
              </thead>
              <tbody id="driverPaymentTableBody" class="divide-y divide-zinc-200 text-black font-bold">
                <!-- Dynamically populated via JS -->
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- PANE 4: AI INSIGHTS & TELEMETRY -->
      <div id="paneDriverInsights" class="hidden space-y-4">
        <!-- Congestion & Hotspots -->
        <div class="p-4 rounded-2xl bg-white border-2 border-zinc-300 text-black space-y-2.5 shadow-sm">
          <div class="flex items-center gap-2">
            <span class="text-xl">🚨</span>
            <div>
              <h4 class="text-xs font-black text-black">WAYZEN High-Demand & Campus Congestion Alert</h4>
              <p class="text-xs text-zinc-600 font-semibold">AI prediction based on class timetables and live foot-traffic</p>
            </div>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1 text-xs">
            <div class="p-3.5 rounded-xl bg-zinc-50 border border-zinc-300 space-y-1">
              <span class="text-black font-black block">🏫 Block 34 CSE Class Dispersal (in 10 min)</span>
              <p class="text-xs text-zinc-700 font-medium">~45 students heading towards UniMall and Girls Hostels. High passenger volume expected. Head to Block 34 transit shelter bay.</p>
            </div>
            <div class="p-3.5 rounded-xl bg-zinc-50 border border-zinc-300 space-y-1">
              <span class="text-black font-black block">🎪 Unipolis Cultural Fest Rehearsals</span>
              <p class="text-xs text-zinc-700 font-medium">Speed limit strictly enforced at 15 km/h near Unipolis ring road. Use North Avenue bypass road for faster transit.</p>
            </div>
          </div>
        </div>

        <!-- Vehicle Health Telemetry -->
        <div class="p-4 rounded-2xl bg-white border-2 border-zinc-300 space-y-3 shadow-sm text-black">
          <div class="flex items-center justify-between border-b border-zinc-200 pb-2">
            <div class="flex items-center gap-2">
              <span class="text-xl">⚙️</span>
              <h4 class="text-xs font-black text-black">Vehicle Diagnostic Telemetry</h4>
            </div>
            <span class="px-2.5 py-0.5 rounded-full bg-emerald-100 text-emerald-900 border border-emerald-300 font-black text-[10px] font-mono">ALL SYSTEMS GREEN</span>
          </div>
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
            <div class="p-3 rounded-xl bg-zinc-50 border border-zinc-300">
              <span class="text-zinc-600 font-bold block text-[10px]">Tire Pressure (PSI)</span>
              <span class="font-mono text-base font-black text-black">34.2 PSI</span>
            </div>
            <div class="p-3 rounded-xl bg-zinc-50 border border-zinc-300">
              <span class="text-zinc-600 font-bold block text-[10px]">EV Battery / Fuel</span>
              <span class="font-mono text-base font-black text-emerald-600">84% Optimal</span>
            </div>
            <div class="p-3 rounded-xl bg-zinc-50 border border-zinc-300">
              <span class="text-zinc-600 font-bold block text-[10px]">GPS Sync Accuracy</span>
              <span class="font-mono text-base font-black text-black">±0.4m (RTK)</span>
            </div>
            <div class="p-3 rounded-xl bg-zinc-50 border border-zinc-300">
              <span class="text-zinc-600 font-bold block text-[10px]">Driver Safety Rating</span>
              <span class="font-mono text-base font-black text-black">★ 4.95 / 5.0</span>
            </div>
          </div>
        </div>

      </div>

    </div>

  </section>\n\n  '''

if idx1 != -1 and idx2 != -1:
    c = c[:idx1] + new_driver_dashboard_html + c[idx2:]
    print("[PASS] Successfully updated driverFullScreenDashboard HTML")
else:
    print("[FAIL] Could not locate boundaries for driverFullScreenDashboard")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

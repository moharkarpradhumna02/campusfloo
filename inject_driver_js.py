with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Target for injecting JavaScript: right before function openDriverChat(vehicleId) {
target_js = 'function openDriverChat(vehicleId) {'
assert target_js in html, "target_js not found"

driver_js_code = """    // ================= DRIVER COCKPIT & PASSENGER QUEUE SYSTEM =================
    let activeDriverId = 'bus_1';
    let activeDriverTab = 'pickups';
    let driverIsOnDuty = true;

    // Live Passenger Queue for Drivers
    let DRIVER_PASSENGERS = [
      {
        id: 'pass_1',
        driverId: 'bus_1',
        name: 'Pradhumna Moharkar',
        studentId: 'STU-2024-8891',
        dept: 'School of Computer Science (CSE)',
        year: '3rd Year',
        phone: '+91 98765-43210',
        avatar: '👨‍💻',
        pickup: 'Central Library (B.R. Mittal) - Gate 2',
        pickupCoords: [31.2555, 75.7038],
        destination: 'Academic Blocks 31-36 (CSE & Tech Hub)',
        seat: 'Seat 2A (Window)',
        fare: 15,
        otp: '8392',
        status: 'waiting', // 'waiting', 'boarded', 'completed'
        paymentStatus: 'received',
        paymentMethod: 'Campus Smart Pass Auto-Deduct',
        txnId: 'TXN-994821',
        time: 'Just now'
      },
      {
        id: 'pass_2',
        driverId: 'bus_1',
        name: 'Ananya Sharma',
        studentId: 'STU-2024-4412',
        dept: 'Mittal School of Business (BBA)',
        year: '2nd Year',
        phone: '+91 98142-99011',
        avatar: '👩‍🎓',
        pickup: 'Girls Hostels Sector (GH-3 Gate)',
        pickupCoords: [31.2508, 75.7068],
        destination: 'UniMall Student Complex',
        seat: 'Seat 1B (Aisle)',
        fare: 15,
        otp: '4190',
        status: 'boarded',
        paymentStatus: 'received',
        paymentMethod: 'UPI QR (PhonePe)',
        txnId: 'UPI-881204',
        time: '2 min ago'
      },
      {
        id: 'pass_3',
        driverId: 'bus_1',
        name: 'Rohan Verma',
        studentId: 'STU-2023-7721',
        dept: 'School of Mechanical Engineering',
        year: '4th Year',
        phone: '+91 94170-22334',
        avatar: '🧑‍🔧',
        pickup: 'Main Gate (GT Road NH-44 Shelter)',
        pickupCoords: [31.2485, 75.7015],
        destination: 'Indoor Sports Complex & Gym',
        seat: 'Seat 3A (Window)',
        fare: 15,
        otp: '6219',
        status: 'waiting',
        paymentStatus: 'pending',
        paymentMethod: 'Cash on Boarding',
        txnId: 'CASH-8819',
        time: '4 min ago'
      },
      {
        id: 'pass_4',
        driverId: 'bus_1',
        name: 'Simran Kaur',
        studentId: 'STU-2024-1188',
        dept: 'Biotechnology & Bio-Informatics',
        year: '1st Year',
        phone: '+91 98722-11445',
        avatar: '👩‍🔬',
        pickup: 'UniMall Student Food Court Link',
        pickupCoords: [31.2518, 75.7042],
        destination: 'Robopark & Innovation Arena',
        seat: 'Seat 4C (Front)',
        fare: 10,
        otp: '7731',
        status: 'completed',
        paymentStatus: 'received',
        paymentMethod: 'Campus Smart Pass Auto-Deduct',
        txnId: 'TXN-773199',
        time: '12 min ago'
      }
    ];

    function openDriverPortalModal(driverId) {
      if (driverId) activeDriverId = driverId;
      const v = getAnyVehicle(activeDriverId);

      // Update header info
      const nameEl = document.getElementById('driverConsoleName');
      if (nameEl) nameEl.textContent = v.driver || 'Rajesh Sharma';

      const vehEl = document.getElementById('driverConsoleVehicle');
      if (vehEl) vehEl.textContent = `${v.plate} • ${v.name} (${v.typeName})`;

      const iconEl = document.getElementById('driverConsoleIcon');
      if (iconEl) iconEl.textContent = v.icon || '👨‍✈️';

      const sel = document.getElementById('driverSelectDropdown');
      if (sel) sel.value = v.id;

      // Update telemetry
      const telBat = document.getElementById('telemetryBattery');
      if (telBat) telBat.textContent = `${v.battery || 84}% (Optimal)`;

      renderDriverPassengers();
      renderDriverChats();
      renderDriverPayments();
      openModal('driverPortalModal');
    }

    function switchDriverProfile(driverId) {
      activeDriverId = driverId;
      openDriverPortalModal(driverId);
      showToast(`Switched driver cockpit to ${getAnyVehicle(driverId).driver}!`);
    }

    function setDriverTab(tab) {
      activeDriverTab = tab;
      const tabs = ['pickups', 'chats', 'payments', 'insights'];
      tabs.forEach(t => {
        const btn = document.getElementById(`tabBtn${t.charAt(0).toUpperCase() + t.slice(1)}`);
        const pane = document.getElementById(`paneDriver${t.charAt(0).toUpperCase() + t.slice(1)}`);
        if (t === tab) {
          if (btn) btn.className = 'py-3 text-center border-b-2 border-emerald-400 text-emerald-400 bg-emerald-500/10 flex items-center justify-center gap-2 transition-all';
          if (pane) pane.classList.remove('hidden');
        } else {
          if (btn) btn.className = 'py-3 text-center border-b-2 border-transparent hover:text-white flex items-center justify-center gap-2 transition-all';
          if (pane) pane.classList.add('hidden');
        }
      });

      if (tab === 'pickups') renderDriverPassengers();
      if (tab === 'chats') renderDriverChats();
      if (tab === 'payments') renderDriverPayments();
    }

    function toggleDriverDutyStatus() {
      driverIsOnDuty = !driverIsOnDuty;
      const btn = document.getElementById('driverDutyBtn');
      const text = document.getElementById('driverDutyBtnText');
      const dot = document.getElementById('driverStatusDot');
      if (driverIsOnDuty) {
        if (btn) btn.className = 'px-3.5 py-2 rounded-xl bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 text-xs font-black flex items-center gap-2 hover:bg-emerald-500/30 transition-all shadow-md';
        if (text) text.textContent = '🟢 ON DUTY';
        if (dot) dot.className = 'w-3.5 h-3.5 rounded-full bg-emerald-400 absolute -bottom-0.5 -right-0.5 border-2 border-[#0c142b] animate-pulse';
        showToast('🟢 Driver Duty Status: ON DUTY (Receiving Student Pickups)');
      } else {
        if (btn) btn.className = 'px-3.5 py-2 rounded-xl bg-amber-500/20 text-amber-300 border border-amber-500/40 text-xs font-black flex items-center gap-2 hover:bg-amber-500/30 transition-all shadow-md';
        if (text) text.textContent = '☕ ON BREAK';
        if (dot) dot.className = 'w-3.5 h-3.5 rounded-full bg-amber-400 absolute -bottom-0.5 -right-0.5 border-2 border-[#0c142b]';
        showToast('☕ Driver Duty Status: ON BREAK (Standby at P1 Bay)');
      }
    }

    function renderDriverPassengers() {
      const container = document.getElementById('driverPassengerListContainer');
      if (!container) return;

      const v = getAnyVehicle(activeDriverId);
      const vehiclePos = getCoordOnRoute(v.routeId || 'route_purple', v.s || 0);

      const waitingCount = DRIVER_PASSENGERS.filter(p => p.status === 'waiting').length;
      const boardedCount = DRIVER_PASSENGERS.filter(p => p.status === 'boarded').length;
      const totalFare = DRIVER_PASSENGERS.filter(p => p.status !== 'completed').reduce((sum, p) => sum + p.fare, 0);

      const countEl = document.getElementById('driverPickupCount');
      if (countEl) countEl.textContent = DRIVER_PASSENGERS.filter(p => p.status !== 'completed').length;

      const statTotal = document.getElementById('statQueueTotal');
      if (statTotal) statTotal.textContent = `${DRIVER_PASSENGERS.filter(p => p.status !== 'completed').length} Passengers`;

      const statWait = document.getElementById('statQueueWaiting');
      if (statWait) statWait.textContent = `${waitingCount} Waiting`;

      const statBoard = document.getElementById('statQueueBoarded');
      if (statBoard) statBoard.textContent = `${boardedCount} Boarded`;

      const statFare = document.getElementById('statQueueFare');
      if (statFare) statFare.textContent = `₹${totalFare}.00`;

      container.innerHTML = DRIVER_PASSENGERS.map(p => {
        const isWaiting = p.status === 'waiting';
        const isBoarded = p.status === 'boarded';
        const isCompleted = p.status === 'completed';

        // Calculate distance from vehicle to student pickup
        let distMeters = 150;
        if (p.pickupCoords && p.pickupCoords.length === 2) {
          distMeters = Math.round(haversineDist([vehiclePos.lat, vehiclePos.lng], p.pickupCoords));
        }
        const estDriveMins = Math.max(1, Math.round(distMeters / 250));

        const statusBadge = isWaiting 
          ? '<span class="px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30 text-[10px] font-mono font-bold flex items-center gap-1"><span class="w-1.5 h-1.5 rounded-full bg-amber-400 animate-ping"></span> WAITING AT STOP</span>'
          : (isBoarded 
            ? '<span class="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-[10px] font-mono font-bold">🟢 ON BOARD</span>'
            : '<span class="px-2 py-0.5 rounded-full bg-zinc-700 text-zinc-300 text-[10px] font-mono font-bold">✅ DROPPED OFF</span>');

        const payBadge = p.paymentStatus === 'received'
          ? `<span class="text-emerald-400 font-bold flex items-center gap-1"><span>✅ Paid</span> <span class="text-[10px] text-zinc-400 font-mono">(${p.paymentMethod})</span></span>`
          : `<span class="text-amber-400 font-bold flex items-center gap-1"><span>⏳ Collect Cash</span> <span class="text-[10px] text-zinc-400 font-mono">(₹${p.fare})</span></span>`;

        return `
          <div class="p-4 rounded-2xl glass-card border ${isWaiting ? 'border-amber-500/30 bg-amber-500/5' : (isBoarded ? 'border-emerald-500/30 bg-emerald-500/5' : 'border-white/10 opacity-75')} space-y-3 transition-all">
            <!-- Student Profile Header -->
            <div class="flex flex-wrap items-center justify-between gap-2 border-b border-white/10 pb-2.5">
              <div class="flex items-center gap-3">
                <div class="w-11 h-11 rounded-2xl bg-[#0b1024] border border-white/20 flex items-center justify-center text-2xl shadow-md">
                  ${p.avatar || '🧑‍🎓'}
                </div>
                <div>
                  <div class="flex items-center gap-2">
                    <h4 class="text-sm font-black text-white">${p.name}</h4>
                    <span class="text-[10px] font-mono text-brand-cyan font-bold bg-brand-cyan/10 px-2 py-0.2 rounded-md">${p.studentId}</span>
                  </div>
                  <p class="text-[11px] text-zinc-300 font-medium">${p.dept} • ${p.year}</p>
                </div>
              </div>
              <div class="flex items-center gap-2">
                ${statusBadge}
                <a href="tel:${p.phone}" class="p-2 rounded-xl bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 hover:bg-emerald-500/30 font-bold text-xs flex items-center gap-1" title="Call Student">
                  📞 ${p.phone}
                </a>
              </div>
            </div>

            <!-- Route & Live Pickup Details -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
              <div class="p-2.5 rounded-xl bg-black/40 border border-white/5 space-y-1">
                <div class="flex items-center justify-between">
                  <span class="text-zinc-400 text-[10px] font-bold uppercase">📍 Exact Pickup Spot:</span>
                  <span class="text-brand-cyan font-mono font-bold text-[10px]">${distMeters}m away (~${estDriveMins}m drive)</span>
                </div>
                <strong class="text-white block text-xs">${p.pickup}</strong>
                <p class="text-[10px] text-zinc-400 font-mono">GPS: ${p.pickupCoords[0].toFixed(5)}, ${p.pickupCoords[1].toFixed(5)}</p>
              </div>

              <div class="p-2.5 rounded-xl bg-black/40 border border-white/5 space-y-1">
                <div class="flex items-center justify-between">
                  <span class="text-zinc-400 text-[10px] font-bold uppercase">🎯 Destination & Seat:</span>
                  <span class="text-emerald-400 font-mono font-bold">Fare: ₹${p.fare}</span>
                </div>
                <strong class="text-white block text-xs">${p.destination}</strong>
                <p class="text-[10px] text-zinc-400">Assigned: <span class="text-brand-cyan font-mono font-bold">${p.seat}</span></p>
              </div>
            </div>

            <!-- Payment & Security OTP Section -->
            <div class="flex flex-wrap items-center justify-between gap-2 p-2.5 rounded-xl bg-[#060a18] border border-white/10 text-xs">
              <div>
                <span class="text-[10px] text-zinc-400 block font-bold">Payment Status:</span>
                ${payBadge}
              </div>

              <!-- OTP Verification / Boarding Box -->
              ${isWaiting ? `
                <div class="flex items-center gap-2">
                  <div class="flex items-center gap-1">
                    <span class="text-[10px] text-zinc-400">Student OTP:</span>
                    <input type="text" id="otp_inp_${p.id}" placeholder="${p.otp}" maxlength="4" class="w-16 px-2 py-1 text-center font-mono font-black text-xs rounded-lg bg-white/10 border border-white/20 text-white focus:outline-none focus:border-emerald-400">
                  </div>
                  <button onclick="verifyPassengerOtp('${p.id}')" class="px-3 py-1.5 rounded-xl bg-gradient-to-r from-emerald-400 to-teal-400 text-black font-black text-xs hover:opacity-90 flex items-center gap-1 shadow-md">
                    ✅ Verify & Board
                  </button>
                </div>
              ` : (isBoarded ? `
                <div class="flex items-center gap-2">
                  <span class="text-[10px] text-emerald-400 font-mono font-bold">OTP ${p.otp} Verified</span>
                  <button onclick="completePassengerDrop('${p.id}')" class="px-3.5 py-1.5 rounded-xl bg-purple-500/20 hover:bg-purple-500/30 text-purple-300 border border-purple-500/40 font-black text-xs flex items-center gap-1">
                    🏁 Mark Dropped Off
                  </button>
                </div>
              ` : `
                <span class="text-[10px] text-zinc-500 font-mono font-bold">Trip Successfully Completed</span>
              `)}
            </div>

            <!-- Driver Action Buttons -->
            <div class="flex items-center justify-between pt-1 border-t border-white/5 text-[11px]">
              <div class="flex items-center gap-2">
                <button onclick="locatePassengerOnMap(${p.pickupCoords[0]}, ${p.pickupCoords[1]}, '${p.name}')" class="px-3 py-1.5 rounded-xl bg-brand-cyan/20 hover:bg-brand-cyan/30 text-brand-cyan font-bold flex items-center gap-1.5 border border-brand-cyan/30 transition-all">
                  🗺️ Locate on Campus Map
                </button>
                <button onclick="setDriverTab('chats')" class="px-3 py-1.5 rounded-xl bg-white/10 hover:bg-white/20 text-white font-bold flex items-center gap-1.5 border border-white/10 transition-all">
                  💬 Open Chat
                </button>
              </div>

              <button onclick="viewPaymentReceipt('${p.txnId}')" class="text-zinc-400 hover:text-white font-mono text-[10px] underline">
                🧾 View Receipt (${p.txnId})
              </button>
            </div>
          </div>
        `;
      }).join('');
    }

    function verifyPassengerOtp(passId) {
      const p = DRIVER_PASSENGERS.find(x => x.id === passId);
      if (!p) return;

      const inp = document.getElementById(`otp_inp_${passId}`);
      const enteredOtp = inp ? (inp.value || '').trim() : '';
      if (enteredOtp && enteredOtp !== p.otp) {
        showToast('❌ Incorrect OTP! Please verify 4 digits from passenger screen.');
        return;
      }

      p.status = 'boarded';
      playBeep(880, 'sine', 0.2);
      showToast(`🎉 Verified OTP ${p.otp}! ${p.name} is now on board.`);
      renderDriverPassengers();
    }

    function completePassengerDrop(passId) {
      const p = DRIVER_PASSENGERS.find(x => x.id === passId);
      if (!p) return;
      p.status = 'completed';
      playBeep(720, 'sine', 0.15);
      showToast(`🏁 Trip completed! ${p.name} dropped off at ${p.destination}.`);
      renderDriverPassengers();
      renderDriverPayments();
    }

    function locatePassengerOnMap(lat, lng, name) {
      closeModal('driverPortalModal');
      launchTransportDashboard();
      if (map) {
        map.setView([lat, lng], 18, { animate: true });
        // Set student location marker if not present
        setStudentLiveLocation(lat, lng);
        showToast(`🗺️ Centered map on ${name}'s live pickup spot!`);
      }
    }

    function renderDriverChats() {
      const stream = document.getElementById('driverPortalChatStream');
      if (!stream) return;

      stream.innerHTML = driverChatHistory.map(m => {
        const isDriver = m.sender === 'driver';
        return `
          <div class="flex ${isDriver ? 'justify-end' : 'justify-start'}">
            <div class="max-w-[80%] rounded-2xl p-3 ${isDriver ? 'bg-gradient-to-r from-emerald-500/20 to-teal-500/20 text-emerald-200 border border-emerald-500/30' : 'bg-white/10 text-zinc-200 border border-white/15'} text-xs space-y-1">
              <span class="text-[9px] font-mono font-bold block ${isDriver ? 'text-emerald-400 text-right' : 'text-brand-cyan'}">
                ${isDriver ? '👨‍✈️ Driver (You)' : '🧑‍🎓 Passenger'}
              </span>
              <p class="leading-relaxed">${m.text}</p>
            </div>
          </div>
        `;
      }).join('');
      stream.scrollTop = stream.scrollHeight;
    }

    function sendDriverQuickReply(text) {
      driverChatHistory.push({ sender: 'driver', text });
      renderDriverChats();
      renderChatMessages();
      playBeep(640, 'sine', 0.1);
      showToast(`Sent to passenger: "${text}"`);
    }

    function sendDriverCustomReply() {
      const inp = document.getElementById('driverCustomChatInput');
      if (!inp || !inp.value.trim()) return;
      const text = inp.value.trim();
      inp.value = '';
      sendDriverQuickReply(text);
    }

    function renderDriverPayments() {
      const tbody = document.getElementById('driverPaymentTableBody');
      if (!tbody) return;

      const receivedTotal = DRIVER_PASSENGERS.filter(p => p.paymentStatus === 'received').reduce((sum, p) => sum + p.fare, 0);
      const pendingTotal = DRIVER_PASSENGERS.filter(p => p.paymentStatus === 'pending').reduce((sum, p) => sum + p.fare, 0);

      const statRev = document.getElementById('statTodayRevenue');
      if (statRev) statRev.textContent = `₹ ${(1375 + receivedTotal).toFixed(2)}`;

      const statPend = document.getElementById('statPendingCash');
      if (statPend) statPend.textContent = `₹ ${(45 + pendingTotal).toFixed(2)}`;

      tbody.innerHTML = DRIVER_PASSENGERS.map(p => {
        const isReceived = p.paymentStatus === 'received';
        return `
          <tr class="hover:bg-white/5 transition-colors">
            <td class="p-3">
              <div class="flex items-center gap-2">
                <span class="text-base">${p.avatar || '🧑‍🎓'}</span>
                <div>
                  <strong class="text-white block">${p.name}</strong>
                  <span class="text-[10px] text-zinc-400 font-mono">${p.studentId}</span>
                </div>
              </div>
            </td>
            <td class="p-3">
              <div class="space-y-0.5">
                <span class="text-zinc-300 block truncate max-w-[160px]">📍 ${p.pickup}</span>
                <span class="text-brand-cyan text-[10px] block truncate max-w-[160px]">➔ ${p.destination}</span>
              </div>
            </td>
            <td class="p-3 font-mono text-zinc-300 font-bold">${p.seat}</td>
            <td class="p-3 font-mono font-black text-emerald-400">₹${p.fare}.00</td>
            <td class="p-3">
              ${isReceived ? `
                <span class="px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-[10px] font-mono font-bold inline-flex items-center gap-1">
                  <span>✅ Received</span>
                </span>
                <span class="text-[9px] text-zinc-400 block font-mono">${p.txnId}</span>
              ` : `
                <span class="px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30 text-[10px] font-mono font-bold inline-flex items-center gap-1">
                  <span>⏳ Pending Cash</span>
                </span>
                <button onclick="markPaymentCashReceived('${p.txnId}')" class="text-[10px] text-emerald-400 underline block mt-0.5 font-bold hover:text-emerald-300">
                  Mark Paid (₹${p.fare})
                </button>
              `}
            </td>
            <td class="p-3 text-right">
              <button onclick="viewPaymentReceipt('${p.txnId}')" class="px-2.5 py-1 rounded-lg bg-white/10 hover:bg-white/20 text-white font-bold text-[10px] transition-all">
                🧾 Receipt
              </button>
            </td>
          </tr>
        `;
      }).join('');
    }

    function markPaymentCashReceived(txnId) {
      const p = DRIVER_PASSENGERS.find(x => x.txnId === txnId);
      if (!p) return;
      p.paymentStatus = 'received';
      p.paymentMethod = 'Cash Paid at Boarding (Verified by Driver)';
      playBeep(880, 'sine', 0.15);
      showToast(`💵 Received ₹${p.fare}.00 cash payment from ${p.name}!`);
      renderDriverPayments();
      renderDriverPassengers();
    }

    function viewPaymentReceipt(txnId) {
      const p = DRIVER_PASSENGERS.find(x => x.txnId === txnId) || DRIVER_PASSENGERS[0];
      const v = getAnyVehicle(activeDriverId);

      document.getElementById('receiptTxnId').textContent = p.txnId;
      document.getElementById('receiptStudentName').textContent = p.name;
      document.getElementById('receiptStudentId').textContent = `${p.studentId} • ${p.dept}`;
      document.getElementById('receiptPickupSpot').textContent = p.pickup;
      document.getElementById('receiptDestSpot').textContent = p.destination;
      document.getElementById('receiptVehicleSeat').textContent = `${v.name} (${v.plate}) • ${p.seat}`;
      document.getElementById('receiptBaseFare').textContent = `₹${p.fare}.00`;
      document.getElementById('receiptTotalFare').textContent = `₹${p.fare}.00`;
      document.getElementById('receiptPayMethod').textContent = p.paymentMethod;

      openModal('driverReceiptModal');
    }

    """

html = html.replace(target_js, driver_js_code + target_js, 1)

print("Injected driver portal JavaScript functions successfully")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

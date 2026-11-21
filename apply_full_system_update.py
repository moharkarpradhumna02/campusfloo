import re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Add 5-minute QR Timer variables and functions
qr_timer_js = '''
    // ================= 5-MINUTE DYNAMIC UPI QR TIMER & BOOKING ENGINE =================
    let upiCountdownSeconds = 300; // 5 minutes
    let upiCountdownInterval = null;

    let currentBookingContext = {
      vehicleId: 'bus_1',
      vehicleName: 'Shuttle #1 (Ring Loop)',
      driver: 'Rajesh Sharma',
      plate: 'PB 08 BX 9021',
      pickup: 'Main Gate Transit Shelter (GT Road NH-44)',
      pickupCoords: [31.2485, 75.7015],
      destination: 'Academic Blocks 31-36 (CSE & Tech Hub)',
      fare: 15,
      seat: 'Seat 2A (Window)',
      category: 'bus'
    };

    function startUpiQrTimer() {
      if (upiCountdownInterval) clearInterval(upiCountdownInterval);
      upiCountdownSeconds = 300; // 5:00
      updateUpiTimerDisplay();

      upiCountdownInterval = setInterval(() => {
        upiCountdownSeconds--;
        if (upiCountdownSeconds <= 0) {
          clearInterval(upiCountdownInterval);
          upiCountdownSeconds = 0;
          updateUpiTimerDisplay();
          onUpiQrExpired();
        } else {
          updateUpiTimerDisplay();
        }
      }, 1000);
    }

    function updateUpiTimerDisplay() {
      const mins = Math.floor(upiCountdownSeconds / 60);
      const secs = upiCountdownSeconds % 60;
      const timeStr = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
      
      const textEl = document.getElementById('upiCountdownText');
      if (textEl) {
        textEl.textContent = `⏱️ ${timeStr}`;
      }
      const barEl = document.getElementById('upiTimerProgressBar');
      if (barEl) {
        const pct = (upiCountdownSeconds / 300) * 100;
        barEl.style.width = `${pct}%`;
      }
    }

    function onUpiQrExpired() {
      const overlay = document.getElementById('upiQrExpiredOverlay');
      if (overlay) overlay.classList.remove('hidden');
      const textEl = document.getElementById('upiCountdownText');
      if (textEl) {
        textEl.textContent = '⚠️ Expired';
      }
    }

    function refreshUpiQrCode() {
      const overlay = document.getElementById('upiQrExpiredOverlay');
      if (overlay) overlay.classList.add('hidden');
      const qrImg = document.getElementById('upiQrImage');
      const net = Math.max(0, currentBookingContext.fare - (appliedCoupon === 'CAMPUS10' ? currentBookingContext.fare * 0.1 : appliedCoupon === 'FREEFIRST' ? currentBookingContext.fare : 0));
      if (qrImg) {
        qrImg.src = `https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=upi://pay?pa=campusflow@okaxis%26pn=LPU%20Campus%20Transit%26am=${net}%26cu=INR%26tn=Trip-${Date.now()}`;
      }
      startUpiQrTimer();
      showToast('🔄 Fresh 5-minute QR Code generated!');
    }

    function openPaymentAndBookingModal(ctx) {
      if (ctx) {
        currentBookingContext = Object.assign(currentBookingContext, ctx);
      }
      selectedMoney = currentBookingContext.fare || 15;

      // Update Header Summary
      const sumVeh = document.getElementById('paySummaryVehicle');
      if (sumVeh) sumVeh.textContent = currentBookingContext.vehicleName;
      const sumRoute = document.getElementById('paySummaryRoute');
      if (sumRoute) sumRoute.textContent = `${currentBookingContext.pickup} ➔ ${currentBookingContext.destination}`;
      const sumSeat = document.getElementById('paySummarySeat');
      if (sumSeat) sumSeat.textContent = currentBookingContext.seat || 'Open Boarding';
      const sumFare = document.getElementById('paySummaryFare');
      if (sumFare) sumFare.textContent = `₹${selectedMoney.toFixed(2)}`;

      const sumIcon = document.getElementById('paySummaryIcon');
      if (sumIcon) {
        sumIcon.textContent = currentBookingContext.category === 'auto' ? '🛺' : (currentBookingContext.category === 'ev' ? '⚡' : '🚌');
      }

      // Update wallet balance preview
      const wBal = document.getElementById('modalWalletBalance');
      if (wBal) wBal.textContent = `₹ ${walletBalance.toFixed(2)}`;

      recalculatePrice();
      switchPayTab('upi');
      refreshUpiQrCode();
      openModal('paymentBookingModal');
    }

    function switchPayTab(mode) {
      currentPaymentMethod = mode;
      const tabs = ['upi', 'wallet', 'cash'];
      tabs.forEach(t => {
        const btn = document.getElementById(`payTab${t.charAt(0).toUpperCase() + t.slice(1)}`);
        const content = document.getElementById(`payContent${t.charAt(0).toUpperCase() + t.slice(1)}`);
        if (t === mode) {
          if (btn) btn.className = 'pay-method-tab py-2.5 rounded-xl bg-black text-white shadow-sm flex items-center justify-center gap-1 transition-all';
          if (content) content.classList.remove('hidden');
        } else {
          if (btn) btn.className = 'pay-method-tab py-2.5 rounded-xl text-zinc-700 hover:text-black font-extrabold flex items-center justify-center gap-1 transition-all';
          if (content) content.classList.add('hidden');
        }
      });
      recalculatePrice();
    }

    function recalculatePrice() {
      let base = currentBookingContext.fare || selectedMoney || 15;
      let discount = 0;
      let label = '0%';
      if (appliedCoupon === 'CAMPUS10') {
        discount = base * 0.10;
        label = '10%';
      } else if (appliedCoupon === 'FREEFIRST') {
        discount = base;
        label = '100%';
      }
      const net = Math.max(0, base - discount);
      const bEl = document.getElementById('priceSummaryBase');
      if (bEl) bEl.textContent = `₹${base.toFixed(2)}`;
      const lEl = document.getElementById('priceSummaryDiscountLabel');
      if (lEl) lEl.textContent = label;
      const dEl = document.getElementById('priceSummaryDiscount');
      if (dEl) dEl.textContent = `-₹${discount.toFixed(2)}`;
      const tEl = document.getElementById('priceSummaryTotal');
      if (tEl) tEl.textContent = `₹${net.toFixed(2)}`;

      // Update confirm button label
      const cBtn = document.getElementById('confirmPayBtn');
      if (cBtn) {
        if (currentPaymentMethod === 'cash') {
          cBtn.innerHTML = `<span>Book with Cash on Boarding (Pay ₹${net.toFixed(2)})</span> <i data-lucide="shield-check" class="w-4 h-4"></i>`;
        } else if (currentPaymentMethod === 'wallet') {
          cBtn.innerHTML = `<span>Confirm Auto-Deduct (₹${net.toFixed(2)}) &amp; Get OTP</span> <i data-lucide="shield-check" class="w-4 h-4"></i>`;
        } else {
          cBtn.innerHTML = `<span>Confirm UPI Payment (₹${net.toFixed(2)}) &amp; Get OTP</span> <i data-lucide="shield-check" class="w-4 h-4"></i>`;
        }
      }

      // Update QR code with net amount
      const qrImg = document.getElementById('upiQrImage');
      if (qrImg && currentPaymentMethod === 'upi') {
        qrImg.src = `https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=upi://pay?pa=campusflow@okaxis%26pn=LPU%20Campus%20Transit%26am=${net.toFixed(2)}%26cu=INR%26tn=Trip-${Date.now()}`;
      }

      // Wallet status check
      const wStatus = document.getElementById('walletPayStatusText');
      if (wStatus) {
        if (walletBalance >= net) {
          wStatus.innerHTML = `✅ Sufficient balance! ₹${net.toFixed(2)} will be debited. (Remaining: ₹${(walletBalance - net).toFixed(2)})`;
          wStatus.className = 'text-xs text-black font-bold';
        } else {
          wStatus.innerHTML = `⚠️ Low balance! Current balance is ₹${walletBalance.toFixed(2)}. Need ₹${(net - walletBalance).toFixed(2)} more. Please top up or use UPI/Cash.`;
          wStatus.className = 'text-xs text-red-600 font-bold';
        }
      }
    }

    function confirmPaymentAndBookTrip() {
      const net = Math.max(0, currentBookingContext.fare - (appliedCoupon === 'CAMPUS10' ? currentBookingContext.fare * 0.1 : appliedCoupon === 'FREEFIRST' ? currentBookingContext.fare : 0));
      
      if (currentPaymentMethod === 'wallet') {
        if (walletBalance < net) {
          showToast(`⚠️ Insufficient Wallet Balance (₹${walletBalance.toFixed(2)}). Ride fare is ₹${net.toFixed(2)}. Please choose UPI or Cash.`);
          return;
        }
        walletBalance -= net;
        updateWalletDisplay();
      }

      // Generate 4-digit security OTP
      const code = Math.floor(1000 + Math.random() * 9000).toString();
      activeOtpCode = code;

      // Method label for receipt & driver cockpit
      let methodLabel = 'UPI Dynamic QR (Verified)';
      let paymentStatus = 'received';
      if (currentPaymentMethod === 'wallet') {
        methodLabel = 'Campus Smart Pass Auto-Deduct';
        paymentStatus = 'received';
      } else if (currentPaymentMethod === 'cash') {
        methodLabel = 'Cash on Boarding (Pending)';
        paymentStatus = 'pending';
      }

      // Record Transaction in Wallet
      const newTxn = {
        id: 'TXN-' + Math.floor(100000 + Math.random() * 900000),
        type: 'ride',
        title: `${currentBookingContext.vehicleName} (${currentPaymentMethod.toUpperCase()})`,
        amount: currentPaymentMethod === 'cash' ? 0 : -net,
        date: 'Just now',
        status: 'OTP: ' + code
      };
      paymentHistory.unshift(newTxn);
      renderWalletHistory();

      // Create & Insert Passenger into DRIVER_PASSENGERS for Driver Cockpit
      const newPassenger = {
        id: 'pass_' + Date.now(),
        driverId: currentBookingContext.vehicleId || activeDriverId || 'bus_1',
        name: currentUser && currentUser.name ? currentUser.name : 'Student Rider',
        studentId: currentUser && currentUser.studentId ? currentUser.studentId : 'STU-2024-8891',
        dept: 'School of Computer Science (CSE)',
        year: '3rd Year',
        phone: currentUser && currentUser.phone ? currentUser.phone : '+91 98765-43210',
        avatar: '🧑‍🎓',
        pickup: currentBookingContext.pickup,
        pickupCoords: currentBookingContext.pickupCoords,
        destination: currentBookingContext.destination,
        seat: currentBookingContext.seat,
        fare: net,
        otp: code,
        status: 'waiting',
        paymentStatus: paymentStatus,
        paymentMethod: methodLabel,
        txnId: newTxn.id,
        time: 'Just now'
      };
      DRIVER_PASSENGERS.unshift(newPassenger);

      // Decrement vehicle seats
      const v = getAnyVehicle(currentBookingContext.vehicleId);
      if (v && v.availableSeats > 0) {
        v.availableSeats--;
        v.occupiedSeats++;
      }
      renderFleetList();
      renderDriverPassengers();

      // Update Active Trip Banner
      const tripBanner = document.getElementById('activeTripBanner');
      if (tripBanner) {
        tripBanner.classList.remove('hidden');
        document.getElementById('activeTripVehicleName').textContent = currentBookingContext.vehicleName;
        document.getElementById('activeTripOtpBadge').textContent = `OTP: ${code}`;
        document.getElementById('activeTripDriverInfo').textContent = `Driver: ${currentBookingContext.driver} (${currentBookingContext.plate}) • ${currentBookingContext.seat}`;
      }

      if (upiCountdownInterval) clearInterval(upiCountdownInterval);
      closeModal('paymentBookingModal');
      playBeep(880, 'sine', 0.25);
      showToast(`🎉 Ride Booked! ${currentBookingContext.vehicleName} • OTP: ${code}`);
    }

    // Connect all booking actions to Payment Modal
    function bookSpecificVehicle(id) {
      const v = getAnyVehicle(id);
      openPaymentAndBookingModal({
        vehicleId: v.id,
        vehicleName: v.name,
        driver: v.driver,
        plate: v.plate,
        pickup: 'Main Gate Transit Shelter (GT Road NH-44)',
        pickupCoords: [31.2485, 75.7015],
        destination: 'Academic Blocks 31-36 (CSE & Tech Hub)',
        fare: v.fare || 15,
        seat: 'Express Boarding',
        category: v.category || 'bus'
      });
    }

    function bookParkedVehicle(id) {
      const pv = PARKED_FLEET.find(x => x.id === id);
      if (!pv) return;
      if (pv.availableSeats <= 0) {
        showToast('⚠️ Sorry, all seats for this scheduled trip are full!');
        return;
      }
      openPaymentAndBookingModal({
        vehicleId: pv.id,
        vehicleName: pv.name,
        driver: pv.driver,
        plate: pv.plate,
        pickup: pv.parkedAt,
        pickupCoords: [pv.lat, pv.lng],
        destination: pv.destination,
        fare: pv.fare || 15,
        seat: 'Seat ' + (pv.totalSeats - pv.availableSeats + 1) + ' (Reserved)',
        category: pv.category || 'bus'
      });
    }

    function bookRideFromMainGate() {
      const sel = document.getElementById('mainGateDestSelect');
      const destName = sel ? sel.options[sel.selectedIndex].text : 'Campus Block';
      openPaymentAndBookingModal({
        vehicleId: activeDriverId || 'bus_1',
        vehicleName: 'Express #4 (Blocks 1-36 Core)',
        driver: 'Amit Patel',
        plate: 'PB 08 BX 9410',
        pickup: studentLiveLocation ? `Near ${studentLiveLocation.nearestStop.name} (Live GPS Pin)` : 'Main Gate Transit Shelter (GT Road NH-44)',
        pickupCoords: studentLiveLocation ? [studentLiveLocation.lat, studentLiveLocation.lng] : [31.2485, 75.7015],
        destination: destName,
        fare: 15,
        seat: 'Direct Main Gate Bay',
        category: 'bus'
      });
    }

    function requestPickupAtMySpot() {
      if (!studentLiveLocation) {
        toggleLocationPickerMode(true);
        return;
      }
      const s = studentLiveLocation;
      openPaymentAndBookingModal({
        vehicleId: s.nearestVehicle ? s.nearestVehicle.id : 'bus_1',
        vehicleName: s.nearestVehicle ? s.nearestVehicle.name : 'Eco EV #6',
        driver: s.nearestVehicle ? s.nearestVehicle.driver : 'Rajesh Sharma',
        plate: s.nearestVehicle ? s.nearestVehicle.plate : 'PB 08 BX 9021',
        pickup: `Near ${s.nearestStop.name} (Live Student Pin)`,
        pickupCoords: [s.lat, s.lng],
        destination: 'Academic Blocks 31-36 (CSE & Tech Hub)',
        fare: 15,
        seat: 'Live Spot Boarding',
        category: s.nearestVehicle ? s.nearestVehicle.category : 'ev'
      });
    }
'''

# Replace existing openPaymentAndBookingModal & related functions up to bookSpecificVehicle
old_pay_start = c.find('// Payment & Booking Modal')
old_pay_end = c.find('// Helper: Find vehicle in either Moving FLEET or PARKED_FLEET')

if old_pay_start != -1 and old_pay_end != -1:
    c = c[:old_pay_start] + qr_timer_js + '\n    ' + c[old_pay_end:]
    print("[PASS] Replaced Payment and Booking JS engine with 5-minute timer & universal context")
else:
    print("[WARN] Payment & Booking JS markers not found, attempting alternate match")

# 2. Update renderDriverPassengers in JS with High-Contrast Layout
new_render_passengers_js = '''function renderDriverPassengers() {
      const container = document.getElementById('driverPassengerListContainer');
      if (!container) return;

      const v = getAnyVehicle(activeDriverId);
      const vehiclePos = getCoordOnRoute(v.routeId || 'route_purple', v.s || 0);

      const waitingCount = DRIVER_PASSENGERS.filter(p => p.status === 'waiting').length;
      const boardedCount = DRIVER_PASSENGERS.filter(p => p.status === 'boarded').length;
      const totalFare = DRIVER_PASSENGERS.filter(p => p.status !== 'completed').reduce((sum, p) => sum + p.fare, 0);

      const remainingCount = DRIVER_PASSENGERS.filter(p => p.status !== 'completed').length;
      ['driverPickupCount', 'fsDriverPickupCount'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.textContent = remainingCount;
      });

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
          ? '<span class="px-3 py-1 rounded-full bg-amber-100 text-amber-900 border border-amber-300 font-black text-xs flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-amber-500 animate-ping"></span> WAITING AT STOP</span>'
          : (isBoarded 
            ? '<span class="px-3 py-1 rounded-full bg-emerald-100 text-emerald-900 border border-emerald-300 font-black text-xs flex items-center gap-1.5">🟢 ON BOARD</span>'
            : '<span class="px-3 py-1 rounded-full bg-zinc-200 text-zinc-800 font-black text-xs">✅ DROPPED OFF</span>');

        const payBadge = p.paymentStatus === 'received'
          ? `<span class="px-2.5 py-1 rounded-lg bg-emerald-100 text-emerald-900 border border-emerald-300 font-black text-xs flex items-center gap-1"><span>✅ Paid</span> <span class="text-[11px] font-bold text-zinc-700">(${p.paymentMethod})</span></span>`
          : `<div class="flex items-center gap-2"><span class="px-2.5 py-1 rounded-lg bg-amber-100 text-amber-900 border border-amber-300 font-black text-xs flex items-center gap-1"><span>⏳ Collect Cash (₹${p.fare})</span></span> <button onclick="markPaymentCashReceived('${p.txnId}')" class="px-2.5 py-1 rounded-lg bg-black text-white hover:bg-zinc-800 text-[11px] font-black transition-all">Confirm Received ✓</button></div>`;

        return `
          <div class="p-5 rounded-2xl bg-white border-2 border-zinc-300 hover:border-black shadow-md space-y-4 text-black transition-all">
            <!-- Student Profile Header -->
            <div class="flex flex-wrap items-center justify-between gap-3 border-b border-zinc-200 pb-3">
              <div class="flex items-center gap-3">
                <div class="w-12 h-12 rounded-2xl bg-zinc-100 border border-zinc-300 flex items-center justify-center text-2xl shadow-sm">
                  ${p.avatar || '🧑‍🎓'}
                </div>
                <div>
                  <div class="flex items-center gap-2">
                    <h4 class="text-base font-black text-black">${p.name}</h4>
                    <span class="text-xs font-mono font-black text-black bg-zinc-100 px-2.5 py-0.5 rounded-lg border border-zinc-300">${p.studentId}</span>
                  </div>
                  <p class="text-xs text-zinc-600 font-bold">${p.dept} • ${p.year}</p>
                </div>
              </div>
              <div class="flex items-center gap-2">
                ${statusBadge}
                <a href="tel:${p.phone}" class="px-3 py-1.5 rounded-xl bg-zinc-100 hover:bg-zinc-200 border border-zinc-300 text-black font-black text-xs flex items-center gap-1.5 shadow-sm transition-all" style="color: #000000 !important;" title="Call Student">
                  📞 ${p.phone}
                </a>
              </div>
            </div>

            <!-- Route & Live Pickup Details (Clean Light Boxes) -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
              <div class="p-3.5 rounded-xl bg-zinc-50 border border-zinc-200 space-y-1">
                <div class="flex items-center justify-between">
                  <span class="text-zinc-600 text-[10px] font-black uppercase tracking-wider">📍 Exact Pickup Spot:</span>
                  <span class="text-black font-mono font-black text-xs">${distMeters}m away (~${estDriveMins}m drive)</span>
                </div>
                <strong class="text-black block text-sm font-black">${p.pickup}</strong>
                <p class="text-[11px] text-zinc-500 font-mono font-bold">GPS: ${p.pickupCoords[0].toFixed(5)}, ${p.pickupCoords[1].toFixed(5)}</p>
              </div>

              <div class="p-3.5 rounded-xl bg-zinc-50 border border-zinc-200 space-y-1">
                <div class="flex items-center justify-between">
                  <span class="text-zinc-600 text-[10px] font-black uppercase tracking-wider">🎯 Destination & Seat:</span>
                  <span class="text-black font-mono font-black text-sm">Fare: ₹${p.fare}</span>
                </div>
                <strong class="text-black block text-sm font-black">${p.destination}</strong>
                <p class="text-xs font-bold text-zinc-700">Assigned: <span class="text-black font-mono font-black bg-zinc-200 px-2 py-0.5 rounded">${p.seat}</span></p>
              </div>
            </div>

            <!-- Payment & Security OTP Section (High Contrast Light Panel) -->
            <div class="flex flex-wrap items-center justify-between gap-3 p-3.5 rounded-xl bg-zinc-100 border border-zinc-300 text-xs">
              <div>
                <span class="text-[10px] text-zinc-600 block font-black uppercase tracking-wider mb-1">Payment Status:</span>
                ${payBadge}
              </div>

              <!-- OTP Verification / Boarding Box -->
              ${isWaiting ? `
                <div class="flex items-center gap-2">
                  <div class="flex items-center gap-1.5">
                    <span class="text-xs font-black text-black">Student OTP:</span>
                    <input type="text" id="otp_inp_${p.id}" placeholder="${p.otp}" maxlength="4" class="w-20 px-2.5 py-1.5 text-center font-mono font-black text-xs rounded-xl bg-white border-2 border-zinc-300 text-black focus:outline-none focus:border-black">
                  </div>
                  <button onclick="verifyPassengerOtp('${p.id}')" class="px-4 py-2 rounded-xl bg-black text-white hover:bg-zinc-800 font-black text-xs flex items-center gap-1 shadow-md transition-all">
                    ✅ Verify & Board
                  </button>
                </div>
              ` : (isBoarded ? `
                <div class="flex items-center gap-2">
                  <span class="text-xs font-black text-emerald-900 bg-emerald-100 px-2.5 py-1 rounded-lg border border-emerald-300 font-mono">OTP ${p.otp} Verified</span>
                  <button onclick="completePassengerDrop('${p.id}')" class="px-4 py-2 rounded-xl bg-black text-white hover:bg-zinc-800 font-black text-xs flex items-center gap-1 shadow-md transition-all">
                    🏁 Mark Dropped Off
                  </button>
                </div>
              ` : `
                <span class="text-xs text-zinc-700 font-mono font-black">Trip Successfully Completed ✓</span>
              `)}
            </div>

            <!-- Driver Action Buttons -->
            <div class="flex items-center justify-between pt-1 border-t border-zinc-200 text-xs">
              <div class="flex items-center gap-2">
                <button onclick="locatePassengerOnMap(${p.pickupCoords[0]}, ${p.pickupCoords[1]}, '${p.name}')" class="px-3 py-1.5 rounded-xl bg-zinc-100 hover:bg-zinc-200 text-black font-black flex items-center gap-1.5 border border-zinc-300 shadow-sm transition-all" style="color: #000000 !important;">
                  🗺️ Locate on Campus Map
                </button>
                <button onclick="setDriverTab('chats')" class="px-3 py-1.5 rounded-xl bg-zinc-100 hover:bg-zinc-200 text-black font-black flex items-center gap-1.5 border border-zinc-300 shadow-sm transition-all" style="color: #000000 !important;">
                  💬 Open Chat
                </button>
              </div>

              <button onclick="viewPaymentReceipt('${p.txnId}')" class="text-zinc-600 hover:text-black font-mono text-[11px] font-bold underline">
                🧾 View Receipt (${p.txnId})
              </button>
            </div>
          </div>
        `;
      }).join('');
    }'''

passengers_js_start = c.find('function renderDriverPassengers()')
passengers_js_end = c.find('function verifyPassengerOtp', passengers_js_start)

if passengers_js_start != -1 and passengers_js_end != -1:
    c = c[:passengers_js_start] + new_render_passengers_js + '\n\n    ' + c[passengers_js_end:]
    print("[PASS] Replaced renderDriverPassengers function with high contrast theme")
else:
    print("[FAIL] Could not find boundaries for renderDriverPassengers function!")

# 3. Update renderDriverPayments with High Contrast Table
new_render_payments_js = '''function renderDriverPayments() {
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
          <tr class="hover:bg-zinc-100 transition-colors">
            <td class="p-3.5">
              <div class="flex items-center gap-2.5">
                <span class="text-lg">${p.avatar || '🧑‍🎓'}</span>
                <div>
                  <strong class="text-black font-black block">${p.name}</strong>
                  <span class="text-xs text-zinc-600 font-mono font-bold">${p.studentId}</span>
                </div>
              </div>
            </td>
            <td class="p-3.5">
              <div class="space-y-0.5">
                <span class="text-black font-bold block truncate max-w-[170px]">📍 ${p.pickup}</span>
                <span class="text-zinc-600 text-[11px] block truncate max-w-[170px]">➔ ${p.destination}</span>
              </div>
            </td>
            <td class="p-3.5 font-mono text-black font-black text-sm">
              ₹${p.fare.toFixed(2)}
            </td>
            <td class="p-3.5">
              <span class="text-xs text-black font-bold">${p.paymentMethod}</span>
            </td>
            <td class="p-3.5">
              <span class="px-2.5 py-0.5 rounded-full font-mono font-black text-[10px] ${isReceived ? 'bg-emerald-100 text-emerald-900 border border-emerald-300' : 'bg-amber-100 text-amber-900 border border-amber-300'}">
                ${isReceived ? '● RECEIVED' : '● PENDING CASH'}
              </span>
            </td>
            <td class="p-3.5 text-right">
              <button onclick="viewPaymentReceipt('${p.txnId}')" class="px-2.5 py-1 rounded-lg bg-zinc-100 hover:bg-zinc-200 text-black border border-zinc-300 text-xs font-black shadow-sm">
                🧾 Receipt
              </button>
            </td>
          </tr>
        `;
      }).join('');
    }'''

payments_js_start = c.find('function renderDriverPayments()')
payments_js_end = c.find('function markPaymentCashReceived', payments_js_start)

if payments_js_start != -1 and payments_js_end != -1:
    c = c[:payments_js_start] + new_render_payments_js + '\n\n    ' + c[payments_js_end:]
    print("[PASS] Replaced renderDriverPayments function with high contrast table")
else:
    print("[FAIL] Could not find boundaries for renderDriverPayments function!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("System update applied to index.html successfully.")

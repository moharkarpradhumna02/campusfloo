import re

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# ================= 1. REWRITE PAYMENT & BOOKING MODAL =================
modal_start_idx = c.find('<!-- ================= MODAL 2: CASH / UPI PAYMENT & BOOKING ================= -->')
if modal_start_idx == -1:
    modal_start_idx = c.find('id="paymentBookingModal"')
    modal_start_idx = c.rfind('<div', 0, modal_start_idx)

seat_modal_idx = c.find('<!-- ================= SEAT LAYOUT & RESERVATION MODAL ================= -->')

new_payment_modal_html = '''<!-- ================= MODAL 2: CASH / UPI PAYMENT & BOOKING ================= -->
  <div id="paymentBookingModal" class="fixed inset-0 z-[1000] bg-black/80 backdrop-blur-md hidden place-items-center p-4">
    <div class="bg-white w-full max-w-xl rounded-3xl border-2 border-zinc-300 overflow-hidden shadow-2xl animate-pop-in flex flex-col max-h-[92vh] text-black">
      
      <!-- Modal Header -->
      <div class="p-5 border-b border-zinc-200 flex items-center justify-between bg-zinc-50 shrink-0">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-2xl bg-black text-white flex items-center justify-center text-xl shadow-md">
            💳
          </div>
          <div>
            <h3 class="text-base font-black text-[#DC2626]">Campus Ride Payment & Boarding Pass</h3>
            <p class="text-xs text-zinc-600 font-semibold">UPI Dynamic QR, Campus Smart Pass, or Cash to Driver</p>
          </div>
        </div>
        <button onclick="closeModal('paymentBookingModal')" class="p-2 rounded-xl text-zinc-500 hover:text-black hover:bg-zinc-200 transition-all">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <!-- Live Trip Booking Summary Card -->
      <div class="p-4 mx-6 mt-4 rounded-2xl bg-zinc-100 border border-zinc-300 space-y-2">
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-2">
            <span class="text-xl" id="paySummaryIcon">🚌</span>
            <div>
              <h4 class="text-xs font-black text-black" id="paySummaryVehicle">Shuttle #1 (Ring Loop)</h4>
              <p class="text-[11px] text-zinc-600 font-bold" id="paySummaryRoute">Main Gate ➔ Central Library</p>
            </div>
          </div>
          <div class="text-right">
            <span class="text-sm font-black text-black font-mono" id="paySummaryFare">₹15.00</span>
            <span class="text-[10px] text-zinc-500 font-bold block" id="paySummarySeat">Seat: 2A</span>
          </div>
        </div>
      </div>

      <!-- Scrollable Body -->
      <div class="p-6 overflow-y-auto space-y-5 flex-1 custom-scrollbar">
        
        <!-- Coupon Code Box -->
        <div class="p-3.5 rounded-2xl bg-zinc-50 border border-zinc-300 space-y-2.5">
          <div class="flex items-center justify-between">
            <span class="text-xs font-black uppercase text-black flex items-center gap-1.5">
              🏷️ Promo Coupon
            </span>
            <span class="text-[11px] text-zinc-500 font-bold">Use <strong class="text-black">CAMPUS10</strong> for 10% off</span>
          </div>
          <div class="flex gap-2">
            <input type="text" id="couponCodeInput" placeholder="Enter coupon (e.g. CAMPUS10)" value="CAMPUS10" class="flex-1 px-3 py-2 rounded-xl bg-white border border-zinc-300 text-xs font-mono font-black uppercase text-black focus:border-black focus:outline-none">
            <button onclick="applyCouponCode()" class="px-4 py-2 rounded-xl bg-black hover:bg-zinc-800 text-white font-black text-xs shadow-sm transition-all">
              Apply
            </button>
          </div>
          <div class="flex items-center gap-2 pt-0.5">
            <button onclick="quickApplyCoupon('CAMPUS10')" class="px-2.5 py-1 rounded-lg bg-zinc-200 hover:bg-zinc-300 text-[10px] font-mono font-bold text-black border border-zinc-300">
              🏷️ CAMPUS10 (10% Off)
            </button>
            <button onclick="quickApplyCoupon('FREEFIRST')" class="px-2.5 py-1 rounded-lg bg-zinc-200 hover:bg-zinc-300 text-[10px] font-mono font-bold text-black border border-zinc-300">
              🎁 FREEFIRST (100% Free)
            </button>
          </div>
        </div>

        <!-- Payment Method Tabs: UPI QR / Wallet / Cash -->
        <div class="space-y-3">
          <label class="block text-xs font-black uppercase tracking-wider text-black">
            Choose Payment Method:
          </label>
          <div class="grid grid-cols-3 gap-1.5 p-1.5 rounded-2xl bg-zinc-100 border border-zinc-300 text-xs font-black">
            <button id="payTabUpi" onclick="switchPayTab('upi')" class="pay-method-tab py-2.5 rounded-xl bg-black text-white shadow-sm flex items-center justify-center gap-1 transition-all">
              📱 Dynamic QR (5m)
            </button>
            <button id="payTabWallet" onclick="switchPayTab('wallet')" class="pay-method-tab py-2.5 rounded-xl text-zinc-700 hover:text-black font-extrabold flex items-center justify-center gap-1 transition-all">
              💳 Smart Pass
            </button>
            <button id="payTabCash" onclick="switchPayTab('cash')" class="pay-method-tab py-2.5 rounded-xl text-zinc-700 hover:text-black font-extrabold flex items-center justify-center gap-1 transition-all">
              💵 Cash on Board
            </button>
          </div>

          <!-- Tab Content: UPI Dynamic QR Code (5-Minute Live Timer) -->
          <div id="payContentUpi" class="space-y-4 pt-1">
            <div class="p-5 rounded-3xl border-2 border-zinc-300 flex flex-col items-center justify-center text-center space-y-3.5 bg-zinc-50 relative overflow-hidden">
              
              <!-- 5-Minute Countdown Header -->
              <div class="w-full space-y-1.5">
                <div class="flex items-center justify-between text-xs font-bold text-zinc-700">
                  <span class="flex items-center gap-1.5 text-black font-black">
                    <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-ping"></span>
                    Live 5-Minute UPI Session
                  </span>
                  <span id="upiCountdownText" class="font-mono font-black text-black bg-zinc-200 px-2 py-0.5 rounded-lg border border-zinc-300">
                    ⏱️ 05:00
                  </span>
                </div>
                <!-- Countdown Progress Bar -->
                <div class="w-full h-1.5 rounded-full bg-zinc-200 overflow-hidden">
                  <div id="upiTimerProgressBar" class="h-full bg-black rounded-full transition-all duration-1000" style="width: 100%;"></div>
                </div>
              </div>

              <!-- QR Code Canvas / Container -->
              <div class="relative w-52 h-52 bg-white p-3 rounded-2xl border-2 border-black shadow-xl flex items-center justify-center">
                <img id="upiQrImage" src="https://api.qrserver.com/v1/create-qr-code/?size=220x220&data=upi://pay?pa=campusflow@okaxis%26pn=LPU%20Campus%20Transit%26am=15%26cu=INR" alt="UPI QR Code" class="w-full h-full object-contain rounded-xl">
                
                <!-- Expired Overlay -->
                <div id="upiQrExpiredOverlay" class="hidden absolute inset-0 bg-white/95 backdrop-blur-sm rounded-2xl flex flex-col items-center justify-center p-3 text-center space-y-2">
                  <span class="text-3xl">⏱️</span>
                  <p class="text-xs font-black text-red-600">QR Code Expired</p>
                  <p class="text-[10px] text-zinc-600 font-bold">5-minute payment window elapsed</p>
                  <button onclick="refreshUpiQrCode()" class="px-3 py-1.5 rounded-xl bg-black text-white font-black text-xs hover:bg-zinc-800 shadow-md">
                    🔄 Refresh New QR
                  </button>
                </div>
              </div>

              <!-- Supported UPI Apps & Instructions -->
              <div class="space-y-1">
                <p class="text-xs font-black text-black">
                  Scan with Google Pay, PhonePe, Paytm, or BHIM
                </p>
                <p class="text-[11px] font-mono font-bold text-zinc-600">UPI ID: <span class="text-black font-black">campusflow@okaxis</span></p>
              </div>

              <div class="flex items-center gap-2 pt-1">
                <button onclick="copyUpiId()" class="px-3 py-1.5 rounded-xl bg-white hover:bg-zinc-200 border border-zinc-300 text-xs font-black text-black shadow-sm flex items-center gap-1.5">
                  <i data-lucide="copy" class="w-3.5 h-3.5"></i> Copy UPI ID
                </button>
                <button onclick="refreshUpiQrCode()" class="px-3 py-1.5 rounded-xl bg-white hover:bg-zinc-200 border border-zinc-300 text-xs font-black text-black shadow-sm flex items-center gap-1.5" title="Generate New 5-Minute Timer">
                  🔄 Refresh Timer
                </button>
              </div>

            </div>
          </div>

          <!-- Tab Content: Campus Smart Pass / Wallet -->
          <div id="payContentWallet" class="hidden space-y-4 pt-1">
            <div class="p-5 rounded-3xl border-2 border-zinc-300 space-y-4 bg-zinc-50">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-xs text-zinc-600 font-bold uppercase">Available Pass Balance</p>
                  <p class="text-2xl font-black text-black font-mono" id="modalWalletBalance">₹ 240.00</p>
                  <p class="text-[10px] text-zinc-500 font-mono font-bold">STU-2024-8891 • Active Pass</p>
                </div>
                <button onclick="openWalletModal()" class="px-3 py-1.5 rounded-xl bg-white hover:bg-zinc-200 border border-zinc-300 text-xs font-black text-black shadow-sm">
                  + Add Money
                </button>
              </div>

              <div id="walletPayStatusBox" class="p-3 rounded-xl bg-zinc-100 border border-zinc-300 text-xs font-bold text-black flex items-center gap-2">
                <span class="text-base">⚡</span>
                <span id="walletPayStatusText">1-Tap Auto-Debit: Fare will be deducted from your Campus Pass instantly.</span>
              </div>
            </div>
          </div>

          <!-- Tab Content: Cash on Boarding -->
          <div id="payContentCash" class="hidden space-y-4 pt-1">
            <div class="p-5 rounded-3xl border-2 border-zinc-300 space-y-3 bg-zinc-50 text-left">
              <div class="flex items-center gap-2.5">
                <span class="text-2xl">💵</span>
                <div>
                  <h4 class="text-xs font-black text-black">Pay Cash to Driver upon Boarding</h4>
                  <p class="text-[11px] text-zinc-600 font-semibold">Zero upfront digital deduction required</p>
                </div>
              </div>
              <p class="text-xs text-zinc-700 leading-relaxed font-semibold">
                Your seat and ride pass will be reserved instantly with a verified 4-digit OTP. Simply hand the exact fare in cash to your vehicle driver when boarding. The driver will confirm receipt on their cockpit screen.
              </p>
              <div class="p-2.5 rounded-xl bg-amber-50 border border-amber-300 text-amber-900 text-xs font-bold flex items-center gap-2">
                <span>⚠️</span>
                <span>Driver will verify your OTP and mark fare collected on entering.</span>
              </div>
            </div>
          </div>

        </div>

        <!-- Net Price Calculation Summary -->
        <div class="p-4 rounded-2xl bg-zinc-100 border border-zinc-300 space-y-1.5 text-xs font-bold">
          <div class="flex items-center justify-between text-zinc-600">
            <span>Base Ride Fare:</span>
            <span id="priceSummaryBase" class="font-mono font-bold text-black">₹15.00</span>
          </div>
          <div class="flex items-center justify-between text-zinc-600">
            <span>Coupon Discount (<span id="priceSummaryDiscountLabel">0%</span>):</span>
            <span id="priceSummaryDiscount" class="font-mono font-bold text-emerald-600">-₹0.00</span>
          </div>
          <div class="flex items-center justify-between pt-1 border-t border-zinc-300 text-black text-sm font-black">
            <span>Net Payable Fare:</span>
            <span id="priceSummaryTotal" class="font-mono text-base font-black text-black">₹15.00</span>
          </div>
        </div>

        <!-- Confirm Booking Button -->
        <button onclick="confirmPaymentAndBookTrip()" id="confirmPayBtn" class="w-full py-4 rounded-2xl bg-black hover:bg-zinc-800 text-white font-black text-sm flex items-center justify-center gap-2 shadow-xl transition-all">
          <span>Confirm Payment & Generate Driver OTP</span>
          <i data-lucide="shield-check" class="w-4 h-4"></i>
        </button>

      </div>

    </div>
  </div>\n\n  '''

if modal_start_idx != -1 and seat_modal_idx != -1:
    c = c[:modal_start_idx] + new_payment_modal_html + c[seat_modal_idx:]
    print("[PASS] Replaced Payment & Booking Modal HTML with 5-minute dynamic QR code & all payment modes")
else:
    print("[FAIL] Could not locate boundaries for Payment Modal!")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Modal replacement step completed.")

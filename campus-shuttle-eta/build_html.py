import os

with open('qr_base64.txt') as f:
    qr_b64 = f.read().strip()

html_content = f'''<!DOCTYPE html>
<html lang="en" class="dark scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Campus Flow — Smart Shuttle, Smart Campus (Real-Time Predictive ETA)</title>

  <!-- Tailwind CSS & Lucide Icons -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {{
      darkMode: 'class',
      theme: {{
        extend: {{
          fontFamily: {{
            sans: ['"Plus Jakarta Sans"', 'system-ui', '-apple-system', 'sans-serif'],
            mono: ['ui-monospace', 'Menlo', 'Consolas', 'monospace']
          }},
          colors: {{
            brand: {{
              cyan: '#00f0ff',
              violet: '#a855f7',
              purple: '#6366f1',
              emerald: '#10b981',
              amber: '#f59e0b'
            }}
          }},
          keyframes: {{
            glowPulse: {{
              '0%, 100%': {{ opacity: '0.4', transform: 'scale(1)' }},
              '50%': {{ opacity: '0.8', transform: 'scale(1.06)' }}
            }},
            float3D: {{
              '0%, 100%': {{ transform: 'translateY(0px)' }},
              '50%': {{ transform: 'translateY(-6px)' }}
            }}
          }},
          animation: {{
            'glow-pulse': 'glowPulse 4s ease-in-out infinite',
            'float-3d': 'float3D 3.5s ease-in-out infinite'
          }}
        }}
      }}
    }}
  </script>

  <!-- Google Fonts, Leaflet & Lucide -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <script src="https://unpkg.com/lucide@latest"></script>

  <style>
    :root {{
      --bg-dark: #070913;
      --card-glass: rgba(13, 17, 34, 0.82);
      --border-glass: rgba(255, 255, 255, 0.14);
      --cyan-glow: rgba(0, 240, 255, 0.35);
    }}

    body {{
      background-color: var(--bg-dark);
      color: #f1f5f9;
      font-family: 'Plus Jakarta Sans', system-ui, sans-serif;
      overflow-x: hidden;
    }}

    .glass-card {{
      background: var(--card-glass);
      backdrop-filter: blur(24px);
      -webkit-backdrop-filter: blur(24px);
      border: 1px solid var(--border-glass);
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }}

    .glass-card-glow {{
      box-shadow: 0 0 50px rgba(0, 240, 255, 0.22), 0 20px 60px rgba(0, 0, 0, 0.7), inset 0 1px 0 rgba(255, 255, 255, 0.25);
    }}

    .btn-gradient {{
      position: relative;
      overflow: hidden;
      background: linear-gradient(135deg, #00f0ff 0%, #6366f1 50%, #a855f7 100%);
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      box-shadow: 0 10px 30px -5px rgba(99, 102, 241, 0.5);
    }}
    .btn-gradient:hover {{
      box-shadow: 0 14px 40px -4px rgba(0, 240, 255, 0.6);
      transform: translateY(-2px);
    }}
    .btn-gradient:active {{
      transform: scale(0.97);
    }}
    .btn-gradient::after {{
      content: '';
      position: absolute;
      top: -50%;
      left: -60%;
      width: 40%;
      height: 200%;
      background: linear-gradient(to right, transparent, rgba(255, 255, 255, 0.4), transparent);
      transform: rotate(30deg);
      transition: transform 0.75s ease;
      pointer-events: none;
    }}
    .btn-gradient:hover::after {{
      transform: translateX(450%) rotate(30deg);
    }}

    .ripple {{
      position: absolute;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.45);
      transform: scale(0);
      animation: ripple-anim 0.6s linear;
      pointer-events: none;
    }}
    @keyframes ripple-anim {{
      to {{ transform: scale(4); opacity: 0; }}
    }}

    .click-spark {{
      position: fixed;
      pointer-events: none;
      z-index: 999999;
      width: 14px;
      height: 14px;
      border-radius: 50%;
      background: radial-gradient(circle, #00f0ff 0%, rgba(168,85,247,0.8) 50%, transparent 80%);
      transform: scale(0);
      animation: sparkAnim 0.5s ease-out forwards;
    }}
    @keyframes sparkAnim {{
      0% {{ transform: scale(0.2); opacity: 1; }}
      100% {{ transform: scale(3.2); opacity: 0; }}
    }}

    .transit-marker {{
      width: 44px;
      height: 44px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 20px;
      border: 3px solid #ffffff;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6), 0 0 15px currentColor;
      transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      cursor: pointer;
      position: relative;
    }}
    .transit-marker:hover {{
      transform: scale(1.22);
    }}
    .transit-marker .pulse-ring {{
      position: absolute;
      inset: -6px;
      border-radius: 50%;
      border: 2px solid currentColor;
      animation: markerPulse 2s cubic-bezier(0.24, 0, 0.38, 1) infinite;
    }}
    @keyframes markerPulse {{
      0% {{ transform: scale(0.8); opacity: 1; }}
      100% {{ transform: scale(2.0); opacity: 0; }}
    }}
    .transit-marker .heading-needle {{
      position: absolute;
      top: -9px;
      left: 50%;
      margin-left: -5px;
      width: 0;
      height: 0;
      border-left: 5px solid transparent;
      border-right: 5px solid transparent;
      border-bottom: 9px solid #00f0ff;
      transform-origin: 5px 27px;
    }}

    .stop-badge-pill {{
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 4px 10px;
      border-radius: 9999px;
      background: rgba(15, 23, 42, 0.94);
      color: #ffffff;
      font-weight: 800;
      font-size: 11px;
      border: 1px solid rgba(0, 240, 255, 0.4);
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5), 0 0 10px rgba(0, 240, 255, 0.2);
      transform: translate(-50%, -140%);
      white-space: nowrap;
    }}
    .stop-badge-pill.on-time {{
      border-color: #10b981;
      color: #34d399;
    }}
    .stop-badge-pill.late {{
      border-color: #f59e0b;
      color: #fbbf24;
    }}

    .flow-line {{
      stroke-dasharray: 12, 16;
      animation: dashFlow 1.2s linear infinite;
    }}
    @keyframes dashFlow {{
      to {{ stroke-dashoffset: -28; }}
    }}

    /* Background video styles */
    .bg-video-container {{
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      overflow: hidden;
      z-index: 1;
    }}
    .bg-video {{
      width: 100%;
      height: 100%;
      object-fit: cover;
      object-position: center;
      filter: brightness(0.95) contrast(1.1);
      transform: scale(1.02);
      transition: opacity 0.8s ease;
    }}
  </style>
</head>
<body class="min-h-screen flex flex-col antialiased selection:bg-brand-cyan selection:text-black">

  <!-- ================= TOP NAVIGATION BAR ================= -->
  <header class="sticky top-0 z-50 bg-[#070913]/90 backdrop-blur-xl border-b border-white/10 transition-colors">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-18 py-3.5 flex items-center justify-between gap-4">
      
      <!-- Brand Logo -->
      <a href="#" onclick="showLandingPage()" class="flex items-center gap-3 font-extrabold text-xl tracking-tight text-white group">
        <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-brand-cyan via-brand-purple to-brand-violet flex items-center justify-center text-white shadow-lg shadow-brand-cyan/20 group-hover:scale-105 transition-transform">
          <i data-lucide="navigation-2" class="w-5 h-5 text-black fill-black"></i>
        </div>
        <div>
          <span class="text-white text-lg font-black tracking-tight flex items-center gap-1.5">
            Campus Flow
            <span class="w-2 h-2 rounded-full bg-brand-cyan animate-ping"></span>
          </span>
          <span class="block text-[10px] text-zinc-400 font-medium tracking-normal -mt-0.5">Smart Shuttle. Smart Campus.</span>
        </div>
      </a>

      <!-- Center Links -->
      <nav class="hidden md:flex items-center gap-1 text-sm font-semibold text-zinc-300">
        <button onclick="showLandingPage()" class="px-3.5 py-1.5 rounded-xl hover:text-white hover:bg-white/5 transition-colors">Home</button>
        <button onclick="openPaymentAndBookingModal()" class="px-3.5 py-1.5 rounded-xl text-brand-cyan hover:bg-brand-cyan/10 transition-colors flex items-center gap-1.5">
          <i data-lucide="credit-card" class="w-4 h-4"></i> Pay / Buy Pass
        </button>
        <button onclick="launchTransportDashboard()" class="px-3.5 py-1.5 rounded-xl text-brand-purple hover:bg-brand-purple/10 transition-colors flex items-center gap-1.5">
          <i data-lucide="map" class="w-4 h-4"></i> Live Map
        </button>
        <button onclick="openFarePassesModal()" class="px-3.5 py-1.5 rounded-xl hover:text-white hover:bg-white/5 transition-colors">Fares</button>
      </nav>

      <!-- Right Actions -->
      <div class="flex items-center gap-3">
        <!-- Background Video Toggle -->
        <button id="btnToggleBgVideo" onclick="toggleHeroBgVideo()" class="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 text-[11px] font-bold text-zinc-300">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span id="btnToggleBgVideoText">🎥 3D Video Active</span>
        </button>

        <button onclick="openPaymentAndBookingModal()" class="hidden sm:inline-flex items-center gap-2 px-3.5 py-2 rounded-xl bg-white/10 hover:bg-white/15 border border-white/10 text-xs font-bold text-white transition-all">
          <span class="text-brand-cyan">💳</span>
          <span>Cash / UPI Pay</span>
        </button>

        <button id="userAccountPill" onclick="showLandingPage()" class="px-4 py-2 rounded-xl bg-gradient-to-r from-brand-cyan to-brand-purple text-black font-extrabold text-xs tracking-wide shadow-lg shadow-brand-cyan/30 hover:opacity-95 transition-all">
          Sign Up / Login
        </button>
      </div>

    </div>
  </header>

  <!-- ================= NOTIFICATION TOAST ================= -->
  <div id="toast" class="fixed bottom-6 right-6 z-[9999] max-w-md bg-zinc-900/95 text-white px-4 py-3 rounded-2xl shadow-2xl flex items-center gap-3 text-xs font-semibold translate-y-24 opacity-0 pointer-events-none transition-all duration-300 backdrop-blur-xl border border-brand-cyan/40">
    <div id="toastIcon" class="w-6 h-6 rounded-full bg-brand-cyan text-black flex items-center justify-center shrink-0">
      <i data-lucide="check" class="w-4 h-4"></i>
    </div>
    <span id="toastMsg" class="flex-1">Notification</span>
    <button onclick="hideToast()" class="text-zinc-400 hover:text-white ml-2">
      <i data-lucide="x" class="w-4 h-4"></i>
    </button>
  </div>

  <!-- ================= LANDING PAGE & SIGN UP WITH LIVE 3D VIDEO BACKGROUND ================= -->
  <section id="landingHeroSection" class="relative min-h-[calc(100vh-72px)] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 overflow-hidden">
    
    <!-- Video Background Container (Plays gemini_generated_video_67b851a0.mp4) -->
    <div class="bg-video-container pointer-events-none">
      <video id="heroBgVideo" autoplay loop muted playsinline class="bg-video">
        <source src="campus-flow-bg.mp4" type="video/mp4">
      </video>
      <!-- Gradient Overlays for perfect legibility -->
      <div class="absolute inset-0 bg-gradient-to-r from-[#070913]/95 via-[#070913]/75 to-[#070913]/40"></div>
      <div class="absolute inset-0 bg-gradient-to-t from-[#070913] via-transparent to-[#070913]/80"></div>
      <div class="absolute inset-0 bg-brand-cyan/5 mix-blend-screen"></div>
    </div>

    
    

    <div class="max-w-7xl w-full mx-auto grid grid-cols-1 lg:grid-cols-12 gap-10 items-center relative z-10">
      
      <!-- LEFT HERO: Campus Flow Introduction & Floating Transit Badges -->
      <div class="lg:col-span-7 space-y-6">
        
        <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-brand-cyan/10 border border-brand-cyan/30 text-brand-cyan text-xs font-bold tracking-wide backdrop-blur-md">
          <span class="w-2 h-2 rounded-full bg-brand-cyan animate-pulse"></span>
          Campus Transit: Buses 🚌 · Auto Rickshaws 🛺 · Eco EVs ⚡
        </div>

        <h1 class="text-4xl sm:text-6xl xl:text-7xl font-black tracking-tight text-white leading-[1.06] drop-shadow-xl">
          Next Stop: <br>
          <span class="text-transparent bg-clip-text bg-gradient-to-r from-brand-cyan via-indigo-400 to-brand-violet">
            Your Campus.
          </span>
        </h1>

        <p class="text-xl sm:text-2xl font-extrabold text-zinc-200 tracking-tight drop-shadow-md">
          Track. Plan. Arrive On Time.
        </p>

        <p class="text-sm sm:text-base text-zinc-300 max-w-xl leading-relaxed drop-shadow">
          Real-time shuttle tracking with AI-powered ETA, even when GPS goes silent. Multi-modal campus transport with Indian drivers, live UPI QR payment & verified driver OTP security.
        </p>

        <!-- Feature Badges -->
        <div class="flex flex-wrap items-center gap-3 pt-2">
          <div class="flex items-center gap-2 px-3.5 py-2 rounded-2xl bg-black/40 backdrop-blur-md border border-white/10 text-xs font-bold text-zinc-200 shadow-sm">
            <div class="w-6 h-6 rounded-lg bg-brand-cyan/20 text-brand-cyan flex items-center justify-center">
              <i data-lucide="target" class="w-3.5 h-3.5"></i>
            </div>
            Smart Route Matching
          </div>

          <div class="flex items-center gap-2 px-3.5 py-2 rounded-2xl bg-black/40 backdrop-blur-md border border-white/10 text-xs font-bold text-zinc-200 shadow-sm">
            <div class="w-6 h-6 rounded-lg bg-amber-400/20 text-amber-400 flex items-center justify-center">
              <i data-lucide="clock" class="w-3.5 h-3.5"></i>
            </div>
            Accurate ETA (±2 min)
          </div>

          <div class="flex items-center gap-2 px-3.5 py-2 rounded-2xl bg-black/40 backdrop-blur-md border border-white/10 text-xs font-bold text-zinc-200 shadow-sm">
            <div class="w-6 h-6 rounded-lg bg-emerald-400/20 text-emerald-400 flex items-center justify-center">
              <i data-lucide="bell-ring" class="w-3.5 h-3.5"></i>
            </div>
            Delay Alerts
          </div>
        </div>

        <!-- Floating Live Badges matching user image -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-3">
          <div class="p-3 rounded-2xl bg-black/40 backdrop-blur-md border border-white/15 flex items-center gap-3 glass-card hover:border-brand-cyan/50 transition-all">
            <span class="text-2xl">🚌</span>
            <div>
              <p class="text-xs font-bold text-white">Shuttle #1</p>
              <p class="text-[11px] font-extrabold text-brand-cyan">ETA: 4 min</p>
            </div>
          </div>

          <div class="p-3 rounded-2xl bg-black/40 backdrop-blur-md border border-white/15 flex items-center gap-3 glass-card hover:border-brand-cyan/50 transition-all">
            <span class="text-2xl">🛺</span>
            <div>
              <p class="text-xs font-bold text-white">Auto #2</p>
              <p class="text-[11px] font-extrabold text-amber-400">ETA: 2 min</p>
            </div>
          </div>

          <div class="p-3 rounded-2xl bg-black/40 backdrop-blur-md border border-white/15 flex items-center gap-3 glass-card hover:border-brand-cyan/50 transition-all">
            <span class="text-2xl">⚡</span>
            <div>
              <p class="text-xs font-bold text-white">EV Cart #3</p>
              <p class="text-[11px] font-extrabold text-emerald-400">ETA: 5 min</p>
            </div>
          </div>

          <div class="p-3 rounded-2xl bg-black/40 backdrop-blur-md border border-white/15 flex items-center gap-3 glass-card hover:border-brand-cyan/50 transition-all">
            <span class="text-2xl">🚌</span>
            <div>
              <p class="text-xs font-bold text-white">Express #4</p>
              <p class="text-[11px] font-extrabold text-brand-violet">ETA: 3 min</p>
            </div>
          </div>
        </div>

        <!-- Quick Payment & Ride Booking Callout -->
        <div class="p-4 rounded-3xl bg-black/60 backdrop-blur-xl border border-brand-cyan/40 flex items-center justify-between gap-4 max-w-xl shadow-2xl">
          <div class="space-y-0.5">
            <span class="text-xs font-extrabold text-brand-cyan flex items-center gap-1.5">
              <span>🎁</span> First Ride 100% Free · Coupon: CAMPUS10 for 10% Off
            </span>
            <p class="text-[11px] text-zinc-300">Pay via Google Pay UPI QR or Cash on Board with OTP</p>
          </div>
          <button onclick="openPaymentAndBookingModal()" class="px-4 py-2.5 rounded-xl bg-brand-cyan text-black font-black text-xs shrink-0 shadow-lg hover:scale-105 transition-all">
            Book / Pay Now
          </button>
        </div>

      </div>

      <!-- RIGHT HERO: CREATE ACCOUNT CARD (FLOATING ON FRONT OF THE LIVE VIDEO) -->
      <div class="lg:col-span-5 relative">
        <div class="absolute -inset-1 bg-gradient-to-r from-brand-cyan to-brand-violet rounded-3xl blur-2xl opacity-40 group-hover:opacity-70 transition duration-1000 animate-glow-pulse"></div>

        <div class="relative glass-card glass-card-glow rounded-3xl p-7 sm:p-8 border border-white/25 text-white space-y-4">
          
          <div class="text-center space-y-1 pb-1">
            <div class="inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-brand-cyan/20 border border-brand-cyan/40 text-brand-cyan mb-2 shadow-inner">
              <i data-lucide="navigation-2" class="w-6 h-6 fill-brand-cyan"></i>
            </div>
            <h3 class="text-xl font-black text-white tracking-tight">Campus Flow</h3>
            <p class="text-xs text-brand-cyan font-semibold">Your Campus Shuttle Companion</p>
            <h4 class="text-2xl font-black text-white pt-2">Create Account</h4>
            <p class="text-xs text-zinc-400">Join thousands of students riding smarter!</p>
          </div>

          <!-- Sign Up Form -->
          <form id="heroSignUpForm" onsubmit="event.preventDefault(); handleUserSignUp();" class="space-y-3 pt-2">
            
            <div class="relative">
              <i data-lucide="user" class="w-4 h-4 text-zinc-400 absolute left-3.5 top-1/2 -translate-y-1/2"></i>
              <input type="text" id="suFullName" required placeholder="Full Name (e.g. Aarav Sharma)" class="w-full pl-10 pr-4 py-3 bg-black/40 border border-white/15 rounded-2xl text-xs font-semibold text-white placeholder-zinc-500 focus:outline-none focus:border-brand-cyan focus:ring-1 focus:ring-brand-cyan transition-all">
            </div>

            <div class="relative">
              <i data-lucide="mail" class="w-4 h-4 text-zinc-400 absolute left-3.5 top-1/2 -translate-y-1/2"></i>
              <input type="email" id="suEmail" required placeholder="University Email (e.g. student@campus.edu)" class="w-full pl-10 pr-4 py-3 bg-black/40 border border-white/15 rounded-2xl text-xs font-semibold text-white placeholder-zinc-500 focus:outline-none focus:border-brand-cyan focus:ring-1 focus:ring-brand-cyan transition-all">
            </div>

            <div class="relative">
              <i data-lucide="id-card" class="w-4 h-4 text-zinc-400 absolute left-3.5 top-1/2 -translate-y-1/2"></i>
              <input type="text" id="suStudentId" required placeholder="Student ID / Roll No. (e.g. 23BCE1042)" class="w-full pl-10 pr-4 py-3 bg-black/40 border border-white/15 rounded-2xl text-xs font-semibold text-white placeholder-zinc-500 focus:outline-none focus:border-brand-cyan focus:ring-1 focus:ring-brand-cyan transition-all">
            </div>

            <div class="relative">
              <i data-lucide="lock" class="w-4 h-4 text-zinc-400 absolute left-3.5 top-1/2 -translate-y-1/2"></i>
              <input type="password" id="suPassword" required placeholder="Password" class="w-full pl-10 pr-10 py-3 bg-black/40 border border-white/15 rounded-2xl text-xs font-semibold text-white placeholder-zinc-500 focus:outline-none focus:border-brand-cyan focus:ring-1 focus:ring-brand-cyan transition-all">
              <button type="button" onclick="togglePasswordVisibility('suPassword')" class="absolute right-3.5 top-1/2 -translate-y-1/2 text-zinc-400 hover:text-white">
                <i data-lucide="eye" class="w-4 h-4"></i>
              </button>
            </div>

            <div class="relative">
              <i data-lucide="lock" class="w-4 h-4 text-zinc-400 absolute left-3.5 top-1/2 -translate-y-1/2"></i>
              <input type="password" id="suConfirmPassword" required placeholder="Confirm Password" class="w-full pl-10 pr-10 py-3 bg-black/40 border border-white/15 rounded-2xl text-xs font-semibold text-white placeholder-zinc-500 focus:outline-none focus:border-brand-cyan focus:ring-1 focus:ring-brand-cyan transition-all">
              <button type="button" onclick="togglePasswordVisibility('suConfirmPassword')" class="absolute right-3.5 top-1/2 -translate-y-1/2 text-zinc-400 hover:text-white">
                <i data-lucide="eye" class="w-4 h-4"></i>
              </button>
            </div>

            <!-- Vehicle Mode Selector -->
            <div class="pt-1">
              <label class="block text-[10px] font-bold uppercase tracking-wider text-zinc-400 mb-1.5">Favorite Mode of Commute</label>
              <div class="grid grid-cols-3 gap-2 text-[11px] font-bold">
                <button type="button" onclick="setCommuteMode('bus', this)" class="commute-chip p-2 rounded-xl border border-brand-cyan bg-brand-cyan/20 text-brand-cyan flex items-center justify-center gap-1">
                  🚌 Shuttles
                </button>
                <button type="button" onclick="setCommuteMode('auto', this)" class="commute-chip p-2 rounded-xl border border-white/15 bg-black/40 text-zinc-300 flex items-center justify-center gap-1">
                  🛺 Autos
                </button>
                <button type="button" onclick="setCommuteMode('ev', this)" class="commute-chip p-2 rounded-xl border border-white/15 bg-black/40 text-zinc-300 flex items-center justify-center gap-1">
                  ⚡ Eco EVs
                </button>
              </div>
            </div>

            <div class="flex items-center gap-2 pt-1 text-xs text-zinc-400">
              <input type="checkbox" id="suTerms" required class="w-4 h-4 rounded bg-white/10 border-white/20 text-brand-cyan focus:ring-brand-cyan">
              <label for="suTerms" class="text-[11px]">
                I agree to the <a href="#" class="text-brand-cyan hover:underline">Terms of Service</a> & <a href="#" class="text-brand-cyan hover:underline">Privacy Policy</a>
              </label>
            </div>

            <button type="submit" class="w-full py-3.5 rounded-2xl text-black font-extrabold text-sm tracking-wide flex items-center justify-center gap-2 btn-gradient">
              <span>Sign Up</span>
              <i data-lucide="arrow-right" class="w-4 h-4"></i>
            </button>

            <button type="button" onclick="handleGoogleSignIn()" class="w-full py-2.5 rounded-2xl bg-white/5 hover:bg-white/10 border border-white/15 text-xs font-bold text-white flex items-center justify-center gap-2 transition-all">
              <svg class="w-4 h-4" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
              </svg>
              Continue with Google
            </button>

            <button type="button" onclick="handleGuestDirectAccess()" class="w-full py-2 text-center text-xs text-brand-cyan hover:underline font-bold">
              ⚡ Guest Mode: Explore Live Campus Transport Instantly →
            </button>

          </form>

        </div>
      </div>

    </div>
  </section>

  <!-- ================= MAIN TRANSPORT DASHBOARD ================= -->
  <section id="mainTransportDashboard" class="hidden flex-1 grid grid-cols-1 lg:grid-cols-12 overflow-hidden h-[calc(100vh-72px)] bg-[#070913]">
    
    <!-- Left Sidebar -->
    <aside class="lg:col-span-4 xl:col-span-4 border-r border-white/10 bg-[#0d1122]/90 backdrop-blur-2xl flex flex-col h-full overflow-hidden">
      
      <!-- Search & Filters -->
      <div class="p-4 border-b border-white/10 space-y-3 shrink-0">
        <div class="flex items-center gap-2">
          <div class="relative flex-1">
            <i data-lucide="search" class="w-4 h-4 text-zinc-400 absolute left-3 top-1/2 -translate-y-1/2"></i>
            <input type="text" id="transitSearchInput" placeholder="Search Bus, Auto, EV or Stop..." class="w-full pl-9 pr-4 py-2.5 bg-white/5 border border-white/10 text-xs font-semibold rounded-xl text-white placeholder-zinc-500 focus:outline-none focus:border-brand-cyan">
          </div>
          <button onclick="openPaymentAndBookingModal()" title="Book / Pay Pass" class="p-2.5 rounded-xl bg-brand-cyan text-black hover:opacity-90 font-bold">
            <i data-lucide="credit-card" class="w-4 h-4"></i>
          </button>
        </div>

        <!-- Mode Selectors: All / Shuttles 🚌 / Autos 🛺 / EVs ⚡ -->
        <div class="grid grid-cols-4 p-1 rounded-2xl bg-black/40 border border-white/10 text-[11px] font-extrabold text-zinc-400">
          <button data-type="all" onclick="filterFleetCategory('all', this)" class="fleet-cat-btn py-1.5 rounded-xl bg-white/15 text-brand-cyan shadow-sm">All (8)</button>
          <button data-type="bus" onclick="filterFleetCategory('bus', this)" class="fleet-cat-btn py-1.5 rounded-xl hover:text-white">🚌 Shuttles</button>
          <button data-type="auto" onclick="filterFleetCategory('auto', this)" class="fleet-cat-btn py-1.5 rounded-xl hover:text-white">🛺 Autos</button>
          <button data-type="ev" onclick="filterFleetCategory('ev', this)" class="fleet-cat-btn py-1.5 rounded-xl hover:text-white">⚡ EVs</button>
        </div>

        <!-- System Delay Status Banner -->
        <div id="fleetStatusBanner" class="p-2.5 rounded-xl text-xs font-bold flex items-center justify-between bg-emerald-500/10 border border-emerald-500/30 text-emerald-400">
          <div class="flex items-center gap-2">
            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
            <span id="bannerStatusText">All vehicles matched & on schedule</span>
          </div>
          <span class="text-[10px] font-mono uppercase bg-emerald-500/20 px-2 py-0.5 rounded">±2m Confirmed</span>
        </div>

        <!-- Active Trip OTP Security Banner -->
        <div id="activeTripBanner" class="hidden p-3 rounded-2xl bg-gradient-to-r from-emerald-950/60 to-black border border-emerald-500/40 space-y-2">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-ping"></span>
              <strong class="text-xs font-black text-white" id="activeTripVehicleName">Shuttle A1</strong>
            </div>
            <div class="px-2.5 py-1 rounded-full bg-emerald-400/20 text-emerald-400 text-xs font-mono font-black" id="activeTripOtpBadge">
              OTP: 8392
            </div>
          </div>
          <div class="flex items-center justify-between text-xs text-zinc-300">
            <span id="activeTripDriverInfo">Driver: Rajesh Sharma (PB 08 CA 1201)</span>
            <button onclick="openDriverChat()" class="px-3 py-1 rounded-lg bg-emerald-500 text-black font-extrabold hover:bg-emerald-400">
              💬 Chat Driver
            </button>
          </div>
        </div>

      </div>

      <!-- Scrollable Fleet List -->
      <div class="flex-1 overflow-y-auto p-4 space-y-3" id="fleetItemsContainer">
        <!-- Rendered via JS -->
      </div>

      <!-- Bottom Quick Actions: Fares, Stress Test & Driver Support -->
      <div class="p-4 border-t border-white/10 bg-black/30 grid grid-cols-3 gap-2 text-xs font-bold shrink-0">
        <button onclick="openPaymentAndBookingModal()" class="py-2.5 rounded-xl bg-brand-cyan/15 hover:bg-brand-cyan/25 border border-brand-cyan/30 text-brand-cyan flex items-center justify-center gap-1.5">
          💳 Pay / UPI
        </button>
        <button onclick="openFarePassesModal()" class="py-2.5 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 text-zinc-200 flex items-center justify-center gap-1.5">
          🎟️ Passes
        </button>
        <button onclick="openH4StressModal()" class="py-2.5 rounded-xl bg-red-500/15 hover:bg-red-500/25 border border-red-500/30 text-red-400 flex items-center justify-center gap-1.5">
          🛰️ 2m Drop
        </button>
      </div>

    </aside>

    <!-- Right Map View -->
    <main class="lg:col-span-8 xl:col-span-8 relative h-full flex flex-col overflow-hidden">
      
      <div id="campusMap" class="w-full h-full bg-[#0a0e1a]"></div>

      <!-- Floating Controls -->
      <div class="absolute top-4 left-4 z-[400] flex items-center gap-2">
        <select id="mapLayerThemeSelect" class="bg-black/80 backdrop-blur-md border border-white/20 text-xs font-bold rounded-xl px-3 py-2 text-white focus:outline-none">
          <option value="dark">🌙 Cyber Dark Map</option>
          <option value="voyager">🗺️ Street Vector</option>
          <option value="satellite">🛰️ Satellite Campus</option>
        </select>

        <div class="flex items-center rounded-xl bg-black/80 backdrop-blur-md border border-white/20 p-1 text-xs font-bold text-zinc-400">
          <button onclick="setSimWarp(1, this)" class="warp-btn px-2.5 py-1 rounded-lg hover:text-white">1×</button>
          <button onclick="setSimWarp(3, this)" class="warp-btn px-2.5 py-1 rounded-lg bg-brand-cyan text-black">3×</button>
          <button onclick="setSimWarp(8, this)" class="warp-btn px-2.5 py-1 rounded-lg hover:text-white">8×</button>
        </div>
      </div>

      <!-- Live Campus Clock -->
      <div class="absolute top-4 right-4 z-[400] flex items-center gap-2">
        <div class="px-3.5 py-2 rounded-xl bg-black/85 backdrop-blur-md border border-white/15 text-xs font-bold font-mono text-brand-cyan shadow-xl flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-brand-cyan animate-pulse"></span>
          <span id="dashboardClock">12:00:00 PM</span>
        </div>
      </div>

      <!-- Slide-Over Drawer: Selected Vehicle Telemetry -->
      <div id="vehicleTelemetryDrawer" class="absolute bottom-6 right-6 z-[450] w-96 max-w-[calc(100vw-3rem)] glass-card rounded-3xl p-5 border border-white/20 shadow-2xl translate-y-[130%] opacity-0 pointer-events-none transition-all duration-300">
        <div class="flex items-center justify-between pb-3 border-b border-white/10">
          <div class="flex items-center gap-3">
            <div id="dtVehicleEmoji" class="w-11 h-11 rounded-2xl bg-brand-cyan/20 border border-brand-cyan/40 text-white flex items-center justify-center font-bold text-xl shadow-md">
              🚌
            </div>
            <div>
              <h3 id="dtVehicleTitle" class="text-base font-extrabold text-white">Campus Shuttle PB 08</h3>
              <p id="dtVehicleDriver" class="text-xs text-brand-cyan font-semibold">Driver: Rajesh Sharma</p>
            </div>
          </div>
          <button onclick="closeVehicleDrawer()" class="p-1.5 rounded-xl hover:bg-white/10 text-zinc-400 hover:text-white">
            <i data-lucide="x" class="w-4 h-4"></i>
          </button>
        </div>

        <div class="py-4 grid grid-cols-3 gap-2 text-center">
          <div class="p-2.5 rounded-2xl bg-white/5 border border-white/10">
            <span class="text-[10px] text-zinc-400 font-bold block uppercase">Speed</span>
            <span id="dtSpeed" class="text-lg font-black text-white">24</span> <span class="text-[10px] text-zinc-400">km/h</span>
          </div>

          <div class="p-2.5 rounded-2xl bg-white/5 border border-white/10">
            <span class="text-[10px] text-zinc-400 font-bold block uppercase">Capacity</span>
            <span id="dtCapacity" class="text-lg font-black text-brand-cyan">18</span> <span class="text-[10px] text-zinc-400">free</span>
          </div>

          <div class="p-2.5 rounded-2xl bg-white/5 border border-white/10">
            <span class="text-[10px] text-zinc-400 font-bold block uppercase">Signal</span>
            <span id="dtSignal" class="text-xs font-black text-emerald-400 block mt-1">Locked</span>
          </div>
        </div>

        <div class="space-y-2">
          <span class="text-[11px] font-bold uppercase tracking-wider text-zinc-400">Approaching Stops</span>
          <div id="dtStopSequence" class="space-y-1.5 text-xs max-h-36 overflow-y-auto">
            <!-- Rendered by JS -->
          </div>
        </div>

        <div class="grid grid-cols-2 gap-2 mt-4 pt-3 border-t border-white/10">
          <button id="btnFollowVehicle" onclick="followSelectedVehicle()" class="py-2.5 rounded-xl bg-brand-cyan text-black text-xs font-black flex items-center justify-center gap-1.5 transition-all">
            <i data-lucide="crosshair" class="w-3.5 h-3.5"></i> Follow Live
          </button>
          <button id="btnCallDriver" onclick="openDriverChat()" class="py-2.5 rounded-xl bg-white/10 hover:bg-white/20 border border-white/10 text-xs font-bold flex items-center justify-center gap-1.5 transition-all">
            <i data-lucide="message-square" class="w-3.5 h-3.5 text-brand-cyan"></i> Chat (OTP)
          </button>
        </div>
      </div>

    </main>

  </div>

  <!-- ================= PAYMENT & RIDE BOOKING MODAL ================= -->
  <div id="paymentBookingModal" class="fixed inset-0 z-[1000] bg-black/80 backdrop-blur-md hidden place-items-center p-4">
    <div class="w-full max-w-xl glass-card rounded-3xl p-6 sm:p-7 border border-white/20 shadow-2xl relative space-y-4 max-h-[92vh] overflow-y-auto">
      
      <div class="flex items-center justify-between pb-3 border-b border-white/10">
        <div>
          <h3 class="text-xl font-black text-white flex items-center gap-2">
            <span>💳</span> Campus Transit Payment
          </h3>
          <p class="text-xs text-brand-cyan">Instant UPI QR & Cash on Board with Driver OTP</p>
        </div>
        <button onclick="closeModal('paymentBookingModal')" class="text-zinc-400 hover:text-white p-1">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <!-- Money Select Option -->
      <div class="space-y-2">
        <label class="block text-xs font-bold text-zinc-300 uppercase tracking-wider">1. Select Fare / Amount</label>
        <div class="grid grid-cols-3 sm:grid-cols-5 gap-2 text-xs font-extrabold" id="moneySelectChips">
          <button type="button" onclick="selectMoneyAmount(15, this)" class="money-chip p-2.5 rounded-xl border border-brand-cyan bg-brand-cyan/20 text-brand-cyan">
            ₹15 <span class="block text-[9px] font-normal text-zinc-300">Single</span>
          </button>
          <button type="button" onclick="selectMoneyAmount(30, this)" class="money-chip p-2.5 rounded-xl border border-white/10 bg-white/5 text-zinc-300 hover:border-white/30">
            ₹30 <span class="block text-[9px] font-normal text-zinc-400">Return</span>
          </button>
          <button type="button" onclick="selectMoneyAmount(40, this)" class="money-chip p-2.5 rounded-xl border border-white/10 bg-white/5 text-zinc-300 hover:border-white/30">
            ₹40 <span class="block text-[9px] font-normal text-zinc-400">Day Pass</span>
          </button>
          <button type="button" onclick="selectMoneyAmount(150, this)" class="money-chip p-2.5 rounded-xl border border-white/10 bg-white/5 text-zinc-300 hover:border-white/30">
            ₹150 <span class="block text-[9px] font-normal text-zinc-400">Weekly</span>
          </button>
          <button type="button" onclick="selectMoneyAmount(999, this)" class="money-chip p-2.5 rounded-xl border border-white/10 bg-white/5 text-zinc-300 hover:border-white/30">
            ₹999 <span class="block text-[9px] font-normal text-zinc-400">Semester</span>
          </button>
        </div>

        <div class="flex items-center gap-2 pt-1">
          <span class="text-xs text-zinc-400 font-bold">Custom:</span>
          <div class="relative flex-1">
            <span class="absolute left-3 top-1/2 -translate-y-1/2 text-xs text-zinc-400 font-bold">₹</span>
            <input type="number" id="customAmountInput" placeholder="Enter custom amount" class="w-full pl-7 pr-3 py-2 bg-white/5 border border-white/10 rounded-xl text-xs font-bold text-white focus:outline-none focus:border-brand-cyan" oninput="handleCustomAmount(this.value)">
          </div>
        </div>
      </div>

      <!-- Coupon & Discount Section -->
      <div class="p-3.5 rounded-2xl bg-white/5 border border-white/10 space-y-2">
        <label class="block text-[11px] font-bold text-zinc-300 uppercase tracking-wider flex items-center justify-between">
          <span>2. Apply Coupon Code</span>
          <span class="text-emerald-400 text-[10px]">🎁 10% First Ride Discount Available</span>
        </label>
        
        <div class="flex items-center gap-2">
          <input type="text" id="couponCodeInput" placeholder="Enter coupon (e.g. CAMPUS10)" class="flex-1 px-3 py-2 bg-black/40 border border-white/10 rounded-xl text-xs font-mono uppercase text-white focus:outline-none focus:border-brand-cyan">
          <button onclick="applyCouponCode()" class="px-4 py-2 rounded-xl bg-white/15 hover:bg-white/25 text-white font-bold text-xs transition-all">
            Apply
          </button>
        </div>

        <div class="flex items-center gap-2 pt-1 text-[11px]">
          <button onclick="quickApplyCoupon('CAMPUS10')" class="px-2.5 py-1 rounded-lg bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 font-bold hover:bg-emerald-500/25">
            🏷️ CAMPUS10 (10% OFF)
          </button>
          <button onclick="quickApplyCoupon('FREEFIRST')" class="px-2.5 py-1 rounded-lg bg-brand-cyan/15 border border-brand-cyan/30 text-brand-cyan font-bold hover:bg-brand-cyan/25">
            🎁 FREEFIRST (1st Ride Free)
          </button>
        </div>
      </div>

      <!-- Payment Method Toggle -->
      <div class="space-y-2">
        <label class="block text-xs font-bold text-zinc-300 uppercase tracking-wider">3. Choose Payment Method</label>
        
        <div class="grid grid-cols-2 p-1 bg-black/40 border border-white/10 rounded-2xl text-xs font-extrabold">
          <button id="payTabUpi" onclick="switchPayTab('upi')" class="py-2.5 rounded-xl bg-white/15 text-brand-cyan flex items-center justify-center gap-2 shadow-sm transition-all">
            📱 UPI / QR Code
          </button>
          <button id="payTabCash" onclick="switchPayTab('cash')" class="py-2.5 rounded-xl text-zinc-400 hover:text-white flex items-center justify-center gap-2 transition-all">
            💵 Cash on Board
          </button>
        </div>
      </div>

      <!-- A. UPI QR View -->
      <div id="upiPaymentArea" class="space-y-3">
        <div class="p-4 rounded-3xl bg-zinc-950 border border-white/10 text-center space-y-3">
          
          <div class="flex items-center justify-between text-xs text-zinc-400 font-semibold px-2">
            <span>Scan to Pay with Any UPI App</span>
            <span class="text-amber-400 flex items-center gap-1 font-mono">
              <span class="w-2 h-2 rounded-full bg-amber-400 animate-ping"></span>
              Expires: <strong id="upiTimerClock">04:59</strong>
            </span>
          </div>

          <!-- User Google Pay QR Code Image -->
          <div class="relative w-56 h-56 mx-auto bg-white p-3 rounded-3xl shadow-2xl overflow-hidden border-2 border-brand-cyan/40">
            <img src="upi-qr.jpg" onerror="this.src='data:image/jpeg;base64,{qr_b64}'" alt="Google Pay UPI QR Code" class="w-full h-full object-contain rounded-2xl">
          </div>

          <p class="text-[11px] text-zinc-400 font-medium">Google Pay · PhonePe · Paytm · BHIM · Any Bank UPI</p>

          <div class="inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-white/5 border border-white/10 text-xs font-mono text-zinc-300">
            <span>UPI ID: <strong class="text-brand-cyan">campusflow@okaxis</strong></span>
            <button onclick="copyUpiId()" class="p-1 hover:text-white" title="Copy UPI ID">
              <i data-lucide="copy" class="w-3.5 h-3.5"></i>
            </button>
          </div>

        </div>
      </div>

      <!-- B. Cash View -->
      <div id="cashPaymentArea" class="hidden p-5 rounded-3xl bg-zinc-950 border border-white/10 space-y-3">
        <div class="flex items-center gap-3">
          <div class="w-12 h-12 rounded-2xl bg-amber-500/20 text-amber-400 flex items-center justify-center text-2xl font-bold">
            💵
          </div>
          <div>
            <h4 class="text-sm font-black text-white">Cash on Boarding</h4>
            <p class="text-xs text-zinc-400">Pay cash directly to the driver upon entering.</p>
          </div>
        </div>
        <p class="text-xs text-zinc-300 leading-relaxed bg-white/5 p-3 rounded-2xl border border-white/10">
          A 4-digit ride verification OTP will be issued immediately. Share this OTP with the driver to start your trip. Exact cash preferred.
        </p>
      </div>

      <!-- Fare Calculation Breakdown -->
      <div class="p-4 rounded-2xl bg-black/40 border border-white/10 space-y-1.5 text-xs">
        <div class="flex justify-between text-zinc-400">
          <span>Selected Fare Amount</span>
          <span class="font-bold text-white" id="summaryBasePrice">₹15.00</span>
        </div>
        <div class="flex justify-between text-emerald-400" id="summaryDiscountRow">
          <span>Student Discount (20%)</span>
          <span id="summaryStudentDiscount">-₹3.00</span>
        </div>
        <div class="flex justify-between text-brand-cyan hidden" id="summaryCouponRow">
          <span id="summaryCouponLabel">Coupon CAMPUS10 (10%)</span>
          <span id="summaryCouponDiscount">-₹1.20</span>
        </div>
        <div class="flex justify-between pt-2 border-t border-white/10 text-sm font-black text-white">
          <span>Final Total Payable</span>
          <span class="text-brand-cyan text-base" id="summaryFinalPrice">₹12.00</span>
        </div>
      </div>

      <button id="btnCompletePayment" onclick="handlePaymentSuccess()" class="w-full py-3.5 rounded-2xl text-black font-extrabold text-sm tracking-wide btn-gradient flex items-center justify-center gap-2">
        <span id="btnPayText">I've Paid via UPI & Get OTP →</span>
      </button>

    </div>
  </div>

  <!-- ================= DRIVER CHAT & OTP VERIFICATION MODAL ================= -->
  <div id="driverChatModal" class="fixed inset-0 z-[1050] bg-black/80 backdrop-blur-md hidden place-items-center p-4">
    <div class="w-full max-w-md glass-card rounded-3xl border border-white/20 shadow-2xl overflow-hidden flex flex-col h-[560px] animate-fade-in-up">
      
      <!-- Chat Header -->
      <div class="p-4 bg-zinc-950 border-b border-white/10 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-2xl bg-brand-cyan/20 border border-brand-cyan/40 text-brand-cyan flex items-center justify-center font-bold text-base">
            👨🏽‍✈️
          </div>
          <div>
            <h4 class="text-sm font-black text-white" id="chatDriverName">Rajesh Sharma</h4>
            <p class="text-[10px] text-emerald-400 flex items-center gap-1 font-mono">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
              On Duty · PB 08 CA 1201 · Tata Starbus EV
            </p>
          </div>
        </div>
        <button onclick="closeModal('driverChatModal')" class="text-zinc-400 hover:text-white p-1">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <!-- Security OTP Display Strip -->
      <div class="p-3 bg-emerald-950/40 border-b border-emerald-500/30 flex items-center justify-between text-xs">
        <span class="text-zinc-300 font-semibold">Your Security Ride Start OTP:</span>
        <span class="px-3 py-1 rounded-full bg-emerald-400 text-black font-black font-mono tracking-widest text-sm shadow-md" id="chatOtpDisplay">
          8392
        </span>
      </div>

      <!-- Messages Thread -->
      <div id="chatMessagesBox" class="flex-1 p-4 overflow-y-auto space-y-3 text-xs bg-black/50">
      </div>

      <!-- Quick Message Chips -->
      <div class="p-2 border-t border-white/10 bg-zinc-950 flex items-center gap-1.5 overflow-x-auto text-[11px]" id="chatQuickChips">
        <button onclick="sendQuickChatMessage('My OTP is ' + currentTripOtp)" class="chip-btn px-2.5 py-1 rounded-lg bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-bold shrink-0">
          🔑 Share OTP
        </button>
        <button onclick="sendQuickChatMessage('Where are you?')" class="chip-btn px-2.5 py-1 rounded-lg bg-white/5 text-zinc-300 border border-white/10 font-medium shrink-0">
          📍 Where are you?
        </button>
        <button onclick="sendQuickChatMessage('Please wait 2 minutes')" class="chip-btn px-2.5 py-1 rounded-lg bg-white/5 text-zinc-300 border border-white/10 font-medium shrink-0">
          ⏳ Wait 2 min
        </button>
        <button onclick="sendQuickChatMessage('I am at the main gate')" class="chip-btn px-2.5 py-1 rounded-lg bg-white/5 text-zinc-300 border border-white/10 font-medium shrink-0">
          🚪 At Main Gate
        </button>
      </div>

      <!-- Input Bar -->
      <div class="p-3 border-t border-white/10 bg-zinc-950 flex items-center gap-2">
        <input type="text" id="chatMessageInput" placeholder="Message driver..." class="flex-1 px-3.5 py-2.5 rounded-xl bg-white/5 border border-white/10 text-xs text-white focus:outline-none focus:border-brand-cyan" onkeydown="if(event.key==='Enter') sendChatMessage()">
        <button onclick="sendChatMessage()" class="p-2.5 rounded-xl bg-brand-cyan text-black hover:opacity-90 font-bold transition-all">
          <i data-lucide="send" class="w-4 h-4"></i>
        </button>
      </div>

    </div>
  </div>

  <!-- ================= FARES PASSES MODAL ================= -->
  <div id="farePassesModal" class="fixed inset-0 z-[1000] bg-black/75 backdrop-blur-md hidden place-items-center p-4">
    <div class="w-full max-w-lg glass-card rounded-3xl p-6 border border-white/20 shadow-2xl relative space-y-4">
      <div class="flex items-center justify-between pb-3 border-b border-white/10">
        <div>
          <h3 class="text-xl font-black text-white">Campus Transit Passes</h3>
          <p class="text-xs text-brand-cyan">Valid across Campus Shuttles, Auto Rickshaws & EVs</p>
        </div>
        <button onclick="closeModal('farePassesModal')" class="text-zinc-400 hover:text-white">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <div class="grid grid-cols-2 gap-3" id="fareCardsGrid">
      </div>
    </div>
  </div>

  <!-- ================= H4 SIGNAL STRESS TEST MODAL ================= -->
  <div id="h4StressModal" class="fixed inset-0 z-[1000] bg-black/75 backdrop-blur-md hidden place-items-center p-4">
    <div class="w-full max-w-md glass-card rounded-3xl p-6 border border-white/20 shadow-2xl relative space-y-4">
      <div class="flex items-center justify-between pb-3 border-b border-white/10">
        <div>
          <h3 class="text-lg font-black text-white flex items-center gap-2">
            <i data-lucide="flask-conical" class="w-5 h-5 text-brand-cyan"></i>
            H4 GPS Dropout Injector
          </h3>
          <p class="text-xs text-zinc-400">Test dead-reckoning during 120s blackout</p>
        </div>
        <button onclick="closeModal('h4StressModal')" class="text-zinc-400 hover:text-white">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <div class="space-y-3">
        <label class="block text-xs font-bold text-zinc-300">Target Vehicle</label>
        <select id="stressSelectVehicle" class="w-full px-3 py-2.5 rounded-xl bg-white/5 border border-white/10 text-xs font-semibold text-white focus:outline-none">
        </select>

        <div class="grid grid-cols-2 gap-2 pt-2">
          <button onclick="triggerBlackoutOnSelected()" class="py-3 rounded-xl bg-red-600 hover:bg-red-700 text-white font-extrabold text-xs flex items-center justify-center gap-1.5 transition-all">
            🛰️ Cut GPS (120s)
          </button>
          <button onclick="triggerJamOnSelected()" class="py-3 rounded-xl bg-amber-600 hover:bg-amber-700 text-white font-extrabold text-xs flex items-center justify-center gap-1.5 transition-all">
            🚧 Inject Jam
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- ================= SCRIPTS ================= -->
  <script>
    const CAMPUS_CENTER = [31.2548, 75.7052];
    const KLAT = 111320;
    const KLNG = 111320 * Math.cos(CAMPUS_CENTER[0] * Math.PI / 180);
    const toXY = p => [(p[1] - CAMPUS_CENTER[1]) * KLNG, (p[0] - CAMPUS_CENTER[0]) * KLAT];
    const toLL = x => [CAMPUS_CENTER[0] + x[1] / KLAT, CAMPUS_CENTER[1] + x[0] / KLNG];

    const CAMPUS_STOPS = [
      {{ id: 0, name: "Main Campus Gate & Metro Link", code: "MG", emoji: "🚪", offset: [-0.0055, -0.0040], dwell: 20 }},
      {{ id: 1, name: "Admin Block & Senate Hall", code: "AB", emoji: "🏛️", offset: [-0.0030, -0.0045], dwell: 15 }},
      {{ id: 2, name: "Central Library & Digital Hub", code: "CL", emoji: "📚", offset: [0.0005, -0.0040], dwell: 20 }},
      {{ id: 3, name: "Boys Hostel Quadrangle (H1-H4)", code: "BH", emoji: "🛏️", offset: [0.0045, -0.0030], dwell: 25 }},
      {{ id: 4, name: "Innovation Hub & Biotech Labs", code: "IH", emoji: "💡", offset: [0.0060, 0.0020], dwell: 20 }},
      {{ id: 5, name: "Olympic Sports Complex & Pool", code: "SC", emoji: "🏟️", offset: [0.0030, 0.0055], dwell: 15 }},
      {{ id: 6, name: "Student Activity Center & Food Court", code: "FC", emoji: "🍜", offset: [-0.0010, 0.0050], dwell: 25 }},
      {{ id: 7, name: "Girls Hostel Complex (G1-G3)", code: "GH", emoji: "🏢", offset: [-0.0045, 0.0035], dwell: 20 }},
      {{ id: 8, name: "University Hospital & Medical Wing", code: "HW", emoji: "🏥", offset: [-0.0050, 0.0005], dwell: 15 }}
    ].map(s => ({{ ...s, ll: [CAMPUS_CENTER[0] + s.offset[0], CAMPUS_CENTER[1] + s.offset[1]] }}));

    const CAMPUS_ROUTES = [
      {{ id: 'A', name: 'Green Loop (Outer Campus)', color: '#00f0ff', stops: [0, 1, 2, 3, 4, 5, 6, 7, 8] }},
      {{ id: 'B', name: 'Blue Express (Hostels & Food)', color: '#a855f7', stops: [0, 2, 3, 6, 7] }}
    ];

    const FLEET_DEFINITIONS = [
      {{ id: 'BUS-1', type: 'bus', name: 'Campus Shuttle A1', model: 'Tata Starbus EV', plate: 'PB 08 CA 1201', driver: 'Rajesh Sharma', phone: '+91 98110 44211', cap: 35, route: 'A', f: 0.0, color: '#00f0ff', emoji: '🚌' }},
      {{ id: 'BUS-2', type: 'bus', name: 'Campus Shuttle A2', model: 'Ashok Leyland Oyster', plate: 'PB 08 CA 1202', driver: 'Vikram Singh', phone: '+91 98110 44212', cap: 35, route: 'A', f: 0.5, color: '#00f0ff', emoji: '🚌' }},
      {{ id: 'AUTO-1', type: 'auto', name: 'Campus Auto Rickshaw #1', model: 'Bajaj RE EV Auto', plate: 'MP 04 AR 4521', driver: 'Suresh Yadav', phone: '+91 94250 88201', cap: 4, route: 'B', f: 0.15, color: '#f59e0b', emoji: '🛺' }},
      {{ id: 'AUTO-2', type: 'auto', name: 'Campus Auto Rickshaw #2', model: 'Piaggio Ape E-City', plate: 'MP 04 AR 4522', driver: 'Amit Patel', phone: '+91 94250 88202', cap: 4, route: 'B', f: 0.65, color: '#f59e0b', emoji: '🛺' }},
      {{ id: 'AUTO-3', type: 'auto', name: 'Campus Auto Rickshaw #3', model: 'Mahindra Treo Electric', plate: 'MP 04 AR 4523', driver: 'Manoj Tiwari', phone: '+91 94250 88203', cap: 4, route: 'A', f: 0.85, color: '#f59e0b', emoji: '🛺' }},
      {{ id: 'EV-1', type: 'ev', name: 'Eco Campus EV Cart #1', model: 'ClubCar Onward 8-Seater', plate: 'DL 01 EV 8801', driver: 'Priya Verma', phone: '+91 99100 23114', cap: 8, route: 'A', f: 0.35, color: '#10b981', emoji: '⚡' }},
      {{ id: 'EV-2', type: 'ev', name: 'Eco Campus EV Cart #2', model: 'Volmac Smart Campus EV', plate: 'DL 01 EV 8802', driver: 'Sunita Gupta', phone: '+91 99100 23115', cap: 8, route: 'B', f: 0.75, color: '#10b981', emoji: '⚡' }},
      {{ id: 'BUS-EX', type: 'bus', name: 'Express Campus Shuttle B1', model: 'Eicher Skyline Pro', plate: 'PB 08 CB 8820', driver: 'Ramesh Kumar', phone: '+91 98110 99200', cap: 28, route: 'B', f: 0.40, color: '#a855f7', emoji: '🚌' }}
    ];

    const FARES = [
      {{ id: 'single', name: 'Single Trip Pass', emoji: '🎫', price: 15, desc: '1 ride on Bus, Auto, or EV' }},
      {{ id: 'day', name: 'All-Day Pass', emoji: '☀️', price: 40, desc: 'Unlimited rides across campus' }},
      {{ id: 'weekly', name: 'Weekly Pass', emoji: '📅', price: 150, desc: '7 days unlimited campus transit' }},
      {{ id: 'sem', name: 'Semester Pass', emoji: '🎓', price: 999, desc: 'Whole semester access + VIP perks' }}
    ];

    let currentUser = JSON.parse(localStorage.getItem('cf_user') || 'null');
    let map = null;
    let tileLayer = null;
    let routeLayers = {{}};
    let stopMarkers = {{}};
    let vehicleMarkers = {{}};
    let activeCategoryFilter = 'all';
    let selectedVehicleId = null;
    let followingVehicleId = null;
    let simSpeedWarp = 3;
    let simTime = 0;
    let simClockDate = Date.now();
    const FLEET = [];

    // Payment & OTP State
    let selectedMoney = 15;
    let appliedCoupon = '';
    let currentPaymentMethod = 'upi';
    let currentTripOtp = '7429';
    let isTripStarted = false;
    let activeVehicleForTrip = null;
    let chatMessages = [];
    let upiTimerInterval = null;
    let isBgVideoPlaying = true;

    const mod = (x, L) => ((x % L) + L) % L;
    const wrapD = (x, L) => ((x + L/2) % L + L) % L - L/2;
    const gauss = () => {{ let u = 0; for (let i = 0; i < 6; i++) u += Math.random(); return (u - 3) / 0.707; }};

    function buildRouteGeometry(R, pts) {{
      R.pts = pts;
      R.xy = pts.map(toXY);
      R.cum = [0];
      for (let i = 1; i < pts.length; i++) {{
        R.cum[i] = R.cum[i-1] + Math.hypot(R.xy[i][0] - R.xy[i-1][0], R.xy[i][1] - R.xy[i-1][1]);
      }}
      R.totalLength = R.cum[R.cum.length - 1];
    }}

    function getPositionAtS(R, s) {{
      s = mod(s, R.totalLength);
      let lo = 0, hi = R.cum.length - 1;
      while (hi - lo > 1) {{
        const mid = (lo + hi) >> 1;
        if (R.cum[mid] <= s) lo = mid; else hi = mid;
      }}
      const f = (s - R.cum[lo]) / ((R.cum[hi] - R.cum[lo]) || 1);
      const a = R.xy[lo], b = R.xy[hi];
      const x = a[0] + f * (b[0] - a[0]);
      const y = a[1] + f * (b[1] - a[1]);
      const hd = (Math.atan2(b[0] - a[0], b[1] - a[1]) * 180 / Math.PI + 360) % 360;
      return {{ xy: [x, y], ll: toLL([x, y]), hd }};
    }}

    function projectToRoute(R, xy) {{
      let best = null;
      for (let i = 0; i < R.xy.length - 1; i++) {{
        const a = R.xy[i], b = R.xy[i + 1];
        const dx = b[0] - a[0], dy = b[1] - a[1];
        const l2 = dx * dx + dy * dy || 1e-9;
        let t = Math.max(0, Math.min(1, ((xy[0] - a[0]) * dx + (xy[1] - a[1]) * dy) / l2));
        const dist = Math.hypot(xy[0] - (a[0] + t * dx), xy[1] - (a[1] + t * dy));
        const s = R.cum[i] + t * Math.sqrt(l2);
        if (!best || dist < best.d) best = {{ s, d: dist }};
      }}
      return best;
    }}

    function initRoutesAndFleet() {{
      CAMPUS_ROUTES.forEach(R => {{
        const wp = R.stops.map(i => CAMPUS_STOPS[i].ll);
        wp.push(wp[0]);
        const densified = [];
        for (let i = 0; i < wp.length - 1; i++) {{
          const a = toXY(wp[i]), b = toXY(wp[i+1]);
          const steps = Math.max(1, Math.round(Math.hypot(b[0] - a[0], b[1] - a[1]) / 25));
          for (let k = 0; k < steps; k++) {{
            densified.push(toLL([a[0] + (b[0] - a[0]) * k / steps, a[1] + (b[1] - a[1]) * k / steps]));
          }}
        }}
        densified.push(wp[0]);
        buildRouteGeometry(R, densified);

        R.stopList = R.stops.map(i => {{
          const p = projectToRoute(R, toXY(CAMPUS_STOPS[i].ll));
          return {{ i, s: p.s, name: CAMPUS_STOPS[i].name, emoji: CAMPUS_STOPS[i].emoji, dwell: CAMPUS_STOPS[i].dwell }};
        }}).sort((x, y) => x.s - y.s);
      }});

      FLEET_DEFINITIONS.forEach(d => {{
        const R = CAMPUS_ROUTES.find(r => r.id === d.route);
        const s = R.totalLength * d.f;
        const v = {{
          ...d,
          R,
          s,
          speed: d.type === 'auto' ? 7.2 : d.type === 'ev' ? 5.2 : 6.0,
          dwellTimer: 0,
          nextStopIdx: 0,
          blackoutTimer: 0,
          jamTimer: 0,
          freeSeats: Math.max(1, Math.floor(d.cap * (0.3 + Math.random() * 0.5))),
          est: {{ s, v: 5.8, lastFix: 0 }},
          disp: s,
          isDelayed: false
        }};
        v.nextStopIdx = R.stopList.findIndex(st => st.s > s);
        if (v.nextStopIdx < 0) v.nextStopIdx = 0;
        FLEET.push(v);
      }});
    }}

    function stepFleetSimulation(v, dt) {{
      const R = v.R;
      if (v.blackoutTimer > 0) v.blackoutTimer -= dt;
      if (v.jamTimer > 0) v.jamTimer -= dt;

      if (v.dwellTimer > 0) {{
        v.dwellTimer -= dt;
      }} else {{
        const st = R.stopList[v.nextStopIdx];
        const dist = mod(st.s - v.s, R.totalLength);
        const targetV = (v.jamTimer > 0 ? 2.0 : v.speed) * (1 + 0.04 * gauss());
        const ds = targetV * dt;

        if (ds >= dist - 0.5 || dist < 2.0) {{
          v.s = st.s;
          v.dwellTimer = st.dwell || 18;
          v.nextStopIdx = (v.nextStopIdx + 1) % R.stopList.length;
          v.freeSeats = Math.max(1, Math.min(v.cap, v.freeSeats + Math.floor(gauss() * 3)));
        }} else {{
          v.s = mod(v.s + ds, R.totalLength);
        }}
      }}

      const age = simTime - v.est.lastFix;
      const w = Math.exp(-age / 90.0);
      const blendedV = v.est.v * w + 5.8 * (1.0 - w);
      v.est.s = mod(v.est.s + blendedV * dt, R.totalLength);

      if (v.blackoutTimer <= 0) {{
        v.est.s = v.s;
        v.est.lastFix = simTime;
      }}
    }}

    function calculateETAs(v) {{
      const R = v.R;
      const currS = v.est.s;
      const L = R.totalLength;
      const effSpeed = Math.max(2.5, v.speed);

      return R.stopList.map(st => {{
        const rawDist = (st.s - currS) % L;
        const dist = rawDist > 10 ? rawDist : L + rawDist;
        const etaSec = Math.round(dist / effSpeed);
        return {{ stop: st, dist, etaSec, isLate: v.jamTimer > 0 }};
      }}).sort((a, b) => a.dist - b.dist);
    }}

    function formatEtaMin(sec) {{
      if (sec < 45) return 'Due';
      return `${{Math.max(1, Math.round(sec / 60))}} min`;
    }}

    function initCampusMap() {{
      map = L.map('campusMap', {{ zoomControl: false }}).setView(CAMPUS_CENTER, 15);
      L.control.zoom({{ position: 'bottomright' }}).addTo(map);

      setMapTheme('dark');

      CAMPUS_ROUTES.forEach(R => {{
        const grp = L.layerGroup().addTo(map);
        L.polyline(R.pts, {{ color: R.color, weight: 14, opacity: 0.22 }}).addTo(grp);
        L.polyline(R.pts, {{ color: R.color, weight: 4.5, opacity: 0.95, className: 'flow-line' }}).addTo(grp);
        routeLayers[R.id] = grp;
      }});

      CAMPUS_STOPS.forEach(s => {{
        const m = L.marker(s.ll, {{
          icon: L.divIcon({{
            className: '',
            html: `<div class="stop-badge-pill on-time" id="pill_${{s.id}}">${{s.emoji}} <b>--</b></div>`,
            iconSize: [0, 0]
          }})
        }}).addTo(map);

        m.on('click', () => {{
          map.flyTo(s.ll, 16.5, {{ duration: 0.8 }});
          showToast(`📍 Selected: ${{s.name}}`);
        }});
        stopMarkers[s.id] = m;
      }});

      FLEET.forEach(v => {{
        const pos = getPositionAtS(v.R, v.s);
        const m = L.marker(pos.ll, {{
          zIndexOffset: 1000,
          icon: L.divIcon({{
            className: '',
            html: `
              <div class="transit-marker" id="vmarker_${{v.id}}" style="background: ${{v.color}}; color: ${{v.color}}">
                <div class="pulse-ring"></div>
                <div class="heading-needle" id="vneedle_${{v.id}}"></div>
                <span>${{v.emoji}}</span>
              </div>
            `,
            iconSize: [44, 44],
            iconAnchor: [22, 22]
          }})
        }}).addTo(map);

        m.on('click', () => selectVehicle(v.id));
        vehicleMarkers[v.id] = m;
      }});

      map.on('dragstart', () => {{
        followingVehicleId = null;
      }});
    }}

    const MAP_STYLES = {{
      dark: ['https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', '&copy; CARTO &copy; OSM'],
      voyager: ['https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}{{r}}.png', '&copy; CARTO &copy; OSM'],
      satellite: ['https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{{z}}/{{y}}/{{x}}', '&copy; Esri']
    }};

    function setMapTheme(name) {{
      if (tileLayer) map.removeLayer(tileLayer);
      const conf = MAP_STYLES[name] || MAP_STYLES.dark;
      tileLayer = L.tileLayer(conf[0], {{ maxZoom: 19, attribution: conf[1] }}).addTo(map);
      tileLayer.bringToBack();
    }}

    function renderFleetList() {{
      const cont = document.getElementById('fleetItemsContainer');
      if (!cont) return;

      const filtered = FLEET.filter(v => {{
        if (activeCategoryFilter !== 'all' && v.type !== activeCategoryFilter) return false;
        const q = (document.getElementById('transitSearchInput').value || '').toLowerCase();
        if (q && !(v.name + v.driver + v.plate + v.R.name).toLowerCase().includes(q)) return false;
        return true;
      }});

      cont.innerHTML = filtered.map(v => {{
        const etas = calculateETAs(v);
        const next = etas[0];
        const isSelected = selectedVehicleId === v.id;
        const inDropout = v.blackoutTimer > 0;

        return `
          <div onclick="selectVehicle('${{v.id}}')" class="p-4 rounded-2xl border transition-all cursor-pointer glass-card ${{isSelected ? 'border-brand-cyan shadow-lg shadow-brand-cyan/20 ring-1 ring-brand-cyan' : 'border-white/10 hover:border-white/20'}}">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-3">
                <span class="w-10 h-10 rounded-2xl flex items-center justify-center font-bold text-xl shadow-md" style="background: ${{v.color}}20; border: 1px solid ${{v.color}}">
                  ${{v.emoji}}
                </span>
                <div>
                  <h4 class="text-sm font-extrabold text-white flex items-center gap-1.5">
                    ${{v.name}}
                    ${{inDropout ? '<span class="text-[9px] px-1.5 py-0.5 rounded bg-amber-500/20 text-amber-300">🛰️ 2m Drop</span>' : ''}}
                  </h4>
                  <p class="text-xs text-brand-cyan font-medium">Driver: <strong class="text-white">${{v.driver}}</strong> (${{v.plate}})</p>
                </div>
              </div>
              <div class="text-right">
                <span class="text-base font-black text-white">${{formatEtaMin(next.etaSec)}}</span>
                <span class="block text-[10px] text-zinc-400 font-mono">${{Math.round(v.speed * 3.6)}} km/h</span>
              </div>
            </div>

            <div class="flex items-center justify-between mt-3 pt-2.5 border-t border-white/10 text-xs">
              <span class="text-zinc-400">Next: <strong class="text-zinc-200">${{next.stop.name}}</strong></span>
              <span class="font-bold text-emerald-400">${{v.freeSeats}} seats free</span>
            </div>
          </div>
        `;
      }}).join('');

      CAMPUS_STOPS.forEach(s => {{
        let earliest = null;
        FLEET.forEach(v => {{
          const etas = calculateETAs(v);
          const forStop = etas.find(e => e.stop.i === s.id);
          if (forStop && (!earliest || forStop.etaSec < earliest.etaSec)) {{
            earliest = forStop;
          }}
        }});
        const pill = document.getElementById(`pill_${{s.id}}`);
        if (pill) {{
          pill.innerHTML = `${{s.emoji}} <b>${{earliest ? formatEtaMin(earliest.etaSec) : '--'}}</b>`;
          pill.className = `stop-badge-pill ${{earliest ? (earliest.isLate ? 'late' : 'on-time') : ''}}`;
        }}
      }});

      if (selectedVehicleId) updateVehicleDrawer();

      simClockDate += 1000 * simSpeedWarp;
      document.getElementById('dashboardClock').textContent = new Date(simClockDate).toLocaleTimeString([], {{ hour12: true }});
    }}

    function selectVehicle(id) {{
      selectedVehicleId = id;
      followingVehicleId = id;
      const v = FLEET.find(x => x.id === id);
      if (v && map) {{
        const pos = getPositionAtS(v.R, v.est.s);
        map.flyTo(pos.ll, 16.5, {{ duration: 0.8 }});
      }}
      openVehicleDrawer();
      renderFleetList();
    }}

    function openVehicleDrawer() {{
      const d = document.getElementById('vehicleTelemetryDrawer');
      d.classList.remove('translate-y-[130%]', 'opacity-0', 'pointer-events-none');
    }}

    function closeVehicleDrawer() {{
      selectedVehicleId = null;
      followingVehicleId = null;
      const d = document.getElementById('vehicleTelemetryDrawer');
      d.classList.add('translate-y-[130%]', 'opacity-0', 'pointer-events-none');
      renderFleetList();
    }}

    function updateVehicleDrawer() {{
      const v = FLEET.find(x => x.id === selectedVehicleId);
      if (!v) return;

      const etas = calculateETAs(v);
      document.getElementById('dtVehicleEmoji').textContent = v.emoji;
      document.getElementById('dtVehicleTitle').textContent = `${{v.name}} (${{v.plate}})`;
      document.getElementById('dtVehicleDriver').textContent = `Driver: ${{v.driver}} · ${{v.model}}`;
      document.getElementById('dtSpeed').textContent = Math.round(v.speed * 3.6);
      document.getElementById('dtCapacity').textContent = v.freeSeats;
      document.getElementById('dtSignal').textContent = v.blackoutTimer > 0 ? `Dead-Reckon (${{Math.round(v.blackoutTimer)}}s)` : 'Locked (±2m)';

      document.getElementById('dtStopSequence').innerHTML = etas.slice(0, 4).map(e => `
        <div class="flex items-center justify-between p-2 rounded-xl bg-white/5">
          <span>${{e.stop.emoji}} ${{e.stop.name}}</span>
          <span class="font-extrabold text-brand-cyan">${{formatEtaMin(e.etaSec)}}</span>
        </div>
      `).join('');
    }}

    function followSelectedVehicle() {{
      followingVehicleId = selectedVehicleId;
      showToast(`🎯 Centered on ${{selectedVehicleId}}`);
    }}

    function filterFleetCategory(cat, btn) {{
      activeCategoryFilter = cat;
      document.querySelectorAll('.fleet-cat-btn').forEach(b => {{
        b.className = 'fleet-cat-btn py-1.5 rounded-xl hover:text-white';
      }});
      btn.className = 'fleet-cat-btn py-1.5 rounded-xl bg-white/15 text-brand-cyan shadow-sm';
      renderFleetList();
    }}

    function setSimWarp(mult, btn) {{
      simSpeedWarp = mult;
      document.querySelectorAll('.warp-btn').forEach(b => b.className = 'warp-btn px-2.5 py-1 rounded-lg hover:text-white');
      btn.className = 'warp-btn px-2.5 py-1 rounded-lg bg-brand-cyan text-black';
      showToast(`⚡ Simulation speed: ${{mult}}×`);
    }}

    // Toggle Ambient Background Video
    function toggleHeroBgVideo() {{
      const vid = document.getElementById('heroBgVideo');
      const txt = document.getElementById('btnToggleBgVideoText');
      if (vid.paused) {{
        vid.play();
        isBgVideoPlaying = true;
        txt.textContent = '🎥 3D Video Active';
        showToast('3D Video Background resumed');
      }} else {{
        vid.pause();
        isBgVideoPlaying = false;
        txt.textContent = '⏸ Video Paused';
        showToast('Video Background paused');
      }}
    }}

    // Payment, Money Select & Coupon
    function openPaymentAndBookingModal() {{
      recalculatePrice();
      startUpiCountdown();
      openModal('paymentBookingModal');
    }}

    function selectMoneyAmount(amount, btn) {{
      selectedMoney = amount;
      document.getElementById('customAmountInput').value = '';
      if (btn) {{
        document.querySelectorAll('.money-chip').forEach(b => {{
          b.className = 'money-chip p-2.5 rounded-xl border border-white/10 bg-white/5 text-zinc-300 hover:border-white/30';
        }});
        btn.className = 'money-chip p-2.5 rounded-xl border border-brand-cyan bg-brand-cyan/20 text-brand-cyan font-black';
      }}
      recalculatePrice();
    }}

    function handleCustomAmount(val) {{
      const num = parseFloat(val);
      if (!isNaN(num) && num > 0) {{
        selectedMoney = num;
        document.querySelectorAll('.money-chip').forEach(b => {{
          b.className = 'money-chip p-2.5 rounded-xl border border-white/10 bg-white/5 text-zinc-300 hover:border-white/30';
        }});
        recalculatePrice();
      }}
    }}

    function quickApplyCoupon(code) {{
      document.getElementById('couponCodeInput').value = code;
      applyCouponCode();
    }}

    function applyCouponCode() {{
      const code = document.getElementById('couponCodeInput').value.trim().toUpperCase();
      if (code === 'CAMPUS10' || code === 'FIRSTRIDE10') {{
        appliedCoupon = 'CAMPUS10';
        showToast('🎉 Coupon CAMPUS10 applied! 10% discount on first ride.');
      }} else if (code === 'FREEFIRST') {{
        appliedCoupon = 'FREEFIRST';
        showToast('🎁 Coupon FREEFIRST applied! 100% Free Single Ride.');
      }} else if (code === '') {{
        appliedCoupon = '';
        showToast('Coupon removed.');
      }} else {{
        showToast('Invalid Coupon. Try CAMPUS10 or FREEFIRST.');
        return;
      }}
      recalculatePrice();
    }}

    function recalculatePrice() {{
      const base = selectedMoney;
      document.getElementById('summaryBasePrice').textContent = `₹${{base.toFixed(2)}}`;

      const studentDisc = base * 0.20;
      document.getElementById('summaryStudentDiscount').textContent = `-₹${{studentDisc.toFixed(2)}}`;

      let afterStudent = Math.max(0, base - studentDisc);
      let couponDisc = 0;

      const couponRow = document.getElementById('summaryCouponRow');
      if (appliedCoupon === 'CAMPUS10') {{
        couponDisc = afterStudent * 0.10;
        couponRow.classList.remove('hidden');
        document.getElementById('summaryCouponLabel').textContent = 'Coupon CAMPUS10 (10% OFF)';
        document.getElementById('summaryCouponDiscount').textContent = `-₹${{couponDisc.toFixed(2)}}`;
      }} else if (appliedCoupon === 'FREEFIRST') {{
        couponDisc = afterStudent;
        couponRow.classList.remove('hidden');
        document.getElementById('summaryCouponLabel').textContent = 'Coupon FREEFIRST (100% OFF)';
        document.getElementById('summaryCouponDiscount').textContent = `-₹${{couponDisc.toFixed(2)}}`;
      }} else {{
        couponRow.classList.add('hidden');
      }}

      const finalPrice = Math.max(0, afterStudent - couponDisc);
      document.getElementById('summaryFinalPrice').textContent = `₹${{finalPrice.toFixed(2)}}`;
      
      const btnText = document.getElementById('btnPayText');
      if (currentPaymentMethod === 'upi') {{
        btnText.textContent = finalPrice === 0 ? "Claim Free Ride (UPI) & Get OTP →" : `I've Paid ₹${{finalPrice.toFixed(2)}} via UPI & Get OTP →`;
      }} else {{
        btnText.textContent = `Confirm Cash Ride (₹${{finalPrice.toFixed(2)}}) & Get OTP →`;
      }}
    }}

    function switchPayTab(tab) {{
      currentPaymentMethod = tab;
      const tabUpi = document.getElementById('payTabUpi');
      const tabCash = document.getElementById('payTabCash');
      const areaUpi = document.getElementById('upiPaymentArea');
      const areaCash = document.getElementById('cashPaymentArea');

      if (tab === 'upi') {{
        tabUpi.className = 'py-2.5 rounded-xl bg-white/15 text-brand-cyan flex items-center justify-center gap-2 shadow-sm transition-all';
        tabCash.className = 'py-2.5 rounded-xl text-zinc-400 hover:text-white flex items-center justify-center gap-2 transition-all';
        areaUpi.classList.remove('hidden');
        areaCash.classList.add('hidden');
      }} else {{
        tabCash.className = 'py-2.5 rounded-xl bg-white/15 text-amber-400 flex items-center justify-center gap-2 shadow-sm transition-all';
        tabUpi.className = 'py-2.5 rounded-xl text-zinc-400 hover:text-white flex items-center justify-center gap-2 transition-all';
        areaUpi.classList.add('hidden');
        areaCash.classList.remove('hidden');
      }}
      recalculatePrice();
    }}

    function copyUpiId() {{
      navigator.clipboard.writeText('campusflow@okaxis');
      showToast('📋 UPI ID copied: campusflow@okaxis');
    }}

    function startUpiCountdown() {{
      clearInterval(upiTimerInterval);
      let sec = 300;
      const timerEl = document.getElementById('upiTimerClock');
      upiTimerInterval = setInterval(() => {{
        sec--;
        if (sec <= 0) {{
          clearInterval(upiTimerInterval);
          sec = 300;
        }}
        const m = String(Math.floor(sec / 60)).padStart(2, '0');
        const s = String(sec % 60).padStart(2, '0');
        if (timerEl) timerEl.textContent = `${{m}}:${{s}}`;
      }}, 1000);
    }}

    function handlePaymentSuccess() {{
      closeModal('paymentBookingModal');
      clearInterval(upiTimerInterval);

      currentTripOtp = String(Math.floor(1000 + Math.random() * 9000));
      isTripStarted = false;
      activeVehicleForTrip = FLEET[Math.floor(Math.random() * FLEET.length)];

      const banner = document.getElementById('activeTripBanner');
      banner.classList.remove('hidden');
      document.getElementById('activeTripVehicleName').textContent = `${{activeVehicleForTrip.name}} (${{activeVehicleForTrip.plate}})`;
      document.getElementById('activeTripOtpBadge').textContent = `OTP: ${{currentTripOtp}}`;
      document.getElementById('activeTripDriverInfo').textContent = `Driver: ${{activeVehicleForTrip.driver}} (${{activeVehicleForTrip.model}})`;

      chatMessages = [
        {{ from: 'driver', text: `Namaste! I am on my way in ${{activeVehicleForTrip.name}} (${{activeVehicleForTrip.plate}}). Please share your 4-digit OTP when boarding.`, time: new Date().toLocaleTimeString([], {{hour: '2-digit', minute:'2-digit'}}) }}
      ];

      launchTransportDashboard();
      showToast(`🎉 Ride Booked with ${{activeVehicleForTrip.driver}}! Your OTP is ${{currentTripOtp}}`);
      setTimeout(() => openDriverChat(), 800);
    }}

    function openDriverChat() {{
      if (!activeVehicleForTrip) {{
        activeVehicleForTrip = FLEET[0];
        currentTripOtp = '7429';
      }}
      document.getElementById('chatDriverName').textContent = `${{activeVehicleForTrip.driver}} (${{activeVehicleForTrip.name}})`;
      document.getElementById('chatOtpDisplay').textContent = currentTripOtp;
      renderChatMessages();
      openModal('driverChatModal');
    }}

    function renderChatMessages() {{
      const box = document.getElementById('chatMessagesBox');
      box.innerHTML = chatMessages.map(m => `
        <div class="flex flex-col ${{m.from === 'user' ? 'items-end' : 'items-start'}}">
          <div class="p-3 rounded-2xl max-w-[82%] ${{m.from === 'user' ? 'bg-brand-cyan text-black font-semibold' : 'bg-white/10 text-white border border-white/10'}} shadow-sm">
            ${{m.text}}
          </div>
          <span class="text-[9px] text-zinc-500 mt-0.5 px-1 font-mono">${{m.time}}</span>
        </div>
      `).join('');
      box.scrollTop = box.scrollHeight;
    }}

    function sendChatMessage() {{
      const inp = document.getElementById('chatMessageInput');
      const text = inp.value.trim();
      if (!text) return;
      inp.value = '';
      executeMessageExchange(text);
    }}

    function sendQuickChatMessage(text) {{
      executeMessageExchange(text);
    }}

    function executeMessageExchange(userText) {{
      const now = new Date().toLocaleTimeString([], {{hour: '2-digit', minute:'2-digit'}});
      chatMessages.push({{ from: 'user', text: userText, time: now }});
      renderChatMessages();

      setTimeout(() => {{
        let reply = "Got it! Keeping the shuttle on track.";
        const low = userText.toLowerCase();

        if (userText.includes(currentTripOtp)) {{
          isTripStarted = true;
          reply = `✅ OTP ${{currentTripOtp}} Verified! Trip started with ${{activeVehicleForTrip.driver}}. Driving safely to destination.`;
          document.getElementById('bannerStatusText').textContent = `🟢 Trip Active with ${{activeVehicleForTrip.driver}} (OTP Verified)`;
          showToast(`✅ OTP ${{currentTripOtp}} Verified by Driver!`);
        }} else if (low.includes('where') || low.includes('location')) {{
          reply = "I am approaching your pickup stop now. Estimated 2 minutes.";
        }} else if (low.includes('wait') || low.includes('minute')) {{
          reply = "Sure, I will wait 2 minutes at the stop point.";
        }} else if (low.includes('gate') || low.includes('here')) {{
          reply = "Understood. See you at the gate.";
        }}

        chatMessages.push({{ from: 'driver', text: reply, time: new Date().toLocaleTimeString([], {{hour: '2-digit', minute:'2-digit'}}) }});
        renderChatMessages();
      }}, 800);
    }}

    function closeModal(id) {{
      document.getElementById(id).classList.add('hidden');
      document.getElementById(id).classList.remove('grid');
    }}
    function openModal(id) {{
      document.getElementById(id).classList.remove('hidden');
      document.getElementById(id).classList.add('grid');
      lucide.createIcons();
    }}

    function openFarePassesModal() {{
      document.getElementById('fareCardsGrid').innerHTML = FARES.map(f => `
        <div class="p-4 rounded-2xl bg-white/5 border border-white/10 space-y-2">
          <span class="text-3xl">${{f.emoji}}</span>
          <h4 class="text-sm font-black text-white">${{f.name}}</h4>
          <p class="text-[11px] text-zinc-400">${{f.desc}}</p>
          <div class="text-lg font-black text-brand-cyan">₹${{f.price}}</div>
          <button onclick="selectMoneyAmount(${{f.price}}, null); closeModal('farePassesModal'); openPaymentAndBookingModal();" class="w-full py-2 rounded-xl bg-brand-cyan text-black font-extrabold text-xs">Buy / Pay</button>
        </div>
      `).join('');
      openModal('farePassesModal');
    }}

    function openH4StressModal() {{
      document.getElementById('stressSelectVehicle').innerHTML = FLEET.map(v => `<option value="${{v.id}}">${{v.emoji}} ${{v.name}} (${{v.driver}})</option>`).join('');
      openModal('h4StressModal');
    }}

    function triggerBlackoutOnSelected() {{
      const id = document.getElementById('stressSelectVehicle').value;
      const v = FLEET.find(x => x.id === id);
      if (v) {{
        v.blackoutTimer = 120.0;
        closeModal('h4StressModal');
        showToast(`🛰️ ${{v.name}}: 2-minute blackout active. Dead-reckon ETA running!`);
        renderFleetList();
      }}
    }}

    function triggerJamOnSelected() {{
      const id = document.getElementById('stressSelectVehicle').value;
      const v = FLEET.find(x => x.id === id);
      if (v) {{
        v.jamTimer = 90.0;
        closeModal('h4StressModal');
        showToast(`🚧 Traffic delay injected on ${{v.name}}`);
        renderFleetList();
      }}
    }}

    function showLandingPage() {{
      document.getElementById('landingHeroSection').classList.remove('hidden');
      document.getElementById('mainTransportDashboard').classList.add('hidden');
    }}

    function launchTransportDashboard() {{
      document.getElementById('landingHeroSection').classList.add('hidden');
      document.getElementById('mainTransportDashboard').classList.remove('hidden');

      if (!map) {{
        initRoutesAndFleet();
        initCampusMap();
        startSimulationEngine();
      }}
      setTimeout(() => map && map.invalidateSize(), 80);
      renderFleetList();
    }}

    function handleUserSignUp() {{
      const name = document.getElementById('suFullName').value;
      const email = document.getElementById('suEmail').value;
      currentUser = {{ name, email }};
      localStorage.setItem('cf_user', JSON.stringify(currentUser));
      updateUserAccountPill();
      showToast(`Welcome, ${{name}}! Launching live transport...`);
      setTimeout(launchTransportDashboard, 600);
    }}

    function handleGoogleSignIn() {{
      currentUser = {{ name: "Aarav Sharma", email: "aarav.sharma@campus.edu" }};
      localStorage.setItem('cf_user', JSON.stringify(currentUser));
      updateUserAccountPill();
      showToast(`Welcome, Aarav! Signed in with Google.`);
      setTimeout(launchTransportDashboard, 600);
    }}

    function handleGuestDirectAccess() {{
      currentUser = {{ name: "Guest Commuter", email: "guest@campus.edu" }};
      localStorage.setItem('cf_user', JSON.stringify(currentUser));
      updateUserAccountPill();
      showToast("Exploring live campus transport as guest...");
      launchTransportDashboard();
    }}

    function togglePasswordVisibility(fieldId) {{
      const f = document.getElementById(fieldId);
      f.type = f.type === 'password' ? 'text' : 'password';
    }}

    function setCommuteMode(mode, btn) {{
      document.querySelectorAll('.commute-chip').forEach(b => {{
        b.className = 'commute-chip p-2 rounded-xl border border-white/10 bg-white/5 text-zinc-300 flex items-center justify-center gap-1';
      }});
      btn.className = 'commute-chip p-2 rounded-xl border border-brand-cyan bg-brand-cyan/20 text-brand-cyan flex items-center justify-center gap-1';
      showToast(`Default preference: ${{mode.toUpperCase()}}`);
    }}

    function updateUserAccountPill() {{
      const pill = document.getElementById('userAccountPill');
      if (currentUser) {{
        pill.textContent = `👤 ${{currentUser.name.split(' ')[0]}}`;
        pill.onclick = () => {{
          if (confirm('Sign out from Campus Flow?')) {{
            currentUser = null;
            localStorage.removeItem('cf_user');
            updateUserAccountPill();
            showLandingPage();
          }}
        }};
      }} else {{
        pill.textContent = 'Sign Up / Login';
        pill.onclick = showLandingPage;
      }}
    }}

    let toastT;
    function showToast(msg) {{
      const t = document.getElementById('toast');
      document.getElementById('toastMsg').textContent = msg;
      t.classList.remove('translate-y-24', 'opacity-0', 'pointer-events-none');
      clearTimeout(toastT);
      toastT = setTimeout(hideToast, 3500);
      lucide.createIcons();
    }}
    function hideToast() {{
      document.getElementById('toast').classList.add('translate-y-24', 'opacity-0', 'pointer-events-none');
    }}

    function startSimulationEngine() {{
      setInterval(() => {{
        const dt = 0.05 * simSpeedWarp;
        simTime += dt;
        FLEET.forEach(v => stepFleetSimulation(v, dt));

        FLEET.forEach(v => {{
          v.disp = mod(v.disp + wrapD(v.est.s - v.disp, v.R.totalLength) * 0.15, v.R.totalLength);
          const pos = getPositionAtS(v.R, v.disp);
          if (vehicleMarkers[v.id]) {{
            vehicleMarkers[v.id].setLatLng(pos.ll);
            const needle = document.getElementById(`vneedle_${{v.id}}`);
            if (needle) needle.style.transform = `rotate(${{pos.hd}}deg)`;
          }}
        }});

        if (followingVehicleId) {{
          const v = FLEET.find(x => x.id === followingVehicleId);
          if (v && map) {{
            const pos = getPositionAtS(v.R, v.disp);
            map.panTo(pos.ll, {{ animate: true, duration: 0.2 }});
          }}
        }}
      }}, 50);

      setInterval(renderFleetList, 1000);
    }}

    document.addEventListener('click', e => {{
      const spark = document.createElement('div');
      spark.className = 'click-spark';
      spark.style.left = `${{e.clientX - 7}}px`;
      spark.style.top = `${{e.clientY - 7}}px`;
      document.body.appendChild(spark);
      setTimeout(() => spark.remove(), 500);

      const btn = e.target.closest('.btn-gradient');
      if (btn) {{
        const rect = btn.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const rip = document.createElement('span');
        rip.className = 'ripple';
        rip.style.width = rip.style.height = `${{size}}px`;
        rip.style.left = `${{e.clientX - rect.left - size / 2}}px`;
        rip.style.top = `${{e.clientY - rect.top - size / 2}}px`;
        btn.appendChild(rip);
        setTimeout(() => rip.remove(), 600);
      }}
    }});

    window.addEventListener('DOMContentLoaded', () => {{
      // Canvas loop removed as requested
      updateUserAccountPill();

      document.getElementById('mapLayerThemeSelect').addEventListener('change', e => {{
        setMapTheme(e.target.value);
      }});

      document.getElementById('transitSearchInput').addEventListener('input', renderFleetList);

      lucide.createIcons();
    }});
  </script>
</body>
</html>
'''

with open('index.html', 'w') as f:
    f.write(html_content)

print("Generated updated index.html with live video background in the front of sign-up page.")

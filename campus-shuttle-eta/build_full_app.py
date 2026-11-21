# build_full_app.py
import os

with open('qr_base64.txt') as f:
    qr_b64 = f.read().strip()

# We read parts or construct cleanly
app_code = r'''<!DOCTYPE html>
<html lang="en" class="dark scroll-smooth">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Campus Flow — Smart Shuttle, Smart Campus (Real-Time Predictive ETA)</title>

  <!-- Tailwind CSS & Lucide Icons -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['Inter', '"Plus Jakarta Sans"', 'system-ui', '-apple-system', 'sans-serif'],
            display: ['Space Grotesk', 'Inter', 'sans-serif'],
            mono: ['JetBrains Mono', 'ui-monospace', 'Menlo', 'Consolas', 'monospace']
          },
          colors: {
            brand: {
              cyan: '#00f0ff',
              violet: '#a855f7',
              purple: '#6366f1',
              emerald: '#10b981',
              amber: '#f59e0b',
              rose: '#f43f5e'
            }
          },
          keyframes: {
            glowPulse: {
              '0%, 100%': { opacity: '0.4', transform: 'scale(1)' },
              '50%': { opacity: '0.8', transform: 'scale(1.06)' }
            },
            float3D: {
              '0%, 100%': { transform: 'translateY(0px)' },
              '50%': { transform: 'translateY(-6px)' }
            },
            wiggle: {
              '0%, 100%': { transform: 'rotate(-3deg)' },
              '50%': { transform: 'rotate(3deg)' }
            },
            popIn: {
              '0%': { opacity: '0', transform: 'scale(0.8) translateY(10px)' },
              '100%': { opacity: '1', transform: 'scale(1) translateY(0)' }
            }
          },
          animation: {
            'glow-pulse': 'glowPulse 4s ease-in-out infinite',
            'float-3d': 'float3D 3.5s ease-in-out infinite',
            'wiggle': 'wiggle 2s ease-in-out infinite',
            'pop-in': 'popIn 0.3s cubic-bezier(0.16, 1, 0.3, 1)'
          }
        }
      }
    }
  </script>

  <!-- Google Fonts: Inter + Space Grotesk + JetBrains Mono (from reference) + Plus Jakarta Sans -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;500;600&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">

  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>

  <!-- Three.js for Kinetic Particle Hero -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>

  <!-- Leaflet CSS & JS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

  <style>
    body {
      background-color: #05070e;
      color: #f1f5f9;
      overflow-x: hidden;
    }
    
    /* Glassmorphism Classes matching shadcn/ui dark aesthetic */
    .glass-panel {
      background: rgba(13, 17, 34, 0.75);
      backdrop-filter: blur(20px);
      -webkit-backdrop-filter: blur(20px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
    }
    .glass-card {
      background: rgba(255, 255, 255, 0.03);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.08);
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .glass-card:hover {
      background: rgba(255, 255, 255, 0.06);
      border-color: rgba(0, 240, 255, 0.35);
      transform: translateY(-2px);
    }
    .glass-input {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.12);
      transition: all 0.2s ease;
    }
    .glass-input:focus {
      border-color: #00f0ff;
      box-shadow: 0 0 15px rgba(0, 240, 255, 0.25);
      outline: none;
    }

    /* Buttons with Micro-interactions */
    .btn-gradient {
      background: linear-gradient(135deg, #00f0ff 0%, #6366f1 50%, #a855f7 100%);
      transition: all 0.25s ease;
      position: relative;
      overflow: hidden;
    }
    .btn-gradient:hover {
      transform: translateY(-2px) scale(1.02);
      box-shadow: 0 10px 25px rgba(0, 240, 255, 0.4);
    }
    .btn-gradient:active {
      transform: translateY(0) scale(0.98);
    }

    /* Button Ripple */
    .ripple {
      position: absolute;
      border-radius: 50%;
      background: rgba(255, 255, 255, 0.5);
      transform: scale(0);
      animation: rippleEffect 0.6s linear;
      pointer-events: none;
    }
    @keyframes rippleEffect {
      to {
        transform: scale(4);
        opacity: 0;
      }
    }

    /* Click Spark */
    .click-spark {
      position: fixed;
      width: 14px;
      height: 14px;
      border-radius: 50%;
      background: #00f0ff;
      pointer-events: none;
      z-index: 99999;
      transform: scale(1);
      animation: sparkAnim 0.5s ease-out forwards;
      box-shadow: 0 0 12px #00f0ff, 0 0 20px #a855f7;
    }
    @keyframes sparkAnim {
      to {
        transform: scale(3.5);
        opacity: 0;
      }
    }

    
    /* Leaflet Dark HUD Popup Styling */
    .leaflet-popup-content-wrapper {
      background: rgba(11, 15, 30, 0.96) !important;
      backdrop-filter: blur(24px) !important;
      -webkit-backdrop-filter: blur(24px) !important;
      border: 1px solid rgba(0, 240, 255, 0.35) !important;
      border-radius: 20px !important;
      color: #f1f5f9 !important;
      box-shadow: 0 20px 45px rgba(0, 0, 0, 0.75), 0 0 20px rgba(0, 240, 255, 0.25) !important;
      padding: 0 !important;
      overflow: hidden;
    }
    .leaflet-popup-content {
      margin: 0 !important;
      line-height: 1.4 !important;
    }
    .leaflet-popup-tip {
      background: rgba(11, 15, 30, 0.96) !important;
      border: 1px solid rgba(0, 240, 255, 0.35) !important;
    }
    .leaflet-container a.leaflet-popup-close-button {
      color: #94a3b8 !important;
      padding: 8px 10px !important;
      font-size: 16px !important;
    }
    .leaflet-container a.leaflet-popup-close-button:hover {
      color: #00f0ff !important;
    }

    /* Custom Leaflet Markers */
    .pulse-marker-icon {
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .bus-marker-3d {
      width: 38px;
      height: 38px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 0 20px rgba(0, 240, 255, 0.6);
      border: 2px solid #ffffff;
      font-weight: 800;
      position: relative;
      transition: transform 0.2s ease;
    }
    .bus-heading-needle {
      position: absolute;
      top: -6px;
      width: 0;
      height: 0;
      border-left: 5px solid transparent;
      border-right: 5px solid transparent;
      border-bottom: 8px solid #00f0ff;
      transform-origin: 50% 25px;
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: rgba(0, 0, 0, 0.2);
    }
    ::-webkit-scrollbar-thumb {
      background: rgba(255, 255, 255, 0.15);
      border-radius: 9999px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: rgba(0, 240, 255, 0.5);
    }

    /* Hero Background Video */
    .hero-video-container {
      position: absolute;
      inset: 0;
      width: 100%;
      height: 100%;
      overflow: hidden;
      z-index: 0;
      pointer-events: none;
    }
    .bg-video {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      min-width: 100%;
      min-height: 100%;
      width: auto;
      height: auto;
      object-fit: cover;
      filter: brightness(0.9) contrast(1.15);
      transition: opacity 0.8s ease;
    }

    /* Speech Bubble Triangle */
    .speech-bubble-tail::after {
      content: '';
      position: absolute;
      bottom: -8px;
      right: 28px;
      width: 0;
      height: 0;
      border-left: 8px solid transparent;
      border-right: 8px solid transparent;
      border-top: 8px solid rgba(13, 17, 34, 0.95);
    }

    /* Holographic Smart Card */
    .hologram-card {
      background: linear-gradient(135deg, rgba(20, 27, 54, 0.95) 0%, rgba(35, 18, 59, 0.95) 50%, rgba(10, 37, 54, 0.95) 100%);
      border: 1px solid rgba(255, 255, 255, 0.15);
      position: relative;
      overflow: hidden;
    }
    .hologram-card::before {
      content: '';
      position: absolute;
      top: -50%;
      left: -50%;
      width: 200%;
      height: 200%;
      background: radial-gradient(circle, rgba(0, 240, 255, 0.15) 0%, transparent 60%);
      transform: rotate(30deg);
      pointer-events: none;
    }
  </style>
</head>
<body class="min-h-screen flex flex-col antialiased selection:bg-brand-cyan selection:text-black">

  <!-- ================= TOP NAVIGATION BAR ================= -->
  <header class="sticky top-0 z-50 backdrop-blur-xl bg-[#070913]/90 border-b border-white/10 px-4 sm:px-6 lg:px-8 h-[72px] flex items-center justify-between transition-all">
    <div class="flex items-center justify-between w-full max-w-7xl mx-auto">
      
      <!-- Brand Logo -->
      <a href="#" onclick="showLandingPage(); window.scrollTo({top:0, behavior:'smooth'});" class="flex items-center gap-3 font-extrabold text-xl tracking-tight text-white group">
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

      <!-- Center Links (Clean & Public) -->
      <nav class="hidden md:flex items-center gap-1 text-sm font-semibold text-zinc-300">
        <button onclick="showLandingPage(); window.scrollTo({top:0, behavior:'smooth'});" class="px-3.5 py-1.5 rounded-xl hover:text-white hover:bg-white/5 transition-colors font-bold">Home</button>
        <button onclick="scrollToLandingSection('systemOverviewSection')" class="px-3.5 py-1.5 rounded-xl hover:text-white hover:bg-white/5 transition-colors font-bold text-brand-cyan">Overview</button>
        <button onclick="scrollToLandingSection('aboutUsSection')" class="px-3.5 py-1.5 rounded-xl hover:text-white hover:bg-white/5 transition-colors font-bold">About Us</button>
        <button onclick="scrollToLandingSection('faqSection')" class="px-3.5 py-1.5 rounded-xl hover:text-white hover:bg-white/5 transition-colors font-bold">Q&A</button>
      </nav>

      <!-- Right Actions -->
      <div class="flex items-center gap-2.5">
        


        <!-- Wallet Button with Live Balance (Visible only after login) -->
        <button id="navWalletBtn" onclick="openWalletModal()" class="hidden inline-flex items-center gap-2 px-3 py-1.5 rounded-xl bg-gradient-to-r from-brand-cyan/15 to-brand-purple/15 hover:from-brand-cyan/25 hover:to-brand-purple/25 border border-brand-cyan/30 text-xs font-bold text-white transition-all shadow-sm">
          <span class="text-brand-cyan">💳</span>
          <span class="hidden sm:inline text-zinc-300">Wallet:</span>
          <span id="navWalletBalance" class="text-brand-cyan font-black">₹240.00</span>
        </button>

        <!-- WAYZEN Quick AI Trigger -->
        <button onclick="toggleWayzenChat()" class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-purple-500/15 hover:bg-purple-500/25 border border-purple-500/30 text-xs font-bold text-purple-300 transition-all">
          <span class="animate-bounce text-sm">🤖</span>
          <span class="hidden sm:inline">WAYZEN AI</span>
        </button>

        <!-- Sign Up / Login Pill -->
        <button id="userAccountPill" onclick="showLandingPage(); window.scrollTo({top:0, behavior:'smooth'});" class="px-3.5 py-1.5 rounded-xl bg-gradient-to-r from-brand-cyan to-brand-purple text-black font-extrabold text-xs tracking-wide shadow-lg shadow-brand-cyan/25 hover:opacity-95 transition-all">
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

  <!-- ================= LANDING PAGE WRAPPER ================= -->
  <div id="landingPageWrapper" class="flex flex-col">

    <!-- ================= 1. HERO SECTION WITH VIDEO ================= -->
    <section id="landingHeroSection" class="relative min-h-[calc(100vh-72px)] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8 overflow-hidden">
      
      <!-- Video Background (Seamlessly playing in hero, no navigation button) -->
      <div class="hero-video-container">
        <video id="heroBgVideo" autoplay loop muted playsinline class="bg-video">
          <source src="campus-flow-bg.mp4" type="video/mp4">
        </video>
        <!-- Dark gradient vignette overlay for perfect contrast -->
        <div class="absolute inset-0 bg-gradient-to-r from-[#05070e]/95 via-[#05070e]/75 to-[#05070e]/90 z-[1]"></div>
      </div>

      <!-- Ambient Glow Spotlights -->
      <div class="absolute -top-32 -left-32 w-96 h-96 bg-brand-cyan/20 rounded-full blur-[120px] pointer-events-none z-[2]"></div>
      <div class="absolute -bottom-32 -right-32 w-96 h-96 bg-brand-purple/20 rounded-full blur-[120px] pointer-events-none z-[2]"></div>

      <div class="relative z-10 w-full max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-center">
        
        <!-- Left Hero Content -->
        <div class="lg:col-span-7 space-y-6 text-left">
          
          <!-- Mode Tag -->
          <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-brand-cyan/10 border border-brand-cyan/30 text-brand-cyan text-xs font-bold tracking-wide animate-glow-pulse">
            <span class="w-2 h-2 rounded-full bg-brand-cyan animate-ping"></span>
            Campus Transit: Buses 🚌 • Auto Rickshaws 🛺 • Eco EVs ⚡
          </div>

          <!-- Headline -->
          <div class="space-y-2">
            <h1 class="text-4xl sm:text-6xl xl:text-7xl font-black tracking-tight text-white leading-none">
              Next Stop: <br>
              <span class="bg-gradient-to-r from-brand-cyan via-brand-purple to-brand-violet bg-clip-text text-transparent">
                Your Campus.
              </span>
            </h1>
            <p class="text-xl sm:text-2xl font-bold text-zinc-200">
              Track. Plan. Arrive On Time.
            </p>
          </div>

          <!-- Subtitle -->
          <p class="text-sm sm:text-base text-zinc-300 max-w-xl font-normal leading-relaxed">
            Real-time shuttle tracking with AI-powered predictive ETA, even when GPS goes silent. Multi-modal campus transport with Indian drivers, live UPI QR payment & verified driver OTP security.
          </p>

          <!-- Feature Pills -->
          <div class="flex flex-wrap items-center gap-3 pt-2">
            <div class="glass-card px-3.5 py-2 rounded-2xl flex items-center gap-2 text-xs font-bold text-zinc-200">
              <i data-lucide="target" class="w-4 h-4 text-brand-cyan"></i>
              Smart Route Matching
            </div>
            <div class="glass-card px-3.5 py-2 rounded-2xl flex items-center gap-2 text-xs font-bold text-zinc-200">
              <i data-lucide="clock" class="w-4 h-4 text-brand-amber"></i>
              Accurate ETA (±2 min)
            </div>
            <div class="glass-card px-3.5 py-2 rounded-2xl flex items-center gap-2 text-xs font-bold text-zinc-200">
              <i data-lucide="bell" class="w-4 h-4 text-brand-emerald"></i>
              Delay Alerts
            </div>
          </div>

          <!-- Quick Live Vehicle Mini-Cards -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2">
            <div class="glass-panel p-3 rounded-2xl text-left border-l-4 border-l-blue-400">
              <span class="text-lg">🚌</span>
              <p class="text-[11px] font-bold text-zinc-400">Shuttle #1</p>
              <p class="text-sm font-black text-brand-cyan" id="heroEtaShuttle1">ETA: 4 min</p>
            </div>
            <div class="glass-panel p-3 rounded-2xl text-left border-l-4 border-l-emerald-400">
              <span class="text-lg">🛺</span>
              <p class="text-[11px] font-bold text-zinc-400">Auto #2</p>
              <p class="text-sm font-black text-emerald-400" id="heroEtaAuto2">ETA: 2 min</p>
            </div>
            <div class="glass-panel p-3 rounded-2xl text-left border-l-4 border-l-amber-400">
              <span class="text-lg">⚡</span>
              <p class="text-[11px] font-bold text-zinc-400">EV Cart #3</p>
              <p class="text-sm font-black text-brand-amber" id="heroEtaEv3">ETA: 5 min</p>
            </div>
            <div class="glass-panel p-3 rounded-2xl text-left border-l-4 border-l-purple-400">
              <span class="text-lg">🚌</span>
              <p class="text-[11px] font-bold text-zinc-400">Express #4</p>
              <p class="text-sm font-black text-purple-400" id="heroEtaExpress4">ETA: 3 min</p>
            </div>
          </div>



        </div>

        <!-- Right Hero Auth Card (Dual Mode: Sign Up & Sign In) -->
        <div class="lg:col-span-5 w-full">
          <div class="glass-panel p-6 sm:p-8 rounded-3xl border border-white/15 shadow-2xl relative overflow-hidden backdrop-blur-2xl">
            
            <!-- Top Branding Header -->
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-brand-cyan to-brand-purple flex items-center justify-center text-black font-black">
                  <i data-lucide="navigation-2" class="w-5 h-5 fill-black"></i>
                </div>
                <div>
                  <h3 class="text-sm font-black text-white">Campus Flow</h3>
                  <p class="text-[10px] text-zinc-400">Your Campus Shuttle Companion</p>
                </div>
              </div>
              <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-brand-cyan/15 text-brand-cyan border border-brand-cyan/30">
                STU-AUTH v2.1
              </span>
            </div>

            <!-- Segmented Pill Switcher (Sign Up vs Sign In) -->
            <div class="grid grid-cols-2 p-1 rounded-2xl bg-black/40 border border-white/10 mb-4 text-xs font-black">
              <button type="button" id="tabBtnSignUp" onclick="switchHeroAuthMode('signup')" class="py-2 rounded-xl transition-all bg-gradient-to-r from-brand-cyan to-brand-purple text-black shadow-md flex items-center justify-center gap-1.5">
                <span>Create Account</span>
              </button>
              <button type="button" id="tabBtnLogin" onclick="switchHeroAuthMode('login')" class="py-2 rounded-xl transition-all text-zinc-400 hover:text-white flex items-center justify-center gap-1.5">
                <span>Sign In</span>
              </button>
            </div>

            <!-- ================= VIEW 1: SIGN UP ================= -->
            <div id="heroSignUpSection">
              <div class="mb-4">
                <h2 class="text-xl sm:text-2xl font-black text-white tracking-tight">Create Account</h2>
                <p class="text-xs text-zinc-400 mt-0.5">Join thousands of students riding smarter!</p>
              </div>

              <form id="heroSignUpForm" onsubmit="event.preventDefault(); handleUserSignUp();" class="space-y-3 pt-1">
                <!-- Full Name -->
                <div class="relative">
                  <i data-lucide="user" class="w-4 h-4 text-zinc-400 absolute left-3.5 top-1/2 -translate-y-1/2"></i>
                  <input type="text" id="suFullName" required placeholder="Full Name (e.g. Aarav Sharma)" oninput="previewUserName(this.value)" class="glass-input w-full pl-10 pr-4 py-2.5 rounded-xl text-xs font-semibold text-white placeholder-zinc-500">
                </div>

                <!-- University Email -->
                <div class="relative">
                  <i data-lucide="mail" class="w-4 h-4 text-zinc-400 absolute left-3.5 top-1/2 -translate-y-1/2"></i>
                  <input type="email" id="suEmail" required placeholder="University Email (e.g. rollno@uni.edu.in)" class="glass-input w-full pl-10 pr-4 py-2.5 rounded-xl text-xs font-semibold text-white placeholder-zinc-500">
                </div>

                <!-- Student ID -->
                <div class="relative">
                  <i data-lucide="credit-card" class="w-4 h-4 text-zinc-400 absolute left-3.5 top-1/2 -translate-y-1/2"></i>
                  <input type="text" id="suStudentId" placeholder="Student ID / Roll No. (e.g. 2024-CSE-089)" class="glass-input w-full pl-10 pr-4 py-2.5 rounded-xl text-xs font-semibold text-white placeholder-zinc-500">
                </div>

                <!-- Password -->
                <div class="relative">
                  <i data-lucide="lock" class="w-4 h-4 text-zinc-400 absolute left-3.5 top-1/2 -translate-y-1/2"></i>
                  <input type="password" id="suPassword" required placeholder="Password" class="glass-input w-full pl-10 pr-10 py-2.5 rounded-xl text-xs font-semibold text-white placeholder-zinc-500">
                  <button type="button" onclick="togglePasswordVisibility('suPassword')" class="absolute right-3.5 top-1/2 -translate-y-1/2 text-zinc-400 hover:text-white">
                    <i data-lucide="eye" class="w-4 h-4"></i>
                  </button>
                </div>

                <!-- Confirm Password -->
                <div class="relative">
                  <i data-lucide="lock" class="w-4 h-4 text-zinc-400 absolute left-3.5 top-1/2 -translate-y-1/2"></i>
                  <input type="password" id="suConfirmPassword" required placeholder="Confirm Password" class="glass-input w-full pl-10 pr-10 py-2.5 rounded-xl text-xs font-semibold text-white placeholder-zinc-500">
                  <button type="button" onclick="togglePasswordVisibility('suConfirmPassword')" class="absolute right-3.5 top-1/2 -translate-y-1/2 text-zinc-400 hover:text-white">
                    <i data-lucide="eye" class="w-4 h-4"></i>
                  </button>
                </div>

                <!-- Favorite Commute Mode Chips -->
                <div class="pt-1">
                  <label class="block text-[10px] font-bold uppercase tracking-wider text-zinc-400 mb-1.5">
                    Favorite Mode of Commute
                  </label>
                  <div class="grid grid-cols-3 gap-2">
                    <button type="button" onclick="setCommuteMode('bus', this)" class="commute-chip py-1.5 px-2 rounded-xl text-[11px] font-bold border border-brand-cyan bg-brand-cyan/15 text-brand-cyan text-center">
                      🚌 Shuttles
                    </button>
                    <button type="button" onclick="setCommuteMode('auto', this)" class="commute-chip py-1.5 px-2 rounded-xl text-[11px] font-bold border border-white/10 bg-white/5 text-zinc-300 hover:border-white/30 text-center">
                      🛺 Rickshaws
                    </button>
                    <button type="button" onclick="setCommuteMode('ev', this)" class="commute-chip py-1.5 px-2 rounded-xl text-[11px] font-bold border border-white/10 bg-white/5 text-zinc-300 hover:border-white/30 text-center">
                      ⚡ Eco EVs
                    </button>
                  </div>
                </div>

                <!-- Terms Checkbox -->
                <div class="flex items-center gap-2 pt-1">
                  <input type="checkbox" id="termsCheck" required class="rounded accent-brand-cyan bg-white/10 border-white/20">
                  <label for="termsCheck" class="text-[11px] text-zinc-400">
                    I agree to the <a href="#" class="text-brand-cyan hover:underline">Terms of Service</a> & <a href="#" class="text-brand-cyan hover:underline">Privacy Policy</a>
                  </label>
                </div>

                <!-- Sign Up Submit Button -->
                <button type="submit" id="suSubmitBtn" class="btn-gradient w-full py-3 rounded-xl text-black font-black text-xs uppercase tracking-wider flex items-center justify-center gap-2 mt-2 shadow-lg shadow-brand-cyan/20">
                  <span>Sign Up & Launch Dashboard</span>
                  <i data-lucide="arrow-right" class="w-4 h-4"></i>
                </button>

                <div class="relative flex items-center justify-center my-3">
                  <div class="border-t border-white/10 w-full"></div>
                  <span class="bg-[#0b0f20] px-3 text-[10px] text-zinc-500 uppercase tracking-widest absolute">or</span>
                </div>

                <!-- Google Auth -->
                <button type="button" onclick="handleGoogleSignIn()" class="w-full py-2.5 rounded-xl border border-white/15 bg-white/5 hover:bg-white/10 text-white font-bold text-xs flex items-center justify-center gap-2.5 transition-all">
                  <svg class="w-4 h-4" viewBox="0 0 24 24">
                    <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                    <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                    <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
                    <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
                  </svg>
                  Continue with Google
                </button>

                <div class="pt-2 text-center">
                  <p class="text-xs text-zinc-400">
                    Already have an account? 
                    <button type="button" onclick="switchHeroAuthMode('login')" class="text-brand-cyan hover:underline font-bold ml-1">
                      Sign In →
                    </button>
                  </p>
                </div>

                <button type="button" onclick="handleGuestDirectAccess()" class="w-full py-2 text-center text-xs text-brand-cyan hover:underline font-bold">
                  ⚡ Guest Mode: Explore Live Campus Transport Instantly →
                </button>
              </form>
            </div>

            <!-- ================= VIEW 2: LOGIN ================= -->
            <div id="heroLoginSection" class="hidden">
              <div class="mb-4">
                <h2 class="text-xl sm:text-2xl font-black text-white tracking-tight">Welcome Back</h2>
                <p class="text-xs text-zinc-400 mt-0.5">Sign in to access your campus transit & wallet!</p>
              </div>

              <form id="heroLoginForm" onsubmit="event.preventDefault(); handleUserLogin();" class="space-y-3.5 pt-1">
                <!-- University Email -->
                <div class="relative">
                  <i data-lucide="mail" class="w-4 h-4 text-zinc-400 absolute left-3.5 top-1/2 -translate-y-1/2"></i>
                  <input type="email" id="liEmail" required placeholder="University Email (e.g. rollno@uni.edu.in)" class="glass-input w-full pl-10 pr-4 py-2.5 rounded-xl text-xs font-semibold text-white placeholder-zinc-500">
                </div>

                <!-- Password -->
                <div class="relative">
                  <i data-lucide="lock" class="w-4 h-4 text-zinc-400 absolute left-3.5 top-1/2 -translate-y-1/2"></i>
                  <input type="password" id="liPassword" required placeholder="Password" class="glass-input w-full pl-10 pr-10 py-2.5 rounded-xl text-xs font-semibold text-white placeholder-zinc-500">
                  <button type="button" onclick="togglePasswordVisibility('liPassword')" class="absolute right-3.5 top-1/2 -translate-y-1/2 text-zinc-400 hover:text-white">
                    <i data-lucide="eye" class="w-4 h-4"></i>
                  </button>
                </div>

                <div class="flex items-center justify-between text-xs pt-1">
                  <label class="flex items-center gap-2 text-zinc-400 cursor-pointer">
                    <input type="checkbox" id="liRemember" checked class="rounded accent-brand-cyan bg-white/10 border-white/20">
                    <span>Remember me</span>
                  </label>
                  <a href="#" onclick="showToast('Password reset link sent to registered email!')" class="text-brand-cyan hover:underline text-[11px] font-bold">Forgot password?</a>
                </div>

                <!-- Sign In Submit Button -->
                <button type="submit" id="liSubmitBtn" class="btn-gradient w-full py-3 rounded-xl text-black font-black text-xs uppercase tracking-wider flex items-center justify-center gap-2 mt-2 shadow-lg shadow-brand-cyan/20">
                  <span>Sign In & Open Dashboard</span>
                  <i data-lucide="arrow-right" class="w-4 h-4"></i>
                </button>

                <div class="relative flex items-center justify-center my-3">
                  <div class="border-t border-white/10 w-full"></div>
                  <span class="bg-[#0b0f20] px-3 text-[10px] text-zinc-500 uppercase tracking-widest absolute">or</span>
                </div>

                <!-- Google Auth -->
                <button type="button" onclick="handleGoogleSignIn()" class="w-full py-2.5 rounded-xl border border-white/15 bg-white/5 hover:bg-white/10 text-white font-bold text-xs flex items-center justify-center gap-2.5 transition-all">
                  <svg class="w-4 h-4" viewBox="0 0 24 24">
                    <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                    <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                    <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
                    <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
                  </svg>
                  Continue with Google
                </button>

                <div class="pt-2 text-center">
                  <p class="text-xs text-zinc-400">
                    Don't have an account? 
                    <button type="button" onclick="switchHeroAuthMode('signup')" class="text-brand-cyan hover:underline font-bold ml-1">
                      Create Account →
                    </button>
                  </p>
                </div>

                <button type="button" onclick="handleGuestDirectAccess()" class="w-full py-2 text-center text-xs text-brand-cyan hover:underline font-bold">
                  ⚡ Guest Mode: Explore Live Campus Transport Instantly →
                </button>
              </form>
            </div>

          </div>
        </div>

      </div>
    </section>

        <!-- ================= 2. SYSTEM OVERVIEW SECTION ================= -->
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

    <!-- ================= 3. ABOUT US PORTAL ================= -->
    <section id="aboutUsSection" class="py-20 px-4 sm:px-6 lg:px-8 border-t border-white/10 bg-[#090d1e] relative z-10">
      <div class="max-w-7xl mx-auto space-y-12">
        
        <!-- Header -->
        <div class="text-center max-w-3xl mx-auto space-y-4">
          <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-brand-cyan/10 border border-brand-cyan/30 text-brand-cyan text-xs font-bold uppercase tracking-wider">
            <i data-lucide="info" class="w-3.5 h-3.5"></i>
            About Campus Flow • University Smart Mobility
          </div>
          <h2 class="text-3xl sm:text-5xl font-black text-white tracking-tight">
            Revolutionizing University Transit with <span class="bg-gradient-to-r from-brand-cyan to-brand-purple bg-clip-text text-transparent">AI & Clean Energy</span>
          </h2>
          <p class="text-sm sm:text-base text-zinc-400 leading-relaxed">
            Built by students, for students. Campus Flow eliminates the anxiety of missed 8:30 AM lectures, crowded shuttle stops, and unpredictable campus transport. By pairing mathematical dead-reckoning with an eco-conscious multimodal fleet, we ensure every student arrives on time, safely.
          </p>
        </div>

        <!-- 4 Pillars Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          
          <!-- Pillar 1 -->
          <div class="glass-panel p-6 rounded-3xl space-y-4 border border-white/10 hover:border-brand-cyan/40 transition-all">
            <div class="w-12 h-12 rounded-2xl bg-brand-cyan/15 border border-brand-cyan/30 flex items-center justify-center text-brand-cyan text-2xl font-black">
              🛰️
            </div>
            <h3 class="text-lg font-black text-white">Dead-Reckoning AI</h3>
            <p class="text-xs text-zinc-400 leading-relaxed">
              When monsoon tree canopy or hostel basements choke GPS signals, our 2D Kalman filter & kinematic dead-reckoning engine maintains continuous tracking with ±2 minute accuracy.
            </p>
            <div class="pt-2 text-[11px] font-mono font-bold text-brand-cyan flex items-center gap-1.5">
              <span>HMM Road Snapping</span> • <span>p85 Travel Baseline</span>
            </div>
          </div>

          <!-- Pillar 2 -->
          <div class="glass-panel p-6 rounded-3xl space-y-4 border border-white/10 hover:border-brand-emerald/40 transition-all">
            <div class="w-12 h-12 rounded-2xl bg-emerald-500/15 border border-emerald-500/30 flex items-center justify-center text-emerald-400 text-2xl font-black">
              🛺
            </div>
            <h3 class="text-lg font-black text-white">Multimodal Fleet</h3>
            <p class="text-xs text-zinc-400 leading-relaxed">
              Choose between express campus buses, prompt auto-rickshaws for last-mile quad sprints, or silent electric golf carts (EVs) linking the medical center and sports grounds.
            </p>
            <div class="pt-2 text-[11px] font-mono font-bold text-emerald-400 flex items-center gap-1.5">
              <span>Buses 🚌</span> • <span>Autos 🛺</span> • <span>Eco EVs ⚡</span>
            </div>
          </div>

          <!-- Pillar 3 -->
          <div class="glass-panel p-6 rounded-3xl space-y-4 border border-white/10 hover:border-brand-purple/40 transition-all">
            <div class="w-12 h-12 rounded-2xl bg-purple-500/15 border border-purple-500/30 flex items-center justify-center text-purple-400 text-2xl font-black">
              💳
            </div>
            <h3 class="text-lg font-black text-white">UPI QR & Smart Wallet</h3>
            <p class="text-xs text-zinc-400 leading-relaxed">
              No change? No problem. Scan the onboard Google Pay / PhonePe UPI QR code directly, tap your student NFC smart pass, or top up your Campus Flow wallet in 5 seconds.
            </p>
            <div class="pt-2 text-[11px] font-mono font-bold text-purple-400 flex items-center gap-1.5">
              <span>Google Pay</span> • <span>PhonePe</span> • <span>₹240 Wallet</span>
            </div>
          </div>

          <!-- Pillar 4 -->
          <div class="glass-panel p-6 rounded-3xl space-y-4 border border-white/10 hover:border-brand-amber/40 transition-all">
            <div class="w-12 h-12 rounded-2xl bg-amber-500/15 border border-amber-500/30 flex items-center justify-center text-amber-400 text-2xl font-black">
              🔐
            </div>
            <h3 class="text-lg font-black text-white">4-Digit Driver OTP</h3>
            <p class="text-xs text-zinc-400 leading-relaxed">
              Every ride is cryptographically protected. Share your unique 4-digit OTP with verified Indian drivers (Rajesh Sharma, Vikram Singh, etc.) to validate your reserved seat.
            </p>
            <div class="pt-2 text-[11px] font-mono font-bold text-amber-400 flex items-center gap-1.5">
              <span>Safe Boarding</span> • <span>Verified Drivers</span>
            </div>
          </div>

        </div>

        <!-- Campus Stats Banner -->
        <div class="glass-panel p-6 sm:p-8 rounded-3xl border border-white/15 bg-gradient-to-r from-brand-cyan/10 via-brand-purple/10 to-brand-emerald/10">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
            <div class="space-y-1">
              <p class="text-3xl sm:text-4xl font-black text-white">10,000+</p>
              <p class="text-xs font-bold uppercase tracking-wider text-zinc-400">Daily Student Rides</p>
            </div>
            <div class="space-y-1">
              <p class="text-3xl sm:text-4xl font-black text-brand-cyan">99.8%</p>
              <p class="text-xs font-bold uppercase tracking-wider text-zinc-400">On-Time Accuracy</p>
            </div>
            <div class="space-y-1">
              <p class="text-3xl sm:text-4xl font-black text-brand-emerald">45+</p>
              <p class="text-xs font-bold uppercase tracking-wider text-zinc-400">Clean Fleet Vehicles</p>
            </div>
            <div class="space-y-1">
              <p class="text-3xl sm:text-4xl font-black text-brand-purple">2.4 min</p>
              <p class="text-xs font-bold uppercase tracking-wider text-zinc-400">Average Wait Time</p>
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- ================= 3. MAIN Q&A (FAQ) ACCORDION ================= -->
    <section id="faqSection" class="py-20 px-4 sm:px-6 lg:px-8 border-t border-white/10 bg-[#070913] relative z-10">
      <div class="max-w-4xl mx-auto space-y-10">
        
        <div class="text-center space-y-3">
          <div class="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-brand-purple/10 border border-brand-purple/30 text-brand-purple text-xs font-bold uppercase tracking-wider">
            <i data-lucide="help-circle" class="w-3.5 h-3.5"></i>
            Frequently Asked Questions
          </div>
          <h2 class="text-3xl sm:text-4xl font-black text-white tracking-tight">
            Got Questions? We’ve Got Answers.
          </h2>
          <p class="text-xs sm:text-sm text-zinc-400">
            Clear insights into tracking, payments, OTP security, and our conversational AI buddy WAYZEN.
          </p>
        </div>

        <!-- FAQ Items -->
        <div class="space-y-4">
          
          <!-- Q1 -->
          <div class="glass-panel rounded-2xl border border-white/10 overflow-hidden transition-all">
            <button onclick="toggleFaqAccordion(1)" class="w-full p-5 text-left flex items-center justify-between gap-4 hover:bg-white/5 transition-colors">
              <span class="text-sm font-bold text-white flex items-center gap-3">
                <span class="w-6 h-6 rounded-full bg-brand-cyan/20 text-brand-cyan text-xs flex items-center justify-center font-black">1</span>
                How does Campus Flow predict accurate ETAs when GPS signal is completely lost?
              </span>
              <i id="faqChevron1" data-lucide="chevron-down" class="w-5 h-5 text-zinc-400 transition-transform"></i>
            </button>
            <div id="faqAnswer1" class="hidden px-5 pb-5 pt-1 text-xs text-zinc-300 leading-relaxed border-t border-white/5 space-y-2">
              <p>Campus Flow uses a 3-layer dead-reckoning pipeline based on the Newson & Krumm (2009) Hidden Markov Model map matcher and a 2D Kalman filter. When raw GPS jumps, has an accuracy radius &gt;65m, or drops entirely (e.g. entering hostel tunnels or under dense trees), the engine automatically falls back to an exponential decay model: \(w = e^{-\Delta t / 90}\), blending instantaneous speed with historical p85 segment travel times. This guarantees 100% survival over 120-second dropouts with Mean Absolute Error under 90 seconds!</p>
            </div>
          </div>

          <!-- Q2 -->
          <div class="glass-panel rounded-2xl border border-white/10 overflow-hidden transition-all">
            <button onclick="toggleFaqAccordion(2)" class="w-full p-5 text-left flex items-center justify-between gap-4 hover:bg-white/5 transition-colors">
              <span class="text-sm font-bold text-white flex items-center gap-3">
                <span class="w-6 h-6 rounded-full bg-emerald-500/20 text-emerald-400 text-xs flex items-center justify-center font-black">2</span>
                How do I pay using UPI QR, Smart Wallet, or Cash on board?
              </span>
              <i id="faqChevron2" data-lucide="chevron-down" class="w-5 h-5 text-zinc-400 transition-transform"></i>
            </button>
            <div id="faqAnswer2" class="hidden px-5 pb-5 pt-1 text-xs text-zinc-300 leading-relaxed border-t border-white/5 space-y-2">
              <p>You have 3 easy payment options:
                <br>• <strong>Instant UPI QR:</strong> Click "Pay / Buy Pass", scan the onboard Google Pay QR code with any UPI app (GPay, PhonePe, Paytm, BHIM), and your ride pass is validated instantly.
                <br>• <strong>Campus Flow Wallet:</strong> Tap the Wallet button on top, recharge via UPI or Debit card, and pay rides in 1-click even with poor mobile internet.
                <br>• <strong>Cash on Board:</strong> Pay exact cash to the vehicle driver upon boarding; the driver will verify your 4-digit OTP to confirm the trip.
              </p>
            </div>
          </div>

          <!-- Q3 -->
          <div class="glass-panel rounded-2xl border border-white/10 overflow-hidden transition-all">
            <button onclick="toggleFaqAccordion(3)" class="w-full p-5 text-left flex items-center justify-between gap-4 hover:bg-white/5 transition-colors">
              <span class="text-sm font-bold text-white flex items-center gap-3">
                <span class="w-6 h-6 rounded-full bg-purple-500/20 text-purple-400 text-xs flex items-center justify-center font-black">3</span>
                What is the Driver 4-Digit Security OTP system and why is it needed?
              </span>
              <i id="faqChevron3" data-lucide="chevron-down" class="w-5 h-5 text-zinc-400 transition-transform"></i>
            </button>
            <div id="faqAnswer3" class="hidden px-5 pb-5 pt-1 text-xs text-zinc-300 leading-relaxed border-t border-white/5 space-y-2">
              <p>During peak campus hours (e.g. 8:30 AM lectures and 5:00 PM hostel return), unverified boarding creates chaos. When you book a ride or pass, Campus Flow generates a secure 4-digit OTP (e.g. 8392). When the vehicle arrives, share this OTP with driver Rajesh Sharma or Vikram Singh or type it in the Driver Chat window. The trip officially activates only once the driver confirms the OTP, ensuring only authorized students occupy reserved seats.</p>
            </div>
          </div>

          <!-- Q4 -->
          <div class="glass-panel rounded-2xl border border-white/10 overflow-hidden transition-all">
            <button onclick="toggleFaqAccordion(4)" class="w-full p-5 text-left flex items-center justify-between gap-4 hover:bg-white/5 transition-colors">
              <span class="text-sm font-bold text-white flex items-center gap-3">
                <span class="w-6 h-6 rounded-full bg-amber-500/20 text-amber-400 text-xs flex items-center justify-center font-black">4</span>
                How do I apply the 10% first ride discount (CAMPUS10) or 100% free ride?
              </span>
              <i id="faqChevron4" data-lucide="chevron-down" class="w-5 h-5 text-zinc-400 transition-transform"></i>
            </button>
            <div id="faqAnswer4" class="hidden px-5 pb-5 pt-1 text-xs text-zinc-300 leading-relaxed border-t border-white/5 space-y-2">
              <p>In the Payment modal, enter the promo coupon code <strong>CAMPUS10</strong> to get an instant 10% discount on any ride or semester pass. For your very first trip of the academic term, use coupon <strong>FREEFIRST</strong> for a 100% free ride. You can also ask WAYZEN AI: <em>"WAYZEN, best coupon batao"</em> and it will apply it for you in one click!</p>
            </div>
          </div>

          <!-- Q5 -->
          <div class="glass-panel rounded-2xl border border-white/10 overflow-hidden transition-all">
            <button onclick="toggleFaqAccordion(5)" class="w-full p-5 text-left flex items-center justify-between gap-4 hover:bg-white/5 transition-colors">
              <span class="text-sm font-bold text-white flex items-center gap-3">
                <span class="w-6 h-6 rounded-full bg-rose-500/20 text-rose-400 text-xs flex items-center justify-center font-black">5</span>
                Who is WAYZEN and how does it assist students in Hinglish?
              </span>
              <i id="faqChevron5" data-lucide="chevron-down" class="w-5 h-5 text-zinc-400 transition-transform"></i>
            </button>
            <div id="faqAnswer5" class="hidden px-5 pb-5 pt-1 text-xs text-zinc-300 leading-relaxed border-t border-white/5 space-y-2">
              <p><strong>WAYZEN</strong> is our intelligent, cute, and funny 24/7 campus transit companion! It speaks both clean English and natural Indian Hinglish (<em>"Haan bhai, bus 4 min me library pahunch rahi hai!"</em>). WAYZEN can fetch live vehicle ETAs, check your wallet balance, summon an auto rickshaw, generate security OTPs, direct you to campus blocks, and crack hilarious college jokes when you're stressed before exams!</p>
            </div>
          </div>

        </div>

      </div>
    </section>

    <!-- ================= 5. CAMPUS FOOTER ================= -->
    <footer class="py-12 px-4 sm:px-6 lg:px-8 border-t border-white/10 bg-[#05060d] text-zinc-400 text-xs">
      <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
        
        <div class="space-y-2 text-center md:text-left">
          <div class="flex items-center justify-center md:justify-start gap-2.5">
            <div class="w-7 h-7 rounded-xl bg-brand-cyan flex items-center justify-center text-black font-black">
              <i data-lucide="navigation-2" class="w-4 h-4 fill-black"></i>
            </div>
            <span class="text-white font-black text-sm">Campus Flow Transit System</span>
          </div>
          <p class="text-zinc-500 max-w-sm">
            AI-driven university transit connecting Metro Link, Central Library, Hostels, and Academic Blocks.
          </p>
        </div>

        <div class="flex flex-wrap items-center justify-center gap-6 text-xs font-semibold text-zinc-300">
          <button onclick="showLandingPage(); window.scrollTo({top:0, behavior:'smooth'});" class="hover:text-brand-cyan">Home</button>
          <button onclick="scrollToLandingSection('aboutUsSection')" class="hover:text-brand-cyan">About Us</button>
          <button onclick="scrollToLandingSection('faqSection')" class="hover:text-brand-cyan">Q&A</button>
          <button onclick="handleGuestDirectAccess()" class="hover:text-brand-cyan">Guest Access</button>
        </div>

        <div class="text-center md:text-right space-y-1">
          <p class="text-zinc-400 font-bold">Campus Helpline: <span class="text-brand-cyan">1800-CAMPUS-SAFE</span></p>
          <p class="text-[10px] text-zinc-600">© 2026 Campus Flow University Mobility. All rights reserved.</p>
        </div>

      </div>
    </footer>

  </div>

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
          <button onclick="openWalletModal()" title="Campus Wallet" class="p-2.5 rounded-xl bg-purple-500/20 text-purple-300 border border-purple-500/30 hover:bg-purple-500/30 font-bold">
            <i data-lucide="wallet" class="w-4 h-4"></i>
          </button>
          <button onclick="openFarePassesModal()" title="Student Transit Fares & Passes" class="p-2.5 rounded-xl bg-amber-500/20 text-amber-300 border border-amber-500/30 hover:bg-amber-500/30 font-bold">
            <i data-lucide="ticket" class="w-4 h-4"></i>
          </button>
          <button onclick="openPaymentAndBookingModal()" title="Book / Pay Pass" class="p-2.5 rounded-xl bg-brand-cyan text-black hover:opacity-90 font-bold shadow-md">
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

                <!-- Persistent Student Transit Pass & Wallet Card (Visible After Sign Up / Login) -->
        <div id="sidebarTransitPassCard" class="p-3.5 rounded-2xl bg-gradient-to-br from-brand-cyan/15 via-[#131b38] to-purple-950/40 border border-brand-cyan/30 shadow-xl relative overflow-hidden backdrop-blur-xl shrink-0">
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center gap-2">
              <div class="w-7 h-7 rounded-lg bg-gradient-to-tr from-brand-cyan to-brand-purple flex items-center justify-center text-black font-black">
                <i data-lucide="wallet" class="w-3.5 h-3.5 text-black"></i>
              </div>
              <div>
                <p class="text-[9px] font-black uppercase tracking-wider text-brand-cyan">Campus Smart Pass</p>
                <p class="text-xs font-black text-white truncate max-w-[150px]" id="sidebarPassName">Student</p>
              </div>
            </div>
            <span class="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-bold flex items-center gap-1">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span> Active
            </span>
          </div>
          <div class="flex items-end justify-between pt-1">
            <div>
              <p class="text-[10px] text-zinc-400 uppercase font-bold tracking-wider">Wallet Balance</p>
              <p class="text-lg font-black text-brand-cyan font-mono" id="sidebarPassBalance">₹ 240.00</p>
              <p class="text-[10px] text-zinc-400 font-mono" id="sidebarPassId">STU-2024-8891</p>
            </div>
            <div class="flex items-center gap-1.5">
              <button onclick="openWalletModal()" class="px-2.5 py-1.5 rounded-xl bg-brand-cyan text-black font-black text-[11px] hover:opacity-90 transition-all flex items-center gap-1 shadow-md">
                <i data-lucide="plus" class="w-3 h-3"></i> Top-Up
              </button>
              <button onclick="openWalletModal(); filterWalletHistory('all')" class="px-2.5 py-1.5 rounded-xl bg-white/10 text-white font-bold text-[11px] hover:bg-white/20 transition-all border border-white/15">
                History
              </button>
            </div>
          </div>
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

      <!-- Bottom Quick Actions -->
      <div class="p-3 border-t border-white/10 bg-black/40 flex items-center justify-between gap-2 text-xs font-bold">
        <button onclick="openFarePassesModal()" class="flex-1 py-2 px-3 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 text-zinc-300 text-center flex items-center justify-center gap-1.5">
          <i data-lucide="ticket" class="w-3.5 h-3.5 text-brand-cyan"></i>
          Fares & Passes
        </button>
        <button onclick="openH4StressModal()" class="flex-1 py-2 px-3 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 text-amber-400 text-center flex items-center justify-center gap-1.5">
          <i data-lucide="zap" class="w-3.5 h-3.5"></i>
          H4 Stress Test
        </button>
        <button onclick="toggleWayzenChat()" class="p-2 rounded-xl bg-purple-500/20 hover:bg-purple-500/30 border border-purple-500/30 text-purple-300 font-black" title="Chat with WAYZEN">
          🤖
        </button>
      </div>

    </aside>

    <!-- Right Live Interactive Map -->
    <main class="lg:col-span-8 xl:col-span-8 relative h-full w-full">
      <div id="campusMap" class="w-full h-full z-0"></div>

      <!-- LPU Multi-Transit Route Legend Overlay -->
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
      </div>

      <!-- Top Floating Map Controls -->
      <div class="absolute top-4 left-4 z-[400] flex flex-wrap items-center gap-2">
        <div class="glass-panel px-3.5 py-2 rounded-2xl flex items-center gap-3 text-xs font-black shadow-lg">
          <span class="flex items-center gap-1.5 text-brand-cyan">
            <span class="w-2 h-2 rounded-full bg-brand-cyan animate-ping"></span>
            Kalman + HMM Road Snapped
          </span>
          <span class="text-zinc-500">|</span>
          <span class="text-zinc-300 font-mono" id="simClockDisplay">10:45:00 AM</span>
        </div>

        <div class="glass-panel p-1 rounded-2xl flex items-center gap-1 text-xs font-bold text-zinc-400">
          <button onclick="setSimWarp(1, this)" class="warp-btn px-2.5 py-1 rounded-xl bg-white/15 text-brand-cyan">1x</button>
          <button onclick="setSimWarp(2, this)" class="warp-btn px-2.5 py-1 rounded-xl hover:text-white">2x</button>
          <button onclick="setSimWarp(5, this)" class="warp-btn px-2.5 py-1 rounded-xl hover:text-white">5x</button>
        </div>
      </div>

      <!-- Map Theme & Layer Switcher -->
      <div class="absolute top-4 right-4 z-[400] flex items-center gap-2">
        <select id="mapLayerThemeSelect" class="glass-panel px-3 py-2 rounded-2xl text-xs font-bold text-white bg-black/60 border border-white/20 focus:outline-none">
          <option value="dark">Carto Dark (Default)</option>
          <option value="osm">Standard Street</option>
          <option value="satellite">Satellite Aerial</option>
        </select>
        <button onclick="recenterCampusMap()" title="Recenter Campus" class="p-2.5 rounded-2xl glass-panel text-white hover:text-brand-cyan shadow-lg">
          <i data-lucide="crosshair" class="w-4 h-4"></i>
        </button>
      </div>

      <!-- Bottom Floating Legend -->
      <div class="absolute bottom-4 left-4 right-4 sm:right-auto z-[400] glass-panel p-3 rounded-2xl flex flex-wrap items-center gap-4 text-xs font-bold text-zinc-300">
        <div class="flex items-center gap-2">
          <span class="w-3 h-3 rounded-full bg-emerald-400"></span>
          <span>Outer Green Loop</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="w-3 h-3 rounded-full bg-blue-400"></span>
          <span>Blue Express Route</span>
        </div>
        <div class="flex items-center gap-2">
          <span class="w-3 h-3 rounded-full bg-brand-cyan animate-pulse"></span>
          <span>9 Major Stops</span>
        </div>
        <div class="flex items-center gap-2 text-zinc-400 text-[11px]">
          <span>Dead-Reckoning Dropout Tolerance: <strong>120s</strong></span>
        </div>
      </div>

    </main>

  </section>

  <!-- ================= MODAL 1: CAMPUS WALLET & PAYMENT HISTORY ================= -->
  <div id="walletModal" class="fixed inset-0 z-[1020] bg-black/80 backdrop-blur-md hidden place-items-center p-4">
    <div class="glass-panel w-full max-w-xl rounded-3xl border border-white/15 overflow-hidden shadow-2xl animate-pop-in flex flex-col max-h-[90vh]">
      
      <!-- Header -->
      <div class="p-5 border-b border-white/10 flex items-center justify-between bg-white/5 shrink-0">
        <div class="flex items-center gap-2.5">
          <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-brand-cyan to-brand-purple flex items-center justify-center text-black font-black text-lg">
            💳
          </div>
          <div>
            <h3 class="text-base font-black text-white">Campus Flow Smart Wallet</h3>
            <p class="text-[11px] text-zinc-400">Instant Cashless Transit & Passbook</p>
          </div>
        </div>
        <button onclick="closeModal('walletModal')" class="p-2 rounded-xl text-zinc-400 hover:text-white hover:bg-white/10">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <div class="p-6 overflow-y-auto space-y-6 flex-1">
        
        <!-- Hologram Digital Card -->
        <div class="hologram-card p-5 rounded-3xl space-y-5 shadow-xl text-white">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <span class="text-brand-cyan text-sm font-black tracking-widest uppercase">Campus Flow Pass</span>
              <span class="text-xs">⚡</span>
            </div>
            <i data-lucide="wifi" class="w-5 h-5 text-brand-cyan rotate-90"></i>
          </div>

          <div class="space-y-1">
            <p class="text-[10px] uppercase tracking-wider text-zinc-400">Current Available Balance</p>
            <p class="text-3xl sm:text-4xl font-black text-white tracking-tight flex items-center gap-2">
              <span id="walletCardBalance">₹ 240.00</span>
              <span class="text-[11px] px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">Active</span>
            </p>
          </div>

          <div class="flex items-center justify-between text-xs pt-1 font-mono text-zinc-300">
            <div>
              <p class="text-[9px] text-zinc-500 uppercase">Card Holder</p>
              <p class="font-bold text-white" id="walletCardHolder">Student</p>
            </div>
            <div>
              <p class="text-[9px] text-zinc-500 uppercase">Student ID</p>
              <p class="font-bold text-white" id="walletCardStudentId">STU-2024-8891</p>
            </div>
            <div>
              <p class="text-[9px] text-zinc-500 uppercase">Card No.</p>
              <p class="font-bold text-white">•••• 4092</p>
            </div>
          </div>
        </div>

        <!-- Top-Up Wallet Section -->
        <div class="glass-card p-5 rounded-2xl space-y-4">
          <div class="flex items-center justify-between">
            <h4 class="text-xs font-black uppercase tracking-wider text-zinc-300 flex items-center gap-2">
              <i data-lucide="plus-circle" class="w-4 h-4 text-brand-cyan"></i>
              Top Up Wallet Instantly
            </h4>
            <span class="text-[10px] text-emerald-400 font-bold">Zero Convenience Fee</span>
          </div>

          <!-- Quick Amount Chips -->
          <div class="grid grid-cols-5 gap-2">
            <button onclick="selectTopUpAmount(50, this)" class="topup-chip py-2 rounded-xl text-xs font-bold border border-white/10 bg-white/5 text-zinc-300 hover:border-brand-cyan">+₹50</button>
            <button onclick="selectTopUpAmount(100, this)" class="topup-chip py-2 rounded-xl text-xs font-bold border border-brand-cyan bg-brand-cyan/20 text-brand-cyan font-black">+₹100</button>
            <button onclick="selectTopUpAmount(200, this)" class="topup-chip py-2 rounded-xl text-xs font-bold border border-white/10 bg-white/5 text-zinc-300 hover:border-brand-cyan">+₹200</button>
            <button onclick="selectTopUpAmount(500, this)" class="topup-chip py-2 rounded-xl text-xs font-bold border border-white/10 bg-white/5 text-zinc-300 hover:border-brand-cyan">+₹500</button>
            <button onclick="selectTopUpAmount(1000, this)" class="topup-chip py-2 rounded-xl text-xs font-bold border border-white/10 bg-white/5 text-zinc-300 hover:border-brand-cyan">+₹1k</button>
          </div>

          <!-- Custom Top-up Input -->
          <div class="relative">
            <span class="absolute left-4 top-1/2 -translate-y-1/2 text-sm font-bold text-zinc-400">₹</span>
            <input type="number" id="customTopUpInput" placeholder="Or enter custom amount..." oninput="handleCustomTopUp(this.value)" class="glass-input w-full pl-8 pr-4 py-2.5 rounded-xl text-xs font-semibold text-white">
          </div>

          <!-- Payment Mode for Top-up -->
          <div class="space-y-1.5 pt-1">
            <label class="block text-[10px] uppercase font-bold text-zinc-400">Select Payment Source</label>
            <div class="grid grid-cols-3 gap-2">
              <button onclick="selectTopUpMethod('upi', this)" class="topup-method-btn p-2 rounded-xl text-[11px] font-bold border border-brand-cyan bg-brand-cyan/20 text-brand-cyan text-center">
                📱 UPI Apps
              </button>
              <button onclick="selectTopUpMethod('card', this)" class="topup-method-btn p-2 rounded-xl text-[11px] font-bold border border-white/10 bg-white/5 text-zinc-300 hover:border-white/30 text-center">
                💳 Debit Card
              </button>
              <button onclick="selectTopUpMethod('netbanking', this)" class="topup-method-btn p-2 rounded-xl text-[11px] font-bold border border-white/10 bg-white/5 text-zinc-300 hover:border-white/30 text-center">
                🏦 Net Banking
              </button>
            </div>
          </div>

          <!-- Top-Up Submit Button -->
          <button onclick="executeWalletTopUp()" class="btn-gradient w-full py-3 rounded-xl text-black font-black text-xs uppercase tracking-wider flex items-center justify-center gap-2 shadow-lg">
            <span>Recharge Wallet with <span id="topUpBtnAmount">₹100</span></span>
            <i data-lucide="check" class="w-4 h-4"></i>
          </button>
        </div>

        <!-- Payment History / Passbook -->
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <h4 class="text-xs font-black uppercase tracking-wider text-zinc-300 flex items-center gap-2">
              <i data-lucide="history" class="w-4 h-4 text-brand-purple"></i>
              Payment History & Passbook
            </h4>
            <button onclick="downloadPassbookReceipt()" class="text-[11px] text-brand-cyan hover:underline font-bold">
              Download Statement ↓
            </button>
          </div>

          <!-- Filter Tabs -->
          <div class="grid grid-cols-4 p-1 rounded-xl bg-white/5 border border-white/10 text-[10px] font-bold text-zinc-400">
            <button onclick="filterWalletHistory('all', this)" class="wallet-hist-btn py-1 rounded-lg bg-white/15 text-white">All</button>
            <button onclick="filterWalletHistory('ride', this)" class="wallet-hist-btn py-1 rounded-lg hover:text-white">Rides</button>
            <button onclick="filterWalletHistory('topup', this)" class="wallet-hist-btn py-1 rounded-lg hover:text-white">Top-Ups</button>
            <button onclick="filterWalletHistory('promo', this)" class="wallet-hist-btn py-1 rounded-lg hover:text-white">Cashback</button>
          </div>

          <!-- History List Container -->
          <div id="walletHistoryContainer" class="space-y-2 max-h-56 overflow-y-auto pr-1">
            <!-- Dynamic Items in JS -->
          </div>
        </div>

      </div>

    </div>
  </div>

  <!-- ================= MODAL 2: CASH / UPI PAYMENT & BOOKING ================= -->
  <div id="paymentBookingModal" class="fixed inset-0 z-[1000] bg-black/80 backdrop-blur-md hidden place-items-center p-4">
    <div class="glass-panel w-full max-w-xl rounded-3xl border border-white/15 overflow-hidden shadow-2xl animate-pop-in flex flex-col max-h-[90vh]">
      
      <!-- Modal Header -->
      <div class="p-5 border-b border-white/10 flex items-center justify-between bg-white/5 shrink-0">
        <div class="flex items-center gap-2.5">
          <div class="w-9 h-9 rounded-xl bg-gradient-to-tr from-brand-cyan to-brand-purple flex items-center justify-center text-black font-black text-lg">
            ⚡
          </div>
          <div>
            <h3 class="text-base font-black text-white">Campus Ride Pass & Payment</h3>
            <p class="text-[11px] text-zinc-400">UPI QR, Campus Wallet, or Cash on Board</p>
          </div>
        </div>
        <button onclick="closeModal('paymentBookingModal')" class="p-2 rounded-xl text-zinc-400 hover:text-white hover:bg-white/10">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <!-- Scrollable Body -->
      <div class="p-6 overflow-y-auto space-y-6 flex-1">
        
        <!-- Ride Type & Amount Selector -->
        <div class="space-y-3">
          <label class="block text-xs font-black uppercase tracking-wider text-zinc-300">
            1. Select Fare / Pass Amount
          </label>
          <div class="grid grid-cols-5 gap-2 text-center text-xs font-bold">
            <button onclick="selectMoneyAmount(15, this)" class="money-chip p-2.5 rounded-xl border border-brand-cyan bg-brand-cyan/20 text-brand-cyan font-black">₹15<br><span class="text-[9px] font-normal">Single</span></button>
            <button onclick="selectMoneyAmount(30, this)" class="money-chip p-2.5 rounded-xl border border-white/10 bg-white/5 text-zinc-300 hover:border-white/30">₹30<br><span class="text-[9px] font-normal">Auto 🛺</span></button>
            <button onclick="selectMoneyAmount(40, this)" class="money-chip p-2.5 rounded-xl border border-white/10 bg-white/5 text-zinc-300 hover:border-white/30">₹40<br><span class="text-[9px] font-normal">Daily</span></button>
            <button onclick="selectMoneyAmount(150, this)" class="money-chip p-2.5 rounded-xl border border-white/10 bg-white/5 text-zinc-300 hover:border-white/30">₹150<br><span class="text-[9px] font-normal">Weekly</span></button>
            <button onclick="selectMoneyAmount(999, this)" class="money-chip p-2.5 rounded-xl border border-white/10 bg-white/5 text-zinc-300 hover:border-white/30">₹999<br><span class="text-[9px] font-normal">Semester</span></button>
          </div>

          <!-- Custom Amount Input -->
          <div class="relative">
            <span class="absolute left-4 top-1/2 -translate-y-1/2 text-sm font-bold text-zinc-400">₹</span>
            <input type="number" id="customAmountInput" placeholder="Enter custom amount..." oninput="handleCustomAmount(this.value)" class="glass-input w-full pl-8 pr-4 py-2 rounded-xl text-xs font-semibold text-white">
          </div>
        </div>

        <!-- Coupon Code Box -->
        <div class="glass-card p-4 rounded-2xl space-y-3 border border-brand-cyan/30">
          <div class="flex items-center justify-between">
            <span class="text-xs font-black uppercase text-brand-cyan flex items-center gap-1.5">
              <i data-lucide="tag" class="w-4 h-4"></i> Apply Promo Coupon
            </span>
            <span class="text-[10px] text-zinc-400">Try: <strong class="text-white">CAMPUS10</strong></span>
          </div>
          <div class="flex gap-2">
            <input type="text" id="couponCodeInput" placeholder="Enter coupon (e.g. CAMPUS10)" value="CAMPUS10" class="glass-input flex-1 px-3 py-2 rounded-xl text-xs font-mono font-bold uppercase text-white">
            <button onclick="applyCouponCode()" class="px-4 py-2 rounded-xl bg-brand-cyan text-black font-extrabold text-xs hover:opacity-90">
              Apply
            </button>
          </div>
          <div class="flex items-center gap-2 pt-1">
            <button onclick="quickApplyCoupon('CAMPUS10')" class="px-2 py-1 rounded-lg bg-white/10 hover:bg-white/20 text-[10px] font-mono text-zinc-200">
              🏷️ CAMPUS10 (10% Off)
            </button>
            <button onclick="quickApplyCoupon('FREEFIRST')" class="px-2 py-1 rounded-lg bg-white/10 hover:bg-white/20 text-[10px] font-mono text-zinc-200">
              🎁 FREEFIRST (100% Free)
            </button>
          </div>
        </div>

        <!-- Payment Method Tabs: UPI QR / Wallet / Cash -->
        <div class="space-y-3">
          <label class="block text-xs font-black uppercase tracking-wider text-zinc-300">
            2. Choose Payment Mode
          </label>
          <div class="grid grid-cols-3 p-1 rounded-2xl bg-black/40 border border-white/10 text-xs font-extrabold">
            <button id="payTabUpi" onclick="switchPayTab('upi')" class="pay-method-tab py-2 rounded-xl bg-white/15 text-brand-cyan shadow-sm">
              📱 Google Pay UPI
            </button>
            <button id="payTabWallet" onclick="switchPayTab('wallet')" class="pay-method-tab py-2 rounded-xl text-zinc-400 hover:text-white">
              💳 Campus Wallet
            </button>
            <button id="payTabCash" onclick="switchPayTab('cash')" class="pay-method-tab py-2 rounded-xl text-zinc-400 hover:text-white">
              💵 Cash on Board
            </button>
          </div>

          <!-- Tab Content: UPI QR Code -->
          <div id="payContentUpi" class="space-y-4 pt-1">
            <div class="glass-card p-4 rounded-3xl border border-white/15 flex flex-col items-center justify-center text-center space-y-3 bg-[#0a0e20]">
              <div class="w-48 h-48 bg-white p-2.5 rounded-2xl shadow-xl flex items-center justify-center">
                <img src="upi-qr.jpg" onerror="this.src='data:image/jpeg;base64,__QR_B64__'" alt="Google Pay UPI QR Code" class="w-full h-full object-contain rounded-2xl">
              </div>
              <div class="space-y-1">
                <p class="text-xs font-bold text-white flex items-center justify-center gap-1.5">
                  <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                  Scan to Pay with Any UPI App
                </p>
                <p class="text-[11px] font-mono text-zinc-400">UPI ID: <span id="displayedUpiId" class="text-white font-bold">campusflow@okaxis</span></p>
              </div>
              <div class="flex items-center gap-2">
                <button onclick="copyUpiId()" class="px-3 py-1.5 rounded-xl bg-white/10 hover:bg-white/20 text-[11px] font-bold text-zinc-300 flex items-center gap-1.5">
                  <i data-lucide="copy" class="w-3.5 h-3.5"></i> Copy UPI ID
                </button>
                <div class="text-[11px] text-zinc-400 font-mono" id="upiCountdownText">Auto-verifying: 04:59</div>
              </div>
            </div>
          </div>

          <!-- Tab Content: Campus Wallet -->
          <div id="payContentWallet" class="hidden space-y-4 pt-1">
            <div class="glass-card p-5 rounded-3xl border border-white/15 space-y-4 bg-[#0a0e20]">
              <div class="flex items-center justify-between">
                <div>
                  <p class="text-xs text-zinc-400">Available Wallet Balance</p>
                  <p class="text-2xl font-black text-white" id="modalWalletBalance">₹ 240.00</p>
                </div>
                <button onclick="openWalletModal()" class="px-3 py-1.5 rounded-xl bg-white/10 hover:bg-white/20 text-xs font-bold text-brand-cyan">
                  + Add Money
                </button>
              </div>
              <p class="text-xs text-zinc-300" id="walletPayStatusText">
                Instant 1-click deduction from your Campus Flow Smart Wallet pass.
              </p>
            </div>
          </div>

          <!-- Tab Content: Cash on Board -->
          <div id="payContentCash" class="hidden space-y-4 pt-1">
            <div class="glass-card p-5 rounded-3xl border border-white/15 space-y-3 bg-[#0a0e20]">
              <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-2xl bg-amber-500/20 text-amber-400 flex items-center justify-center text-xl font-black">
                  💵
                </div>
                <div>
                  <h4 class="text-xs font-black text-white">Cash Payment to Driver</h4>
                  <p class="text-[11px] text-zinc-400">Pay cash upon boarding vehicle</p>
                </div>
              </div>
              <p class="text-xs text-zinc-300 leading-relaxed">
                Hand exact change to driver upon entry. The driver will verify your 4-digit security OTP to activate your ride.
              </p>
            </div>
          </div>
        </div>

        <!-- Net Calculation Summary -->
        <div class="p-4 rounded-2xl bg-black/50 border border-white/10 space-y-2 text-xs">
          <div class="flex justify-between text-zinc-400">
            <span>Base Fare / Pass:</span>
            <span id="priceSummaryBase">₹15.00</span>
          </div>
          <div class="flex justify-between text-brand-cyan">
            <span>Coupon Discount (<span id="priceSummaryDiscountLabel">10%</span>):</span>
            <span id="priceSummaryDiscount">-₹1.50</span>
          </div>
          <div class="border-t border-white/10 pt-2 flex justify-between font-black text-white text-sm">
            <span>Net Amount to Pay:</span>
            <span id="priceSummaryTotal" class="text-brand-cyan text-base font-black">₹13.50</span>
          </div>
        </div>

        <!-- Action Button -->
        <button onclick="handlePaymentSuccess()" class="btn-gradient w-full py-3.5 rounded-2xl text-black font-black text-xs uppercase tracking-wider flex items-center justify-center gap-2 shadow-xl">
          <span>Confirm & Generate 4-Digit Driver OTP</span>
          <i data-lucide="shield-check" class="w-4 h-4"></i>
        </button>

      </div>

    </div>
  </div>

    <!-- ================= SEAT LAYOUT & RESERVATION MODAL ================= -->
  <div id="seatLayoutModal" class="fixed inset-0 z-[1060] bg-black/85 backdrop-blur-md hidden place-items-center p-4">
    <div class="glass-panel w-full max-w-xl rounded-3xl border border-white/15 overflow-hidden shadow-2xl animate-pop-in flex flex-col max-h-[90vh]">
      
      <!-- Header -->
      <div class="p-4 border-b border-white/10 flex items-center justify-between bg-white/5 shrink-0">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-brand-cyan to-brand-purple text-black flex items-center justify-center text-xl font-black" id="seatModalVehicleIcon">
            🚌
          </div>
          <div>
            <div class="flex items-center gap-2">
              <h3 class="text-sm font-black text-white" id="seatModalVehicleName">Shuttle #1</h3>
              <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-brand-cyan/20 text-brand-cyan font-bold" id="seatModalVehiclePlate">PB 08 BX 9021</span>
            </div>
            <p class="text-[11px] text-zinc-400" id="seatModalVehicleType">50-Seater Campus Shuttle • Driver: Rajesh Sharma (★ 4.9)</p>
          </div>
        </div>
        <button onclick="closeModal('seatLayoutModal')" class="p-2 rounded-xl text-zinc-400 hover:text-white hover:bg-white/10">
          <i data-lucide="x" class="w-5 h-5"></i>
        </button>
      </div>

      <!-- Live Seat Legend & Stats -->
      <div class="p-3 bg-gradient-to-r from-[#0d1226] via-[#10193a] to-[#0d1226] border-b border-white/10 flex flex-wrap items-center justify-between gap-3 text-xs shrink-0">
        <div class="flex items-center gap-4">
          <div class="flex items-center gap-1.5">
            <span class="w-3.5 h-3.5 rounded-lg bg-emerald-500/20 border border-emerald-500 text-emerald-400 flex items-center justify-center text-[9px]">✓</span>
            <span class="text-zinc-300">Available</span>
          </div>
          <div class="flex items-center gap-1.5">
            <span class="w-3.5 h-3.5 rounded-lg bg-rose-500/20 border border-rose-500/40 text-rose-400 flex items-center justify-center text-[9px]">✕</span>
            <span class="text-zinc-400">Booked</span>
          </div>
          <div class="flex items-center gap-1.5">
            <span class="w-3.5 h-3.5 rounded-lg bg-brand-cyan border border-brand-cyan text-black flex items-center justify-center text-[9px] font-bold">★</span>
            <span class="text-brand-cyan font-bold">Selected</span>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-zinc-400 font-bold" id="seatModalStatsText">8 of 50 Seats Free</span>
          <span class="text-brand-cyan font-bold font-mono" id="seatModalFareText">Fare: ₹15</span>
        </div>
      </div>

      <!-- Vehicle Cabin Grid (Scrollable) -->
      <div class="flex-1 overflow-y-auto p-5 space-y-4">
        
        <!-- Driver Cabin Indicator -->
        <div class="p-3 rounded-2xl bg-black/40 border border-white/10 flex items-center justify-between text-xs">
          <div class="flex items-center gap-2 text-zinc-400">
            <span class="text-lg">🛞</span>
            <span class="font-bold">Driver Cabin (Front)</span>
          </div>
          <div class="flex items-center gap-2 text-emerald-400 font-mono text-[11px]">
            <span>🚪 Entry / Exit Door</span>
          </div>
        </div>

        <!-- Seats Grid Container -->
        <div id="seatGridContainer" class="p-4 rounded-2xl bg-[#080c1d] border border-white/10 space-y-3">
          <!-- Rendered dynamically -->
        </div>

        <!-- Selected Seat Banner -->
        <div id="seatSelectionBanner" class="p-3 rounded-2xl bg-brand-cyan/10 border border-brand-cyan/30 flex items-center justify-between text-xs">
          <div class="flex items-center gap-2">
            <span class="text-lg">💺</span>
            <div>
              <p class="font-bold text-white" id="selectedSeatLabel">Click an available green seat to select</p>
              <p class="text-[10px] text-zinc-400" id="selectedSeatSubtitle">Window or aisle seats available with live USB charging</p>
            </div>
          </div>
          <span class="text-sm font-black text-brand-cyan font-mono" id="selectedSeatPrice"></span>
        </div>

      </div>

      <!-- Footer Buttons -->
      <div class="p-4 border-t border-white/10 bg-white/5 flex items-center justify-between gap-3 shrink-0">
        <button onclick="openDriverChat(currentSeatModalVehicleId)" class="px-4 py-2.5 rounded-xl bg-white/10 hover:bg-white/20 text-white font-bold text-xs flex items-center gap-1.5 border border-white/15">
          💬 Ask Driver About Seat / Luggage
        </button>
        <button id="btnConfirmSeatBooking" onclick="confirmSeatBooking()" class="px-5 py-2.5 rounded-xl btn-gradient text-black font-black text-xs uppercase tracking-wider flex items-center gap-2 shadow-lg shadow-brand-cyan/20">
          <span>Confirm Seat & Ride</span>
          <i data-lucide="arrow-right" class="w-4 h-4"></i>
        </button>
      </div>

    </div>
  </div>

  <!-- ================= MODAL 3: DRIVER CHAT & OTP SECURITY ================= -->
  <div id="driverChatModal" class="fixed inset-0 z-[1050] bg-black/80 backdrop-blur-md hidden place-items-center p-4">
    <div class="glass-panel w-full max-w-lg rounded-3xl border border-white/15 overflow-hidden shadow-2xl animate-pop-in flex flex-col h-[580px]">
      
      <!-- Chat Header -->
      <div class="p-4 border-b border-white/10 flex items-center justify-between bg-white/5 shrink-0">
        <div class="flex items-center gap-3">
          <div class="relative">
            <div class="w-10 h-10 rounded-2xl bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 flex items-center justify-center text-lg font-black">
              🛺
            </div>
            <span class="w-2.5 h-2.5 rounded-full bg-emerald-400 absolute -bottom-0.5 -right-0.5 border-2 border-black"></span>
          </div>
          <div>
            <div class="flex items-center gap-2">
              <h3 class="text-sm font-black text-white" id="chatDriverName">Rajesh Sharma</h3>
              <span class="text-[10px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400 font-bold" id="chatPlate">PB 08 CA 1201</span>
            </div>
            <p class="text-[11px] text-zinc-400" id="chatVehicleType">Campus Auto-Rickshaw #2 • Rating: 4.9 ★</p>
          </div>
        </div>
        <div class="flex items-center gap-2">
          <button id="btnCallDriverModal" onclick="callCurrentDriver()" class="px-3 py-1.5 rounded-xl bg-emerald-500/20 text-emerald-400 hover:bg-emerald-500/30 border border-emerald-500/30 font-bold text-xs flex items-center gap-1.5 transition-all">
            <span>📞 Call</span>
          </button>
          <button onclick="closeModal('driverChatModal')" class="p-2 rounded-xl text-zinc-400 hover:text-white hover:bg-white/10">
            <i data-lucide="x" class="w-5 h-5"></i>
          </button>
        </div>
      </div>

      <!-- OTP Warning Banner -->
      <div class="p-3 bg-gradient-to-r from-emerald-950/70 to-black border-b border-emerald-500/30 flex items-center justify-between shrink-0">
        <div class="flex items-center gap-2">
          <i data-lucide="key" class="w-4 h-4 text-emerald-400"></i>
          <span class="text-xs text-zinc-300">Your Security OTP for this ride:</span>
        </div>
        <div class="px-3 py-1 rounded-xl bg-emerald-400/20 border border-emerald-400/40 text-emerald-400 font-mono font-black text-sm tracking-widest" id="chatOtpDisplay">
          8392
        </div>
      </div>

      <!-- Messages Area -->
      <div id="driverChatMessages" class="flex-1 overflow-y-auto p-4 space-y-3 text-xs">
        <!-- Rendered via JS -->
      </div>

      <!-- Quick Canned Student Chips -->
      <div class="p-2 border-t border-white/5 bg-white/5 flex items-center gap-1.5 overflow-x-auto text-[11px] font-semibold text-zinc-300 shrink-0">
        <button onclick="sendQuickChatMessage('Bhaiya, where are you right now?')" class="px-2.5 py-1 rounded-lg bg-white/10 hover:bg-white/20 whitespace-nowrap">📍 Where are you?</button>
        <button onclick="sendQuickChatMessage('I have reached the stop!')" class="px-2.5 py-1 rounded-lg bg-white/10 hover:bg-white/20 whitespace-nowrap">🚏 Reached the stop</button>
        <button onclick="sendQuickChatMessage('Please wait 2 mins for me!')" class="px-2.5 py-1 rounded-lg bg-white/10 hover:bg-white/20 whitespace-nowrap">⏳ Wait 2 mins</button>
        <button onclick="sendQuickChatMessage('OTP is 8392')" class="px-2.5 py-1 rounded-lg bg-emerald-500/20 text-emerald-400 hover:bg-emerald-500/30 whitespace-nowrap font-mono font-bold">🔢 Send OTP</button>
      </div>

      <!-- Message Input -->
      <div class="p-3 border-t border-white/10 bg-[#070913] flex items-center gap-2 shrink-0">
        <input type="text" id="driverChatInput" placeholder="Message driver (English / Hindi)..." onkeydown="if(event.key==='Enter') sendChatMessage()" class="glass-input flex-1 px-4 py-2.5 rounded-xl text-xs font-semibold text-white">
        <button onclick="sendChatMessage()" class="p-2.5 rounded-xl bg-emerald-500 text-black hover:bg-emerald-400 font-bold">
          <i data-lucide="send" class="w-4 h-4"></i>
        </button>
      </div>

    </div>
  </div>

  <!-- ================= MODAL 4: FARES & PASSES ================= -->
  <div id="farePassesModal" class="fixed inset-0 z-[1000] bg-black/75 backdrop-blur-md hidden place-items-center p-4">
    <div class="glass-panel w-full max-w-md p-6 rounded-3xl border border-white/15 space-y-5 animate-pop-in">
      <div class="flex items-center justify-between">
        <h3 class="text-base font-black text-white">University Transit Passes</h3>
        <button onclick="closeModal('farePassesModal')" class="text-zinc-400 hover:text-white"><i data-lucide="x" class="w-5 h-5"></i></button>
      </div>
      <div class="space-y-3 text-xs">
        <div class="p-3 rounded-2xl bg-white/5 border border-white/10 flex justify-between items-center">
          <div><p class="font-bold text-white">Single Ride (Bus / Auto)</p><p class="text-zinc-400 text-[11px]">Valid 45 mins across campus</p></div>
          <span class="text-sm font-black text-brand-cyan">₹15</span>
        </div>
        <div class="p-3 rounded-2xl bg-white/5 border border-white/10 flex justify-between items-center">
          <div><p class="font-bold text-white">Daily Unlimited Pass</p><p class="text-zinc-400 text-[11px]">Unlimited rides on all Shuttles & EVs</p></div>
          <span class="text-sm font-black text-brand-cyan">₹40</span>
        </div>
        <div class="p-3 rounded-2xl bg-white/5 border border-white/10 flex justify-between items-center">
          <div><p class="font-bold text-white">Semester Pass (4 Months)</p><p class="text-zinc-400 text-[11px]">Includes all routes + priority booking</p></div>
          <span class="text-sm font-black text-brand-cyan">₹999</span>
        </div>
      </div>
      <button onclick="closeModal('farePassesModal'); openPaymentAndBookingModal();" class="btn-gradient w-full py-2.5 rounded-xl text-black font-extrabold text-xs">
        Buy Pass Now →
      </button>
    </div>
  </div>

  <!-- ================= MODAL 5: H4 STRESS TEST SIMULATOR ================= -->
  <div id="h4StressModal" class="fixed inset-0 z-[1000] bg-black/75 backdrop-blur-md hidden place-items-center p-4">
    <div class="glass-panel w-full max-w-md p-6 rounded-3xl border border-white/15 space-y-4 animate-pop-in">
      <div class="flex items-center justify-between">
        <h3 class="text-base font-black text-amber-400 flex items-center gap-2">
          <i data-lucide="alert-triangle" class="w-5 h-5"></i> H4 Benchmark Stress Test
        </h3>
        <button onclick="closeModal('h4StressModal')" class="text-zinc-400 hover:text-white"><i data-lucide="x" class="w-5 h-5"></i></button>
      </div>
      <p class="text-xs text-zinc-300 leading-relaxed">
        Simulate severe real-world challenges as defined in the H4 Project Guide: 120s GPS signal blackouts and unexpected campus road blocks.
      </p>
      <div class="space-y-3 pt-2">
        <button onclick="triggerBlackoutOnSelected()" class="w-full py-2.5 rounded-xl bg-amber-500/20 border border-amber-500/40 text-amber-300 font-extrabold text-xs hover:bg-amber-500/30 flex items-center justify-center gap-2">
          <i data-lucide="wifi-off" class="w-4 h-4"></i> Trigger 120s GPS Blackout (Dead-Reckoning)
        </button>
        <button onclick="triggerJamOnSelected()" class="w-full py-2.5 rounded-xl bg-rose-500/20 border border-rose-500/40 text-rose-300 font-extrabold text-xs hover:bg-rose-500/30 flex items-center justify-center gap-2">
          <i data-lucide="traffic-cone" class="w-4 h-4"></i> Inject Campus Traffic Jam (+15 min Delay)
        </button>
      </div>
    </div>
  </div>

  <!-- ================= FLOATING WAYZEN CHATBOT WIDGET ================= -->
  <!-- Cute Speech Bubble Popping Out -->
  <div id="wayzenSpeechBubble" class="fixed bottom-24 right-6 z-[9990] max-w-xs glass-panel speech-bubble-tail p-3.5 rounded-2xl border border-brand-cyan/40 shadow-2xl animate-pop-in transition-all cursor-pointer" onclick="toggleWayzenChat()">
    <div class="flex items-start justify-between gap-2">
      <div class="flex items-center gap-1.5 text-brand-cyan font-black text-[11px]">
        <span class="animate-bounce">🤖</span>
        <span>WAYZEN AI</span>
      </div>
      <button onclick="event.stopPropagation(); closeWayzenBubble();" class="text-zinc-400 hover:text-white text-xs">×</button>
    </div>
    <p id="wayzenBubbleText" class="text-xs text-white mt-1 leading-snug font-medium">
      👋 Oye hero! 8:30 AM class ke liye late ho raha hai? Bus ka ETA puch le! 🚌
    </p>
  </div>

  <!-- Cute Floating Button -->
  <button id="wayzenFloatingBtn" onclick="toggleWayzenChat()" class="fixed bottom-6 right-6 z-[9990] w-14 h-14 rounded-full bg-gradient-to-tr from-brand-cyan via-purple-600 to-brand-violet p-0.5 shadow-2xl hover:scale-110 active:scale-95 transition-all group flex items-center justify-center animate-wiggle" title="WAYZEN Campus AI Buddy">
    <div class="w-full h-full rounded-full bg-[#090d1e] flex items-center justify-center relative overflow-hidden">
      <!-- Glow Aura -->
      <div class="absolute inset-0 bg-brand-cyan/20 rounded-full animate-ping pointer-events-none"></div>
      <span class="text-2xl group-hover:scale-125 transition-transform">🤖</span>
      <!-- Notification Dot -->
      <span class="absolute top-1 right-1 w-3 h-3 rounded-full bg-brand-cyan border-2 border-black"></span>
    </div>
  </button>

  <!-- WAYZEN Chat Modal / Window -->
  <div id="wayzenChatModal" class="fixed bottom-24 right-4 sm:right-6 z-[9995] w-[92vw] sm:w-[410px] h-[550px] max-h-[85vh] glass-panel rounded-3xl border border-brand-cyan/30 shadow-2xl hidden flex-col overflow-hidden animate-pop-in backdrop-blur-2xl bg-[#090d1e]/95">
    
    <!-- Header -->
    <div class="p-4 border-b border-white/10 flex items-center justify-between bg-white/5 shrink-0">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-2xl bg-gradient-to-tr from-brand-cyan to-brand-purple flex items-center justify-center text-xl shadow-lg shadow-brand-cyan/20 shrink-0">
          🤖
        </div>
        <div>
          <div class="flex items-center gap-1.5">
            <h3 class="text-sm font-black text-white">WAYZEN</h3>
            <span class="text-[9px] font-mono px-2 py-0.5 rounded-full bg-brand-cyan/20 text-brand-cyan font-bold border border-brand-cyan/30">AI Buddy</span>
          </div>
          <p class="text-[10px] text-zinc-400">Speaks English + Hinglish • 24/7 Active</p>
        </div>
      </div>
      <div class="flex items-center gap-1.5">
        <button onclick="toggleHinglishMode()" id="wayzenHinglishToggle" class="px-2 py-1 rounded-lg bg-brand-cyan/20 text-brand-cyan text-[10px] font-bold border border-brand-cyan/40" title="Toggle Hinglish">
          🇮🇳 Hinglish
        </button>
        <button onclick="toggleWayzenSound()" id="wayzenSoundBtn" class="p-1.5 rounded-lg text-zinc-400 hover:text-white hover:bg-white/10" title="Sound Effects">
          🔊
        </button>
        <button onclick="toggleWayzenChat()" class="p-1.5 rounded-lg text-zinc-400 hover:text-white hover:bg-white/10">
          <i data-lucide="x" class="w-4 h-4"></i>
        </button>
      </div>
    </div>

    <!-- Quick Action Chips -->
    <div class="p-2 border-b border-white/5 bg-black/30 flex items-center gap-1.5 overflow-x-auto text-[11px] font-semibold text-zinc-300 shrink-0">
      <button onclick="sendWayzenPrompt('Next bus kab aayegi?')" class="px-2.5 py-1 rounded-xl bg-white/5 hover:bg-white/15 whitespace-nowrap border border-white/10">🚏 Next Bus?</button>
      <button onclick="sendWayzenPrompt('Auto bula do')" class="px-2.5 py-1 rounded-xl bg-white/5 hover:bg-white/15 whitespace-nowrap border border-white/10">🛺 Auto Bulao</button>
      <button onclick="sendWayzenPrompt('Mera wallet balance kitna hai?')" class="px-2.5 py-1 rounded-xl bg-white/5 hover:bg-white/15 whitespace-nowrap border border-white/10">💳 Wallet?</button>
      <button onclick="sendWayzenPrompt('Driver OTP do')" class="px-2.5 py-1 rounded-xl bg-white/5 hover:bg-white/15 whitespace-nowrap border border-white/10">🔢 Driver OTP</button>
      <button onclick="sendWayzenPrompt('Koi discount coupon hai?')" class="px-2.5 py-1 rounded-xl bg-white/5 hover:bg-white/15 whitespace-nowrap border border-white/10">🎟️ 10% Off</button>
      <button onclick="sendWayzenPrompt('Ek campus joke sunao!')" class="px-2.5 py-1 rounded-xl bg-white/5 hover:bg-white/15 whitespace-nowrap border border-white/10">😂 Joke Sunao</button>
      <button onclick="sendWayzenPrompt('Library kaise jau?')" class="px-2.5 py-1 rounded-xl bg-white/5 hover:bg-white/15 whitespace-nowrap border border-white/10">📍 Library Route</button>
    </div>

    <!-- Chat Messages Scroll Container -->
    <div id="wayzenChatMessages" class="flex-1 overflow-y-auto p-4 space-y-3.5 text-xs">
      <!-- Welcome message populated via JS -->
    </div>

    <!-- Input Bar -->
    <div class="p-3 border-t border-white/10 bg-[#070913] flex items-center gap-2 shrink-0">
      <input type="text" id="wayzenInput" placeholder="Puchho WAYZEN se (Hindi / English / Hinglish)..." onkeydown="if(event.key==='Enter') sendWayzenMessage()" class="glass-input flex-1 px-4 py-2.5 rounded-xl text-xs font-semibold text-white">
      <button onclick="sendWayzenMessage()" class="btn-gradient p-2.5 rounded-xl text-black font-bold">
        <i data-lucide="send" class="w-4 h-4"></i>
      </button>
    </div>

  </div>

  <!-- ================= JAVASCRIPT LOGIC ================= -->
  <script>
    // System State Variables
    let map = null;
    let vehicleMarkers = {};
    let stopMarkers = [];
    let routePolylineLayer = null;
    let simSpeedWarp = 1;
    let simTime = 0;
    let currentUser = null;
    let selectedVehicleId = 'bus_1';
    let followingVehicleId = null;
    let currentFilterType = 'all';

    // Payment & Wallet State
    let selectedMoney = 15;
    let appliedCoupon = 'CAMPUS10';
    let currentPaymentMethod = 'upi';
    let walletBalance = 240.00;
    let activeOtpCode = '8392';
    let topUpAmount = 100;
    let topUpMethod = 'upi';

    // WAYZEN Chat State
    let wayzenHinglish = true;
    let wayzenSound = true;
    let wayzenBubbleInterval = null;
    const WAYZEN_PUNCHLINES = [
      "👋 Oye hero! 8:30 AM class ke liye late ho raha hai? Bus ka ETA puch le! 🚌",
      "🛺 Rickshaw wale bhaiya meter se nahi, dil se chalte hain! Book karun kya?",
      "🤑 Wallet me paise khatam? WAYZEN se 10% coupon code CAMPUS10 le lo!",
      "⚡ Hostel se Library EV cart sirf 3 min dur hai! Hop on!",
      "🤖 WAYZEN is 24/7 active! Ask me anything in English ya Hinglish!",
      "🎒 Attendance 75% se kam hai? Chalo jaldi shuttle pakdo!",
      "🍕 Food Court jana hai? Auto #2 is arriving in 2 minutes!"
    ];

    // Transaction History Array
    let paymentHistory = [
      { id: 'TXN-9041', type: 'topup', title: 'Wallet Top-Up via Google Pay UPI', amount: 200.00, date: 'Today, 11:45 AM', status: 'Success ✅' },
      { id: 'TXN-8820', type: 'ride', title: 'Shuttle #1 Ride to Central Library', amount: -15.00, date: 'Today, 10:15 AM', status: 'OTP Verified 🚌' },
      { id: 'TXN-7911', type: 'ride', title: 'Auto #2 to Boys Hostel Quad', amount: -30.00, date: 'Yesterday, 8:30 PM', status: 'OTP Verified 🛺' },
      { id: 'TXN-6540', type: 'promo', title: 'Promo Discount Cashback (CAMPUS10)', amount: 15.00, date: 'Yesterday, 8:31 PM', status: 'Applied 🎁' },
      { id: 'TXN-5410', type: 'ride', title: 'Eco EV #3 to Sports Complex', amount: -10.00, date: '19 Nov, 4:20 PM', status: 'Completed ⚡' }
    ];

    // Driver Chat Log
    let driverChatHistory = [
      { sender: 'driver', text: 'Namaste ji! I am near Central Library circle. Please have your 4-digit OTP ready.' }
    ];

    // WAYZEN Chat Log
    let wayzenChatLog = [
      {
        sender: 'wayzen',
        text: '👋 Arre Namaste! Main hoon <strong>WAYZEN</strong>, tumhara 24/7 AI Campus Transit Buddy! 🤖✨<br><br>Main English aur Hinglish dono mast samajhta hoon. Shuttles ka live ETA, Auto booking, Wallet top-up, ya Driver OTP—kuch bhi puchho!',
        quickAction: null
      }
    ];

    // Audio Synthesizer (Offline Web Audio API)
    function playBeep(freq = 600, type = 'sine', duration = 0.08) {
      if (!wayzenSound) return;
      try {
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.15, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime + duration);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + duration);
      } catch(e) {}
    }

    // Campus Stops Dataset
        // ================= LOVELY PROFESSIONAL UNIVERSITY (LPU) MULTI-ROUTE TRANSIT =================
    // 21 Verified Campus Landmarks, Blocks 1-36, Hostels BH 1-12, GH 1-7, UniMall, Unipolis & Parkings
    const LPU_STOPS = [
      // Primary Gate & Admin
      { id: 'lpu_main_gate', name: 'Main Gate (GT Road NH-44)', code: 'MG', cat: 'gate', icon: '⛩️', lat: 31.2485, lng: 75.7015, desc: 'Main University Entrance, Welcome Arch & Security Checkpoint' },
      { id: 'lpu_admission', name: 'Admission Block (Block 30)', code: 'AB-30', cat: 'admin', icon: '🏛️', lat: 31.2500, lng: 75.7032, desc: 'Division of Admissions, International Relations & Student Center' },
      
      // Central Student Hubs
      { id: 'lpu_unimall', name: 'UniMall Student Complex', code: 'UM', cat: 'mall', icon: '🛍️', lat: 31.2518, lng: 75.7042, desc: '5-Story Campus Mall: Food Courts, Banks, Stationery, Supermarket & Salon' },
      { id: 'lpu_unipolis', name: 'Unipolis Open Amphitheatre', code: 'UP', cat: 'landmark', icon: '🎪', lat: 31.2535, lng: 75.7040, desc: 'Iconic Covered Mega Arena & Campus Cultural Heart' },
      { id: 'lpu_library', name: 'Central Library (B.R. Mittal)', code: 'LIB', cat: 'library', icon: '📚', lat: 31.2555, lng: 75.7038, desc: '9-Story Resource Library, 24/7 Digital Archives & Quiet Reading Halls' },
      { id: 'lpu_robopark', name: 'Robopark & Innovation Arena', code: 'ROBO', cat: 'innov', icon: '🤖', lat: 31.2578, lng: 75.7065, desc: 'Robotics Center, Drone Arena, AI Labs & Electric Vehicle Prototyping' },

      // Sports & Fitness
      { id: 'lpu_cricket', name: 'International Cricket Stadium', code: 'CS', cat: 'sports', icon: '🏏', lat: 31.2530, lng: 75.7095, desc: 'ICC-Standard Turf Pitch, Pavilion & Floodlit Night Matches' },
      { id: 'lpu_indoor_sports', name: 'Indoor Sports Complex & Gym', code: 'ISC', cat: 'sports', icon: '🏊', lat: 31.2550, lng: 75.7100, desc: 'Olympic Swimming Pool, 12 Badminton Courts, Squash & High-Performance Gym' },

      // 4 Dedicated Campus Parkings
      { id: 'lpu_parking_1', name: 'Parking P1 (Main Gate & Visitors)', code: 'P1', cat: 'parking', icon: '🅿️', lat: 31.2492, lng: 75.7030, desc: 'Capacity: 350 Vehicles • EV Fast Charging Stations' },
      { id: 'lpu_parking_2', name: 'Parking P2 (UniMall Multilevel)', code: 'P2', cat: 'parking', icon: '🅿️', lat: 31.2520, lng: 75.7052, desc: 'Capacity: 500 Vehicles • Student 2-Wheelers & Day-Scholar Cars' },
      { id: 'lpu_parking_3', name: 'Parking P3 (Block 34 North Parking)', code: 'P3', cat: 'parking', icon: '🅿️', lat: 31.2575, lng: 75.7045, desc: 'Capacity: 300 Vehicles • Engineering Faculty & Tech Commuters' },
      { id: 'lpu_parking_4', name: 'Parking P4 (Sports Arena East)', code: 'P4', cat: 'parking', icon: '🅿️', lat: 31.2555, lng: 75.7115, desc: 'Capacity: 400 Vehicles • Tournament & Stadium Parking' },

      // Academic Block Clusters (Blocks 1 to 36)
      { id: 'lpu_blocks_1_5', name: 'Academic Blocks 1-5 (Polytechnic)', code: 'B1-5', cat: 'academic', icon: '🏫', lat: 31.2510, lng: 75.7018, desc: 'Blocks 1, 2, 3, 4, 5 — Diploma, Physics, Basic Chemistry & Electrical Labs' },
      { id: 'lpu_blocks_6_10', name: 'Academic Blocks 6-10 (Applied Sciences)', code: 'B6-10', cat: 'academic', icon: '🏫', lat: 31.2528, lng: 75.7022, desc: 'Blocks 6, 7, 8, 9, 10 — Mathematics, Humanities, Social Sciences & Languages' },
      { id: 'lpu_blocks_11_15', name: 'Academic Blocks 11-15 (Business & Law)', code: 'B11-15', cat: 'academic', icon: '🏫', lat: 31.2545, lng: 75.7025, desc: 'Blocks 11 to 15 — Mittal School of Business, Moot Court & Economics' },
      { id: 'lpu_blocks_16_24', name: 'Academic Blocks 16-24 (Design & Media)', code: 'B16-24', cat: 'academic', icon: '🏫', lat: 31.2562, lng: 75.7032, desc: 'Blocks 16 to 24 — Fashion Design Studios, Architecture & Film Making' },
      { id: 'lpu_blocks_25_29', name: 'Academic Blocks 25-29 (Agri & Biotech)', code: 'B25-29', cat: 'academic', icon: '🏫', lat: 31.2582, lng: 75.7042, desc: 'Blocks 25 to 29 — Agriculture Research Farms, Pharmacy & Bio-Tech Labs' },
      { id: 'lpu_blocks_31_36', name: 'Academic Blocks 31-36 (CSE & Tech Hub)', code: 'B31-36', cat: 'academic', icon: '💻', lat: 31.2568, lng: 75.7052, desc: 'Blocks 31 to 36 — School of CSE, Supercomputing, Data Science & Placement Hub' },

      // Hostels
      { id: 'lpu_girls_hostels', name: 'Girls Hostels Sector (GH 1 to GH 7)', code: 'GH1-7', cat: 'hostel_girls', icon: '🏡', lat: 31.2508, lng: 75.7068, desc: 'Residential Sector GH-1 to GH-7: Dedicated Dining, Salon & Strict Curfew Security' },
      { id: 'lpu_boys_hostels_1_6', name: 'Boys Hostels North (BH 1 to BH 6)', code: 'BH1-6', cat: 'hostel_boys', icon: '🏢', lat: 31.2592, lng: 75.7052, desc: 'Residential Towers BH-1, BH-2, BH-3, BH-4, BH-5, BH-6 along North Avenue' },
      { id: 'lpu_boys_hostels_7_12', name: 'Boys Hostels East (BH 7 to BH 12)', code: 'BH7-12', cat: 'hostel_boys', icon: '🏢', lat: 31.2572, lng: 75.7092, desc: 'Residential Towers BH-7, BH-8, BH-9, BH-10, BH-11, BH-12 near Sports Complex' }
    ];

    const STOPS = LPU_STOPS; // Backward compatibility

    // 4 Complex, Intersecting Transit Routes around LPU Roads
    const LPU_ROUTES = {
      route_purple: {
        id: 'route_purple',
        name: 'Ring Road & Hostels Loop',
        code: 'LINE-1',
        color: '#a855f7',
        coords: [
          [31.2485, 75.7015], [31.2492, 75.7030], [31.2500, 75.7032], [31.2508, 75.7068],
          [31.2520, 75.7080], [31.2530, 75.7095], [31.2550, 75.7100], [31.2555, 75.7115],
          [31.2570, 75.7105], [31.2572, 75.7092], [31.2585, 75.7075], [31.2578, 75.7065],
          [31.2592, 75.7052], [31.2582, 75.7042], [31.2562, 75.7032], [31.2545, 75.7025],
          [31.2528, 75.7022], [31.2510, 75.7018], [31.2485, 75.7015]
        ]
      },
      route_cyan: {
        id: 'route_cyan',
        name: 'Academic Core & Blocks 1-36',
        code: 'LINE-2',
        color: '#00f0ff',
        coords: [
          [31.2485, 75.7015], [31.2510, 75.7018], [31.2528, 75.7022], [31.2545, 75.7025],
          [31.2535, 75.7040], [31.2555, 75.7038], [31.2568, 75.7052], [31.2578, 75.7065],
          [31.2575, 75.7045], [31.2582, 75.7042], [31.2562, 75.7032], [31.2555, 75.7038],
          [31.2535, 75.7040], [31.2518, 75.7042], [31.2492, 75.7030], [31.2485, 75.7015]
        ]
      },
      route_emerald: {
        id: 'route_emerald',
        name: 'Auto Rapid Cross-Campus Connect',
        code: 'LINE-3',
        color: '#10b981',
        coords: [
          [31.2572, 75.7092], [31.2550, 75.7100], [31.2530, 75.7095], [31.2518, 75.7042],
          [31.2520, 75.7052], [31.2508, 75.7068], [31.2500, 75.7032], [31.2510, 75.7018],
          [31.2535, 75.7040], [31.2568, 75.7052], [31.2592, 75.7052], [31.2578, 75.7065],
          [31.2572, 75.7092]
        ]
      },
      route_amber: {
        id: 'route_amber',
        name: 'Eco EV Green Campus Circulator',
        code: 'LINE-4',
        color: '#f59e0b',
        coords: [
          [31.2578, 75.7065], [31.2568, 75.7052], [31.2555, 75.7038], [31.2535, 75.7040],
          [31.2518, 75.7042], [31.2508, 75.7068], [31.2530, 75.7095], [31.2550, 75.7100],
          [31.2555, 75.7115], [31.2570, 75.7105], [31.2578, 75.7065]
        ]
      }
    };

    const CAMPUS_ROUTE_COORDS = LPU_ROUTES.route_purple.coords;

    // Simulation Fleet with Real-time Seat Occupancy, Route Assignment & Independent Offsets
    let FLEET = [
      { id: 'bus_1', category: 'bus', routeId: 'route_purple', typeName: '50-Seater Campus Shuttle', name: 'Shuttle #1 (Ring Loop)', plate: 'PB 08 BX 9021', driver: 'Rajesh Sharma', phone: '+91 98765-43210', totalSeats: 50, occupiedSeats: 42, availableSeats: 8, fare: 15, rating: 4.9, speed: 28, battery: 84, s: 300, icon: '🚌', color: '#a855f7', delay: 0 },
      { id: 'auto_2', category: 'auto', routeId: 'route_emerald', typeName: '3-Seater Campus Auto', name: 'Auto #2 (Hostels ➔ UniMall)', plate: 'PB 08 CA 1201', driver: 'Vikram Singh', phone: '+91 98140-55672', totalSeats: 3, occupiedSeats: 2, availableSeats: 1, fare: 30, rating: 4.8, speed: 32, battery: 92, s: 200, icon: '🛺', color: '#10b981', delay: 0 },
      { id: 'ev_3', category: 'ev', routeId: 'route_amber', typeName: '6-Seater Eco EV Cart', name: 'Eco EV #3 (Robopark Circulator)', plate: 'PB 08 EV 0044', driver: 'Suresh Yadav', phone: '+91 94170-88321', totalSeats: 6, occupiedSeats: 5, availableSeats: 1, fare: 10, rating: 4.9, speed: 20, battery: 78, s: 400, icon: '⚡', color: '#f59e0b', delay: 0 },
      { id: 'bus_4', category: 'bus', routeId: 'route_cyan', typeName: '50-Seater Express Bus', name: 'Express #4 (Blocks 1-36 Core)', plate: 'PB 08 BX 9410', driver: 'Amit Patel', phone: '+91 99882-11490', totalSeats: 50, occupiedSeats: 35, availableSeats: 15, fare: 15, rating: 4.7, speed: 30, battery: 65, s: 800, icon: '🚌', color: '#00f0ff', delay: 0 },
      { id: 'auto_5', category: 'auto', routeId: 'route_emerald', typeName: '3-Seater Campus Auto', name: 'Auto #5 (Sports & Unipolis)', plate: 'PB 08 CA 3381', driver: 'Priya Verma', phone: '+91 98721-66710', totalSeats: 3, occupiedSeats: 1, availableSeats: 2, fare: 30, rating: 5.0, speed: 31, battery: 88, s: 1300, icon: '🛺', color: '#10b981', delay: 0 },
      { id: 'ev_6', category: 'ev', routeId: 'route_amber', typeName: '6-Seater Medical & Sports Cart', name: 'Eco EV #6 (Library Shuttle)', plate: 'PB 08 EV 0092', driver: 'Sunita Gupta', phone: '+91 94630-11220', totalSeats: 6, occupiedSeats: 4, availableSeats: 2, fare: 10, rating: 4.9, speed: 18, battery: 95, s: 1500, icon: '⚡', color: '#f59e0b', delay: 0 },
      { id: 'bus_7', category: 'bus', routeId: 'route_purple', typeName: '50-Seater AC Shuttle', name: 'Shuttle #7 (BH 1-12 & UniMall)', plate: 'PB 08 BX 8812', driver: 'Ramesh Kumar', phone: '+91 98155-77441', totalSeats: 50, occupiedSeats: 48, availableSeats: 2, fare: 15, rating: 4.8, speed: 26, battery: 54, s: 2100, icon: '🚌', color: '#a855f7', delay: 0 },
      { id: 'auto_8', category: 'auto', routeId: 'route_emerald', typeName: '3-Seater Campus Auto', name: 'Auto #8 (GH 1-7 & Admission)', plate: 'PB 08 CA 5509', driver: 'Deepak Sharma', phone: '+91 98788-33219', totalSeats: 3, occupiedSeats: 0, availableSeats: 3, fare: 30, rating: 4.9, speed: 33, battery: 90, s: 2500, icon: '🛺', color: '#10b981', delay: 0 }
    ];

    // Precompute Cumulative Distances for All Routes
    function haversineDist(c1, c2) {
      const R = 6371000;
      const dLat = (c2[0] - c1[0]) * Math.PI / 180;
      const dLng = (c2[1] - c1[1]) * Math.PI / 180;
      const a = Math.sin(dLat/2)**2 + Math.cos(c1[0]*Math.PI/180) * Math.cos(c2[0]*Math.PI/180) * Math.sin(dLng/2)**2;
      return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    }

    Object.keys(LPU_ROUTES).forEach(k => {
      const r = LPU_ROUTES[k];
      r.totalDist = 0;
      r.cumDistances = [0];
      for (let i = 0; i < r.coords.length - 1; i++) {
        const d = haversineDist(r.coords[i], r.coords[i+1]);
        r.totalDist += d;
        r.cumDistances.push(r.totalDist);
      }
    });

    let routeTotalDist = LPU_ROUTES.route_purple.totalDist;

    function getCoordOnRoute(routeId, dist) {
      const r = LPU_ROUTES[routeId] || LPU_ROUTES.route_purple;
      const d = (dist % r.totalDist + r.totalDist) % r.totalDist;
      for (let i = 0; i < r.cumDistances.length - 1; i++) {
        if (d >= r.cumDistances[i] && d <= r.cumDistances[i+1]) {
          const segDist = r.cumDistances[i+1] - r.cumDistances[i];
          const frac = segDist === 0 ? 0 : (d - r.cumDistances[i]) / segDist;
          const p1 = r.coords[i];
          const p2 = r.coords[i+1];
          const lat = p1[0] + (p2[0] - p1[0]) * frac;
          const lng = p1[1] + (p2[1] - p1[1]) * frac;
          const heading = Math.atan2(p2[1] - p1[1], p2[0] - p1[0]) * 180 / Math.PI;
          return { lat, lng, heading };
        }
      }
      return { lat: r.coords[0][0], lng: r.coords[0][1], heading: 0 };
    }

    function getCoordAtDistance(dist) {
      return getCoordOnRoute('route_purple', dist);
    }

    let routePolylineLayers = {};

    function initCampusMap() {
      if (map) return;
      map = L.map('campusMap', { zoomControl: false }).setView([31.2540, 75.7055], 16);
      setMapTheme('dark');

      // Draw all 4 Multi-Transit Routes on LPU Roads
      Object.keys(LPU_ROUTES).forEach(k => {
        const r = LPU_ROUTES[k];
        const poly = L.polyline(r.coords, {
          color: r.color,
          weight: 4.5,
          opacity: 0.85,
          dashArray: k === 'route_emerald' ? '6, 6' : (k === 'route_amber' ? '4, 4' : null),
          lineCap: 'round'
        }).addTo(map);

        poly.bindTooltip(`<span class="font-bold text-xs">${r.name} (${r.code})</span>`, { sticky: true });
        routePolylineLayers[k] = poly;
      });

      routePolylineLayer = routePolylineLayers.route_purple;

      // LPU Campus Landmarks, Academic Blocks 1-36, Hostels & Parkings
      LPU_STOPS.forEach(stop => {
        const catColors = {
          gate: '#00f0ff',
          admin: '#a855f7',
          mall: '#f59e0b',
          landmark: '#6366f1',
          library: '#3b82f6',
          innov: '#06b6d4',
          sports: '#10b981',
          parking: '#eab308',
          academic: '#8b5cf6',
          hostel_girls: '#ec4899',
          hostel_boys: '#3b82f6'
        };
        const color = catColors[stop.cat] || '#00f0ff';

        const icon = L.divIcon({
          className: 'pulse-marker-icon',
          html: `
            <div class="relative group cursor-pointer">
              <div class="w-6 h-6 rounded-xl bg-[#0b0f22]/90 border border-white/30 text-xs flex items-center justify-center shadow-lg hover:scale-125 transition-transform" style="box-shadow: 0 0 10px ${color}66;">
                <span>${stop.icon || '📍'}</span>
              </div>
              <div class="absolute -bottom-6 left-1/2 -translate-x-1/2 whitespace-nowrap px-1.5 py-0.5 rounded-md bg-black/90 border border-white/20 text-[9px] font-black text-white pointer-events-none hidden group-hover:block z-30">
                ${stop.name}
              </div>
            </div>
          `,
          iconSize: [24, 24],
          iconAnchor: [12, 12]
        });

        const marker = L.marker([stop.lat, stop.lng], { icon }).addTo(map);
        marker.bindPopup(`
          <div class="p-3 text-xs font-sans space-y-1.5 min-w-[230px]">
            <div class="flex items-center gap-2 border-b border-white/10 pb-1.5">
              <span class="text-xl">${stop.icon || '📍'}</span>
              <div>
                <strong class="text-white font-black text-xs">${stop.name}</strong>
                <span class="text-[10px] font-mono text-brand-cyan font-bold block">Code: ${stop.code}</span>
              </div>
            </div>
            <p class="text-[11px] text-zinc-300 leading-snug">${stop.desc}</p>
            <div class="pt-1.5 flex items-center justify-between text-[10px] font-mono text-emerald-400 border-t border-white/10">
              <span>● LPU Active Station</span>
              <button onclick="filterByStop('${stop.id}')" class="text-brand-cyan underline font-bold">Find Shuttles →</button>
            </div>
          </div>
        `);
        stopMarkers.push(marker);
      });

      // Fit map smoothly to the road loop
      if (routePolylineLayer) {
        setTimeout(() => map.fitBounds(routePolylineLayer.getBounds().pad(0.08)), 200);
      }

      // Fleet Markers
      FLEET.forEach(v => {
        const pos = getCoordOnRoute(v.routeId, v.s);
        const seatColor = v.availableSeats > 2 ? '#10b981' : (v.availableSeats > 0 ? '#f59e0b' : '#ef4444');
        const icon = L.divIcon({
          className: 'pulse-marker-icon',
          html: `
            <div class="relative group cursor-pointer" onclick="selectVehicle('${v.id}')">
              <div class="bus-marker-3d" style="background:${v.color};">
                <span class="text-sm font-black">${v.icon}</span>
                <div class="bus-heading-needle" id="needle_${v.id}" style="transform: rotate(${pos.heading}deg)"></div>
              </div>
              <div class="absolute -top-7 left-1/2 -translate-x-1/2 whitespace-nowrap px-2 py-0.5 rounded-full bg-[#080c1e]/95 backdrop-blur-md border border-white/20 text-[9px] font-black shadow-xl flex items-center gap-1 z-20 pointer-events-none">
                <span class="text-brand-cyan">${v.category === 'auto' ? 'Auto' : (v.category === 'ev' ? 'EV' : 'Bus')}</span>
                <span class="w-1 h-1 rounded-full bg-zinc-500"></span>
                <span style="color:${seatColor};" class="font-mono">💺 ${v.availableSeats} free</span>
              </div>
            </div>
          `,
          iconSize: [42, 42],
          iconAnchor: [21, 21]
        });
        const m = L.marker([pos.lat, pos.lng], { icon }).addTo(map);

        // Bind interactive dark HUD popup
        const occupancyPct = Math.round((v.occupiedSeats / v.totalSeats) * 100);
        const popupContent = `
          <div class="p-3.5 space-y-2.5 min-w-[250px] text-xs font-sans">
            <div class="flex items-center justify-between border-b border-white/10 pb-2">
              <div class="flex items-center gap-2">
                <span class="text-2xl">${v.icon}</span>
                <div>
                  <h4 class="font-black text-white text-xs">${v.name}</h4>
                  <span class="text-[10px] font-bold text-brand-cyan uppercase tracking-wider">${v.typeName}</span>
                </div>
              </div>
              <span class="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full ${v.availableSeats > 2 ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : (v.availableSeats > 0 ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30' : 'bg-rose-500/20 text-rose-400 border border-rose-500/30')}">
                💺 ${v.availableSeats} Free
              </span>
            </div>

            <div class="space-y-1">
              <div class="flex items-center justify-between text-[10px] font-semibold text-zinc-300">
                <span>Seats Occupancy: <strong>${v.occupiedSeats} / ${v.totalSeats}</strong></span>
                <span class="${occupancyPct > 85 ? 'text-amber-400' : 'text-emerald-400'} font-mono">${occupancyPct}% Full</span>
              </div>
              <div class="w-full h-2 rounded-full bg-white/10 overflow-hidden">
                <div class="h-full rounded-full ${occupancyPct > 85 ? 'bg-amber-400' : 'bg-brand-cyan'}" style="width: ${occupancyPct}%"></div>
              </div>
            </div>

            <div class="p-2 rounded-xl bg-white/5 border border-white/10 flex items-center justify-between text-[11px]">
              <div>
                <p class="font-bold text-white flex items-center gap-1.5">
                  <span>👨‍✈️ ${v.driver}</span>
                  <span class="text-amber-400 font-mono text-[10px]">★ ${v.rating}</span>
                </p>
                <p class="text-[10px] text-zinc-400 font-mono">${v.plate} • ${v.phone}</p>
              </div>
              <button onclick="callDriver('${v.phone}', '${v.driver}')" class="px-2 py-1 rounded-lg bg-emerald-500/20 text-emerald-400 hover:bg-emerald-500/30 font-bold flex items-center gap-1" title="Call Driver">
                📞 Call
              </button>
            </div>

            <div class="grid grid-cols-2 gap-1.5 pt-1">
              <button onclick="openDriverChat('${v.id}')" class="py-1.5 px-2 rounded-xl bg-gradient-to-r from-brand-cyan to-brand-purple text-black font-black text-[11px] flex items-center justify-center gap-1 hover:opacity-90 shadow-sm">
                💬 Chat Driver
              </button>
              <button onclick="openSeatLayoutModal('${v.id}')" class="py-1.5 px-2 rounded-xl bg-white/10 hover:bg-white/20 text-white font-bold text-[11px] flex items-center justify-center gap-1 border border-white/15">
                💺 View Seats
              </button>
            </div>
          </div>
        `;

        m.bindPopup(popupContent, { maxWidth: 300 });
        m.on('click', () => selectVehicle(v.id));
        vehicleMarkers[v.id] = m;
      });
    }

    function setMapTheme(theme) {
      if (!map) return;
      if (window.currentTileLayer) map.removeLayer(window.currentTileLayer);
      let url = 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png';
      if (theme === 'osm') url = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png';
      else if (theme === 'satellite') url = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';
      window.currentTileLayer = L.tileLayer(url, { maxZoom: 19 }).addTo(map);
    }

    function recenterCampusMap() {
      if (map && routePolylineLayer) { map.fitBounds(routePolylineLayer.getBounds().pad(0.08)); } else if (map) { map.setView([31.2548, 75.7058], 16); }
    }

    // View Navigation
    function showLandingPage() {
      document.getElementById('landingPageWrapper').classList.remove('hidden');
      document.getElementById('mainTransportDashboard').classList.add('hidden');
      if (currentUser && currentUser.name) {
        const inp = document.getElementById('suFullName');
        if (inp && !inp.value) inp.value = currentUser.name;
        updateUserAccountPill();
        updateWalletDisplay();
      }
    }

    function launchTransportDashboard() {
      document.getElementById('landingPageWrapper').classList.add('hidden');
      document.getElementById('mainTransportDashboard').classList.remove('hidden');
      if (!map) {
        initCampusMap();
      }
      setTimeout(() => map && map.invalidateSize(), 100);
      renderFleetList();
    }

    function scrollToLandingSection(id) {
      showLandingPage();
      const el = document.getElementById(id);
      if (el) el.scrollIntoView({ behavior: 'smooth' });
    }

    function toggleHeroBgVideo() {
      // Clean modern background active
    }

    // FAQ Accordion Toggle
    function toggleFaqAccordion(num) {
      const ans = document.getElementById('faqAnswer' + num);
      const chev = document.getElementById('faqChevron' + num);
      if (!ans) return;
      const isHidden = ans.classList.contains('hidden');
      document.querySelectorAll('[id^="faqAnswer"]').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('[id^="faqChevron"]').forEach(el => el.style.transform = 'rotate(0deg)');
      if (isHidden) {
        ans.classList.remove('hidden');
        if (chev) chev.style.transform = 'rotate(180deg)';
      }
    }

    // Wallet Modal & Top-Up
    function openWalletModal() {
      updateWalletDisplay();
      renderWalletHistory();
      openModal('walletModal');
    }

    function previewUserName(val) {
      const trimmed = val.trim();
      const pill = document.getElementById('userAccountPill');
      const cardHolder = document.getElementById('walletCardHolder');
      if (trimmed) {
        if (pill) pill.textContent = `👤 ${trimmed}`;
        if (cardHolder) cardHolder.textContent = trimmed;
      } else {
        if (pill && (!currentUser || !currentUser.name)) pill.textContent = 'Sign Up / Login';
        if (cardHolder && (!currentUser || !currentUser.name)) cardHolder.textContent = 'Student';
      }
    }

    function updateWalletDisplay() {
      const balStr = '₹ ' + walletBalance.toFixed(2);
      const navBal = document.getElementById('navWalletBalance');
      if (navBal) navBal.textContent = balStr;
      const cardBal = document.getElementById('walletCardBalance');
      if (cardBal) cardBal.textContent = balStr;
      const modalBal = document.getElementById('modalWalletBalance');
      if (modalBal) modalBal.textContent = balStr;

      const entered = document.getElementById('suFullName') ? document.getElementById('suFullName').value.trim() : '';
      const name = (currentUser && currentUser.name) ? currentUser.name : (entered || 'Student');
      const studentId = (currentUser && currentUser.studentId) ? currentUser.studentId : (document.getElementById('suStudentId') ? document.getElementById('suStudentId').value.trim() || 'STU-2024-8891' : 'STU-2024-8891');

      const cardHolderEl = document.getElementById('walletCardHolder');
      if (cardHolderEl) cardHolderEl.textContent = name;
      const cardIdEl = document.getElementById('walletCardStudentId');
      if (cardIdEl) cardIdEl.textContent = studentId;

      const passName = document.getElementById('sidebarPassName');
      if (passName) passName.textContent = name;
      const passBal = document.getElementById('sidebarPassBalance');
      if (passBal) passBal.textContent = balStr;
      const passId = document.getElementById('sidebarPassId');
      if (passId) passId.textContent = studentId;
    }

    function selectTopUpAmount(amt, btn) {
      topUpAmount = amt;
      document.getElementById('customTopUpInput').value = '';
      document.getElementById('topUpBtnAmount').textContent = '₹' + amt;
      document.querySelectorAll('.topup-chip').forEach(b => {
        b.className = 'topup-chip py-2 rounded-xl text-xs font-bold border border-white/10 bg-white/5 text-zinc-300 hover:border-brand-cyan';
      });
      if (btn) btn.className = 'topup-chip py-2 rounded-xl text-xs font-bold border border-brand-cyan bg-brand-cyan/20 text-brand-cyan font-black';
    }

    function handleCustomTopUp(val) {
      const num = parseFloat(val);
      if (!isNaN(num) && num > 0) {
        topUpAmount = num;
        document.getElementById('topUpBtnAmount').textContent = '₹' + num;
        document.querySelectorAll('.topup-chip').forEach(b => {
          b.className = 'topup-chip py-2 rounded-xl text-xs font-bold border border-white/10 bg-white/5 text-zinc-300 hover:border-brand-cyan';
        });
      }
    }

    function selectTopUpMethod(mode, btn) {
      topUpMethod = mode;
      document.querySelectorAll('.topup-method-btn').forEach(b => {
        b.className = 'topup-method-btn p-2 rounded-xl text-[11px] font-bold border border-white/10 bg-white/5 text-zinc-300 hover:border-white/30 text-center';
      });
      if (btn) btn.className = 'topup-method-btn p-2 rounded-xl text-[11px] font-bold border border-brand-cyan bg-brand-cyan/20 text-brand-cyan text-center font-black';
    }

    function executeWalletTopUp() {
      walletBalance += topUpAmount;
      const newTxn = {
        id: 'TXN-' + Math.floor(1000 + Math.random() * 9000),
        type: 'topup',
        title: `Wallet Top-Up via ${topUpMethod.toUpperCase()}`,
        amount: topUpAmount,
        date: 'Just now',
        status: 'Success ✅'
      };
      paymentHistory.unshift(newTxn);
      updateWalletDisplay();
      renderWalletHistory();
      playBeep(880, 'sine', 0.15);
      showToast(`🎉 Recharged ₹${topUpAmount} successfully! New Balance: ₹${walletBalance.toFixed(2)}`);
    }

    function renderWalletHistory(filter = 'all') {
      const container = document.getElementById('walletHistoryContainer');
      if (!container) return;
      const filtered = filter === 'all' ? paymentHistory : paymentHistory.filter(x => x.type === filter);
      if (filtered.length === 0) {
        container.innerHTML = `<div class="p-4 text-center text-zinc-500 text-xs">No transactions in this category.</div>`;
        return;
      }
      container.innerHTML = filtered.map(item => `
        <div class="p-3 rounded-2xl bg-white/5 border border-white/10 flex items-center justify-between text-xs hover:border-white/20 transition-all">
          <div class="flex items-center gap-2.5">
            <span class="text-base">${item.type === 'topup' ? '💳' : item.type === 'ride' ? '🚏' : '🎁'}</span>
            <div>
              <p class="font-bold text-white">${item.title}</p>
              <p class="text-[10px] text-zinc-400">${item.date} • <span class="font-mono">${item.id}</span></p>
            </div>
          </div>
          <div class="text-right">
            <p class="font-black ${item.amount > 0 ? 'text-emerald-400' : 'text-zinc-200'}">
              ${item.amount > 0 ? '+₹' : '-₹'}${Math.abs(item.amount).toFixed(2)}
            </p>
            <span class="text-[9px] text-zinc-400">${item.status}</span>
          </div>
        </div>
      `).join('');
    }

    function filterWalletHistory(type, btn) {
      document.querySelectorAll('.wallet-hist-btn').forEach(b => {
        b.className = 'wallet-hist-btn py-1 rounded-lg hover:text-white';
      });
      if (btn) btn.className = 'wallet-hist-btn py-1 rounded-lg bg-white/15 text-white';
      renderWalletHistory(type);
    }

    function downloadPassbookReceipt() {
      showToast('📄 Statement generated! Sent to your university email.');
    }

    // Payment & Booking Modal
    function openPaymentAndBookingModal() {
      recalculatePrice();
      openModal('paymentBookingModal');
    }

    function selectMoneyAmount(amt, btn) {
      selectedMoney = amt;
      document.getElementById('customAmountInput').value = '';
      document.querySelectorAll('.money-chip').forEach(b => {
        b.className = 'money-chip p-2.5 rounded-xl border border-white/10 bg-white/5 text-zinc-300 hover:border-white/30';
      });
      if (btn) btn.className = 'money-chip p-2.5 rounded-xl border border-brand-cyan bg-brand-cyan/20 text-brand-cyan font-black';
      recalculatePrice();
    }

    function handleCustomAmount(val) {
      const num = parseFloat(val);
      if (!isNaN(num) && num > 0) {
        selectedMoney = num;
        document.querySelectorAll('.money-chip').forEach(b => {
          b.className = 'money-chip p-2.5 rounded-xl border border-white/10 bg-white/5 text-zinc-300 hover:border-white/30';
        });
        recalculatePrice();
      }
    }

    function quickApplyCoupon(code) {
      document.getElementById('couponCodeInput').value = code;
      applyCouponCode();
    }

    function applyCouponCode() {
      const code = document.getElementById('couponCodeInput').value.trim().toUpperCase();
      if (code === 'CAMPUS10' || code === 'FIRSTRIDE10') {
        appliedCoupon = 'CAMPUS10';
        showToast('🎉 Coupon CAMPUS10 applied! 10% discount on first ride.');
      } else if (code === 'FREEFIRST') {
        appliedCoupon = 'FREEFIRST';
        showToast('🎁 Coupon FREEFIRST applied! 100% Free Single Ride.');
      } else if (code === '') {
        appliedCoupon = '';
        showToast('Coupon removed.');
      } else {
        appliedCoupon = '';
        showToast('Invalid coupon code. Try CAMPUS10');
      }
      recalculatePrice();
    }

    function recalculatePrice() {
      let base = selectedMoney;
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
      document.getElementById('priceSummaryBase').textContent = `₹${base.toFixed(2)}`;
      document.getElementById('priceSummaryDiscountLabel').textContent = label;
      document.getElementById('priceSummaryDiscount').textContent = `-₹${discount.toFixed(2)}`;
      document.getElementById('priceSummaryTotal').textContent = `₹${net.toFixed(2)}`;

      const statusEl = document.getElementById('walletPayStatusText');
      if (statusEl) {
        if (walletBalance >= net) {
          statusEl.innerHTML = `✅ Sufficient balance! ₹${net.toFixed(2)} will be debited. (Remaining: ₹${(walletBalance - net).toFixed(2)})`;
          statusEl.className = 'text-xs text-emerald-400 font-bold';
        } else {
          statusEl.innerHTML = `⚠️ Low balance! Need ₹${(net - walletBalance).toFixed(2)} more. Please top up.`;
          statusEl.className = 'text-xs text-amber-400 font-bold';
        }
      }
    }

    function switchPayTab(mode) {
      currentPaymentMethod = mode;
      document.querySelectorAll('.pay-method-tab').forEach(b => {
        b.className = 'pay-method-tab py-2 rounded-xl text-zinc-400 hover:text-white';
      });
      document.getElementById('payContentUpi').classList.add('hidden');
      document.getElementById('payContentWallet').classList.add('hidden');
      document.getElementById('payContentCash').classList.add('hidden');

      if (mode === 'upi') {
        document.getElementById('payTabUpi').className = 'pay-method-tab py-2 rounded-xl bg-white/15 text-brand-cyan shadow-sm';
        document.getElementById('payContentUpi').classList.remove('hidden');
      } else if (mode === 'wallet') {
        document.getElementById('payTabWallet').className = 'pay-method-tab py-2 rounded-xl bg-white/15 text-brand-purple shadow-sm';
        document.getElementById('payContentWallet').classList.remove('hidden');
      } else if (mode === 'cash') {
        document.getElementById('payTabCash').className = 'pay-method-tab py-2 rounded-xl bg-white/15 text-brand-amber shadow-sm';
        document.getElementById('payContentCash').classList.remove('hidden');
      }
    }

    function copyUpiId() {
      navigator.clipboard.writeText('campusflow@okaxis');
      showToast('📋 UPI ID copied: campusflow@okaxis');
    }

    function handlePaymentSuccess() {
      const net = Math.max(0, selectedMoney - (appliedCoupon === 'CAMPUS10' ? selectedMoney * 0.1 : appliedCoupon === 'FREEFIRST' ? selectedMoney : 0));
      if (currentPaymentMethod === 'wallet') {
        if (walletBalance < net) {
          showToast('⚠️ Insufficient Wallet Balance! Please top up or choose UPI.');
          return;
        }
        walletBalance -= net;
        updateWalletDisplay();
      }

      activeOtpCode = Math.floor(1000 + Math.random() * 9000).toString();
      document.getElementById('activeTripOtpBadge').textContent = `OTP: ${activeOtpCode}`;
      document.getElementById('chatOtpDisplay').textContent = activeOtpCode;
      document.getElementById('activeTripBanner').classList.remove('hidden');

      const newTxn = {
        id: 'TXN-' + Math.floor(1000 + Math.random() * 9000),
        type: 'ride',
        title: `Ride Pass (${currentPaymentMethod.toUpperCase()})`,
        amount: -net,
        date: 'Just now',
        status: 'OTP: ' + activeOtpCode
      };
      paymentHistory.unshift(newTxn);
      renderWalletHistory();

      closeModal('paymentBookingModal');
      showToast(`✅ Trip booked! Security OTP: ${activeOtpCode}`);
      openDriverChat();
    }

    
    // ================= SEAT LAYOUT & DRIVER CHAT EXTENSIONS =================
    let currentSeatModalVehicleId = 'bus_1';
    let selectedSeatNumber = null;

    function callDriver(phone, name) {
      playBeep(440, 'sine', 0.1);
      setTimeout(() => playBeep(580, 'sine', 0.15), 120);
      showToast(`📞 Dialing Driver ${name} (${phone})...`);
    }

    function callCurrentDriver() {
      const v = FLEET.find(x => x.id === selectedVehicleId) || FLEET[0];
      callDriver(v.phone, v.driver);
    }

    function bookSpecificVehicle(id) {
      selectedVehicleId = id;
      openPaymentAndBookingModal();
    }

    function openSeatLayoutModal(vehicleId) {
      currentSeatModalVehicleId = vehicleId || selectedVehicleId || 'bus_1';
      const v = FLEET.find(x => x.id === currentSeatModalVehicleId) || FLEET[0];
      selectedVehicleId = v.id;
      selectedSeatNumber = null;

      document.getElementById('seatModalVehicleIcon').textContent = v.icon;
      document.getElementById('seatModalVehicleName').textContent = v.name;
      document.getElementById('seatModalVehiclePlate').textContent = v.plate;
      document.getElementById('seatModalVehicleType').textContent = `${v.typeName} • Driver: ${v.driver} (★ ${v.rating})`;
      document.getElementById('seatModalStatsText').textContent = `${v.availableSeats} of ${v.totalSeats} Seats Free`;
      document.getElementById('seatModalFareText').textContent = `Fare: ₹${v.fare}`;

      document.getElementById('selectedSeatLabel').textContent = 'Click an available green seat to select';
      document.getElementById('selectedSeatSubtitle').textContent = 'Window or aisle seats available with live USB charging';
      document.getElementById('selectedSeatPrice').textContent = '';

      renderSeatGrid(v);
      openModal('seatLayoutModal');
    }

    function renderSeatGrid(v) {
      const container = document.getElementById('seatGridContainer');
      if (!container) return;

      if (v.category === 'auto') {
        // Auto Rickshaw Layout: 1 front driver + 3 rear seats
        container.innerHTML = `
          <div class="text-center text-[10px] text-zinc-400 font-bold uppercase tracking-wider mb-2">Auto Rickshaw Passenger Cabin</div>
          <div class="grid grid-cols-3 gap-3 max-w-sm mx-auto">
            <button onclick="pickSeat('Seat 1 (Window)', ${v.fare})" class="p-4 rounded-2xl border ${v.availableSeats >= 1 ? 'bg-emerald-500/20 border-emerald-500 text-emerald-300 hover:scale-105' : 'bg-rose-500/20 border-rose-500/40 text-rose-400 cursor-not-allowed'} font-bold text-center flex flex-col items-center gap-1 transition-all">
              <span class="text-xl">💺</span>
              <span class="text-xs font-black">Seat 1</span>
              <span class="text-[9px] text-zinc-400">Left Window</span>
            </button>
            <button onclick="pickSeat('Seat 2 (Center)', ${v.fare})" class="p-4 rounded-2xl border ${v.availableSeats >= 2 ? 'bg-emerald-500/20 border-emerald-500 text-emerald-300 hover:scale-105' : 'bg-rose-500/20 border-rose-500/40 text-rose-400 cursor-not-allowed'} font-bold text-center flex flex-col items-center gap-1 transition-all">
              <span class="text-xl">💺</span>
              <span class="text-xs font-black">Seat 2</span>
              <span class="text-[9px] text-zinc-400">Center</span>
            </button>
            <button onclick="pickSeat('Seat 3 (Window)', ${v.fare})" class="p-4 rounded-2xl border ${v.availableSeats >= 3 ? 'bg-emerald-500/20 border-emerald-500 text-emerald-300 hover:scale-105' : 'bg-rose-500/20 border-rose-500/40 text-rose-400 cursor-not-allowed'} font-bold text-center flex flex-col items-center gap-1 transition-all">
              <span class="text-xl">💺</span>
              <span class="text-xs font-black">Seat 3</span>
              <span class="text-[9px] text-zinc-400">Right Window</span>
            </button>
          </div>
        `;
      } else if (v.category === 'ev') {
        // Eco EV Cart: 2 rows of 3 seats
        container.innerHTML = `
          <div class="text-center text-[10px] text-zinc-400 font-bold uppercase tracking-wider mb-2">Eco Electric Shuttle Cart Seating</div>
          <div class="space-y-3 max-w-sm mx-auto">
            <div class="text-[10px] font-bold text-zinc-400">Row 1 (Front Facing)</div>
            <div class="grid grid-cols-3 gap-2">
              ${[1, 2, 3].map(n => {
                const isFree = n <= v.availableSeats;
                return `
                  <button onclick="${isFree ? `pickSeat('Seat ${n} (Row 1)', ${v.fare})` : ''}" class="p-3 rounded-xl border ${isFree ? 'bg-emerald-500/20 border-emerald-500 text-emerald-300 hover:scale-105' : 'bg-rose-500/20 border-rose-500/40 text-rose-400 cursor-not-allowed'} text-center font-bold flex flex-col items-center gap-1 transition-all">
                    <span>💺</span>
                    <span class="text-xs">S${n}</span>
                  </button>
                `;
              }).join('')}
            </div>
            <div class="text-[10px] font-bold text-zinc-400 pt-2">Row 2 (Rear Bench)</div>
            <div class="grid grid-cols-3 gap-2">
              ${[4, 5, 6].map(n => {
                const isFree = n <= v.availableSeats;
                return `
                  <button onclick="${isFree ? `pickSeat('Seat ${n} (Row 2)', ${v.fare})` : ''}" class="p-3 rounded-xl border ${isFree ? 'bg-emerald-500/20 border-emerald-500 text-emerald-300 hover:scale-105' : 'bg-rose-500/20 border-rose-500/40 text-rose-400 cursor-not-allowed'} text-center font-bold flex flex-col items-center gap-1 transition-all">
                    <span>💺</span>
                    <span class="text-xs">S${n}</span>
                  </button>
                `;
              }).join('')}
            </div>
          </div>
        `;
      } else {
        // 50-Seater Bus Layout: 8 rows of 2x2 with aisle
        let rowsHtml = '';
        const totalRows = 8;
        const freeCount = v.availableSeats;
        let freeAssigned = 0;

        for (let r = 1; r <= totalRows; r++) {
          const seatsInRow = ['A', 'B', 'C', 'D'];
          const buttons = seatsInRow.map((col, idx) => {
            const isFree = (r * 4 + idx) % 5 === 0 && freeAssigned < freeCount;
            if (isFree) freeAssigned++;
            const seatName = `${r}${col}`;
            const isWindow = col === 'A' || col === 'D';
            return `
              <button onclick="${isFree ? `pickSeat('Seat ${seatName} (${isWindow ? 'Window' : 'Aisle'})', ${v.fare})` : ''}" class="p-2 sm:p-2.5 rounded-xl border ${isFree ? 'bg-emerald-500/20 border-emerald-500 text-emerald-300 hover:scale-105 hover:bg-emerald-500/30' : 'bg-rose-500/15 border-rose-500/30 text-rose-400/70 cursor-not-allowed'} text-center font-bold flex flex-col items-center gap-0.5 transition-all text-xs">
                <span>💺</span>
                <span class="font-mono font-bold">${seatName}</span>
                <span class="text-[8px] text-zinc-400">${isWindow ? 'Win' : 'Ais'}</span>
              </button>
            `;
          });

          rowsHtml += `
            <div class="flex items-center justify-between gap-2">
              <div class="grid grid-cols-2 gap-2 flex-1">
                ${buttons[0]}
                ${buttons[1]}
              </div>
              <div class="w-8 text-center text-[10px] text-zinc-500 font-mono tracking-widest font-black">AISLE</div>
              <div class="grid grid-cols-2 gap-2 flex-1">
                ${buttons[2]}
                ${buttons[3]}
              </div>
            </div>
          `;
        }
        container.innerHTML = rowsHtml;
      }
    }

    function pickSeat(seatName, fare) {
      selectedSeatNumber = seatName;
      playBeep(520, 'sine', 0.08);

      document.getElementById('selectedSeatLabel').innerHTML = `✅ Selected: <strong class="text-brand-cyan">${seatName}</strong>`;
      document.getElementById('selectedSeatSubtitle').textContent = 'Seat reserved for you on this campus vehicle';
      document.getElementById('selectedSeatPrice').textContent = `₹${fare}`;
      showToast(`Selected ${seatName}! Click "Confirm Seat & Ride" below.`);
    }

    function confirmSeatBooking() {
      const v = FLEET.find(x => x.id === currentSeatModalVehicleId) || FLEET[0];
      const seat = selectedSeatNumber || `Seat 2A (${v.category === 'auto' ? 'Window' : 'Front'})`;

      closeModal('seatLayoutModal');
      activeOtpCode = Math.floor(1000 + Math.random() * 9000);

      // Deduct from wallet if balance is available
      if (walletBalance >= v.fare) {
        walletBalance -= v.fare;
        walletHistory.unshift({
          type: 'ride',
          title: `${v.name} (${seat})`,
          date: 'Just now',
          amount: -v.fare,
          method: 'Campus Smart Pass'
        });
        updateWalletDisplay();
      }

      showToast(`🎉 ${seat} reserved on ${v.name}! OTP: ${activeOtpCode}`);

      // Open driver chat directly with the reservation
      openDriverChat(v.id);
      driverChatHistory.push({
        sender: 'user',
        text: `Bhaiya, maine ${v.name} me ${seat} book kiya hai. Mera verification OTP ${activeOtpCode} hai.`
      });
      renderChatMessages();

      setTimeout(() => {
        driverChatHistory.push({
          sender: 'driver',
          text: `Haanji student ji! ${seat} maine reserve kar di hai. OTP ${activeOtpCode} confirm ho gaya. Main 2 minute me aapke stop par aa raha hoon!`
        });
        renderChatMessages();
        playBeep(600, 'sine', 0.1);
      }, 800);
    }

    // Driver Chat Modal
    function openDriverChat(vehicleId) {
      if (vehicleId) {
        selectedVehicleId = vehicleId;
      }
      const v = FLEET.find(x => x.id === selectedVehicleId) || FLEET[0];
      
      const dName = document.getElementById('chatDriverName');
      if (dName) dName.textContent = v.driver;
      const dPlate = document.getElementById('chatPlate');
      if (dPlate) dPlate.textContent = v.plate;
      const dType = document.getElementById('chatVehicleType');
      if (dType) dType.textContent = `${v.typeName} • 💺 ${v.availableSeats} Seats Free • Rating: ${v.rating} ★`;
      const otpDisplay = document.getElementById('chatOtpDisplay');
      if (otpDisplay) otpDisplay.textContent = activeOtpCode;

      // Set fresh driver greeting if history is empty
      if (!driverChatHistory || driverChatHistory.length <= 1) {
        driverChatHistory = [
          { sender: 'driver', text: `Namaste! Main <strong>${v.driver}</strong> (${v.name}). Meri gaadi me <strong>${v.availableSeats} seats</strong> abhi khali hain. Aap kahan wait kar rahe hain?` }
        ];
      }

      renderChatMessages();
      openModal('driverChatModal');
    }

    function renderChatMessages() {
      const container = document.getElementById('driverChatMessages');
      if (!container) return;
      container.innerHTML = driverChatHistory.map(m => `
        <div class="flex flex-col ${m.sender === 'user' ? 'items-end' : 'items-start'}">
          <div class="max-w-[80%] p-3 rounded-2xl ${m.sender === 'user' ? 'bg-brand-cyan text-black font-semibold rounded-br-none' : 'bg-white/10 text-white rounded-bl-none border border-white/10'}">
            ${m.text}
          </div>
          <span class="text-[9px] text-zinc-500 mt-0.5 px-1">${m.sender === 'user' ? 'You' : 'Driver'}</span>
        </div>
      `).join('');
      container.scrollTop = container.scrollHeight;
    }

    function sendChatMessage() {
      const input = document.getElementById('driverChatInput');
      const text = input.value.trim();
      if (!text) return;
      input.value = '';
      executeMessageExchange(text);
    }

    function sendQuickChatMessage(text) {
      executeMessageExchange(text);
    }

    function executeMessageExchange(userText) {
      driverChatHistory.push({ sender: 'user', text: userText });
      renderChatMessages();
      playBeep(440, 'sine', 0.05);

      setTimeout(() => {
        let reply = 'Ji bhaiya, main bas pahunch hi raha hoon!';
        const lower = userText.toLowerCase();
        if (lower.includes('where') || lower.includes('kahan')) {
          reply = 'Main Central Library chowk cross kar chuka hoon, agle 2 minute me aapke stop par hunga.';
        } else if (lower.includes('otp')) {
          reply = `Haanji, OTP ${activeOtpCode} match ho gaya hai! Trip officially verified. Kripya baithiye.`;
          playBeep(700, 'sine', 0.1);
        } else if (lower.includes('wait') || lower.includes('ruko')) {
          reply = 'Theek hai ji, 2 minute main hazard lights on karke wait kar raha hoon. Jaldi aao.';
        } else if (lower.includes('reached') || lower.includes('stop')) {
          reply = 'Superb! Main vehicle gate ke samne khadi kar raha hoon. Blue campus sticker check karein.';
        }
        driverChatHistory.push({ sender: 'driver', text: reply });
        renderChatMessages();
        playBeep(520, 'sine', 0.08);
      }, 700);
    }

    // ================= WAYZEN CHATBOT LOGIC =================
    function toggleWayzenChat() {
      const modal = document.getElementById('wayzenChatModal');
      const isHidden = modal.classList.contains('hidden');
      if (isHidden) {
        modal.classList.remove('hidden');
        renderWayzenMessages();
        closeWayzenBubble();
        playBeep(650, 'sine', 0.1);
      } else {
        modal.classList.add('hidden');
      }
    }

    function closeWayzenBubble() {
      const bubble = document.getElementById('wayzenSpeechBubble');
      if (bubble) bubble.classList.add('hidden');
    }

    function toggleHinglishMode() {
      wayzenHinglish = !wayzenHinglish;
      const btn = document.getElementById('wayzenHinglishToggle');
      if (wayzenHinglish) {
        btn.textContent = '🇮🇳 Hinglish';
        btn.className = 'px-2 py-1 rounded-lg bg-brand-cyan/20 text-brand-cyan text-[10px] font-bold border border-brand-cyan/40';
        showToast('WAYZEN is now in Hinglish mode!');
      } else {
        btn.textContent = '🇬🇧 English';
        btn.className = 'px-2 py-1 rounded-lg bg-white/10 text-zinc-300 text-[10px] font-bold border border-white/20';
        showToast('WAYZEN is now in English mode!');
      }
    }

    function toggleWayzenSound() {
      wayzenSound = !wayzenSound;
      const btn = document.getElementById('wayzenSoundBtn');
      btn.textContent = wayzenSound ? '🔊' : '🔇';
      showToast(wayzenSound ? 'Sound effects enabled' : 'Sound muted');
    }

    function renderWayzenMessages() {
      const container = document.getElementById('wayzenChatMessages');
      if (!container) return;
      container.innerHTML = wayzenChatLog.map(m => `
        <div class="flex flex-col ${m.sender === 'user' ? 'items-end' : 'items-start'}">
          <div class="max-w-[85%] p-3.5 rounded-2xl ${
            m.sender === 'user' 
              ? 'bg-gradient-to-r from-brand-cyan to-brand-purple text-black font-semibold rounded-br-none shadow-md' 
              : 'glass-panel text-white rounded-bl-none border border-brand-cyan/25 shadow-md'
          }">
            <p class="leading-relaxed">${m.text}</p>
            ${m.actionBtn ? `
              <div class="pt-2">
                <button onclick="${m.actionBtn.onclick}" class="px-3 py-1.5 rounded-xl bg-brand-cyan/20 border border-brand-cyan/40 text-brand-cyan hover:bg-brand-cyan hover:text-black font-extrabold text-[11px] transition-all">
                  ${m.actionBtn.label}
                </button>
              </div>
            ` : ''}
          </div>
          <span class="text-[9px] text-zinc-500 mt-1 px-1 flex items-center gap-1">
            ${m.sender === 'user' ? 'You' : '🤖 WAYZEN AI'}
          </span>
        </div>
      `).join('');
      container.scrollTop = container.scrollHeight;
    }

    function sendWayzenPrompt(text) {
      document.getElementById('wayzenInput').value = text;
      sendWayzenMessage();
    }

    function sendWayzenMessage() {
      const input = document.getElementById('wayzenInput');
      const text = input.value.trim();
      if (!text) return;
      input.value = '';

      wayzenChatLog.push({ sender: 'user', text });
      renderWayzenMessages();
      playBeep(480, 'sine', 0.05);

      setTimeout(() => {
        const replyObj = generateWayzenAIResponse(text);
        wayzenChatLog.push(replyObj);
        renderWayzenMessages();
        playBeep(720, 'sine', 0.1);
      }, 500);
    }

    function generateWayzenAIResponse(query) {
      const q = query.toLowerCase();

      // Bus / ETA query
      if (q.includes('bus') || q.includes('eta') || q.includes('shuttle') || q.includes('kab aayegi') || q.includes('aayega')) {
        const s1 = FLEET[0];
        const a2 = FLEET[1];
        if (wayzenHinglish) {
          return {
            sender: 'wayzen',
            text: `🚌 <strong>Shuttle #1</strong> bas <strong>3-4 minute</strong> me Library Chowk pahunch rahi hai!<br>🛺 <strong>Auto #2</strong> (PB 08 CA 1201) bhi sirf <strong>2 min</strong> dur hai. Map pe live track karo!`,
            actionBtn: { label: '📍 Open Live Map Tracker →', onclick: 'launchTransportDashboard()' }
          };
        } else {
          return {
            sender: 'wayzen',
            text: `🚌 <strong>Shuttle #1</strong> is currently <strong>3-4 minutes</strong> away from the Central Library Stop.<br>🛺 <strong>Auto #2</strong> is 2 mins away. Tracking with Kalman-filtered dead-reckoning.`,
            actionBtn: { label: '📍 View on Live Map →', onclick: 'launchTransportDashboard()' }
          };
        }
      }

      // Auto Rickshaw query
      if (q.includes('auto') || q.includes('rickshaw') || q.includes('bulao') || q.includes('rickshaw')) {
        if (wayzenHinglish) {
          return {
            sender: 'wayzen',
            text: `🛺 <strong>Auto Rickshaw #2</strong> (Driver: Vikram Singh) free hai! Boys Hostel Quad se Metro Link ke liye direct sprint le sakta hai. Book karun?`,
            actionBtn: { label: '🛺 Book Auto Ride Now (₹30) →', onclick: 'openPaymentAndBookingModal()' }
          };
        } else {
          return {
            sender: 'wayzen',
            text: `🛺 <strong>Auto-Rickshaw #2</strong> (Driver: Vikram Singh, PB 08 CA 1201) is available for campus point-to-point transit.`,
            actionBtn: { label: 'Book Auto Pass (₹30) →', onclick: 'openPaymentAndBookingModal()' }
          };
        }
      }

      // Wallet query
      if (q.includes('wallet') || q.includes('balance') || q.includes('paise') || q.includes('recharge') || q.includes('top up') || q.includes('topup')) {
        if (wayzenHinglish) {
          return {
            sender: 'wayzen',
            text: `💳 Tumhara live wallet balance hai: <strong>₹${walletBalance.toFixed(2)}</strong>.<br>Zero convenience fee ke saath UPI ya Debit card se 5 second me recharge ho jata hai!`,
            actionBtn: { label: '💳 Open Wallet & Top-Up →', onclick: 'openWalletModal()' }
          };
        } else {
          return {
            sender: 'wayzen',
            text: `💳 Your current Campus Flow Wallet balance is <strong>₹${walletBalance.toFixed(2)}</strong>. You can top up using UPI, cards, or net banking.`,
            actionBtn: { label: '💳 Recharge Wallet →', onclick: 'openWalletModal()' }
          };
        }
      }

      // OTP query
      if (q.includes('otp') || q.includes('driver otp') || q.includes('security') || q.includes('code')) {
        if (wayzenHinglish) {
          return {
            sender: 'wayzen',
            text: `🔐 Tumhara active ride OTP hai: <strong class="text-brand-cyan text-sm tracking-widest font-mono">${activeOtpCode}</strong>.<br>Board karte waqt driver bhaiya ko yehi 4 digit batana, tabhi trip start hogi!`,
            actionBtn: { label: '💬 Chat with Driver →', onclick: 'openDriverChat()' }
          };
        } else {
          return {
            sender: 'wayzen',
            text: `🔐 Your active trip OTP is <strong class="text-brand-cyan font-mono">${activeOtpCode}</strong>. Provide this to your assigned driver to verify boarding.`,
            actionBtn: { label: '💬 Chat Driver →', onclick: 'openDriverChat()' }
          };
        }
      }

      // Coupon / Discount query
      if (q.includes('coupon') || q.includes('discount') || q.includes('free') || q.includes('offer') || q.includes('campus10')) {
        if (wayzenHinglish) {
          return {
            sender: 'wayzen',
            text: `🎟️ Mast offer chal raha hai!<br>• <strong>CAMPUS10</strong>: 10% discount har ride aur pass par!<br>• <strong>FREEFIRST</strong>: Tumhari pehli ride 100% FREE!`,
            actionBtn: { label: '🎟️ Apply CAMPUS10 Now →', onclick: "quickApplyCoupon('CAMPUS10'); openPaymentAndBookingModal();" }
          };
        } else {
          return {
            sender: 'wayzen',
            text: `🎟️ Active Campus Offers:<br>• <strong>CAMPUS10</strong>: 10% instant discount on any ride.<br>• <strong>FREEFIRST</strong>: 100% free first ride of the semester!`,
            actionBtn: { label: 'Apply CAMPUS10 (10% Off) →', onclick: "quickApplyCoupon('CAMPUS10'); openPaymentAndBookingModal();" }
          };
        }
      }

      // Jokes / Humor query
      if (q.includes('joke') || q.includes('fun') || q.includes('hasao') || q.includes('boring')) {
        const jokes = [
          "Teacher: 8:30 AM class me late kyu aaye?<br>Student: Sir, sapne me exam de raha tha, invigilator ne sheet chheen li to dhundhte dhundhte time lag gaya! 😂",
          "Engineering ka 1st Rule: Agar pehli baar me code chal jaye, to samjho kuch to bahut bada gadbad hai! 💻💀",
          "Auto wale bhaiya: Meter se chaloge ya fixed?<br>Student: Sirf Campus Flow UPI QR se! Auto bhaiya: Ye hui na baat! 🛺🔥",
          "Ek student ne attendance sheet pe apna naam do baar likh diya. Professor: Kyu?<br>Student: Sir, meri aatma to pehle se class me thi, sharir abhi bus se aaya hai! 🚌👻"
        ];
        const randomJoke = jokes[Math.floor(Math.random() * jokes.length)];
        return {
          sender: 'wayzen',
          text: `😂 <strong>Campus Joke by WAYZEN:</strong><br><br>${randomJoke}`,
          actionBtn: null
        };
      }

      // Directions query
      if (q.includes('route') || q.includes('library') || q.includes('hostel') || q.includes('kahan hai') || q.includes('kaise jau')) {
        if (wayzenHinglish) {
          return {
            sender: 'wayzen',
            text: `📍 <strong>Central Library</strong> Stop #3 par hai (Outer Loop). Main Gate se Bus #1 ya Eco EV #3 lo, exact 4 minute me drop kar degi!`,
            actionBtn: { label: '📍 View Campus Route Map →', onclick: 'launchTransportDashboard()' }
          };
        } else {
          return {
            sender: 'wayzen',
            text: `📍 <strong>Central Library</strong> is Stop #3 on the Outer Green Loop. Board Shuttle #1 or EV Cart #3 from the Main Gate for a 4-minute commute.`,
            actionBtn: { label: '📍 View Route Map →', onclick: 'launchTransportDashboard()' }
          };
        }
      }

      // EV Cart query
      if (q.includes('ev') || q.includes('cart') || q.includes('green') || q.includes('electric')) {
        return {
          sender: 'wayzen',
          text: `⚡ <strong>Eco EV #3 (Green Cart)</strong> is 100% zero-emission and connecting Central Quad to University Hospital and Olympic Sports Complex. Driver: Suresh Yadav.`,
          actionBtn: { label: 'Book EV Cart (₹15) →', onclick: 'openPaymentAndBookingModal()' }
        };
      }

      // Default fallback
      if (wayzenHinglish) {
        return {
          sender: 'wayzen',
          text: `Bhai, main samajh gaya! Transit ke baare me kuch bhi puchho: <em>"Bus kab aayegi"</em>, <em>"Auto bula do"</em>, <em>"Wallet balance"</em>, <em>"Driver OTP"</em>, ya <em>"Ek joke sunao"</em>. WAYZEN har waqt haazir hai! 🤖✨`,
          actionBtn: { label: '🚏 Check Shuttle Live ETA →', onclick: 'launchTransportDashboard()' }
        };
      } else {
        return {
          sender: 'wayzen',
          text: `I'm WAYZEN, your campus transit assistant. You can ask me for live vehicle ETAs, auto rickshaws, wallet top-up, driver OTP, or campus discount coupons! 🤖`,
          actionBtn: { label: '🚏 Check Live ETAs →', onclick: 'launchTransportDashboard()' }
        };
      }
    }

    // Modal Helpers
    function openModal(id) {
      const modal = document.getElementById(id);
      if (modal) {
        modal.classList.remove('hidden');
        modal.classList.add('grid');
      }
    }

    function closeModal(id) {
      const modal = document.getElementById(id);
      if (modal) {
        modal.classList.add('hidden');
        modal.classList.remove('grid');
      }
    }

    function openFarePassesModal() {
      openModal('farePassesModal');
    }

    function openH4StressModal() {
      openModal('h4StressModal');
    }

    function triggerBlackoutOnSelected() {
      closeModal('h4StressModal');
      showToast('⚠️ 120s GPS Blackout injected! Dead-Reckoning engine active.');
    }

    function triggerJamOnSelected() {
      closeModal('h4StressModal');
      showToast('🚦 Traffic Jam injected! ETA delay recalculated (+15 min).');
    }

    // Fleet List Rendering in Sidebar
    function renderFleetList() {
      const container = document.getElementById('fleetItemsContainer');
      if (!container) return;
      const search = (document.getElementById('transitSearchInput').value || '').toLowerCase();
      const filtered = FLEET.filter(v => {
        const matchesCat = currentFilterType === 'all' || v.category === currentFilterType;
        const matchesSearch = v.name.toLowerCase().includes(search) || v.driver.toLowerCase().includes(search) || v.plate.toLowerCase().includes(search);
        return matchesCat && matchesSearch;
      });

      container.innerHTML = filtered.map(v => {
        const isSelected = v.id === selectedVehicleId;
        const etaMin = Math.max(1, Math.round(v.s / 800));
        const occupancyPct = Math.round((v.occupiedSeats / v.totalSeats) * 100);
        const seatBadgeClass = v.availableSeats > 2 ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/30' : (v.availableSeats > 0 ? 'bg-amber-500/20 text-amber-400 border-amber-500/30' : 'bg-rose-500/20 text-rose-400 border-rose-500/30');

        return `
          <div onclick="selectVehicle('${v.id}')" class="p-3.5 rounded-2xl glass-card cursor-pointer border ${isSelected ? 'border-brand-cyan bg-brand-cyan/15 ring-1 ring-brand-cyan/40' : 'border-white/10'} hover:border-white/30 space-y-2.5 transition-all">
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-2.5">
                <span class="text-2xl">${v.icon}</span>
                <div>
                  <h4 class="text-xs font-black text-white">${v.name}</h4>
                  <p class="text-[10px] text-brand-cyan font-bold uppercase tracking-wider">${v.typeName}</p>
                  <p class="text-[10px] text-zinc-400 font-mono">${v.plate} • 👨‍✈️ ${v.driver} (★ ${v.rating})</p>
                </div>
              </div>
              <div class="text-right">
                <span class="text-xs font-black text-brand-cyan">${etaMin} min ETA</span>
                <p class="text-[9px] text-zinc-400">${v.speed} km/h • ${v.battery}% 🔋</p>
              </div>
            </div>

            <!-- Seat Occupancy Meter -->
            <div class="space-y-1 bg-black/30 p-2 rounded-xl border border-white/5">
              <div class="flex items-center justify-between text-[10px]">
                <span class="text-zinc-400">Available Seats:</span>
                <span class="font-mono font-bold px-2 py-0.5 rounded-full border ${seatBadgeClass}">
                  💺 ${v.availableSeats} of ${v.totalSeats} free
                </span>
              </div>
              <div class="w-full h-1.5 rounded-full bg-white/10 overflow-hidden">
                <div class="h-full rounded-full ${occupancyPct > 85 ? 'bg-amber-400' : 'bg-brand-cyan'}" style="width: ${occupancyPct}%"></div>
              </div>
            </div>

            <!-- Action buttons -->
            <div class="flex items-center justify-between pt-1 border-t border-white/5 text-[11px]">
              <span class="text-zinc-400 font-bold">Fare: <strong class="text-white font-mono">₹${v.fare}</strong></span>
              <div class="flex items-center gap-1.5">
                <button onclick="event.stopPropagation(); openDriverChat('${v.id}')" class="px-2.5 py-1 rounded-xl bg-gradient-to-r from-brand-cyan to-brand-purple text-black font-black hover:opacity-90 flex items-center gap-1 shadow-sm">
                  💬 Chat
                </button>
                <button onclick="event.stopPropagation(); openSeatLayoutModal('${v.id}')" class="px-2.5 py-1 rounded-xl bg-white/10 hover:bg-white/20 text-white font-bold border border-white/10 flex items-center gap-1">
                  💺 Seats
                </button>
                <button onclick="event.stopPropagation(); bookSpecificVehicle('${v.id}')" class="px-2.5 py-1 rounded-xl bg-brand-cyan/20 text-brand-cyan hover:bg-brand-cyan hover:text-black font-bold">
                  Book
                </button>
              </div>
            </div>
          </div>
        `;
      }).join('');
    }

    function filterByStop(stopId) {
      const s = LPU_STOPS.find(x => x.id === stopId);
      if (!s) return;
      document.getElementById('transitSearchInput').value = s.code;
      renderFleetList();
      showToast(`Filtered routes for ${s.name} (${s.code})`);
    }

    function selectVehicle(id) {
      selectedVehicleId = id;
      renderFleetList();
      const v = FLEET.find(x => x.id === id);
      if (v && map) {
        const pos = getCoordOnRoute(v.routeId, v.s);
        map.panTo([pos.lat, pos.lng], { animate: true, duration: 0.5 });
      }
    }

    function filterFleetCategory(cat, btn) {
      currentFilterType = cat;
      document.querySelectorAll('.fleet-cat-btn').forEach(b => {
        b.className = 'fleet-cat-btn py-1.5 rounded-xl hover:text-white';
      });
      if (btn) btn.className = 'fleet-cat-btn py-1.5 rounded-xl bg-white/15 text-brand-cyan shadow-sm';
      renderFleetList();
    }

    function setSimWarp(warp, btn) {
      simSpeedWarp = warp;
      document.querySelectorAll('.warp-btn').forEach(b => {
        b.className = 'warp-btn px-2.5 py-1 rounded-xl hover:text-white';
      });
      if (btn) btn.className = 'warp-btn px-2.5 py-1 rounded-xl bg-white/15 text-brand-cyan font-bold';
      showToast(`Simulation speed set to ${warp}x`);
    }

    // Sign Up, Login & Account Management
    function switchHeroAuthMode(mode) {
      const suSec = document.getElementById('heroSignUpSection');
      const liSec = document.getElementById('heroLoginSection');
      const suBtn = document.getElementById('tabBtnSignUp');
      const liBtn = document.getElementById('tabBtnLogin');
      
      if (!suSec || !liSec) return;

      if (mode === 'login') {
        suSec.classList.add('hidden');
        liSec.classList.remove('hidden');
        if (suBtn) suBtn.className = 'py-2 rounded-xl transition-all text-zinc-400 hover:text-white flex items-center justify-center gap-1.5';
        if (liBtn) liBtn.className = 'py-2 rounded-xl transition-all bg-gradient-to-r from-brand-cyan to-brand-purple text-black shadow-md flex items-center justify-center gap-1.5 font-black';
      } else {
        liSec.classList.add('hidden');
        suSec.classList.remove('hidden');
        if (liBtn) liBtn.className = 'py-2 rounded-xl transition-all text-zinc-400 hover:text-white flex items-center justify-center gap-1.5';
        if (suBtn) suBtn.className = 'py-2 rounded-xl transition-all bg-gradient-to-r from-brand-cyan to-brand-purple text-black shadow-md flex items-center justify-center gap-1.5 font-black';
      }
      if (window.lucide) lucide.createIcons();
    }

    async function handleUserSignUp() {
      const nameInput = document.getElementById('suFullName');
      const emailInput = document.getElementById('suEmail');
      const studentIdInput = document.getElementById('suStudentId');
      const pwInput = document.getElementById('suPassword');
      const cpwInput = document.getElementById('suConfirmPassword');

      const name = (nameInput && nameInput.value.trim()) || 'Campus Student';
      const email = (emailInput && emailInput.value.trim()) || (name.toLowerCase().replace(/[^a-z0-9]/g, '.') + '@uni.edu.in');
      const studentId = (studentIdInput && studentIdInput.value.trim()) || 'STU-' + Math.floor(1000 + Math.random() * 9000);
      const password = (pwInput && pwInput.value) || 'Student@123';
      const confirmPassword = (cpwInput && cpwInput.value) || '';

      if (confirmPassword && password !== confirmPassword) {
        showToast('⚠️ Passwords do not match! Please check.');
        return;
      }

      // Try saving to backend auth server
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 1200);
        const resp = await fetch('http://localhost:8090/api/auth/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name,
            email,
            password,
            student_id: studentId,
            commute_mode: 'bus'
          }),
          signal: controller.signal
        });
        clearTimeout(timeoutId);
        if (resp.ok) {
          const data = await resp.json();
          if (data && data.user) {
            currentUser = {
              name: data.user.name,
              email: data.user.email,
              studentId: data.user.student_id,
              wallet_balance: data.user.wallet_balance || 240.00
            };
          }
        }
      } catch (err) {
        console.log('Backend sync offline fallback, using local storage user');
      }

      if (!currentUser || currentUser.name !== name) {
        currentUser = { name, email, studentId, wallet_balance: 240.00 };
      }

      localStorage.setItem('cf_user', JSON.stringify(currentUser));

      updateUserAccountPill();
      updateWalletDisplay();

      // Dynamic WAYZEN greeting
      if (wayzenChatLog.length > 0 && wayzenChatLog[0].sender === 'wayzen') {
        wayzenChatLog[0].text = `👋 Arre Namaste <strong>${name}</strong>! Main hoon <strong>WAYZEN</strong>, tumhara 24/7 AI Campus Transit Buddy! 🤖✨<br><br>Account create ho gaya aur ₹240 wallet balance active hai! Shuttles ka live ETA, Auto booking, ya Driver OTP—kuch bhi puchho!`;
        renderWayzenMessages();
      }

      showToast(`🎉 Account Created! Welcome to Campus Flow, ${name}!`);
      launchTransportDashboard();
    }

    async function handleUserLogin() {
      const emailInput = document.getElementById('liEmail');
      const pwInput = document.getElementById('liPassword');

      const email = (emailInput && emailInput.value.trim().toLowerCase()) || 'student@uni.edu.in';
      const password = (pwInput && pwInput.value) || '';

      let loggedInName = email.split('@')[0].replace(/[._]/g, ' ');
      loggedInName = loggedInName.charAt(0).toUpperCase() + loggedInName.slice(1);
      let studentId = 'STU-' + Math.floor(1000 + Math.random() * 9000);

      // Attempt backend login
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 1200);
        const resp = await fetch('http://localhost:8090/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, password }),
          signal: controller.signal
        });
        clearTimeout(timeoutId);
        if (resp.ok) {
          const data = await resp.json();
          if (data && data.user) {
            loggedInName = data.user.name;
            studentId = data.user.student_id;
          }
        }
      } catch (err) {
        console.log('Backend sync offline fallback');
      }

      // Check saved user in localStorage
      const saved = localStorage.getItem('cf_user');
      if (saved) {
        try {
          const parsed = JSON.parse(saved);
          if (parsed.email && parsed.email.toLowerCase() === email) {
            loggedInName = parsed.name || loggedInName;
            studentId = parsed.studentId || studentId;
          }
        } catch(e) {}
      }

      currentUser = { name: loggedInName, email, studentId, wallet_balance: walletBalance };
      localStorage.setItem('cf_user', JSON.stringify(currentUser));

      updateUserAccountPill();
      updateWalletDisplay();

      if (wayzenChatLog.length > 0 && wayzenChatLog[0].sender === 'wayzen') {
        wayzenChatLog[0].text = `👋 Welcome back <strong>${loggedInName}</strong>! Main hoon <strong>WAYZEN</strong>! 🤖 Shuttles live track ho rahe hain. Ride book karni hai ya wallet balance check karein?`;
        renderWayzenMessages();
      }

      showToast(`👋 Welcome back, ${loggedInName}!`);
      launchTransportDashboard();
    }

    function handleGoogleSignIn() {
      const entered = (document.getElementById('suFullName') && document.getElementById('suFullName').value.trim()) || '';
      const enteredEmail = (document.getElementById('suEmail') && document.getElementById('suEmail').value.trim()) || '';

      const name = entered || 'Google Student';
      const email = enteredEmail || (name.toLowerCase().replace(/[^a-z0-9]/g, '.') + '@uni.edu.in');
      const studentId = 'STU-G-' + Math.floor(1000 + Math.random() * 9000);

      currentUser = { name, email, studentId, wallet_balance: walletBalance };
      localStorage.setItem('cf_user', JSON.stringify(currentUser));

      updateUserAccountPill();
      updateWalletDisplay();

      if (wayzenChatLog.length > 0 && wayzenChatLog[0].sender === 'wayzen') {
        wayzenChatLog[0].text = `👋 Arre Namaste <strong>${name}</strong>! Main hoon <strong>WAYZEN</strong>, tumhara 24/7 AI Campus Transit Buddy! 🤖✨<br><br>Main English aur Hinglish dono mast samajhta hoon. Shuttles ka live ETA, Auto booking, Wallet top-up, ya Driver OTP—kuch bhi puchho!`;
        renderWayzenMessages();
      }

      showToast(`Signed in as ${name}`);
      launchTransportDashboard();
    }

    function handleGuestDirectAccess() {
      const entered = (document.getElementById('suFullName') && document.getElementById('suFullName').value.trim()) || '';
      const name = entered || 'Guest Student';
      currentUser = { name, email: 'guest@uni.edu.in', studentId: 'GUEST-99', wallet_balance: walletBalance };
      localStorage.setItem('cf_user', JSON.stringify(currentUser));
      updateUserAccountPill();
      updateWalletDisplay();
      showToast(`Exploring in Guest Mode as ${name}!`);
      launchTransportDashboard();
    }

    function togglePasswordVisibility(id) {
      const el = document.getElementById(id);
      if (el) el.type = el.type === 'password' ? 'text' : 'password';
    }

    function setCommuteMode(mode, btn) {
      document.querySelectorAll('.commute-chip').forEach(b => {
        b.className = 'commute-chip py-1.5 px-2 rounded-xl text-[11px] font-bold border border-white/10 bg-white/5 text-zinc-300 hover:border-white/30 text-center';
      });
      if (btn) btn.className = 'commute-chip py-1.5 px-2 rounded-xl text-[11px] font-bold border border-brand-cyan bg-brand-cyan/15 text-brand-cyan text-center';
    }

    function updateUserAccountPill() {
      const saved = localStorage.getItem('cf_user');
      if (saved) {
        try { 
          currentUser = JSON.parse(saved); 
          const entered = document.getElementById('suFullName') ? document.getElementById('suFullName').value.trim() : '';
          if (entered) currentUser.name = entered;
        } catch(e) {}
      }
      const pill = document.getElementById('userAccountPill');
      const navWallet = document.getElementById('navWalletBtn');
      const heroPromoWallet = document.getElementById('heroPromoWalletBtn');
      const sidePass = document.getElementById('sidebarTransitPassCard');

      if (currentUser && currentUser.name) {
        if (pill) pill.textContent = `👤 ${currentUser.name.trim()}`;
        if (navWallet) navWallet.classList.remove('hidden');
        if (heroPromoWallet) heroPromoWallet.classList.remove('hidden');
        if (sidePass) sidePass.classList.remove('hidden');
      } else {
        if (pill) pill.textContent = 'Sign Up / Login';
        if (navWallet) navWallet.classList.add('hidden');
        if (heroPromoWallet) heroPromoWallet.classList.add('hidden');
        if (sidePass) sidePass.classList.add('hidden');
      }
    }

    // Toast Notification
    function showToast(msg) {
      const toast = document.getElementById('toast');
      const msgEl = document.getElementById('toastMsg');
      if (!toast || !msgEl) return;
      msgEl.textContent = msg;
      toast.classList.remove('translate-y-24', 'opacity-0', 'pointer-events-none');
      setTimeout(hideToast, 4000);
    }

    function hideToast() {
      const toast = document.getElementById('toast');
      if (toast) toast.classList.add('translate-y-24', 'opacity-0', 'pointer-events-none');
    }

    // Main Simulation Loop
    function startSimulationEngine() {
      setInterval(() => {
        const dt = 0.05 * simSpeedWarp;
        simTime += dt;

        FLEET.forEach(v => {
          const r = LPU_ROUTES[v.routeId] || LPU_ROUTES.route_purple;
          v.s = (v.s + v.speed * dt * 2.5) % r.totalDist;
          const pos = getCoordOnRoute(v.routeId, v.s);
          if (vehicleMarkers[v.id]) {
            vehicleMarkers[v.id].setLatLng([pos.lat, pos.lng]);
            const needle = document.getElementById(`needle_${v.id}`);
            if (needle) needle.style.transform = `rotate(${pos.heading}deg)`;
          }
        });

        // Update Clock
        const now = new Date();
        const clockEl = document.getElementById('simClockDisplay');
        if (clockEl) clockEl.textContent = now.toLocaleTimeString();

      }, 60);

      setInterval(renderFleetList, 1500);

      // Cycle WAYZEN funny speech bubbles every 9 seconds
      wayzenBubbleInterval = setInterval(() => {
        const bubble = document.getElementById('wayzenSpeechBubble');
        const textEl = document.getElementById('wayzenBubbleText');
        if (!bubble || !textEl) return;
        const randomPunchline = WAYZEN_PUNCHLINES[Math.floor(Math.random() * WAYZEN_PUNCHLINES.length)];
        textEl.textContent = randomPunchline;
        bubble.classList.remove('hidden');
      }, 9000);
    }

    // Click Sparks & Ripples
    document.addEventListener('click', e => {
      const spark = document.createElement('div');
      spark.className = 'click-spark';
      spark.style.left = `${e.clientX - 7}px`;
      spark.style.top = `${e.clientY - 7}px`;
      document.body.appendChild(spark);
      setTimeout(() => spark.remove(), 500);

      const btn = e.target.closest('.btn-gradient');
      if (btn) {
        const rect = btn.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const rip = document.createElement('span');
        rip.className = 'ripple';
        rip.style.width = rip.style.height = `${size}px`;
        rip.style.left = `${e.clientX - rect.left - size / 2}px`;
        rip.style.top = `${e.clientY - rect.top - size / 2}px`;
        btn.appendChild(rip);
        setTimeout(() => rip.remove(), 600);
      }
    });

    // Lifecycle Init
    window.addEventListener('DOMContentLoaded', () => {
      updateUserAccountPill();
      updateWalletDisplay();
      startSimulationEngine();

      document.getElementById('mapLayerThemeSelect').addEventListener('change', e => {
        setMapTheme(e.target.value);
      });
      document.getElementById('transitSearchInput').addEventListener('input', renderFleetList);

      lucide.createIcons();
    });
  </script>
</body>
</html>
'''

# Replace placeholder with base64 data safely
final_html = app_code.replace('__QR_B64__', qr_b64)

with open('index.html', 'w') as f:
    f.write(final_html)

print("Generated full-featured index.html successfully!")

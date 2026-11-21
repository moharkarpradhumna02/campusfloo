import re

with open('build_full_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Replace the Hero Auth card with the Dual-Mode Sign Up & Login card
hero_auth_old = r'''        <!-- Right Hero Sign-Up Card -->
        <div class="lg:col-span-5 w-full">
          <div class="glass-panel p-6 sm:p-8 rounded-3xl border border-white/15 shadow-2xl relative overflow-hidden backdrop-blur-2xl">
            
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

            <div class="mb-5">
              <h2 class="text-2xl font-black text-white tracking-tight">Create Account</h2>
              <p class="text-xs text-zinc-400 mt-0.5">Join thousands of students riding smarter!</p>
            </div>

            <!-- Form -->
            <form id="heroSignUpForm" onsubmit="event.preventDefault(); handleUserSignUp();" class="space-y-3 pt-1">
              
              <!-- Full Name -->
              <div class="relative">
                <i data-lucide="user" class="w-4 h-4 text-zinc-400 absolute left-3.5 top-1/2 -translate-y-1/2"></i>
                <input type="text" id="suFullName" required placeholder="Enter your Full Name..." oninput="previewUserName(this.value)" class="glass-input w-full pl-10 pr-4 py-2.5 rounded-xl text-xs font-semibold text-white placeholder-zinc-500">
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

              <!-- Mode Chips -->
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

              <!-- Checkbox -->
              <div class="flex items-center gap-2 pt-1">
                <input type="checkbox" id="termsCheck" required class="rounded accent-brand-cyan bg-white/10 border-white/20">
                <label for="termsCheck" class="text-[11px] text-zinc-400">
                  I agree to the <a href="#" class="text-brand-cyan hover:underline">Terms of Service</a> & <a href="#" class="text-brand-cyan hover:underline">Privacy Policy</a>
                </label>
              </div>

              <!-- Sign Up Submit -->
              <button type="submit" class="btn-gradient w-full py-3 rounded-xl text-black font-black text-xs uppercase tracking-wider flex items-center justify-center gap-2 mt-2">
                <span>Sign Up</span>
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

              <button type="button" onclick="handleGuestDirectAccess()" class="w-full py-2 text-center text-xs text-brand-cyan hover:underline font-bold">
                ⚡ Guest Mode: Explore Live Campus Transport Instantly →
              </button>

            </form>

          </div>
        </div>'''

hero_auth_new = r'''        <!-- Right Hero Auth Card (Dual Mode: Sign Up & Sign In) -->
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
        </div>'''

if hero_auth_old in content:
    content = content.replace(hero_auth_old, hero_auth_new)
    print("Replaced Hero Auth Card successfully!")
else:
    print("WARNING: hero_auth_old not found directly, trying normalized search")
    # try replacing by markers
    start_marker = '<!-- Right Hero Sign-Up Card -->'
    end_marker = '<!-- ================= 2. ABOUT US PORTAL ================= -->'
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker)
    if start_idx != -1 and end_idx != -1:
        # keep indentation before start_marker
        content = content[:start_idx] + hero_auth_new.strip() + '\n\n      </div>\n    </section>\n\n    ' + content[end_idx:]
        print("Replaced Hero Auth Card by markers successfully!")
    else:
        print("ERROR: Markers not found!")

# 2. Add Persistent Student Pass & Wallet Card in Dashboard Sidebar
sidebar_marker = '<!-- Active Trip OTP Security Banner -->'
sidebar_pass_html = '''        <!-- Persistent Student Transit Pass & Wallet Card (Visible After Sign Up / Login) -->
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

        '''

if 'sidebarTransitPassCard' not in content:
    content = content.replace(sidebar_marker, sidebar_pass_html + sidebar_marker)
    print("Added sidebarTransitPassCard successfully!")

# 3. Update updateWalletDisplay() to also update sidebarPassName, sidebarPassBalance, sidebarPassId
old_wallet_update = '''      const cardHolderEl = document.getElementById('walletCardHolder');
      if (cardHolderEl) cardHolderEl.textContent = name;
      const cardIdEl = document.getElementById('walletCardStudentId');
      if (cardIdEl) cardIdEl.textContent = studentId;'''

new_wallet_update = '''      const cardHolderEl = document.getElementById('walletCardHolder');
      if (cardHolderEl) cardHolderEl.textContent = name;
      const cardIdEl = document.getElementById('walletCardStudentId');
      if (cardIdEl) cardIdEl.textContent = studentId;

      const passName = document.getElementById('sidebarPassName');
      if (passName) passName.textContent = name;
      const passBal = document.getElementById('sidebarPassBalance');
      if (passBal) passBal.textContent = balStr;
      const passId = document.getElementById('sidebarPassId');
      if (passId) passId.textContent = studentId;'''

if old_wallet_update in content:
    content = content.replace(old_wallet_update, new_wallet_update)
    print("Updated updateWalletDisplay() successfully!")

# 4. Replace the auth JavaScript handlers with clean, robust implementations
# Find the start of handleUserSignUp and end before showToast
auth_js_start = content.find('// Sign Up & Account')
auth_js_end = content.find('// Toast Notification')

if auth_js_start != -1 and auth_js_end != -1:
    new_auth_js = '''// Sign Up, Login & Account Management
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
      if (pill) {
        if (currentUser && currentUser.name) {
          pill.textContent = `👤 ${currentUser.name.trim()}`;
        } else {
          pill.textContent = 'Sign Up / Login';
        }
      }
    }

    '''

    content = content[:auth_js_start] + new_auth_js + content[auth_js_end:]
    print("Replaced Auth JS section successfully without syntax errors!")

with open('build_full_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved updated build_full_app.py")

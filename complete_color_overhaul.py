import re

with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Seat layout modal (Auto, EV, Bus)
# Replace emerald seat styling with clean zinc/black
text = text.replace("bg-emerald-500/20 text-emerald-300 border-emerald-500/40 hover:bg-emerald-500/30", "bg-zinc-100 text-black border-zinc-300 hover:bg-zinc-200 font-bold shadow-sm")
text = text.replace("bg-emerald-500/20 text-emerald-400 border-emerald-500/30 hover:bg-emerald-500/30", "bg-zinc-100 text-black border-zinc-300 hover:bg-zinc-200 font-bold shadow-sm")
text = text.replace("bg-emerald-500/15 text-emerald-300 border-emerald-500/40 hover:bg-emerald-500/25", "bg-zinc-100 text-black border-zinc-300 hover:bg-zinc-200 font-bold shadow-sm")

# 2. Driver Portal Tabs & Duty
text = text.replace("border-b-2 border-emerald-400 text-black bg-emerald-500/10", "border-b-2 border-black text-black bg-zinc-100 font-extrabold")
text = text.replace("border-emerald-400 text-black bg-emerald-500/10", "border-black text-black bg-zinc-100 font-extrabold")
text = text.replace("bg-emerald-500/20 text-black border border-emerald-500/40", "bg-black text-white border border-zinc-800 font-extrabold shadow-sm")
text = text.replace("bg-amber-500/20 text-zinc-800 border border-amber-500/40", "bg-zinc-200 text-black border border-zinc-300 font-extrabold")
text = text.replace("bg-gradient-to-r from-emerald-400 to-teal-400 text-black font-extrabold", "bg-black text-white hover:bg-zinc-800 font-extrabold")
text = text.replace("bg-gradient-to-r from-emerald-500/20 to-teal-500/20 text-emerald-200", "bg-zinc-100 text-black")

# 3. Chat and OTP banners
text = text.replace("bg-emerald-400/20 border border-emerald-400/40 text-black", "bg-zinc-100 border border-zinc-300 text-black font-bold")
text = text.replace("bg-emerald-500/20 text-black hover:bg-emerald-500/30", "bg-zinc-100 text-black hover:bg-zinc-200 border border-zinc-300 font-bold")
text = text.replace("bg-emerald-500 text-black hover:bg-emerald-400 font-bold", "bg-black text-white hover:bg-zinc-800 font-bold")
text = text.replace("bg-gradient-to-r from-emerald-950/60 to-black border border-emerald-500/40", "bg-zinc-900 border border-zinc-800 text-white")
text = text.replace("bg-gradient-to-r from-emerald-950/40 via-black to-[#0d152c] border border-emerald-500/30", "bg-zinc-900 border border-zinc-800 text-white")
text = text.replace("bg-gradient-to-r from-emerald-950/70 to-black border-b border-emerald-500/30", "bg-zinc-900 border-b border-zinc-800 text-white")

# 4. Map ping dots & status indicators
text = text.replace("bg-emerald-400 animate-ping", "bg-black animate-ping")
text = text.replace("bg-emerald-400 animate-pulse", "bg-black animate-pulse")
text = text.replace("rounded-full bg-emerald-400", "rounded-full bg-black")
text = text.replace("rounded-full bg-amber-400", "rounded-full bg-zinc-600")

# 5. Badges, borders, and glows
text = text.replace("border-emerald-500/40", "border-zinc-300")
text = text.replace("border-emerald-500/30", "border-zinc-300")
text = text.replace("border-emerald-500/25", "border-zinc-300")
text = text.replace("border-emerald-400/50", "border-zinc-300")
text = text.replace("border-amber-500/40", "border-zinc-300")
text = text.replace("border-amber-500/30", "border-zinc-300")
text = text.replace("border-amber-500/25", "border-zinc-300")
text = text.replace("border-amber-400/40", "border-zinc-300")

text = text.replace("bg-emerald-500/20", "bg-zinc-100")
text = text.replace("bg-emerald-500/15", "bg-zinc-100")
text = text.replace("bg-emerald-500/10", "bg-zinc-100")
text = text.replace("bg-emerald-400/20", "bg-zinc-100")
text = text.replace("bg-emerald-500", "bg-black text-white")
text = text.replace("bg-amber-500/20", "bg-zinc-100")
text = text.replace("bg-amber-500/15", "bg-zinc-100")
text = text.replace("bg-amber-500/10", "bg-zinc-100")
text = text.replace("bg-amber-500/5", "bg-zinc-50")
text = text.replace("bg-amber-400", "bg-zinc-800 text-white")

text = text.replace("shadow-emerald-500/25", "shadow-black/10")
text = text.replace("shadow-emerald-500/20", "shadow-black/10")

# 6. Payment Cash tab
text = text.replace("text-brand-amber", "text-black font-extrabold")
text = text.replace("text-brand-emerald", "text-black font-extrabold")

# 7. Map Route Colors (change bright emerald/amber lines to sleek dark slate & charcoal)
text = text.replace("color: '#10b981'", "color: '#334155'")
text = text.replace("color: '#f59e0b'", "color: '#1e293b'")
text = text.replace("bg-[#10b981]", "bg-[#334155]")
text = text.replace("bg-[#f59e0b]", "bg-[#1e293b]")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("complete_color_overhaul.py applied successfully.")

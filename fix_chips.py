with open("index.html", "r", encoding="utf-8") as f:
    text = f.read()

# Update HTML money chips
old_money_chips = """          <div class="grid grid-cols-5 gap-2 text-center text-xs font-bold">
            <button onclick="selectMoneyAmount(15, this)" class="money-chip p-2.5 rounded-xl border border-brand-cyan bg-brand-cyan/20 text-brand-cyan font-black">₹15<br><span class="text-[9px] font-normal">Single</span></button>
            <button onclick="selectMoneyAmount(30, this)" class="money-chip p-2.5 rounded-xl border border-zinc-200 bg-zinc-50 text-zinc-300 hover:border-white/30">₹30<br><span class="text-[9px] font-normal">Auto 🛺</span></button>
            <button onclick="selectMoneyAmount(40, this)" class="money-chip p-2.5 rounded-xl border border-zinc-200 bg-zinc-50 text-zinc-300 hover:border-white/30">₹40<br><span class="text-[9px] font-normal">Daily</span></button>
            <button onclick="selectMoneyAmount(150, this)" class="money-chip p-2.5 rounded-xl border border-zinc-200 bg-zinc-50 text-zinc-300 hover:border-white/30">₹150<br><span class="text-[9px] font-normal">Weekly</span></button>
            <button onclick="selectMoneyAmount(999, this)" class="money-chip p-2.5 rounded-xl border border-zinc-200 bg-zinc-50 text-zinc-300 hover:border-white/30">₹999<br><span class="text-[9px] font-normal">Semester</span></button>
          </div>"""

new_money_chips = """          <div class="grid grid-cols-5 gap-2 text-center text-xs font-bold">
            <button onclick="selectMoneyAmount(15, this)" class="money-chip p-2.5 rounded-xl border border-black bg-black text-white font-black shadow-sm">₹15<br><span class="text-[9px] font-normal">Single</span></button>
            <button onclick="selectMoneyAmount(30, this)" class="money-chip p-2.5 rounded-xl border border-zinc-200 bg-zinc-100 text-black hover:border-black font-bold">₹30<br><span class="text-[9px] font-normal">Auto 🛺</span></button>
            <button onclick="selectMoneyAmount(40, this)" class="money-chip p-2.5 rounded-xl border border-zinc-200 bg-zinc-100 text-black hover:border-black font-bold">₹40<br><span class="text-[9px] font-normal">Daily</span></button>
            <button onclick="selectMoneyAmount(150, this)" class="money-chip p-2.5 rounded-xl border border-zinc-200 bg-zinc-100 text-black hover:border-black font-bold">₹150<br><span class="text-[9px] font-normal">Weekly</span></button>
            <button onclick="selectMoneyAmount(999, this)" class="money-chip p-2.5 rounded-xl border border-zinc-200 bg-zinc-100 text-black hover:border-black font-bold">₹999<br><span class="text-[9px] font-normal">Semester</span></button>
          </div>"""
text = text.replace(old_money_chips, new_money_chips)

# Update JS selectMoneyAmount
text = text.replace(
    "b.className = 'money-chip p-2.5 rounded-xl border border-zinc-200 bg-zinc-50 text-zinc-300 hover:border-white/30';",
    "b.className = 'money-chip p-2.5 rounded-xl border border-zinc-200 bg-zinc-100 text-black hover:border-black font-bold';"
)
text = text.replace(
    "if (btn) btn.className = 'money-chip p-2.5 rounded-xl border border-brand-cyan bg-brand-cyan/20 text-brand-cyan font-black';",
    "if (btn) btn.className = 'money-chip p-2.5 rounded-xl border border-black bg-black text-white font-black shadow-sm';"
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(text)

print("money-chip successfully updated.")

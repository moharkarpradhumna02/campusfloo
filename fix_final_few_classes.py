with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("hover:border-brand-emerald/40", "hover:border-zinc-400")
text = text.replace("hover:border-brand-amber/40", "hover:border-zinc-400")
text = text.replace("to-brand-emerald/10", "to-zinc-200/50")
text = text.replace("to-brand-emerald", "to-zinc-200")
text = text.replace("hover:bg-emerald-400", "hover:bg-zinc-800")
text = text.replace("h-2.5 w-2.5 bg-emerald-400", "h-2.5 w-2.5 bg-black")
text = text.replace("bg-teal-500/15", "bg-black/5")
text = text.replace("bg-gradient-to-tr from-emerald-500/30 to-teal-500/30 border border-zinc-300", "bg-black text-white border border-zinc-200")
text = text.replace("bg-gradient-to-r from-emerald-400 to-teal-400 text-black", "bg-black text-white hover:bg-zinc-800")
text = text.replace("border border-emerald-500 text-black", "border border-zinc-300 text-black")
text = text.replace("border-emerald-500/40 hover:bg-emerald-500/30", "border-zinc-300 hover:bg-zinc-200")
text = text.replace("border-emerald-500/30", "border-zinc-300")
text = text.replace("border-emerald-500/20", "border-zinc-300")
text = text.replace("bg-gradient-to-r from-amber-400 to-amber-500", "bg-black text-white")
text = text.replace("from-amber-400 to-amber-500", "from-black to-zinc-800")
text = text.replace("hover:bg-amber-500", "hover:bg-zinc-800")

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Final classes cleaned up.")

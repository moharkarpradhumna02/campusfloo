with open('build_full_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = '''      <!-- Clean High-Performance Tech Hero Background (Video Removed) -->
      <div class="absolute inset-0 pointer-events-none z-0">
        <div class="absolute inset-0 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(0,240,255,0.12),rgba(5,7,14,1))]"></div>
        <div class="absolute top-1/4 -left-40 w-96 h-96 bg-brand-cyan/15 rounded-full blur-[140px]"></div>
        <div class="absolute bottom-1/4 -right-40 w-96 h-96 bg-brand-purple/15 rounded-full blur-[140px]"></div>
        <div class="absolute inset-0 bg-[linear-gradient(to_right,rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(to_bottom,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_0%,#000_70%,transparent_100%)]"></div>
      </div>'''

replacement = '''      <!-- Video Background (Seamlessly playing in hero, no navigation button) -->
      <div class="hero-video-container">
        <video id="heroBgVideo" autoplay loop muted playsinline class="bg-video">
          <source src="campus-flow-bg.mp4" type="video/mp4">
        </video>
        <!-- Dark gradient vignette overlay for perfect contrast -->
        <div class="absolute inset-0 bg-gradient-to-r from-[#05070e]/95 via-[#05070e]/75 to-[#05070e]/90 z-[1]"></div>
      </div>'''

if target in content:
    content = content.replace(target, replacement)
    print("Restored hero background video successfully!")
else:
    print("Warning: target not found directly")

with open('build_full_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Saved build_full_app.py!")

with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re
c = re.sub(r'function setSimWarp\([^)]*\)\s*\{[\s\S]*?showToast\([^)]*\);\s*\}', 'function setSimWarp(warp) { simSpeedWarp = warp || 1; }', c, count=1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Cleaned JS.')

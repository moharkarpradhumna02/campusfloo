with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

idx1 = c.find('<!-- ================= 3. DRIVER PORTAL VIEW (FULL SCREEN COCKPIT) ================= -->')
if idx1 == -1:
    idx1 = c.find('id="driverFullScreenDashboard"')
    idx1 = c.rfind('<section', 0, idx1)

idx2 = c.find('<!-- ================= MODAL: FARES & PASSES ================= -->', idx1)
if idx2 == -1:
    idx2 = c.find('<!-- ================= MODAL', idx1)

print("idx1:", idx1, "idx2:", idx2)
print("Start snippet:", c[idx1:idx1+300])
print("End snippet:", c[idx2-200:idx2])

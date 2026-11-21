with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

print("File size:", len(c))
print("Has paymentBookingModal:", "id=\"paymentBookingModal\"" in c)
print("Has driverFullScreenDashboard:", "id=\"driverFullScreenDashboard\"" in c)
print("Has renderDriverPassengers:", "function renderDriverPassengers()" in c)

with open('build_full_app.py') as f:
    text = f.read()

print("FLEET definition at:", text.find('let FLEET = ['))
print("initCampusMap at:", text.find('function initCampusMap() {'))
print("renderFleetList at:", text.find('function renderFleetList() {'))
print("openDriverChat at:", text.find('function openDriverChat() {'))
print("driverChatModal at:", text.find('id="driverChatModal"'))

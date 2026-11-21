import os

with open('qr_base64.txt') as f:
    qr_b64 = f.read().strip()

# We can construct the template cleanly.
# Notice: Since we will write the file directly to index.html, we don't have to double-escape braces if we don't use f-strings for the whole file,
# OR we can simply replace a placeholder __QR_B64__ in the html template!
# This is MUCH safer and cleaner because standard HTML/CSS/JS contains hundreds of single braces `{}` and `${}`!
# By using a placeholder __QR_B64__, we avoid all f-string escaping headaches!

print("Preparing generate_app.py with placeholder approach...")

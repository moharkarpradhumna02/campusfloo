# Script to build full updated Campus Flow app with:
# 1. WAYZEN Chatbot (cute popping speech bubble, English + Hinglish conversational engine, ETA, Wallet, OTP, jokes)
# 2. Campus Flow Wallet (Top-up, Quick chips, UPI/Card/NetBanking, Passbook Payment History)
# 3. About Us Portal Section
# 4. Main Q&A (FAQ Accordion)
# 5. University Happy Students Photo & Testimonials Showcase
# 6. Beautiful Tailwind CSS + shadcn/ui interface for every button

import re

with open('qr_base64.txt') as f:
    qr_b64 = f.read().strip()

print(f"Read QR base64 with length: {len(qr_b64)}")

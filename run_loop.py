import os

# Ganti URL di bawah
url = "https://docs.google.com/forms/d/e/1FAIpQLScJ3b2ZpHY735Qk8fzHlHsIER69u0_1eyqLx5MekJ_qF9Gewg/"

for i in range(200): # Mengisi i kali
    print(f"Mengisi form ke-{i+1}")
    os.system(f'python main.py "{url}"')
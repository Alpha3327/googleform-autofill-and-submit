import argparse
import datetime
import json
import random
import requests
import form

# --- 1. FUNGSI GENERATOR INISIAL ---
def generate_real_indonesian_initials():
    """
    Menghasilkan inisial nama dengan distribusi probabilitas Indonesia.
    Output random antara HURUF BESAR (Kapital) atau huruf kecil.
    """
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    # Estimasi distribusi frekuensi huruf depan nama di Indonesia
    weights = [
        19.5, # A (Agus, Andi...)
        7.5,  # B (Budi...)
        2.5,  # C
        9.0,  # D (Dwi, Dewi...)
        4.5,  # E
        3.5,  # F
        2.0,  # G
        4.5,  # H
        7.5,  # I
        3.5,  # J
        2.5,  # K
        3.0,  # L
        16.0, # M (Muhammad, Made...)
        6.5,  # N (Nur...)
        1.0,  # O
        4.5,  # P (Putri...)
        0.2,  # Q
        12.0, # R (Rizky, Rudi...)
        14.0, # S (Siti, Sri...)
        5.5,  # T
        1.5,  # U
        1.0,  # V
        5.0,  # W (Wahyu...)
        0.1,  # X
        6.5,  # Y
        1.5   # Z
    ]
    
    # Pilih huruf berdasarkan bobot
    chosen_letters = random.choices(letters, weights=weights, k=1)
    
    final_initials = []
    for letter in chosen_letters:
        # LOGIKA RANDOM CAPSLOCK/KECIL
        # 50% peluang jadi huruf kecil
        if random.random() > 0.5:
            letter = letter.lower()
        final_initials.append(letter)
        
    return final_initials

# --- 2. LOGIKA PENGISIAN FORM (WAJIB ADA) ---
def fill_random_value(type_id, entry_id, options, required=False, entry_name=''):
    ''' Fungsi algoritma untuk mengisi jawaban otomatis '''
    
    # Pastikan entry_id diproses sebagai string agar tidak error
    entry_id = str(entry_id)

    # A. LOGIKA PERTANYAAN SKALA (Sangat Setuju - Sangat Tidak Setuju)
    if options and isinstance(options, list) and any("setuju" in opt.lower() for opt in options):
        # Target bobot dasar
        base_w_sts = 5   # Sangat Tidak Setuju
        base_w_ts  = 15  # Tidak Setuju
        base_w_s   = 35  # Setuju
        base_w_ss  = 45  # Sangat Setuju

        # Buat variasi unik per soal menggunakan ID soal sebagai seed
        unique_seed = int(entry_id) if entry_id.isdigit() else len(entry_id)
        bias = random.Random(unique_seed).randint(-5, 5) 

        # Tambahkan variasi acak (jitter) tiap kali submit
        w_sts = max(1, base_w_sts + bias + random.randint(-2, 2))
        w_ts  = max(5, base_w_ts  + bias + random.randint(-3, 3))
        w_s   = max(20, base_w_s  - bias + random.randint(-5, 5))
        w_ss  = max(30, base_w_ss - bias + random.randint(-5, 5))

        final_weights = []
        for opt in options:
            text = opt.lower()
            if "sangat tidak" in text: final_weights.append(w_sts)
            elif "tidak setuju" in text: final_weights.append(w_ts)
            elif "sangat setuju" in text: final_weights.append(w_ss)
            elif "setuju" in text: final_weights.append(w_s)
            else: final_weights.append(10)

        return random.choices(options, weights=final_weights, k=1)[0]

    # B. LOGIKA: NAMA (ID: 1449005772) -> Panggil fungsi inisial
    if entry_id == '1449005772':
        return generate_real_indonesian_initials()

    # C. LOGIKA: SARAN (ID: 102805749)
    if entry_id == '102805749':
        feedbacks = [
            "Tampilan menarik", "Cukup bagus", "tampilan sudah menarik", "Sangat mudah dimengerti",
            "User friendly", "Sudah oke.", "-", ".", "sudah bagus", "menarik banget", "tampilan bagus", "mudah digunakan", "sangat bagus", "biasa aja",
            "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-",
            "Tombol mudah ditemukan", "Tidak ada", "Tidak ada", "Tidak ada", "Tidak ada", "Tidak ada", "Tidak ada", "Tidak ada", "Tidak ada", "Tidak ada", "Tidak ada"
            ]
        # 60% isi saran, 40% kosong
        return random.choice(feedbacks) if random.random() > 0.8 else ""

    # D. LOGIKA: UMUR (ID: 1685270148)
    if entry_id == '1685270148':
        w_umur = []
        for opt in options:
            if "18" in opt: w_umur.append(87)
            elif "25" in opt: w_umur.append(10)
            else: w_umur.append(3)
        return random.choices(options, weights=w_umur, k=1)[0]

    # E. FALLBACK (Untuk tipe soal lain)
    if type_id in [0, 1]: return ''
    if type_id in [2, 3, 5, 7]: return random.choice(options)
    if type_id == 4: return random.sample(options, k=1)
    
    return ''

# --- 3. FUNGSI UTAMA (JANGAN DIHAPUS) ---
def generate_request_body(url: str, only_required = False):
    # Di sini fungsi fill_random_value dipanggil
    data = form.get_form_submit_request(
        url,
        only_required = only_required,
        fill_algorithm = fill_random_value,
        output = "return",
        with_comment = False
    )
    if data:
        data = json.loads(data)
    return data

def submit(url: str, data: any):
    if not data:
        print("Error: No data generated.")
        return
    url_response = form.get_form_response_url(url)
    print(f"Submitting...", end=" ")
    try:
        res = requests.post(url_response, data=data, timeout=10)
        if res.status_code == 200:
            print("SUCCESS!")
        else:
            print(f"FAILED! Status: {res.status_code}")
    except Exception as e:
        print(f"ERROR: {e}")

def main(url, only_required = False):
    payload = generate_request_body(url, only_required = only_required)
    submit(url, payload)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Submit google form with custom data')
    parser.add_argument('url', help='Google Form URL')
    parser.add_argument('-r', '--required', action='store_true', help='Only include required fields')
    args = parser.parse_args()
    main(args.url, args.required)
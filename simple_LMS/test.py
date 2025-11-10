# backend/importer.py

import os
import csv
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings # Diperlukan untuk mengakses setting Django
from pathlib import Path

# ... (Pastikan os.environ.setdefault dan django.setup() ada) ...

# Import model setelah setup Django
from users.models import User
from courses.models import Course 

# === BAGIAN KRITIS YANG HARUS DIUBAH ===

# Di Docker, WORKDIR kita adalah /app/backend.
# Kita ingin BASE_DIR menunjuk ke /app/backend.
# Cara paling aman adalah menggunakan path dari manage.py atau menggunakan BASE_DIR dari setting.

# Pilihan A: Menggunakan Path Absolut Kontainer (Paling eksplisit di Docker)
# Asumsi manage.py dan importer.py berada di /app/backend/
BASE_DIR = Path('/app/backend/') 

# Pilihan B: Menggunakan BASE_DIR dari settings (Lebih Django-centric, tapi perlu verifikasi)
# BASE_DIR = settings.BASE_DIR.parent # Jika BASE_DIR di setting adalah simple_LMS/

# Kita gunakan Pilihan A untuk kepastian di konteks Docker.
BASE_DIR = Path('/app/backend/') 

# Path ke folder csv_data adalah /app/backend/csv_data
CSV_PATH = BASE_DIR / 'csv_data' 
# ========================================

# ... (Sisa kode import_users() dan import_courses() tetap sama) ...
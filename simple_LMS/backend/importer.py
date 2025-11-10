# backend/importer.py

import os
import csv
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from pathlib import Path

# === 1. SETUP LINGKUNGAN DJANGO ===
# Baris ini WAJIB untuk menjalankan kode ORM di luar manage.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simple_LMS.settings')
import django
django.setup()

# Import model setelah setup Django
from users.models import User
from courses.models import Course 
from django.conf import settings
from pathlib import Path

# Tentukan path file relatif terhadap BASE_DIR (folder backend)
BASE_DIR = Path('/app/backend/')
CSV_PATH = BASE_DIR / 'csv_data'


def import_users():
    """Mengimpor data User dari users.csv."""
    user_file = CSV_PATH / 'users.csv'
    print(f"Mengimpor data user dari: {user_file}")
    
    try:
        with open(user_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            created_count = 0
            
            for row in reader:
                try:
                    # ORM: Gunakan create_user() untuk keamanan password
                    User.objects.create_user(
                        username=row['username'], 
                        email=row['email'], 
                        password=row['password'], # Password akan di-hash
                        fullname=row['fullname']
                    )
                    created_count += 1
                except Exception as e:
                    print(f"Gagal membuat user {row['username']}: {e}")
            
            print(f"✅ Selesai: {created_count} user berhasil diimpor.")

    except FileNotFoundError:
        print(f"❌ ERROR: File CSV user tidak ditemukan di {user_file}")
    except Exception as e:
        print(f"❌ ERROR: Terjadi kesalahan saat membaca file user: {e}")


def import_courses():
    """Mengimpor data Course dari courses.csv."""
    course_file = CSV_PATH / 'courses.csv'
    print(f"\nMengimpor data kursus dari: {course_file}")
    
    try:
        with open(course_file, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            created_count = 0
            
            for row in reader:
                try:
                    # ORM: Cari objek teacher berdasarkan username
                    teacher_obj = User.objects.get(username=row['teacher_username'])
                    
                    # ORM: Membuat objek Course
                    Course.objects.create(
                        name=row['name'],
                        description=row['description'],
                        # Konversi harga ke integer
                        price=int(row['price']), 
                        teacher=teacher_obj # Gunakan objek teacher yang ditemukan
                    )
                    created_count += 1
                except ObjectDoesNotExist:
                    print(f"⚠️ Peringatan: Guru '{row['teacher_username']}' tidak ditemukan. Kursus '{row['name']}' dilewati.")
                except Exception as e:
                    print(f"Gagal membuat kursus {row['name']}: {e}")
            
            print(f"✅ Selesai: {created_count} kursus berhasil diimpor.")

    except FileNotFoundError:
        print(f"❌ ERROR: File CSV kursus tidak ditemukan di {course_file}")
    except Exception as e:
        print(f"❌ ERROR: Terjadi kesalahan saat membaca file kursus: {e}")


if __name__ == '__main__':
    # Hapus data lama (opsional, untuk pengujian berulang)
    # print("Menghapus semua Course dan User yang ada...")
    # Course.objects.all().delete()
    # User.objects.all().delete()
    
    # Jalankan proses impor
    import_users()
    import_courses()
    
    print("\nProses import data dummy selesai.")
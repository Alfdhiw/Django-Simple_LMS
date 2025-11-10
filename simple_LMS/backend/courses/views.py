# courses/views.py

from django.shortcuts import render
from django.http import JsonResponse
from courses.models import Course 
from django.db.models import Min, Max, Avg, Count # <-- UNTUK FUNGSI AGREGASI
from django.core import serializers # <-- UNTUK SERIALIZER
# Pastikan Anda mengimpor model Course
from .models import Course 

def course_list(request):
    """
    Mengambil semua data kursus dan menampilkannya.
    """
    # === DJANGO ORM QUERY ===
    # Ambil semua objek Course (SELECT * FROM course)
    all_courses = Course.objects.all()
    
    context = {
        'title': 'Daftar Semua Kursus',
        'courses': all_courses
    }
    
    # Merender template HTML baru
    return render(request, 'courses/course_list.html', context)

def course_stat(request):
    """
    Menghasilkan statistik harga, kursus termurah, termahal,
    dan terpopuler dalam format JSON.
    """
    
    # 1. Ambil semua kursus
    courses = Course.objects.all()
    
    # 2. Hitung statistik agregat (Min, Max, Avg)
    stats = courses.aggregate(
        max_price=Max('price'),
        min_price=Min('price'),
        avg_price=Avg('price')
    )
    
    # Dapatkan nilai min_price (untuk filter kursus termurah)
    min_price_val = stats.get('min_price')
    
    # 3. Cari kursus termurah (cheapest)
    # ORM: Filter kursus yang harganya sama dengan min_price yang dihitung
    cheapest = Course.objects.filter(price=min_price_val)
    
    # 4. Cari kursus termahal (expensive)
    # ORM: Filter kursus yang harganya sama dengan max_price
    max_price_val = stats.get('max_price')
    expensive = Course.objects.filter(price=max_price_val)

    # 5. Cari kursus terpopuler (popular)
    # Menggunakan Count melalui relasi 'course_member' (sesuai ERD)
    popular = Course.objects.annotate(
        member_count=Count('memberships')
    ).order_by('-member_count')[:5] # Ambil 5 teratas
    
    # 6. Serialisasi Objek Django ke format JSON/Python
    
    # Gunakan serializers.serialize('python', ...) untuk mendapatkan format data yang serupa
    # dengan struktur pada gambar.
    
    cheapest_serialized = serializers.serialize('python', cheapest)
    expensive_serialized = serializers.serialize('python', expensive)
    popular_serialized = serializers.serialize('python', popular)
    
    # 7. Format Hasil Akhir
    result = {
        'course_count': len(courses),
        # Masukkan statistik agregat langsung ke root JSON
        'max_price': stats.get('max_price'),
        'min_price': stats.get('min_price'),
        'avg_price': round(stats.get('avg_price', 0), 2), # Bulatkan rata-rata
        
        'cheapest': cheapest_serialized,
        'expensive': expensive_serialized,
        'popular': popular_serialized,
        
        # 'unpopular' (kursus yang paling sedikit anggotanya)
        # Di sini kita perlu urutkan terbalik dari popular dan ambil yang terbawah
        'unpopular': serializers.serialize('python', 
                                           Course.objects.annotate(member_count=Count('memberships'))
                                           .order_by('member_count')[:5])
    }
    
    # return JsonResponse(result, safe=False)
    # Catatan: Karena struktur JSON yang dihasilkan oleh serializers.serialize('python')
    # akan sangat mirip dengan yang Anda lihat di gambar, ini adalah cara yang efisien.

    # Untuk menyamakan struktur dengan gambar yang tidak memiliki min/max/avg sebagai sub-dict
    # kita pisahkan stat menjadi field individual.
    
    return JsonResponse(result, safe=False)
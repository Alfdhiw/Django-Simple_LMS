# courses/views.py

from django.shortcuts import render
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
# users/views.py

from django.http import JsonResponse
from users.models import User
from courses.models import Course 
from django.db.models import Count # <-- Import Count untuk agregasi
from django.core import serializers
# ... (pastikan impor lainnya seperti render, redirect, dll. tetap ada) ...

def user_stat(request):
    """
    Menghasilkan statistik user (jumlah, paling aktif, dll.) dalam format JSON.
    """
    
    # 1. Ambil semua user
    all_users = User.objects.all()
    user_count = all_users.count()
    
    # 2. Cari user yang paling banyak mengajar (Teacher Paling Produktif)
    # Gunakan related_name 'course_set' (default) atau yang Anda definisikan untuk FK 'teacher' di model Course.
    # Kita asumsikan related_name default adalah 'course_set'
    most_courses_taught = User.objects.annotate(
        course_count=Count('course_set')
    ).order_by('-course_count')[:5] # 5 guru teratas
    
    # 3. Cari user yang paling banyak mendaftar ke kursus (Student Paling Aktif)
    # Gunakan related_name dari Foreign Key 'user' di model CourseMember
    # Kita asumsikan related_name default adalah 'coursemember_set' atau 'course_enrollments' (seperti yang kita gunakan sebelumnya di dashboard)
    most_enrolled = User.objects.annotate(
        enrollment_count=Count('course_enrollments') # Asumsi related_name adalah 'course_enrollments'
    ).order_by('-enrollment_count')[:5] # 5 siswa teratas
    
    # 4. Serialisasi Objek Django
    teachers_serialized = serializers.serialize('python', most_courses_taught)
    students_serialized = serializers.serialize('python', most_enrolled)

    # 5. Format Hasil Akhir
    result = {
        'total_users': user_count,
        'active_teachers': teachers_serialized,
        'active_students': students_serialized,
        # Contoh tambahan
        'teachers_count': User.objects.filter(is_staff=True).count(),
        'students_count': User.objects.filter(is_staff=False).count(),
    }
    
    return JsonResponse(result, safe=False)
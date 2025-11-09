from django.db import models
from django.conf import settings # Digunakan untuk mengacu pada AUTH_USER_MODEL

# Role choices untuk CourseMember (sesuai skema ENUM)
class CourseRole(models.TextChoices):
    STUDENT = 'Student', 'Student'
    TEACHER = 'Teacher', 'Teacher'

class Course(models.Model):
    """Tabel 'course'"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()
    image = models.CharField(max_length=200, blank=True, null=True)
    
    # Hubungan One-to-Many dengan User yang berperan sebagai 'teacher'
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Jaga data course jika guru dihapus
        related_name='taught_courses',
        null=True
    )
    
    def __str__(self):
        return self.name

class CourseMember(models.Model):
    """Tabel 'course_member' (Junction Table Many-to-Many)"""
    # foreign key ke tabel course
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='memberships')
    
    # foreign key ke tabel user
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='course_enrollments')
    
    # role ENUM di skema
    role = models.CharField(
        max_length=10,
        choices=CourseRole.choices,
        default=CourseRole.STUDENT
    )

    class Meta:
        # Menjamin bahwa satu user hanya terdaftar sekali di satu course
        unique_together = ('course', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.course.name} ({self.role})"

class CourseContent(models.Model):
    """Tabel 'course_content'"""
    name = models.CharField(max_length=200)
    description = models.TextField()
    video_url = models.CharField(max_length=255, blank=True, null=True) # Gunakan CharField dengan panjang yang cukup
    file_attachment = models.CharField(max_length=255, blank=True, null=True)

    # Hubungan Parent-Child untuk konten berjenjang (misal: Unit -> Pelajaran)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL, # Konten tetap ada meski parent-nya dihapus
        related_name='children',
        null=True,
        blank=True
    )

    # foreign key ke tabel course
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='contents')

    def __str__(self):
        return f"{self.name} ({self.course.name})"

class Completion(models.Model):
    """Tabel 'completion' untuk melacak progres siswa"""
    # foreign key ke tabel course_member (menggunakan member_id)
    # Catatan: Skema menggunakan member_id (int), jadi kita pakai ForeignKey ke CourseMember
    member = models.ForeignKey(CourseMember, on_delete=models.CASCADE, related_name='completions')
    
    # foreign key ke tabel course_content (menggunakan content_id)
    content = models.ForeignKey(CourseContent, on_delete=models.CASCADE, related_name='completions')
    
    last_update = models.DateTimeField(auto_now=True) # Otomatis update waktu terakhir selesai

    class Meta:
        # Menjamin bahwa satu member hanya memiliki satu status completion per content
        unique_together = ('member', 'content')
        verbose_name_plural = "Completions"

    def __str__(self):
        return f"Completion: {self.member} - {self.content.name}"
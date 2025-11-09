from django.db import models
from django.conf import settings
from courses.models import CourseContent # Import CourseContent dari aplikasi courses

class Comment(models.Model):
    """Tabel 'comment'"""
    # foreign key ke tabel user
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    
    # foreign key ke tabel course_content
    content = models.ForeignKey(CourseContent, on_delete=models.CASCADE, related_name='comments')
    
    comment = models.TextField() # Isi komentar

    # Opsional: Tambahkan timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.content.name}"
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Model kustom untuk User, menggantikan User default Django.
    Tambahkan field 'fullname' yang unik dari skema.
    """
    # Username, email, password sudah ada di AbstractUser
    fullname = models.CharField(max_length=100, blank=True, null=True)

    # Menghapus 'first_name' dan 'last_name' bawaan jika tidak diperlukan
    first_name = None
    last_name = None

    def __str__(self):
        return self.username

# --- Perubahan di settings.py diperlukan ---
# Pastikan Anda mengatur AUTH_USER_MODEL = 'users.User' di simple_LMS/settings.py
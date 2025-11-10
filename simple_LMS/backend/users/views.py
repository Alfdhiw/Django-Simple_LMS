from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import LoginForm, RegistrationForm
from courses.models import Course
from users.models import User 
from django.contrib import messages
from .forms import UserManagementForm

# --- View Autentikasi ---

def user_registration(request):
    """Menangani permintaan pendaftaran user baru."""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # Menggunakan ORM: create_user()
            user = form.save() 
            login(request, user) # Langsung login setelah pendaftaran berhasil
            return redirect('dashboard')
    else:
        form = RegistrationForm()
        
    return render(request, 'users/register.html', {'form': form, 'title': 'Daftar Akun Baru'})

def user_login(request):
    """Menangani permintaan login user."""
    # Jika user sudah login, arahkan ke dashboard
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Menggunakan ORM: authenticate()
            user = authenticate(
                request, 
                username=form.cleaned_data.get('username'), 
                password=form.cleaned_data.get('password')
            )
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                # Menambahkan pesan error jika autentikasi gagal
                form.add_error(None, "Username atau kata sandi tidak valid.")
    else:
        form = LoginForm()
        
    return render(request, 'users/login.html', {'form': form, 'title': 'Login ke LMS'})

def user_logout(request):
    """Menangani permintaan logout user."""
    logout(request)
    return redirect('login') 

def is_superuser(user):
    return user.is_superuser
# --- View Dashboard ---

@login_required(login_url='login')
def dashboard(request):
    """
    Menampilkan halaman dashboard user, sekarang termasuk daftar semua user.
    """
    current_user = request.user
    
    # === BARIS BARU DITAMBAHKAN ===
    # Query ORM: Ambil semua user yang terdaftar, kecuali diri sendiri
    # Jika Anda ingin menampilkan diri sendiri, hapus .exclude(pk=current_user.pk)
    all_users = User.objects.all().exclude(pk=current_user.pk).order_by('date_joined')
    # ===============================

    # 1. Kursus yang diajar oleh user ini (teacher)
    courses_taught = Course.objects.filter(teacher=current_user).count()
    
    # 2. Kursus yang diikuti user ini (student)
    enrollments = current_user.course_enrollments.all()
    courses_enrolled_count = enrollments.count()
    
    context = {
        'title': 'Dashboard Saya',
        'fullname': current_user.fullname if current_user.fullname else current_user.username,
        'email': current_user.email,
        'courses_taught_count': courses_taught,
        'courses_enrolled_count': courses_enrolled_count,
        'enrollments': enrollments[:5],
        
        # === TAMBAHKAN KE CONTEXT ===
        'all_users': all_users 
        # ============================
    }
    
    return render(request, 'users/dashboard.html', context)

# --- VIEW CREATE USER ---
@login_required
@user_passes_test(is_superuser, login_url='/login/')
def user_create(request):
    """Membuat user baru (hanya untuk Admin)."""
    if request.method == 'POST':
        # Ketika membuat user baru, kita perlu form yang berbeda atau menangani password secara manual.
        # Untuk kesederhanaan, kita akan menggunakan form yang kita buat (tanpa field password)
        # dan meminta admin mengatur password secara manual nanti, atau menggunakan forms.ModelForm standar 
        # yang mencakup password. Namun, lebih aman menggunakan admin/superuser checker.
        form = UserManagementForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            # Karena form ini tidak mengelola password, Anda harus mengaturnya di Admin Django atau membuat 
            # form terpisah untuk password di sini jika ini adalah flow Create yang lengkap.
            user.set_unusable_password() 
            user.save()
            messages.success(request, f'User {user.username} berhasil dibuat. Harap atur passwordnya di Admin.')
            return redirect('dashboard')
    else:
        form = UserManagementForm()
        
    context = {'form': form, 'title': 'Tambah User Baru'}
    return render(request, 'users/user_form.html', context)

# --- VIEW UPDATE USER ---
@login_required
@user_passes_test(is_superuser, login_url='/login/')
def user_update(request, pk):
    """Mengedit data user berdasarkan Primary Key (pk)."""
    # ORM: Ambil objek user berdasarkan PK, atau kembalikan 404 jika tidak ditemukan
    user = get_object_or_404(User, pk=pk) 
    
    if request.method == 'POST':
        form = UserManagementForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Data user {user.username} berhasil diperbarui.')
            return redirect('dashboard')
    else:
        # Isi form dengan data user yang ada
        form = UserManagementForm(instance=user)
        
    context = {'form': form, 'title': f'Edit User: {user.username}'}
    return render(request, 'users/user_form.html', context)

# --- VIEW DELETE USER ---
@login_required
@user_passes_test(is_superuser, login_url='/login/')
def user_delete(request, pk):
    """Menghapus user berdasarkan Primary Key (pk)."""
    # ORM: Ambil objek user
    user = get_object_or_404(User, pk=pk)
    
    # Batasi agar user tidak bisa menghapus dirinya sendiri
    if user == request.user:
        messages.error(request, "Anda tidak dapat menghapus akun Anda sendiri.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        # ORM: Delete user
        user.delete() 
        messages.success(request, f'User {user.username} berhasil dihapus.')
        return redirect('dashboard')
        
    context = {'user': user, 'title': f'Hapus User: {user.username}'}
    return render(request, 'users/user_confirm_delete.html', context)
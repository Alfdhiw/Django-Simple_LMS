# users/forms.py

from django import forms
from users.models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Kata Sandi'})
    )

class RegistrationForm(forms.ModelForm):
    # Field tambahan untuk konfirmasi password
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Konfirmasi Kata Sandi'}),
        label="Konfirmasi Kata Sandi"
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'fullname', 'password')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'fullname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Lengkap'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Kata Sandi'}),
        }
        
    def clean(self):
        # Tambahkan validasi kustom untuk memastikan password sama
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError(
                "Kata sandi dan konfirmasi kata sandi tidak cocok."
            )
        return cleaned_data
        
    def save(self, commit=True):
        # Pastikan kita menggunakan create_user saat menyimpan
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],
            fullname=self.cleaned_data['fullname']
        )
        return user
    
class UserManagementForm(forms.ModelForm):
    # Hapus field password dari sini. Password harus diubah melalui form terpisah atau Admin Django.
    # Jika perlu mengubah password, gunakan fungsi set_password() di view.
    
    class Meta:
        model = User
        fields = ('username', 'email', 'fullname', 'is_staff', 'is_active')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'fullname': forms.TextInput(attrs={'class': 'form-control'}),
        }
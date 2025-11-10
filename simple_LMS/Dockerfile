# Gunakan image resmi Python
FROM python:3.11-slim

# Atur variabel lingkungan agar Django dan Python berjalan dengan benar
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Tetapkan direktori kerja di dalam container
WORKDIR /app/backend

# --- AWAL: Penambahan untuk menginstal sqlite3 CLI ---
RUN apt-get update && \
    apt-get install -y sqlite3 && \
    rm -rf /var/lib/apt/lists/*
# --- AKHIR: Penambahan untuk menginstal sqlite3 CLI ---

# Instal dependensi Python
COPY backend/requirements.txt /app/backend/
RUN pip install --no-cache-dir -r requirements.txt

# Salin sisa kode proyek
COPY backend/ /app/backend/

# Ekspos port 8000
EXPOSE 8000

# Perintah default untuk menjalankan server pengembangan Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
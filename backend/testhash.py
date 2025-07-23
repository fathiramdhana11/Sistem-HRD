from passlib.context import CryptContext

# Ini harus sama dengan konfigurasi di backend/app/utils/security.py
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Ganti "superadmin123" dengan password yang ingin Anda gunakan
new_plain_password = "superadmin123" 
hashed_password = pwd_context.hash(new_plain_password)
print(f"Password '{new_plain_password}' akan di-hash menjadi: {hashed_password}")
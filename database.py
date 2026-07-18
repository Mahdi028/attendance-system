# import sqlite3
# import hashlib
# from datetime import datetime

# import os

# # مسیر دقیق فایل دیتابیس در کنار همین فایل پایتون
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DB_PATH = os.path.join(BASE_DIR, "attendance.db")


# # مسیر ذخیره دیتابیس


# # ------------------ تابع ساخت دیتابیس ------------------
# def init_db():
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     # جدول ادمین (فقط یک ادمین ثابت)
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS admin (
#         id INTEGER PRIMARY KEY CHECK (id = 1),
#         username TEXT UNIQUE NOT NULL,
#         password_hash TEXT NOT NULL,
#         last_updated TEXT
#     )
#     """)

#     # جدول کارمندان
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS employees (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         full_name TEXT NOT NULL,
#         code TEXT UNIQUE NOT NULL,
#         image_path TEXT,
#         date_added TEXT
#     )
#     """)

#     # جدول حضور و غیاب
#     cursor.execute("""
#     CREATE TABLE IF NOT EXISTS attendance (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         employee_id INTEGER,
#         date TEXT,
#         entry_time TEXT,
#         exit_time TEXT,
#         FOREIGN KEY (employee_id) REFERENCES employees(id)
#     )
#     """)

#     # اگر هنوز ادمینی وجود ندارد، ایجاد شود
#     cursor.execute("SELECT COUNT(*) FROM admin")
#     if cursor.fetchone()[0] == 0:
#         cursor.execute("""
#             INSERT INTO admin (id, username, password_hash, last_updated)
#             VALUES (1, ?, ?, ?)
#         """, ("admin123", hash_password("1010"), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
#         print("✅ ادمین پیش‌فرض با نام کاربری 'admin123' و رمز '1010' ساخته شد.")

#     conn.commit()
#     conn.close()


# # ------------------ تابع هش کردن رمز عبور ------------------
# def hash_password(password: str):
#     return hashlib.sha256(password.encode()).hexdigest()


# # ------------------ بررسی ورود ادمین ------------------
# def verify_admin(username: str, password: str) -> bool:
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("SELECT username, password_hash FROM admin WHERE id=1")
#     row = cursor.fetchone()
#     conn.close()

#     if not row:
#         return False

#     db_username, db_password_hash = row
#     return username == db_username and hash_password(password) == db_password_hash


# # ------------------ تغییر نام کاربری ------------------
# # def change_username_in_db(new_username):
# #     """تغییر مستقیم نام کاربری ادمین در دیتابیس"""
# #     conn = sqlite3.connect(DB_PATH)
# #     cursor = conn.cursor()

# #     # بررسی وجود ادمین
# #     cursor.execute("SELECT username FROM admin WHERE id=1")
# #     current = cursor.fetchone()

# #     if not current:
# #         print("❌ هیچ ادمینی وجود ندارد.")
# #         conn.close()
# #         return False

# #     # انجام تغییر
# #     cursor.execute("""
# #         UPDATE admin 
# #         SET username=?, last_updated=?
# #         WHERE id=1
# #     """, (new_username.strip(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

# #     conn.commit()
# #     conn.close()

# #     print(f"✅ نام کاربری با موفقیت به '{new_username}' تغییر یافت.")
# #     return True


# def change_username_in_db(old_username, new_username):
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
    
#     # بررسی وجود ادمین
#     cursor.execute("SELECT username FROM admin WHERE id=1")
#     current = cursor.fetchone()

#     if not current:
#         conn.close()
#         print("❌ ادمین یافت نشد.")
#         return False

#     current_username = current[0]

#     if old_username.strip() != current_username.strip():
#         conn.close()
#         print("❌ نام کاربری فعلی اشتباه است.")
#         return False

#     if old_username.strip() == new_username.strip():
#         conn.close()
#         print("⚠️ نام کاربری جدید با قبلی یکسان است.")
#         return False

#     cursor.execute("""
#         UPDATE admin 
#         SET username=?, last_updated=? 
#         WHERE id=1
#     """, (new_username.strip(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

#     conn.commit()
#     conn.close()
#     print("✅ نام کاربری با موفقیت تغییر کرد.")
#     return True


# # ------------------ تغییر رمز عبور ------------------
# def change_password_in_db(old_password, new_password):
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("SELECT password_hash FROM admin WHERE id=1")
#     current = cursor.fetchone()

#     if not current:
#         conn.close()
#         print("❌ ادمین یافت نشد.")
#         return False

#     stored_hash = current[0]
#     if hash_password(old_password) != stored_hash:
#         conn.close()
#         print("❌ رمز عبور فعلی اشتباه است.")
#         return False

#     cursor.execute("UPDATE admin SET password_hash=?, last_updated=? WHERE id=1",
#                    (hash_password(new_password), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
#     conn.commit()
#     conn.close()
#     print("✅ رمز عبور با موفقیت تغییر کرد.")
#     return True


# # ------------------ افزودن کارمند ------------------
# def add_employee(full_name, code, image_path=None):
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("""
#         INSERT INTO employees (full_name, code, image_path, date_added)
#         VALUES (?, ?, ?, ?)
#     """, (full_name, code, image_path, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
#     conn.commit()
#     conn.close()
#     print(f"✅ کارمند {full_name} اضافه شد.")


# # ------------------ حذف کارمند ------------------
# def remove_employee(code):
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM employees WHERE code=?", (code,))
#     conn.commit()
#     conn.close()
#     print(f"🗑 کارمند با کد {code} حذف شد.")


# # ------------------ ثبت حضور ------------------
# def mark_entry(employee_code):
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("SELECT id FROM employees WHERE code=?", (employee_code,))
#     emp = cursor.fetchone()

#     if not emp:
#         conn.close()
#         print("❌ کارمند یافت نشد.")
#         return

#     emp_id = emp[0]
#     date_today = datetime.now().strftime("%Y-%m-%d")
#     time_now = datetime.now().strftime("%H:%M:%S")

#     cursor.execute("""
#         INSERT INTO attendance (employee_id, date, entry_time)
#         VALUES (?, ?, ?)
#     """, (emp_id, date_today, time_now))
#     conn.commit()
#     conn.close()
#     print(f"✅ حضور کارمند {employee_code} در ساعت {time_now} ثبت شد.")


# # ------------------ ثبت خروج ------------------
# def mark_exit(employee_code):
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("SELECT id FROM employees WHERE code=?", (employee_code,))
#     emp = cursor.fetchone()

#     if not emp:
#         conn.close()
#         print("❌ کارمند یافت نشد.")
#         return

#     emp_id = emp[0]
#     date_today = datetime.now().strftime("%Y-%m-%d")
#     time_now = datetime.now().strftime("%H:%M:%S")

#     cursor.execute("""
#         UPDATE attendance
#         SET exit_time=?
#         WHERE employee_id=? AND date=? AND exit_time IS NULL
#     """, (time_now, emp_id, date_today))
#     conn.commit()
#     conn.close()
#     print(f"✅ خروج کارمند {employee_code} در ساعت {time_now} ثبت شد.")


#############################################################################################################################

import sqlite3
import hashlib
from datetime import datetime
import os

# مسیر دیتابیس
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "attendance.db")

# ------------------ مدیریت دیتابیس ------------------
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # جدول ادمین
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        last_updated TEXT
    )
    """)

    # جدول کارمندان
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        code TEXT UNIQUE NOT NULL,
        image_path TEXT,
        date_added TEXT
    )
    """)

    # جدول حضور و غیاب
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        date TEXT,
        entry_time TEXT,
        exit_time TEXT,
        FOREIGN KEY (employee_id) REFERENCES employees(id)
    )
    """)

    # ایجاد ادمین پیش‌فرض
    cursor.execute("SELECT COUNT(*) FROM admin")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
            INSERT INTO admin (id, username, password_hash, last_updated)
            VALUES (1, ?, ?, ?)
        """, ("admin", hash_password("1010"), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()

# ------------------ هش رمز عبور ------------------
def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

# ------------------ اعتبارسنجی ادمین ------------------
def verify_admin(username: str, password: str) -> bool:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT username, password_hash FROM admin WHERE id=1")
    row = cursor.fetchone()
    conn.close()
    if not row:
        return False
    db_username, db_password_hash = row
    return username == db_username and hash_password(password) == db_password_hash

# ------------------ تغییر نام کاربری ------------------
def change_username_in_db(old_username, new_username):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM admin WHERE id=1")
    current = cursor.fetchone()
    if not current or old_username.strip() != current[0].strip():
        conn.close()
        return False
    cursor.execute("UPDATE admin SET username=?, last_updated=? WHERE id=1", 
                   (new_username.strip(), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    return True

# ------------------ تغییر رمز عبور ------------------
def change_password_in_db(old_password, new_password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM admin WHERE id=1")
    current = cursor.fetchone()
    if not current or hash_password(old_password) != current[0]:
        conn.close()
        return False
    cursor.execute("UPDATE admin SET password_hash=?, last_updated=? WHERE id=1",
                   (hash_password(new_password), datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()
    return True

# ------------------ مدیریت کارمندان ------------------
def add_employee(full_name, code, image_path=None):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO employees (full_name, code, image_path, date_added) VALUES (?, ?, ?, ?)"
                   , (full_name, code, image_path, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def remove_employee(code):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE code=?", (code,))
    conn.commit()
    conn.close()

def get_all_employees():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, full_name, code, image_path FROM employees")
    rows = cursor.fetchall()
    conn.close()
    return rows

# ------------------ ثبت ورود و خروج ------------------
def mark_entry(employee_code):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM employees WHERE code=?", (employee_code,))
    emp = cursor.fetchone()
    if not emp:
        conn.close()
        return False
    emp_id = emp[0]
    date_today = datetime.now().strftime("%Y-%m-%d")
    time_now = datetime.now().strftime("%H:%M:%S")
    cursor.execute("INSERT INTO attendance (employee_id, date, entry_time) VALUES (?, ?, ?)"
                   , (emp_id, date_today, time_now))
    conn.commit()
    conn.close()
    return True

def mark_exit(employee_code):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM employees WHERE code=?", (employee_code,))
    emp = cursor.fetchone()
    if not emp:
        conn.close()
        return False
    emp_id = emp[0]
    date_today = datetime.now().strftime("%Y-%m-%d")
    time_now = datetime.now().strftime("%H:%M:%S")
    cursor.execute("UPDATE attendance SET exit_time=? WHERE employee_id=? AND date=? AND exit_time IS NULL",
                   (time_now, emp_id, date_today))
    conn.commit()
    conn.close()
    return True

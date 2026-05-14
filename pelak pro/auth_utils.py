# auth_utils.py (این کد را در فایل auth_utils.py خودت بگذار)

import hashlib
# فرض می‌کنیم db_utils.py هم دارید و از آن استفاده می‌کنیم
# اگر db_utils.py ندارید یا هنوز آماده نیست، این خط را کامنت کنید
# import db_utils

# --- توابع کمکی ---
def hash_password(password):
    """رمز عبور را هش می‌کند."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(stored_password_hash, provided_password):
    """رمز عبور ارائه شده را با رمز عبور هش شده ذخیره شده مقایسه می‌کند."""
    return stored_password_hash == hash_password(provided_password)

# --- توابع اصلی احراز هویت ---
# فرض می‌کنیم تابع get_user_from_db در db_utils.py وجود دارد
# def get_user_from_db(username):
#     # این تابع باید نام کاربری را بگیرد و اطلاعات کاربر را از دیتابیس برگرداند
#     # مثلاً: return db_utils.get_user_by_username(username)
#     # اگر کاربر پیدا نشد، None برگرداند
#     pass # placeholder

def login_user(username, password):
    """
    ورود کاربر به سیستم.
    نام کاربری و رمز عبور را گرفته و در صورت تطابق، اطلاعات کاربر را برمی‌گرداند.
    """
    # فعلاً برای تست، فرض می‌کنیم اطلاعات کاربر در این دیکشنری هست
    # در حالت واقعی باید از دیتابیس گرفته شود
    # user_data = db_utils.get_user_from_db(username)
    
    # --- شروع بخش موقتی برای تست بدون دیتابیس ---
    # اگر db_utils ندارید، از این بخش استفاده کنید
    mock_users = {
        "admin": {"username": "admin", "password_hash": hash_password("12345")},
        "user1": {"username": "user1", "password_hash": hash_password("qwerty")}
    }
    user_data = mock_users.get(username)
    # --- پایان بخش موقتی ---

    if user_data:
        stored_password_hash = user_data.get('password_hash')
        if verify_password(stored_password_hash, password):
            print(f"ورود موفق برای کاربر: {username}")
            # اینجا می‌توانید اطلاعات اضافه کاربر را برگردانید، مثلاً نقش او
            return {"username": username, "role": "admin" if username == "admin" else "user"} # مثال
        else:
            print("رمز عبور اشتباه است.")
            return None
    else:
        print("کاربر یافت نشد.")
        return None

def register_user(username, password, email=None):
    """
    ثبت‌نام کاربر جدید.
    """
    # فعلاً برای تست، فرض می‌کنیم ثبت‌نام موفقیت‌آمیز است
    # در حالت واقعی باید کاربر را در دیتابیس ذخیره کنید
    print(f"ثبت‌نام کاربر {username} (ایمیل: {email}) انجام شد.")
    # اینجا باید تابع db_utils.create_user را صدا بزنید
    return {"username": username, "email": email} # مثال اطلاعات کاربر ثبت شده

# می‌توانید توابع دیگری مثل logout_user, is_logged_in و ... هم اضافه کنید

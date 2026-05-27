[app]

# نام برنامه که روی گوشی نشون داده میشه
title = Sarkubgar

# نام بسته (فقط حروف کوچک، عدد، زیرخط)
package.name = SarManager

# دامنه معکوس (مهم برای منحصر به فرد بودن)
package.domain = com.javidnam.pelak

# نسخه برنامه
version = 1.0.0

# نسخه کد برای اندروید (عدد صحیح)
android.numeric_version = 1

# نیازمندی‌ها - حتما hashlib نیاز نیست چون داخلیه
requirements = python3==3.9.7,kivy==2.2.1,sqlite3

# فایل اصلی برنامه
source.dir = .
source.include_extras = True

# فایل‌هایی که باید همراه برنامه برن
source.include_patterns = icon.png,*.py,*.db

# آیکون برنامه (همون فایلی که داری)
icon.filename = icon.png

# اجازه دسترسی به حافظه برای دیتابیس
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# پذیرش مجوز SDK
android.accept_sdk_license = True

# نسخه SDK و NDK
android.ndk = 25b
android.sdk = 30
android.ndk_api = 30

# معماری‌های پشتیبانی شده
android.archs = armeabi-v7a, arm64-v8a

# حالت دیباگ
android.release = False
android.debug = True

# لاگ
log_level = 2

[buildozer]

log_level = 2
warn_on_root = 1
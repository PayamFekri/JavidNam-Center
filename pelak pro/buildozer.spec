[app]
title = Sar Manager
package.name = sarmanager
package.domain = org.example # این را می‌توانید با دامنه دلخواه خودتان جایگزین کنید
source.dir = .
source.include_exts = py,kv,sqlite3,db  # فرمت‌های فایل پروژه شما

version = 0.1
requirements = python3,kivy,sqlite3 # sqlite3 معمولا با پایتون هست اما برای اطمینان اضافه شده

# برای دسترسی به حافظه داخلی (برای ذخیره دیتابیس)
android.permissions = WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE

# اگر پروژه شما نیاز به GUI دارد که در buildozer.spec مشخص نشده
# android.force_permissions = INTERNET # اگر در آینده نیاز شد

# orientation = portrait # یا landscape یا all
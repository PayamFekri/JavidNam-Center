باشه! برات یه فایل `README.md` حرفه‌ای برای پروژه **JavidNam Center** می‌نویسم:

```markdown
# 🛍️ JavidNam Center | فروشگاه آنلاین جامع

یک فروشگاه آنلاین کامل و حرفه‌ای ساخته شده با **Django 5.2.14** و قالب مدرن **Kaira**.

![Django Version](https://img.shields.io/badge/Django-5.2.14-green.svg)
![Python Version](https://img.shields.io/badge/Python-3.13-blue.svg)
![License](https://img.shields.io/badge/License-MIT-orange.svg)

---

## ✨ امکانات پروژه

| بخش | وضعیت | توضیحات |
|------|--------|----------|
| 📦 مدیریت محصولات | ✅ کامل | اضافه، ویرایش، حذف محصولات در پنل ادمین |
| 🗂️ دسته‌بندی محصولات | ✅ کامل | مدیریت دسته‌بندی‌ها با تصویر |
| 🛒 سبد خرید | ✅ پیشرفته | افزودن، حذف، تغییر تعداد، محاسبه خودکار قیمت |
| 👤 احراز هویت کاربران | ✅ کامل | ثبت‌نام، ورود، خروج، پروفایل کاربری |
| 🔍 جستجوی محصولات | ✅ پایه | جستجو در محصولات |
| 📧 خبرنامه | ✅ کامل | ثبت ایمیل کاربران، مدیریت در ادمین |
| 🎨 قالب اختصاصی | ✅ کامل | قالب Kaira با طراحی ریسپانسیو |
| 📱 ریسپانسیو | ✅ کامل | سازگار با موبایل، تبلت و دسکتاپ |
| 💾 دیتابیس | ✅ SQLite | قابل تغییر به PostgreSQL |

---

## 🏗️ ساختار پروژه

```
JavidNam-Center/
├── core/                  # تنظیمات اصلی پروژه
│   ├── settings.py        # تنظیمات پروژه
│   ├── urls.py            # URLهای اصلی
│   └── wsgi.py
├── shop/                  # اپلیکیشن اصلی فروشگاه
│   ├── models.py          # مدل‌های Category، Product، Newsletter
│   ├── views.py           # ویوهای محصولات، سبد خرید، خبرنامه
│   ├── cart.py            # منطق سبد خرید
│   └── urls.py            # URLهای فروشگاه
├── accounts/              # اپلیکیشن احراز هویت
│   ├── views.py           # ثبت‌نام، ورود، خروج، پروفایل
│   └── urls.py
├── static/                # فایل‌های استاتیک (CSS, JS, Images)
│   ├── css/               # استایل‌های قالب Kaira
│   ├── js/                # اسکریپت‌های قالب
│   └── images/            # تصاویر قالب
├── templates/             # قالب‌های HTML
│   ├── shop/              # قالب‌های فروشگاه
│   │   ├── includes/      # بخش‌های reusable
│   │   ├── base.html      # قالب اصلی
│   │   ├── index.html     # صفحه اصلی
│   │   ├── product_list.html
│   │   ├── product_detail.html
│   │   └── cart_detail.html
│   └── accounts/          # قالب‌های احراز هویت
│       ├── login.html
│       ├── register.html
│       └── profile.html
├── media/                 # فایل‌های آپلودی (تصاویر محصولات)
├── db.sqlite3             # دیتابیس
└── manage.py
```

---

## 🚀 نصب و راه‌اندازی

### 1. کلون پروژه

```bash
git clone https://github.com/your-username/JavidNam-Center.git
cd JavidNam-Center
```

### 2. ایجاد محیط مجازی

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. نصب وابستگی‌ها

```bash
pip install -r requirements.txt
```

#### وابستگی‌های اصلی:
```
Django==5.2.14
Pillow==12.2.0          # برای مدیریت تصاویر
```

### 4. تنظیمات اولیه

```bash
# اعمال مایگریشن‌ها
python manage.py migrate

# ایجاد سوپر یوزر (مدیر سایت)
python manage.py createsuperuser

# جمع‌آوری فایل‌های استاتیک
python manage.py collectstatic --noinput
```

### 5. اجرای سرور توسعه

```bash
python manage.py runserver
```

سایت در آدرس `http://127.0.0.1:8000` در دسترس است.

---

## 📋 دستورات مفید

| دستور | توضیح |
|-------|-------|
| `python manage.py runserver` | اجرای سرور توسعه |
| `python manage.py makemigrations` | ساخت فایل‌های مایگریشن |
| `python manage.py migrate` | اعمال مایگریشن‌ها |
| `python manage.py createsuperuser` | ساخت کاربر ادمین |
| `python manage.py collectstatic` | جمع‌آوری فایل‌های استاتیک |
| `python manage.py shell` | وارد شدن به شل جنگو |

---

## 🗂️ مدل‌های اصلی

### Category (دسته‌بندی)
- `name` - نام دسته‌بندی
- `slug` - نامک برای URL
- `image` - تصویر دسته‌بندی

### Product (محصول)
- `category` - دسته‌بندی (ForeignKey)
- `name` - نام محصول
- `slug` - نامک برای URL
- `description` - توضیحات
- `price` - قیمت
- `image` - تصویر محصول
- `available` - وضعیت موجودی
- `created` - تاریخ ایجاد
- `updated` - تاریخ بروزرسانی

### Newsletter (خبرنامه)
- `email` - ایمیل کاربر (unique)
- `created_at` - تاریخ ثبت
- `is_active` - وضعیت فعال

---

## 🛒 سبد خرید

سبد خرید با استفاده از **Session** پیاده‌سازی شده و امکانات زیر را دارد:

- ✅ افزودن محصول به سبد خرید
- ✅ افزایش/کاهش تعداد محصول
- ✅ حذف محصول از سبد خرید
- ✅ خالی کردن کل سبد خرید
- ✅ محاسبه خودکار قیمت کل
- ✅ به‌روزرسانی لحظه‌ای با AJAX
- ✅ نمایش تعداد محصولات در نوار ناوبری

---

## 🔐 احراز هویت کاربران

سیستم احراز هویت کامل با استفاده از `django.contrib.auth`:

- ✅ ثبت‌نام کاربر جدید
- ✅ ورود به حساب کاربری
- ✅ خروج از حساب
- ✅ صفحه پروفایل کاربری

---

## 🎨 قالب

قالب **Kaira** یک قالب فروشگاهی مدرن و ریسپانسیو است که شامل:

- اسلایدر تصاویر
- بخش محصولات جدید
- بخش محصولات پرفروش
- بخش دسته‌بندی‌ها
- بخش نظرات مشتریان
- بخش وبلاگ
- بخش اینستاگرام
- فوتر کامل با لینک‌ها و شبکه‌های اجتماعی

---

## 🛠️ رفع خطاهای رایج

### خطای `DEFAULT_AUTO_FIELD`

به `settings.py` اضافه کنید:
```python
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

### خطای 403 در ادمین

به `settings.py` اضافه کنید:
```python
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]
```

### خطای TemplateDoesNotExist

مطمئن شوید پوشه `templates/shop/includes/` تمام فایل‌های مورد نیاز را دارد:
- preloader.html
- search-popup.html
- offcanvas-cart.html
- navbar.html
- footer.html
- و بقیه بخش‌ها

---

## 📸 اسکرین‌شات‌ها

| صفحه اصلی | لیست محصولات | سبد خرید |
|-----------|--------------|----------|
| 🖼️ صفحه اصلی با اسلایدر | 🖼️ نمایش محصولات در قالب گرید | 🖼️ سبد خرید پیشرفته |

---

## 🤝 مشارکت در توسعه

1. Fork کنید
2. Branch جدید بسازید (`git checkout -b feature/amazing-feature`)
3. Commit کنید (`git commit -m 'Add amazing feature'`)
4. Push کنید (`git push origin feature/amazing-feature`)
5. Pull Request باز کنید

---

## 📞 تماس و پشتیبانی

- **ایمیل:** info@javidnam.com
- **تلفن:** 021-12345678
- **وبسایت:** www.javidnam.com

---

## 📄 مجوز

این پروژه تحت مجوز **MIT** منتشر شده است.

---

## 👨‍💻 توسعه‌دهنده

**JavidNam Center** - فروشگاه آنلاین جامع

---

## ⭐ ستاره فراموش نشه!

اگه پروژه برات مفید بود، یه ستاره ⭐ بهش بدید!
```

---

## 📁 همچنین فایل `requirements.txt` رو هم بساز:

```txt
Django==5.2.14
Pillow==12.2.0
```

---
- منبع به مرور زمان کامل میشود
- توضیحات با هوش مصنوعی نوشته شده است در صورت کمبود اصلاح میشود 
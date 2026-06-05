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


``` html 
htmlJavidNam-Center/
│
├── manage.py
├── db.sqlite3
├── requirements.txt
├── README.md
│
├── core/                          # پوشه تنظیمات اصلی پروژه
│   ├── __init__.py
│   ├── settings.py                # تنظیمات اصلی Django
│   ├── urls.py                    # URLهای اصلی پروژه
│   ├── asgi.py
│   ├── wsgi.py
│   └── __pycache__/
│
├── shop/                          # اپلیکیشن اصلی فروشگاه
│   ├── __init__.py
│   ├── admin.py                   # تنظیمات پنل ادمین برای مدل‌ها
│   ├── apps.py
│   ├── models.py                  # مدل‌های Category, Product, Newsletter
│   ├── views.py                   # ویوهای محصولات، سبد خرید، خبرنامه
│   ├── urls.py                    # URLهای فروشگاه
│   ├── cart.py                    # منطق سبد خرید (session-based)
│   ├── tests.py
│   │
│   ├── migrations/
│   │   ├── __init__.py
│   │   ├── 0001_initial.py
│   │   ├── 0002_alter_category_id_alter_product_id.py
│   │   └── __pycache__/
│   │
│   └── __pycache__/
│
├── accounts/                      # اپلیکیشن احراز هویت کاربران
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py                   # ویوهای ثبت‌نام، ورود، خروج، پروفایل
│   ├── urls.py                    # URLهای احراز هویت
│   ├── tests.py
│   │
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── __pycache__/
│   │
│   └── __pycache__/
│
├── static/                        # فایل‌های استاتیک (CSS, JS, Images)
│   ├── favicon.ico
│   ├── favicon.png
│   │
│   ├── css/
│   │   ├── style.css              # استایل اصلی قالب Kaira
│   │   ├── vendor.css
│   │   ├── normalize.css
│   │   ├── swiper-bundle.min.css
│   │   └── ajax-loader.gif
│   │
│   ├── js/
│   │   ├── jquery.min.js
│   │   ├── plugins.js
│   │   ├── script.min.js
│   │   ├── SmoothScroll.js
│   │   └── modernizr.js
│   │
│   └── images/                    # تصاویر قالب (بیش از 70 فایل)
│       ├── banner-image-1.jpg
│       ├── banner-image-2.jpg
│       ├── banner-image-3.jpg
│       ├── banner-image-4.jpg
│       ├── banner-image-5.jpg
│       ├── banner-image-6.jpg
│       ├── cat-item1.jpg
│       ├── cat-item2.jpg
│       ├── cat-item3.jpg
│       ├── product-item-1.jpg
│       ├── product-item-2.jpg
│       ├── product-item-3.jpg
│       ├── product-item-4.jpg
│       ├── product-item-5.jpg
│       ├── product-item-6.jpg
│       ├── product-item-7.jpg
│       ├── product-item-8.jpg
│       ├── product-item-9.jpg
│       ├── product-item-10.jpg
│       ├── logo1.png
│       ├── logo2.png
│       ├── logo3.png
│       ├── logo4.png
│       ├── logo5.png
│       ├── main-logo.png
│       ├── insta-item1.jpg
│       ├── insta-item2.jpg
│       ├── insta-item3.jpg
│       ├── insta-item4.jpg
│       ├── insta-item5.jpg
│       ├── insta-item6.jpg
│       ├── post-image1.jpg
│       ├── post-image2.jpg
│       ├── post-image3.jpg
│       ├── video-image.jpg
│       ├── text-pattern.png
│       ├── pattern-bg.png
│       ├── single-image-2.jpg
│       ├── arct-icon.png
│       ├── dhl-logo.png
│       ├── visa-card.png
│       ├── master-card.png
│       ├── paypal-card.png
│       └── ... (سایر تصاویر)
│
├── media/                         # فایل‌های آپلودی (تصاویر محصولات و دسته‌بندی‌ها)
│   └── products/
│       └── 2026/
│           └── 05/
│               └── 30/
│                   └── *.webp, *.jpg, *.avif
│
├── templates/                     # قالب‌های HTML پروژه
│   │
│   ├── shop/
│   │   ├── base.html              # قالب اصلی (شامل هدر، فوتر، اسکریپت‌ها)
│   │   ├── index.html             # صفحه اصلی (شامل همه بخش‌ها)
│   │   ├── product_list.html      # صفحه لیست محصولات
│   │   ├── product_detail.html    # صفحه جزئیات محصول
│   │   ├── cart_detail.html       # صفحه سبد خرید
│   │   │
│   │   └── includes/              # بخش‌های reusable قالب
│   │       ├── preloader.html
│   │       ├── search-popup.html
│   │       ├── offcanvas-cart.html
│   │       ├── navbar.html
│   │       ├── billboard.html
│   │       ├── features.html
│   │       ├── categories.html
│   │       ├── new-arrivals.html
│   │       ├── collection.html
│   │       ├── best-sellers.html
│   │       ├── video.html
│   │       ├── testimonials.html
│   │       ├── related-products.html
│   │       ├── blog.html
│   │       ├── logo-bar.html
│   │       ├── newsletter.html
│   │       ├── instagram.html
│   │       └── footer.html
│   │
│   └── accounts/                  # قالب‌های صفحات احراز هویت
│       ├── login.html
│       ├── register.html
│       └── profile.html
│
└── venv/                          # محیط مجازی Python (اختیاری - در git ignore)
    ├── Scripts/ (Windows) یا bin/ (Linux/Mac)
    ├── Lib/ (Windows) یا lib/ (Linux/Mac)
    └── ...
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

## 📄 مجوز

این پروژه تحت مجوز **MIT** منتشر شده است.

---

## 👨‍💻 توسعه‌دهنده

**Payam Fekri

---

## ⭐ ستاره فراموش نشه!

اگه پروژه برات مفید بود، یه ستاره ⭐ بهش بدید!


## 📁 همچنین فایل `requirements.txt` رو هم بساز:

```txt
Django==5.2.14
Pillow==12.2.0
```

---
- منبع به مرور زمان کامل میشود
- توضیحات با هوش مصنوعی نوشته شده است در صورت کمبود اصلاح میشود 
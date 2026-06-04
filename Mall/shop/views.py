from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product ,Newsletter
from .cart import Cart
from django.contrib import messages


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    cart = Cart(request)
    
    return render(request, 'shop/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'cart': cart,
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart = Cart(request)
    categories = Category.objects.all()
    related_products = Product.objects.filter(category=product.category, available=True).exclude(id=product.id)[:4]
    
    return render(request, 'shop/product_detail.html', {
        'product': product,
        'cart': cart,
        'categories': categories,
        'related_products': related_products,
    })

def cart_detail(request):
    cart = Cart(request)
    categories = Category.objects.all()
    return render(request, 'shop/cart_detail.html', {
        'cart': cart,
        'categories': categories,
    })

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=1)
    return redirect('shop:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('shop:cart_detail')

def index(request):
    categories = Category.objects.all()
    new_products = Product.objects.filter(available=True).order_by('-created')[:8]
    best_sellers = Product.objects.filter(available=True).order_by('-updated')[:8]
    related_products = Product.objects.filter(available=True).order_by('?')[:5]
    cart = Cart(request)
    
    return render(request, 'shop/index.html', {
        'categories': categories,
        'new_products': new_products,
        'best_sellers': best_sellers,
        'related_products': related_products,
        'cart': cart,
    })
    
def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                obj, created = Newsletter.objects.get_or_create(email=email)
                if created:
                    messages.success(request, 'Your email has been successfully subscribed to the newsletter!')
                else:
                    messages.info(request, 'This email is already subscribed to the newsletter.')
            except Exception as e:
                messages.error(request, 'An error occurred. Please try again.')
        else:
            messages.error(request, 'Please enter a valid email address.')
        
        # Return to the previous page
        return redirect(request.META.get('HTTP_REFERER', 'shop:index'))
    
    return redirect('shop:index')
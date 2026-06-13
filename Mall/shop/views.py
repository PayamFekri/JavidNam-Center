from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product ,Newsletter
from .cart import Cart
from django.contrib import messages
from django.http import JsonResponse
from .forms import OrderCreateForm
from .models import Order, OrderItem

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

def cart_update(request):
    """به‌روزرسانی تعداد محصول در سبد خرید (AJAX)"""
    if request.method == 'POST':
        cart = Cart(request)
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))
        
        if cart.update_quantity(product_id, quantity):
            return JsonResponse({
                'success': True,
                'total_price': cart.get_total_price(),
                'cart_length': len(cart),
                'item_total': cart.cart.get(str(product_id), {}).get('total_price', 0)
            })
    
    return JsonResponse({'success': False})

def cart_remove_ajax(request):
    """حذف محصول از سبد خرید با AJAX"""
    if request.method == 'POST':
        cart = Cart(request)
        product_id = request.POST.get('product_id')
        cart.remove_by_id(product_id)
        return JsonResponse({
            'success': True,
            'total_price': cart.get_total_price(),
            'cart_length': len(cart)
        })
    
    return JsonResponse({'success': False})

def order_create(request):
    cart = Cart(request)
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
                order.email = request.user.email
            order.save()
            
            # Create order items from cart
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            
            # Clear the cart
            cart.clear()
            
            # Redirect to order created page
            return render(request, 'shop/order_created.html', {'order': order})
    else:
        # Pre-fill form for authenticated users
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
            }
        form = OrderCreateForm(initial=initial_data)
    
    return render(request, 'shop/order_create.html', {
        'form': form, 
        'cart': cart,
        'categories': Category.objects.all(),
    })
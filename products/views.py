from django.shortcuts import render, redirect, get_object_or_404
from cart.models import Cart
from django.contrib.auth.decorators import login_required
from orders.models import Order, OrderItem
from django.contrib.auth.models import User
from django.db.models import Sum, Avg
from wishlist.models import Wishlist
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta

from .models import (
    Product,
    Category,
    Review,
    Coupon,
)

def home(request):

    featured_products = Product.objects.all().order_by("-sold")[:4]

    new_products = Product.objects.all().order_by("-created_at")[:4]

    return render(
        request,
        "home.html",
        {
            "featured_products": featured_products,
            "new_products": new_products,
        },
    )


def product_list(request):

    products = Product.objects.all().order_by("-id")
    categories = Category.objects.all()

    category_id = request.GET.get("category")

    if category_id:
        products = products.filter(
            category_id=category_id
        )

    search = request.GET.get("search")

    if search:
        products = products.filter(
            name__icontains=search
        )

    sort = request.GET.get("sort")

    if sort == "low":
        products = products.order_by("price")

    elif sort == "high":
        products = products.order_by("-price")

    elif sort == "new":
        products = products.order_by("-created_at")

    # Products added within the last 7 days
    new_date = timezone.now() - timedelta(days=7)

    for product in products:

        # Average Rating
        product.average_rating = (
            Review.objects.filter(
                product=product
            ).aggregate(
                Avg("rating")
            )["rating__avg"]
        )

        # New Product Badge
        product.is_new = product.created_at >= new_date

    # Pagination
    paginator = Paginator(products, 6)

    page_number = request.GET.get("page")

    products = paginator.get_page(page_number)

    return render(
        request,
        "product_list.html",
        {
            "products": products,
            "categories": categories,
        },
    )
def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == 'POST':

        name = request.POST.get('name')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        Review.objects.create(
            product=product,
            name=name,
            rating=rating,
            comment=comment
        )

        return redirect(
            'product_detail',
            product_id=product.id
        )

    reviews = Review.objects.filter(
        product=product
    ).order_by('-created_at')

    related_products = Product.objects.filter(
        category=product.category
        ).exclude(
            id=product.id
        )[:4]

    return render(
    request,
    'product_detail.html',
    {
        'product': product,
        'reviews': reviews,
        'related_products': related_products
    }
)

@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    # Check if the product is out of stock
    if product.stock <= 0:
        return redirect('products')

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


@login_required
def cart_page(request):

    cart_items = Cart.objects.filter(
        user=request.user
    )

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    return render(
        request,
        'cart.html',
        {
            'items': cart_items,
            'total': total
        }
    )


def login_page(request):
    return render(request, 'login.html')


@login_required
def checkout(request):

    cart_items = Cart.objects.filter(user=request.user)

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    discount = 0
    coupon_code = ""

    if request.method == "POST":

        customer_name = request.POST.get("customer_name")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        payment_method = request.POST.get(
            "payment_method",
            "Cash on Delivery"
        )

        coupon_code = request.POST.get("coupon")

        if coupon_code:

            try:
                coupon = Coupon.objects.get(
                    code=coupon_code.upper()
                )

                discount = total * coupon.discount / 100
                total -= discount

            except Coupon.DoesNotExist:
                pass

        # Create Order
        order = Order.objects.create(
            user=request.user,
            customer_name=customer_name,
            phone=phone,
            address=address,
            total_price=total,
            payment_method=payment_method
        )

        print("Order created:", order.id)

        # Save Order Items
        for item in cart_items:

            print("Creating OrderItem:", item.product.name)

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            # Reduce Stock
            product = item.product
            product.stock -= item.quantity
            product.sold += item.quantity
            product.save()

        # Clear Cart
        cart_items.delete()

        if payment_method == "Online Payment":
            message = "✅ Demo Online Payment Successful!"
        else:
            message = "✅ Order Placed Successfully! Cash on Delivery."

        return render(
            request,
            "order_success.html",
            {
                "message": message,
                "payment_method": payment_method
            }
        )

    return render(
        request,
        "checkout.html",
        {
            "items": cart_items,
            "total": total,
            "discount": discount,
            "coupon": coupon_code
        }
    )

@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'my_orders.html',
        {
            'orders': orders
        }
    )


@login_required
def remove_from_cart(request, cart_id):

    item = Cart.objects.get(
        id=cart_id,
        user=request.user
    )

    item.delete()

    return redirect('cart')


@login_required
def increase_quantity(request, cart_id):

    item = Cart.objects.get(
        id=cart_id,
        user=request.user
    )

    item.quantity += 1
    item.save()

    return redirect('cart')


@login_required
def decrease_quantity(request, cart_id):

    item = Cart.objects.get(
        id=cart_id,
        user=request.user
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart')

@login_required


def account_page(request):

    return render(
        request,
        'account.html'
    )


@login_required
def dashboard(request):

    total_products = Product.objects.count()

    total_orders = Order.objects.count()

    total_users = User.objects.count()

    total_reviews = Review.objects.count()

    total_wishlist = Wishlist.objects.count()

    total_revenue = (
        Order.objects.aggregate(
            Sum("total_price")
        )["total_price__sum"] or 0
    )

    return render(
        request,
        "dashboard.html",
        {
            "total_products": total_products,
            "total_orders": total_orders,
            "total_users": total_users,
            "total_reviews": total_reviews,
            "total_wishlist": total_wishlist,
            "total_revenue": total_revenue,
        }
    )

@login_required

def add_to_wishlist(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect('wishlist')


@login_required
def wishlist_page(request):

    items = Wishlist.objects.filter(
        user=request.user
    )

    return render(
        request,
        'wishlist.html',
        {
            'items': items
        }
    )
    
def contact(request):
    return render(request, "contact.html")

def about(request):
      return render(
        request,
        "about.html"
       )


@login_required
def account(request):

    total_orders = Order.objects.filter(
        user=request.user
    ).count()

    wishlist_count = Wishlist.objects.filter(
        user=request.user
    ).count()

    cart_count = Cart.objects.filter(
        user=request.user
    ).count()

    return render(
        request,
        "account.html",
        {
            "total_orders": total_orders,
            "wishlist_count": wishlist_count,
            "cart_count": cart_count,
        }
    )
@login_required
def order_details(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        "order_detail.html",
        {
            "order": order,
        }
    )
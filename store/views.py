from django.shortcuts import render, redirect
from .models import Product
import random


def index(request):
    products = Product.objects.all()
    return render(request, 'store/index.html', {'products': products})

def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    if 'cart' in request.session:
        cart = request.session['cart']
    else:
        cart = {}
    if product_id in cart:
        cart[product_id]['quantity'] += 1
    else:
        cart[product_id] = {'quantity': 1, 'name': product.name, 'price': float(product.price)}
    request.session['cart'] = cart
    return redirect('index')

def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for product_id, item in cart.items():
        total_price += item['quantity'] * item['price']
        cart_items.append({'product_id': product_id, 'name': item['name'], 'quantity': item['quantity'], 'price': item['price']})
    return render(request, 'store/cart.html', {'cart_items': cart_items, 'total_price': total_price})

def checkout(request):
    # Recupere os itens do carrinho da sessão
    cart = request.session.get('cart', {})
    cart_items = []

    # Lógica para processar os itens do carrinho e calcular o total
    total_price = 0
    for product_id, item_info in cart.items():
        try:
            # Recupere as informações detalhadas do produto do banco de dados com base no product_id
            product = Product.objects.get(pk=product_id)

            # Calcule o preço total deste item no carrinho
            item_total_price = item_info['quantity'] * product.price

            # Adicione as informações do item à lista de cart_items
            cart_items.append({
                'product_name': product.name,
                'quantity': item_info['quantity'],
                'price_per_item': product.price,
                'total_price_for_item': item_total_price,
            })

            # Atualize o preço total global
            total_price += item_total_price
        except Product.DoesNotExist:
            # Lidar com o caso em que o produto não existe
            continue

    # Verifique se o carrinho está vazio
    if not cart_items:
        return redirect('view_cart')

    # Lógica adicional para finalizar a compra, como processamento de pagamento, criação de pedido, etc.
    # Aqui você pode adicionar a lógica necessária para o seu projeto.

    # Limpe o carrinho após a finalização da compra
    request.session['cart'] = {}

    # Renderize a página de checkout com as informações do pedido
    return render(request, 'store/checkout.html', {'cart_items': cart_items, 'total_price': total_price})


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if product_id in cart:
        del cart[product_id]
        request.session['cart'] = cart
    return redirect('view_cart')


def clear_cart(request):
    request.session['cart'] = {}
    return redirect('view_cart')

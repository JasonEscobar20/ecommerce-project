from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse

from basket.basket import Basket
from store.models import Product

def basket_summary(request):
    basket = Basket(request)
    print(basket)
    return render(request, 'basket/summary.html', {'basket': basket})

def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productId'))
        product_qty = int(request.POST.get('productQty'))
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)
        basketqty = basket.__len__()
        response = JsonResponse({'qty': basketqty})
        return response
    
def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productId'))
        # product = get_object_or_404(Product, )
        basket.delete(product=product_id)
        basket_qty = basket.__len__()
        basket_total_price = basket.get_total_price()
        response = JsonResponse({'subtotal': basket_total_price, 'qty': basket_qty})
        return response
    
def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productId'))
        product_qty = int(request.POST.get('productQty'))
        basket.update(product=product_id, product_qty=product_qty)

        basket_qty = basket.__len__()
        basket_total_price = basket.get_total_price()
        response = JsonResponse({'qty': basket_qty, 'subtotal': basket_total_price})

        return response
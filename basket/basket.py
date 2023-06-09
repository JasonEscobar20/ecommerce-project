from decimal import Decimal
from store.models import Product


class Basket():
    """
    A basa Basket class, providing some default behaviors that can be inherited or overrided, as necesary
    """

    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        
        if 'skey' not in request.session:
            basket = self.session['skey'] = {}

        self.basket = basket

    def __iter__(self):
        """"
        Collect the product_id in the session data to query the database
        and return products
        """
        products_ids = self.basket.keys()
        products = Product.products.filter(id__in=products_ids)
        basket = self.basket.copy()

        for product in products:
            basket[str(product.id)]['product'] = product

        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item
    
    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        return sum(item['qty'] for item in self.basket.values())
    
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())
    
    def add(self, product, qty):
        """
        Adding and updating the users basket session data
        """
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]['qty'] = qty
        else:
            self.basket[product_id] = {
                'price': str(product.price),
                'qty': int(qty)
            }

        self.save()

    def delete(self, product):
        """
        Delete item from session data
        """

        product_id = str(product)
        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def update(self, product, product_qty):
        """
        Update values in session data
        """
        product_id = str(product)
        product_qty = product_qty
        
        if product_id in self.basket:
            self.basket[product_id]['qty'] = product_qty

        self.save()

    def save(self):
        self.session.modified = True
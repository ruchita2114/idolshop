from .models import Product

DEFAULT_SESSION_KEY = "cart"


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get(DEFAULT_SESSION_KEY)

        if self.cart is None:
            self.cart = {}
            self.session[DEFAULT_SESSION_KEY] = self.cart

    def add(self, product, quantity=1):
        product_id = str(product.id)

        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price),
            }

        self.cart[product_id]["quantity"] += quantity

        self.session[DEFAULT_SESSION_KEY] = self.cart
        self.session.modified = True

    def remove(self, product, quantity=1):
        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id]["quantity"] -= quantity

            if self.cart[product_id]["quantity"] <= 0:
                del self.cart[product_id]

            self.session[DEFAULT_SESSION_KEY] = self.cart
            self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            item = self.cart[str(product.id)]
            item["product"] = product
            item["price"] = float(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item
    def decrease(self, product, quantity=1):
        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id]["quantity"] -= quantity

            if self.cart[product_id]["quantity"] <= 0:
                del self.cart[product_id]

            self.session.modified = True
    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            float(item["price"]) * item["quantity"]
            for item in self.cart.values()
        )

    def clear(self):
        self.session[DEFAULT_SESSION_KEY] = {}
        self.session.modified = True
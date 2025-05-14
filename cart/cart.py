from django.conf import settings
from main.models import Product


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)

        if cart and isinstance(next(iter(cart.values())), int):
            cart = self._migrate_old_format(cart)

        self.cart = cart or {}

    def _migrate_old_format(self, old_cart):
        """Конвертирует старый формат корзины в новый"""
        new_cart = {}
        for slug, quantity in old_cart.items():
            try:
                product = Product.objects.get(slug=slug)
                new_cart[slug] = {
                    "quantity": quantity,
                    "price": float(product.sell_price()),
                }
            except Product.DoesNotExist:
                continue
        self.session[settings.CART_SESSION_ID] = new_cart
        return new_cart

    def get_total_price(self):
        total = 0
        for item in self.cart.values():
            try:
                # Явное преобразование типов
                price = float(item["price"])
                quantity = int(item["quantity"])
                total += price * quantity
            except (TypeError, ValueError, KeyError):
                # Обработка некорректных данных
                continue
        return round(total, 2)

    # Остальные методы остаются как в оригинале
    def __iter__(self):
        """Генерирует данные для шаблонов БЕЗ хранения объектов Product"""
        product_slugs = self.cart.keys()
        products = Product.objects.filter(slug__in=product_slugs)

        for product in products:
            item = self.cart[str(product.slug)]
            yield {
                "product": product,
                "quantity": item["quantity"],
                "total": item["price"] * item["quantity"],
                "price": item["price"],
                "image_url": (
                    product.image.url
                    if product.image
                    else "/static/images/no-image.png"
                ),
            }

    def save(self):
        self.session.modified = True

    def remove(self, product_slug):
        """Удаляет товар из корзины"""
        slug = str(product_slug)
        if slug in self.cart:
            del self.cart[slug]
            self.save()

    def clear(self):
        """
        Очищает корзину — удаляет все товары из сессии
        """
        self.session[settings.CART_SESSION_ID] = {}
        self.save()

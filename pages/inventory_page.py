class InventoryPage:

    # ─── PART 1: Init ───
    def __init__(self, page):
        self.page = page

        # All selectors in one place
        self.products        = page.locator(".inventory_item")
        self.cart_icon       = page.locator(".shopping_cart_link")
        self.cart_badge      = page.locator(".shopping_cart_badge")
        self.page_title      = page.locator(".title")

    # ─── PART 2: Actions ───

    def is_loaded(self):
        """Check if inventory page is loaded"""
        return "inventory" in self.page.url

    def get_product_count(self):
        """Return number of products on page"""
        return self.products.count()

    def get_page_title(self):
        """Return page heading text"""
        return self.page_title.text_content()

    def add_to_cart(self, product_name):
        """Add a specific product to cart by name"""
        # Convert product name to button ID format
        # "sauce labs backpack" → "add-to-cart-sauce-labs-backpack"
        button_id = "add-to-cart-" + product_name.lower().replace(" ", "-")
        self.page.locator(f"#{button_id}").click()
        print(f"✓ Added to cart: {product_name}")

    def get_cart_count(self):
        """Return number of items in cart"""
        if self.cart_badge.is_visible():
            return int(self.cart_badge.text_content())
        return 0

    def open_cart(self):
        """Click cart icon to open cart"""
        self.cart_icon.click()
        self.page.wait_for_load_state("networkidle")
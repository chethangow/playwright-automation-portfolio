class CartPage:

    # ─── PART 1: Init ───
    def __init__(self, page):
        self.page = page

        # All selectors in one place
        self.cart_items       = page.locator(".cart_item")
        self.checkout_button  = page.locator("#checkout")
        self.continue_button  = page.locator("#continue")
        self.finish_button    = page.locator("#finish")
        self.success_message  = page.locator(".complete-header")
        self.first_name       = page.locator("#first-name")
        self.last_name        = page.locator("#last-name")
        self.postal_code      = page.locator("#postal-code")

    # ─── PART 2: Actions ───

    def is_open(self):
        """Check if cart page is open"""
        return "cart" in self.page.url

    def get_item_count(self):
        """Return number of items in cart"""
        return self.cart_items.count()

    def start_checkout(self):
        """Click checkout button"""
        self.checkout_button.click()
        self.page.wait_for_load_state("networkidle")

    def fill_checkout_details(self, first, last, postal):
        """Fill checkout form"""
        self.first_name.fill(first)
        self.last_name.fill(last)
        self.postal_code.fill(postal)
        self.continue_button.click()
        self.page.wait_for_load_state("networkidle")

    def finish_order(self):
        """Click finish button"""
        self.finish_button.click()
        self.page.wait_for_load_state("networkidle")

    def get_success_message(self):
        """Return order success message"""
        return self.success_message.text_content()

    def is_order_complete(self):
        """Check if order was placed successfully"""
        return self.success_message.is_visible()
class LoginPage:

    # ─── PART 1: Init — store page + define selectors ───
    def __init__(self, page):
        self.page = page

        # All selectors defined in ONE place
        self.username_input = page.locator("#user-name")
        self.password_input = page.locator("#password")
        self.login_button   = page.locator("#login-button")
        self.error_message  = page.locator("[data-test='error']")

    # ─── PART 2: Actions — one method per user action ───

    def goto(self):
        """Navigate to login page"""
        self.page.goto("https://www.saucedemo.com")
        self.page.wait_for_load_state("networkidle")

    def login(self, username, password):
        """Fill credentials and click login"""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        self.page.wait_for_load_state("networkidle")

    def get_error_message(self):
        """Return error message text"""
        return self.error_message.text_content()

    def is_error_visible(self):
        """Check if error message is showing"""
        return self.error_message.is_visible()
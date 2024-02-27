import time

from framework.ui.element.Element import Element
from framework.ui.pages.LoginPage import LoginPage


class TestLogin:
    def test_login_to_trade_hub(self):
        (LoginPage()
         .go_to_login_page()
         .fill_username_input()
         .click_next_button()
         .fill_password_input()
         .click_login_button()
         .fill_mfa_code()
         .click_trade_hub_button())

    def test_is_page_loaded(self):
        time.sleep(10)
        assert Element.by_xpath("//div[contains(@class,'mui-grid-pagination')]").is_visible()

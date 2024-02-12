import os

from framework.ui.Page import Page
from framework.ui.element.Element import Element
from libs.python.mfa.mfa_authenticate import get_mfa_code


class LoginPage(Page):
    __PAGE_URL = os.getenv("LOGIN_URL")
    __USERNAME = os.getenv("LOGIN_USER")
    __PASSWORD = os.getenv("LOGIN_PASSWORD")

    username_input = Element.by_xpath("//input[@id='email']")
    password_input = Element.by_xpath("//input[@id='password']")
    next_button = Element.by_xpath(("//button[contains(@class,'btn red v-btn v-btn--is-elevated v-btn--has-bg "
                                      "theme--light v-size--default')]"))
    login_button = Element.by_xpath(
        ("//button[@class='btn red v-btn v-btn--is-elevated v-btn--has-bg theme--light v-size--default' "
         "and contains(., 'Sign in')]"))
    passcode_hint = Element.by_xpath("//*[contains(text(), 'Enter one-time passcode')]")
    mfa_code_input = Element.by_xpath("//input[@id='code']")
    mfa_verify_button = Element.by_xpath(
        ("//button[@class='btn red v-btn v-btn--is-elevated v-btn--has-bg theme--light "
         "v-size--default' and contains(., 'Verify')]"))
    mfa_used_text = Element.by_xpath("//*[contains(text(), 'Your software token has already been used once.')]")
    trade_hub_button = Element.by_xpath("(//span[contains(text(),'Trade Hub')])[2]")
    invalid_otp_error = Element.by_xpath(
        ("//div[@class='suberror' and (normalize-space(text())='Authenticator code you entered is "
         "incorrect.' or normalize-space(text())='Invalid session for the user, session is "
         "expired.' or normalize-space(text())='Your software token has already been used once.')]"))

    def go_to_login_page(self):
        self.open_page(LoginPage.__PAGE_URL)
        LoginPage.username_input.wait_for_visibility()
        return self

    def fill_username_input(self):
        LoginPage.username_input.send_keys(LoginPage.__USERNAME)
        return self

    def fill_password_input(self):
        LoginPage.password_input.send_keys(LoginPage.__PASSWORD)
        return self

    def click_next_button(self):
        LoginPage.next_button.wait_until_clickable()
        LoginPage.next_button.click()
        return self

    def click_login_button(self):
        LoginPage.login_button.wait_until_clickable()
        LoginPage.login_button.click()
        return self

    def click_verify_button(self):
        LoginPage.mfa_verify_button.click()
        return self

    def fill_mfa_code(self):
        mfa_code_input = LoginPage.mfa_code_input
        mfa_code_input.wait_for_visibility()
        mfa_code_input.clear_text()
        mfa_code_input.send_keys(get_mfa_code())
        self.click_verify_button()
        return self

    def click_trade_hub_button(self):
        LoginPage.trade_hub_button.wait_for_visibility(10)
        LoginPage.trade_hub_button.click()
        return self

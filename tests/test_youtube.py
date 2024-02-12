import time

from selenium.webdriver import Keys
from framework.ui.Page import Page
from framework.ui.element.Element import Element


class TestYoutube:
    def test_one(self):
        Page().open_page("http://www.youtube.com/")
        Element.by_xpath("//button[@class='yt-spec-button-shape-next yt-spec-button-shape-next--filled yt-spec-button-shape-next--mono yt-spec-button-shape-next--size-m']").click()
        time.sleep(2)
        search_bar = Element.by_xpath("//input[@id='search']")
        search_bar.key_down(Keys.SHIFT)
        search_bar.send_keys("sajkdhbkjasdsja")
        assert search_bar.get_value() == "sajkdhbkjasdsja".upper()

    def test_two(self):
        assert Element.by_xpath("//button[@class='yt-spec-button-shape-next yt-spec-button-shape-next--filled yt-spec-button-shape-next--mono yt-spec-button-shape-next--size-m']").is_present()

import os

from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from framework.ui.webdriver.WebDriverSingleton import WebDriverSingleton


class WrappedElement:

    __DEFAULT_TIME_OUT_SECONDS = float(os.getenv("DEFAULT_TIME_OUT_SECONDS"))

    __driver: WebDriver = WebDriverSingleton.get_driver()

    def __init__(self, by, locator, web_element: WebElement = None):
        self.__driver = WrappedElement.__driver
        self.__by = by
        self.__locator = locator
        self.__web_element = web_element

    # Actions

    def click(self):
        self.__get_web_driver_actions().click(self.wait_for_presence()).perform()

    def double_click(self):
        self.__get_web_driver_actions().double_click(self.wait_for_presence()).perform()

    def click_js(self):
        self.execute_javascript("arguments[0].click();", self.__get_web_element())

    def click_invisible_element(self):
        script: str = ("var object = arguments[0];var theEvent = document.createEvent(\"MouseEvent\");"
                       "theEvent.initMouseEvent(\"click\", true, true, window, 0, 0, 0, 0, 0, false, false, false, "
                       "false, 0, null);object.dispatchEvent(theEvent);")
        self.execute_javascript(script, self.__get_web_element())

    def mouse_over(self):
        self.__get_web_driver_actions().move_to_element(self.wait_for_presence()).perform()

    def mouse_down(self):
        self.__get_web_driver_actions().click_and_hold(self.wait_for_presence()).perform()

    def mouse_up(self):
        self.__get_web_driver_actions().release(self.wait_for_presence()).perform()

    def right_click(self):
        self.__get_web_driver_actions().context_click(self.wait_for_presence()).perform()

    def drag_and_drop_to_element(self, element: "WrappedElement"):
        self.__get_web_driver_actions().drag_and_drop(self.wait_for_presence(), element.wait_for_presence()).perform()

    def drag_and_drop_by_offset(self, xoffset: int, yoffset: int):
        self.__get_web_driver_actions().drag_and_drop_by_offset(self.wait_for_presence(), xoffset, yoffset).perform()

    def key_down(self, key: Keys):
        self.wait_for_presence()
        self.__get_web_driver_actions().key_down(str(key)).perform()

    def key_up(self, key: Keys):
        self.wait_for_presence()
        self.__get_web_driver_actions().key_up(str(key)).perform()

    def move_by_offset(self, xoffset: int, yoffset: int):
        self.wait_for_presence()
        self.__get_web_driver_actions().move_by_offset(xoffset, yoffset).perform()

    def move_to_element_with_offset(self, element: "WrappedElement", xoffset: int, yoffset: int):
        self.wait_for_presence()
        (self.__get_web_driver_actions().move_to_element_with_offset(element.wait_for_presence(), xoffset, yoffset)
         .perform())

    def scroll_by_offset(self, xoffset: int, yoffset: int):
        self.wait_for_presence()
        self.__get_web_driver_actions().scroll_by_amount(xoffset, yoffset).perform()

    def scroll_to_element(self, element: "WrappedElement"):
        self.wait_for_presence()
        self.__get_web_driver_actions().scroll_to_element(element.wait_for_presence()).perform()

    def clear_text(self):
        self.wait_for_presence()
        self.__get_web_element().clear()

    def send_keys(self, text: str):
        self.__get_web_driver_actions().send_keys_to_element(self.wait_for_presence(), text).perform()

    def switch_frame(self):
        self.__driver.switch_to.frame(self.__get_web_element())

    def execute_javascript(self, script, *args):
        return self.__driver.execute_script(script, *args)

    # Get data from element
    def get_attribute(self, attribute: str):
        return self.wait_for_presence().get_attribute(attribute)

    def get_text(self):
        return self.wait_for_presence().text

    def get_css_property(self, css_property: str):
        return self.wait_for_presence().value_of_css_property(css_property)

    def get_class_name(self):
        return self.get_attribute("class")

    def get_id(self):
        return self.get_attribute("id")

    def get_value(self):
        return self.get_attribute("value")

    def get_size(self) -> dict:
        return self.wait_for_presence().size

    def get_height(self):
        return self.get_size()["height"]

    def get_width(self):
        return self.get_size()["width"]

    # Check states

    def is_present(self) -> bool:
        try:
            self.__get_web_element()
            return True
        except NoSuchElementException:
            return False

    def is_visible(self) -> bool:
        return self.wait_for_presence().is_displayed()

    def is_clickable(self) -> bool:
        return self.wait_for_presence().is_enabled()

    def is_selected(self) -> bool:
        return self.wait_for_presence().is_selected()

    # Multiple elements

    def get_all_elements(self) -> list["WrappedElement"]:
        web_elements_list = self.__driver.find_elements(self.__get_element_by_and_locator())
        elements_list = []
        if len(web_elements_list) > 0:
            for web_element in web_elements_list:
                elements_list.append(WrappedElement(self.__by, self.__locator, web_element))
        return elements_list

    # Waits

    def wait_for_presence(self, timeout=__DEFAULT_TIME_OUT_SECONDS):
        return self.__get_web_driver_wait(timeout).until(
            ec.presence_of_element_located(self.__get_element_by_and_locator()))

    def wait_for_attribute_in_element(self, attribute: str, timeout=__DEFAULT_TIME_OUT_SECONDS):
        return self.__get_web_driver_wait(timeout).until(
            ec.element_attribute_to_include(self.__get_element_by_and_locator(), attribute))

    def wait_until_selected(self, timeout=__DEFAULT_TIME_OUT_SECONDS):
        return self.__get_web_driver_wait(timeout).until(
            ec.element_located_to_be_selected(self.__get_element_by_and_locator()))

    def wait_until_clickable(self, timeout=__DEFAULT_TIME_OUT_SECONDS):
        return self.__get_web_driver_wait(timeout).until(
            ec.element_to_be_clickable(self.__get_element_by_and_locator()))

    def wait_for_visibility(self, timeout=__DEFAULT_TIME_OUT_SECONDS):
        return self.__get_web_driver_wait(timeout).until(
            ec.visibility_of_element_located(self.__get_element_by_and_locator()))

    def wait_for_invisibility(self, timeout=__DEFAULT_TIME_OUT_SECONDS):
        return self.__get_web_driver_wait(timeout).until(
            ec.invisibility_of_element_located(self.__get_element_by_and_locator()))

    def wait_for_absence(self, timeout=__DEFAULT_TIME_OUT_SECONDS):
        return self.__get_web_driver_wait(timeout).until(
            ec.staleness_of(self.__get_web_element()))

    def wait_until_text_is_present(self, text: str, timeout=__DEFAULT_TIME_OUT_SECONDS):
        return self.__get_web_driver_wait(timeout).until(
            ec.text_to_be_present_in_element(self.__get_element_by_and_locator(), text))

    def wait_until_text_is_present_in_attribute(self, attribute: str, text: str, timeout=__DEFAULT_TIME_OUT_SECONDS):
        return self.__get_web_driver_wait(timeout).until(
            ec.text_to_be_present_in_element_attribute(self.__get_element_by_and_locator(), attribute, text))

    def wait_until_text_is_present_in_value(self, text: str, timeout=__DEFAULT_TIME_OUT_SECONDS):
        return self.__get_web_driver_wait(timeout).until(
            ec.text_to_be_present_in_element_value(self.__get_element_by_and_locator(), text))

    def wait_for_visibility_of_all_elements(self, timeout=__DEFAULT_TIME_OUT_SECONDS):
        return self.__get_web_driver_wait(timeout).until(
            ec.visibility_of_all_elements_located(self.__get_element_by_and_locator()))

    def wait_for_presence_of_all_elements(self, timeout=__DEFAULT_TIME_OUT_SECONDS):
        return self.__get_web_driver_wait(timeout).until(
            ec.presence_of_all_elements_located(self.__get_element_by_and_locator()))

    def wait_for_visibility_of_any_of_the_elements(self, timeout=__DEFAULT_TIME_OUT_SECONDS):
        return self.__get_web_driver_wait(timeout).until(
            ec.visibility_of_any_elements_located(self.__get_element_by_and_locator()))

    # WebDriver related
    def __get_web_element(self) -> WebElement:
        if self.__web_element is None:
            return self.__driver.find_element(self.__by, self.__locator)
        else:
            return self.__web_element

    def __get_web_driver_wait(self, timeout=__DEFAULT_TIME_OUT_SECONDS) -> WebDriverWait:
        return WebDriverWait(self.__driver, timeout)

    def __get_web_driver_actions(self) -> ActionChains:
        return ActionChains(self.__driver)

    def __get_element_by_and_locator(self) -> (str, str):
        return self.__by, self.__locator

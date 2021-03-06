from selenium.webdriver.common.keys import Keys
from unittest import skip

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    def test_cannot_add_empty_list_items(self):
        # User goes to the home page and accidentally tries to submit
        # an empty list item - hits Enter on the empty input box
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # The home page refreshes and there is an error message saying
        # that list items cannot be blank
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.invalid-feedback').text,
            "You can't have an empty list item"
        ))

        # User tries again with some text for the item, which now works
        self.get_item_input_box().send_keys('Buy milk')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Persistently, User tries to submit a second blank list item
        self.browser.get_item_input_box().send_keys(Keys.ENTER)

        # User recerives a similar warning on the list page
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.invalid-feedback').text,
            "You can't have an empty list item"
        ))

        # And finally User decides to correct it by filling some text in
        self.get_item_input_box().send_keys('Make tea')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')
        self.wait_for_row_in_list_table('2: Make tea')

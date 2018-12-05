from selenium.webdriver.common.keys import Keys
from unittest import skip

from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):
    @skip
    def test_cannot_add_empty_list_items(self):
        # User goes to the home page and accidentally tries to submit
        # an empty list item - hits Enter on the empty input box

        # The home page refreshes and there is an erroe message saying
        # that list items cannot be blank

        # User tries again with some text for the item, which not works

        # Persistently, User tries to submit a second blank list item

        # User recerives a similar warning on the list page

        # And finally User decides to correct it by filling some text in
        self.fail('write me later =(')

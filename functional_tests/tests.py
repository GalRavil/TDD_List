from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
    
    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_list_and_retrieve_it_later(self):
        # User1 checks home page
        self.browser.get(self.live_server_url)

        # User1 notices the page title and header mention To-Do lists
        self.assertIn('To-Do', self.browser.title)
        
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Invitation to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # User1 types "By item1" into a test box
        inputbox.send_keys('Buy item1')

        # When user1 hits enter, the page updates, amd now the page lists has:
        # "1: By item1"
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)
        self.check_for_row_in_list_table('1: Buy item1')

        # There is still a text box inviting to add another item.
        # User1 enters "By item2" 
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy item2')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, and now contains two items
        self.check_for_row_in_list_table('1: Buy item1')
        self.check_for_row_in_list_table('2: Buy item2')


        # Check the unique URL
        self.fail('Finish test after you sleep!')

        # User1 visits that URL to make sure the to-do list is still there
    
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import time


MAX_WAIT = 10


class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Chrome()
    
    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return 
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_list_for_one_user(self):
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
        self.wait_for_row_in_list_table('1: Buy item1')

        # There is still a text box inviting to add another item.
        # User1 enters "By item2" 
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy item2')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now contains two items
        self.wait_for_row_in_list_table('1: Buy item1')
        self.wait_for_row_in_list_table('2: Buy item2')


    def test_multiple_users_can_start_lists_at_different_urls(self):
        # User1 starts a new to-do list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy another stuff')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy another stuff')

        # Check the unique URL
        user1_list_url = self.browser.current_url
        self.assertRegex(user1_list_url, '/lists/.+')


        # Now a new user, User2, comes along to the site
        ## We use a new browser session to make sure no information
        ## of User1 is coming thought from cookies and etc
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # User2 visits the home page. There is no sign of User1's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy another stuff', page_text)
        self.assertNotIn('Buy item1', page_text)

        # User2 starts a new list by entering a new item
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # User2 gets his own unique URL
        user2_list_url = self.browser.current_url
        self.assertRegex(user2_list_url, '/lists/.+')
        self.assertNotEqual(user2_list_url, user1_list_url)

        # Again, there is no trace of User1's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy another stuff')
        self.assertIn('Buy milk', page_text)

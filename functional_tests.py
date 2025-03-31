from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time
from selenium.webdriver.common.by import By
class NewVisitorTest(unittest.TestCase):
    def setUp(self):
        #return super().setUp()
        self.browser=webdriver.Chrome()
    def tearDown(self):
        self.browser.quit()
    def test_case(self):
        #打开网页
        self.browser.get('http://localhost:8000')
        #检查标题是否有如下的内容
        self.assertIn('To-Do',self.browser.title,f"browser title was: {self.browser.title}")
        #检查头部包含'To-Do'
        header_text=self.browser.find_element(By.TAG_NAME,'h1').text
        self.assertIn('To-Do',header_text)

        #应用中有文本输入框
        inputbox=self.browser.find_element(By.ID,'id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),'Enter a to-do item')
        
        #输入"Buy flowers"
        inputbox.send_keys('Buy flowers')
        #回车后页面更新
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)
        #待办列表中新增1. Buy flowers
        table=self.browser.find_element(By.ID,'id_list_table')
        rows=table.find_elements(By.TAG_NAME,'tr')
        self.assertIn('1. Buy flowers',[row.text for row in rows])
        #继续输入文本"Give a gift to Lisi"
        inputbox=self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Give a gift to Lisi')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(2)
        #页面更新
        #新增列表
        table=self.browser.find_element(By.ID,'id_list_table')
        rows=table.find_elements(By.TAG_NAME,'tr')
        self.assertIn('1. Buy flowers',[row.text for row in rows])
        self.assertIn('2. Give a gift to Lisi',[row.text for row in rows])
        
        #网站为待办生成唯一的URL

        #访问URL，发现待办事项列表仍在
        #离开
        self.fail('Finish the test!')


if __name__=='__main__':
    unittest.main()
#browser=webdriver.Chrome()
#browser.get('http://localhost:8000')

#assert 'Django' in browser.page_source
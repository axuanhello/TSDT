from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException
MAX_WAIT=10
class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        #return super().setUp()
        self.browser=webdriver.Chrome()
    def tearDown(self):
        self.browser.quit()
    #def check_for_row_in_list_table(self,row_text):
    #    table=self.browser.find_element(By.ID,'id_list_table')
    #    rows=table.find_elements(By.TAG_NAME,'tr')
    #    self.assertIn(row_text,[row.text for row in rows])
    def wait_for_row_in_list_table(self,row_text):
        start_time=time.time()
        while True:
            try:
                table =self.browser.find_element(By.ID,'id_list_table')
                rows=table.find_elements(By.TAG_NAME,'tr')
                self.assertIn(row_text,[row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if(time.time()-start_time>MAX_WAIT):
                    raise
                time.sleep(0.5)
    def test_case(self):
        #打开网页
        self.browser.get(self.live_server_url)
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
        #time.sleep(1)
        #待办列表中新增1. Buy flowers
        #self.check_for_row_in_list_table('1. Buy flowers')
        self.wait_for_row_in_list_table('1. Buy flowers')
        #继续输入文本"Give a gift to Lisi"
        inputbox=self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Give a gift to Lisi')
        inputbox.send_keys(Keys.ENTER)
        #time.sleep(1)
        #页面更新
        #新增列表
        #self.check_for_row_in_list_table('1. Buy flowers')
        #self.check_for_row_in_list_table('2. Give a gift to Lisi')
        self.wait_for_row_in_list_table('1. Buy flowers')
        self.wait_for_row_in_list_table('2. Give a gift to Lisi')
        #网站为待办生成唯一的URL

        #访问URL，发现待办事项列表仍在
        #离开
        #self.fail('Finish the test!')

    def test_multiple_users(self):
        #张三新建一个待办事项清单
        self.browser.get(self.live_server_url)
        inputbox=self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Buy flowers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1. Buy flowers')
        #张三注意到清单有一个唯一的URL
        zhangsan_list_url=self.browser.current_url
        self.assertRegex(zhangsan_list_url,'/lists/.+')
        
        #新用户王五访问网站
        #使用新浏览器会话
        #确保张三的信息不会从cookie中泄露
        self.browser.quit()
        self.browser=webdriver.Chrome()
        #王五访问首页
        #首页中不会呈现张三的清单
        self.browser.get(self.live_server_url)
        page_text=self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Buy flowers',page_text)
        #self.assertNotIn('BGive agift to Lisa',page_text)
        #王五输入新待办事项，新建清单
        inputbox=self.browser.find_element(By.ID,'id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1. Buy milk')
        #王五获得了他唯一的URL
        wangwu_list_url=self.browser.current_url
        self.assertRegex(wangwu_list_url,'/lists/.+')
        self.assertNotEqual(wangwu_list_url,zhangsan_list_url)
        #该页面仍然无张三的清单
        page_text=self.browser.find_element(By.TAG_NAME,'body').text
        self.assertNotIn('Buy flowers',page_text)
        self.assertIn('Buy milk',page_text)
        #二人意满离，然后去睡觉了
    def test_layout_and_styling(self):
        #张三访问首页
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024,768)
        #他看到，输入框完美地、不可挑剔地、无与伦比地居中显示！
        inputbox=self.browser.find_element(By.ID,'id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x']+inputbox.size['width']/2,
            512,
            delta=10
        )
#if __name__=='__main__':
#    unittest.main()
#browser=webdriver.Chrome()
#browser.get('http://localhost:8000')

#assert 'Django' in browser.page_source
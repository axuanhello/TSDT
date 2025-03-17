from selenium import webdriver
import unittest
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
        self.fail('Finish the test!')

        #应用中有文本输入框
        #输入"Buy flowers"

        #页面更新
        #代办列表中新增1. Buy flowers

        #继续输入文本"Send a gift to Lisi"

        #页面更新
        #新增列表

        #网站为代办生成唯一的URL

        #访问URL，发现待办事项列表仍在
        #离开



if __name__=='__main__':
    unittest.main()
#browser=webdriver.Chrome()
#browser.get('http://localhost:8000')

#assert 'Django' in browser.page_source
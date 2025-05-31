
import unittest

from _08_unittest.login_func import login_func

class TestLogin(unittest.TestCase):

    '''夹子：准备前置数据等'''
    @classmethod
    def setUpClass(cls):
        print('i am setup')
        cls.class_value = 'i am class_value!!!'
    @classmethod
    def tearDownClass(cls):
        print('i am tearDown')

    # def setUp(self):
    #     print('i am setup')
    #     self.value = 'i am value!!!'
    # def tearDown(self):
    #     print('i am tearDown')


    # success case
    def test_success(self):
        # print(self.value)
        actual_res = login_func('admin','admin')
        expect_res = {'msg': 'login success'}
        self.assertEqual(expect_res,actual_res,'expect and actual is not euqal!!!')

        # success case
    def test_fail_username(self):
        actual_res = login_func('admin123','admin')
        expect_res = {'msg': 'login success'}
        self.assertEqual(expect_res,actual_res,'expect and actual is not euqal!!!')
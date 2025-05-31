
import unittest
from unittestreport import TestRunner
from _08_unittest.test_login import TestLogin

# instantiation
suite = unittest.TestSuite()
loader = unittest.TestLoader()

'''loader add'''
# tests = loader.discover("_08_unittest")      # search directory，match 【test*.py】
# print(tests)


'''manual add'''
# suite.addTest(TestLogin('test_success'))
# suite.addTest(TestLogin('test_fail_username'))
# print(suite)

# suite.addTests([TestLogin('test_success'),TestLogin('test_fail_username')])
# print(suite)



'''report'''
tests = loader.discover("_08_unittest")      # search directory，match 【test*.py】
runner = TestRunner(tests)
runner.run()

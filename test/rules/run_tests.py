# -*- coding:utf-8 -*-

"""
规则系统测试运行器
运行所有单元测试和集成测试
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))


def run_tests():
	loader = unittest.TestLoader()
	start_dir = os.path.dirname(__file__)
	suite = loader.discover(start_dir, pattern='test_*.py')
	
	runner = unittest.TextTestRunner(verbosity=2)
	result = runner.run(suite)
	
	return result.wasSuccessful()


if __name__ == '__main__':
	print("=" * 60)
	print("规则系统测试套件")
	print("=" * 60)
	
	success = run_tests()
	
	print("\n" + "=" * 60)
	if success:
		print("✓ 所有测试通过！")
		print("=" * 60)
		sys.exit(0)
	else:
		print("✗ 测试失败！")
		print("=" * 60)
		sys.exit(1)
# -*- coding:utf-8 -*-


class Singleton(object):
	instance = None

	def __new__(cls, *args, **kwargs):
		if cls.instance is None:
			cls.instance = object.__new__(cls)
		return cls.instance

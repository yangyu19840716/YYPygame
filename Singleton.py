# -*- coding:utf-8 -*-


class Singleton(object):
    instance = None

    def __new__(cls, *args, **kw):
        if cls.instance is None:
            cls.instance = object.__new__(cls, *args, **kw)
        return cls.instance

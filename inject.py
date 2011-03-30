def inject(cls, static=False, name=None):
    def _builtin_hack(name):
        import ctypes as c

        _get_dict = c.pythonapi._PyObject_GetDictPtr
        _get_dict.restype = c.POINTER(c.py_object)
        _get_dict.argtypes = [c.py_object]

        return _get_dict(name).contents.value

    def wrap(method):
        name_ = name or method.func_name
        method = staticmethod(method) if static else method
        try:
            setattr(cls, name_, method)
        except:
            _builtin_hack(cls)[name_] = method

    return wrap


# for fun, instead of 'test'.upper, let's use 'test.up() :D
inject(str, name='up')(lambda self: self.upper())

print 'test'.up()

# for fun, let's add an extend method to {}

@inject(dict)
def extend(self, new_dict):
    return dict(self, **new_dict)

print {'a':2}.extend({'b':3})





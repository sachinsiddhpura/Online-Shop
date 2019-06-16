import unittest
import datetime
import time
from Orders import Orders
import types
import juspay


def tab(text):
    count = 0
    output = ""
    text = text.split('\n')
    for line in text:
        if '}' in line:
            count -= 1
        i = 0
        while i < count:
            output += '\t'
            i += 1
        if '{' in line:
            count += 1
        output += line
        output += '\n'
    return output


def var_dump(obj, depth=4, l=""):

    non_null_dict = {}
    if depth<0: return repr(obj)
    if isinstance(obj, dict):
        objdict = obj
    else:
        canprint=lambda o:isinstance(o, (int, float, str, unicode, bool, types.NoneType, types.LambdaType))
        try:
            if canprint(obj) or sum(not canprint(o) for o in obj) == 0: return repr(obj)
        except TypeError, e:
            pass
        try:
            return "[\n" + "\n".join(l + var_dump(k, depth=depth-1, l=l+"  ") + "," for k in obj) + "\n" + l + "]"
        except TypeError, e:
            name = (hasattr(obj, '__class__') and obj.__class__.__name__ or type(obj).__name__)
            objdict = {}
            for a in dir(obj):
                if a[:2] != "__" and (not hasattr(obj, a) or not hasattr(getattr(obj, a), '__call__')):
                    if a == a.lower():
                        try: objdict[a] = getattr(obj, a)
                        except Exception, e: objdict[a] = str(e)
    name = (hasattr(obj, '__class__') and obj.__class__.__name__ or type(obj).__name__)
    for k,v in objdict.iteritems():
        if v is not None and v != '':
            non_null_dict[k]=v
    return "\n<" + name + ">" + "\n{\n" + "\n".join(l + repr(k) + ": " + var_dump(v, depth=depth-1) + "," for k, v in non_null_dict.iteritems()) + "\n" + l + "}\n"


class Test(unittest.TestCase):

    juspay.api_key = '4168A8A476B84DBCAF409C24F379BAC5'
    juspay.environment = 'production'

    def setUp(self):
        self.timestamp = int(time.mktime(datetime.datetime.timetuple(datetime.datetime.now())))

    def test__orders(self):

        # Test for list
        order_list = Orders.list()
        self.assertIsNotNone(order_list)
        for order in order_list['list']:
            self.assertIsInstance(order, Orders.Order)
        print tab(var_dump(order_list,3))

if __name__ == '__main__':
    unittest.main()

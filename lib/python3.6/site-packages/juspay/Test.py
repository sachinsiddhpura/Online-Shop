import unittest
import datetime
import time
from Cards import Cards
from Orders import Orders
from Payments import Payments
import types
import juspay
from pprint import pprint


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

        self.order1 = Orders.create(order_id=self.timestamp, amount=1000)
        self.assertIsInstance(self.order1, Orders.Order)
        self.assertEqual(self.order1.status, "CREATED")
        self.order2 = Orders.create(order_id=self.timestamp + 1, amount=1000)

    def test__orders(self):

        # Test for get_status
        status = Orders.status(order_id=self.timestamp)
        self.assertIsInstance(status, Orders.Order)
        self.assertEqual(float(status.order_id), self.timestamp)
        #print tab(var_dump(status, 1))

        # Test for list
        order_list = Orders.list()
        self.assertIsNotNone(order_list)
        for order in order_list['list']:
            self.assertIsInstance(order, Orders.Order)
        #print tab(var_dump(order_list,2))

        # Test for update
        updated_order = Orders.update(order_id=self.timestamp, amount=500)
        status = Orders.status(order_id=self.timestamp)
        self.assertEqual(status.amount, updated_order.amount)
        #print tab(var_dump(updated_order))

        # Test for payment links
        self.assertIsNotNone(order.payment_links)


    def test__refund(self):
        # Test for refund
        refunded_order = Orders.refund(unique_request_id=self.timestamp,order_id=1465833326,amount=10)
        self.assertIsNotNone(refunded_order)
        #print tab(var_dump(refunded_order))

    @staticmethod
    def delete_all_cards():
        card_list = Cards.list(customer_id='user')
        for card in card_list:
            Cards.delete(card_token=card.token)

    def test__cards(self):

        # Test for add
        card = Cards.create(merchant_id='shreyas', customer_id="user", customer_email='abc@xyz.com',
                                card_number=str(int(self.timestamp)*(10**6)), card_exp_year='20', card_exp_month='12')
        self.assertIsNotNone(card.reference)
        self.assertIsNotNone(card.token)
        self.assertIsNotNone(card.fingerprint)
        #print tab(var_dump(card))

        # Test for delete
        deleted_card = Cards.delete(card_token=card.token)
        self.assertTrue(deleted_card.deleted)
        #print tab(var_dump(deleted_card))

        # Test for list
        Test.delete_all_cards()
        Cards.create(merchant_id='shreyas', customer_id="user", customer_email='abc@xyz.com',
                         card_number=str(int(self.timestamp) * (10 ** 6)), card_exp_year='20', card_exp_month='12')
        Cards.create(merchant_id='shreyas', customer_id="user", customer_email='abc@xyz.com',
                         card_number=str((int(self.timestamp)+1) * (10 ** 6)), card_exp_year='20', card_exp_month='12')
        card_list = Cards.list(customer_id='user')
        self.assertIsNotNone(card_list)
        self.assertEqual(len(card_list), 2)
        #print tab(var_dump(card_list))
        Test.delete_all_cards()

    def test__payments(self):

        # Test for create_card_payment
        payment = Payments.create_card_payment(order_id=1465893617,
                                                      merchant_id='juspay_recharge',
                                                      payment_method_type='CARD',
                                                      card_token='68d6b0c6-6e77-473f-a05c-b460ef983fd8',
                                                      redirect_after_payment=False,
                                                      format='json',
                                                      card_number='5243681100075285',
                                                      name_on_card='Customer',
                                                      card_exp_year='20',
                                                      card_exp_month='12', card_security_code='123',
                                                      save_to_locker=False)
        self.assertIsNotNone(payment.txn_id)
        self.assertEqual(payment.status, 'PENDING_VBV')
        #print tab(var_dump(payment))

        # Test for create_net_banking_payment
        payment = Payments.create_net_banking_payment(order_id=1465893617,
                                                             merchant_id='juspay_recharge',
                                                             payment_method_type='NB',
                                                             payment_method='NB_ICICI',
                                                             redirect_after_payment=False,
                                                             format='json')
        self.assertIsNotNone(payment.txn_id)
        self.assertEqual(payment.status, 'PENDING_VBV')
        #print tab(var_dump(payment))


if __name__ == '__main__':
    unittest.main()

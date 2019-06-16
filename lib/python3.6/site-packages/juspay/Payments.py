import util
import sys


class Payments:

    def __init__(self):
        return

    class Transaction:

        class Payment:

            def __init__(self, kwargs):
                auth = Payments.Transaction.Payment.Authentication(util.get_arg(kwargs, 'authentication'))
                self.authentication = auth

            class Authentication:

                def __init__(self, kwargs):
                    self.method = util.get_arg(kwargs, 'method')
                    self.url = util.get_arg(kwargs, 'url')
                    self.params = util.get_arg(kwargs, 'params')

        def __init__(self, kwargs):
            self.order_id = util.get_arg(kwargs, 'order_id')
            self.txn_id = util.get_arg(kwargs, 'txn_id')
            self.status = util.get_arg(kwargs, 'status')
            self.payment = Payments.Transaction.Payment(util.get_arg(kwargs, 'payment'))

    class PaymentMethod:

        def __init__(self, kwargs):
            self.payment_method_type = util.get_arg(kwargs, 'payment_method_type')
            self.payment_method = util.get_arg(kwargs, 'payment_method')
            self.description = util.get_arg(kwargs, 'description')

    @staticmethod
    def create_card_payment(**kwargs):
        method = 'POST'
        url = '/txns'
        parameters = {
            'payment_method_type' : 'CARD',
            'format' : 'json'
        }

        # required_args checks for presence of necessary parameters
        required_args = {}
        for key in ['order_id', 'merchant_id', 'card_token', 'card_number', 'name_on_card',
                    'card_exp_year', 'card_exp_month', 'card_security_code', 'save_to_locker', 'redirect_after_payment']:
            required_args[key] = False

        for key, value in kwargs.iteritems():
            parameters[key] = value
            required_args[key] = True

        # Either token or card number validation
        if required_args['card_token'] == False and next((True for val in ['card_number', 'name_on_card',
                    'card_exp_year','card_exp_month', 'card_security_code'] if required_args[val] == False), False):
            raise Exception('Either [card_token] or [card_number, name_on_card, card_exp_year, card_exp_month, card_security_code] are required arguments for Payments.create_card_payment()\n')

        # Warn user about missing necessary parameters
        for key in ['order_id', 'merchant_id', 'save_to_locker', 'redirect_after_payment']:
            if required_args[key] is False:
                raise Exception('%s is a required argument for Payments.create_card_payment()\n' % key)

        # Warn user about unhandled parameters
        for key in parameters:
            if key not in ['order_id', 'merchant_id', 'payment_method_type', 'payment_method', 'card_token',
                           'name_on_card',
                           'card_number', 'card_exp_year', 'card_exp_month', 'card_security_code', 'save_to_locker',
                           'redirect_after_payment', 'format']:
                sys.stderr.write('%s not a valid argument for Payments.create_card_payment()\n' % key)

        # Type checks
        for key, value in kwargs.iteritems():
            if key == 'save_to_locker':
                if type(parameters['save_to_locker']) is not bool:
                    sys.stderr.write('save_to_locker should be of type bool\n')
            if key == 'redirect_after_payment':
                if type(parameters['redirect_after_payment']) is not bool:
                    sys.stderr.write('redirect_after_payment should be of type bool\n')

        response = util.request(method, url, parameters).json()
        payment = Payments.Transaction(response)
        return payment

    @staticmethod
    def create_net_banking_payment(**kwargs):
        method = 'POST'
        url = '/txns'
        parameters = {
            'payment_method_type' : 'NB',
            'format' : 'json'
        }

        # required_args checks for presence of necessary parameters
        required_args = {}
        for key in ['order_id', 'merchant_id', 'payment_method', 'redirect_after_payment']:
            required_args[key] = False

        for key, value in kwargs.iteritems():
            parameters[key] = value
            required_args[key] = True

        # Warn user about missing necessary parameters
        for key in ['order_id', 'merchant_id', 'payment_method', 'redirect_after_payment']:
            if required_args[key] is False:
                raise Exception('%s is a required argument for Payments.create_net_banking_payment()\n' % key)

        # Warn user about unhandled parameters
        for key in parameters:
            if key not in ['order_id', 'merchant_id', 'payment_method_type', 'payment_method', 'redirect_after_payment',
                           'format']:
                sys.stderr.write('%s not a valid argument for Payments.create_net_banking_payment()\n' % key)

        response = util.request(method, url, parameters).json()
        payment = Payments.Transaction(response)
        return payment

    @staticmethod
    def create_wallet_payment(**kwargs):
        method = 'POST'
        url = '/txns'
        parameters = {
            'payment_method_type' : 'WALLET',
            'format' : 'json'
        }

        # required_args checks for presence of necessary parameters
        required_args = {}
        for key in ['order_id', 'merchant_id', 'payment_method', 'redirect_after_payment']:
            required_args[key] = False

        for key, value in kwargs.iteritems():
            parameters[key] = value
            required_args[key] = True

        # Warn user about missing necessary parameters
        for key in ['order_id', 'merchant_id', 'payment_method', 'redirect_after_payment']:
            if required_args[key] is False:
                raise Exception('%s is a required argument for Payments.create_wallet_payment()\n' % key)

        # Warn user about unhandled parameters
        for key in parameters:
            if key not in ['order_id', 'merchant_id', 'payment_method', 'payment_method_type', 'redirect_after_payment', 'format', 'direct_wallet_token']:
                sys.stderr.write('%s not a valid argument for Payments.create_wallet_payment()\n' % key)

        # Type checks
        for key, value in kwargs.iteritems():
            if key == 'redirect_after_payment':
                if type(parameters['redirect_after_payment']) is not bool:
                    sys.stderr.write('redirect_after_payment should be of type bool\n')

        response = util.request(method, url, parameters).json()
        payment = Payments.Transaction(response)
        return payment

    @staticmethod
    def get_payment_methods(**kwargs):
        merchant_id = util.get_arg(kwargs,'merchant_id')
        if merchant_id is None:
            raise util.InvalidArguementException('`merchant_id` is a required argument for Payments.get_payment_methods()\n')

        method = 'GET'
        url = '/merchants/%s/paymentmethods' % (merchant_id)

        response = util.request(method, url, {}).json()
        response = util.get_arg(response,'payment_methods')
        payment_methods = []
        if response is not None:
            for payment_method in response:
                payment_method = Payments.PaymentMethod(payment_method)
                payment_methods.append(payment_method)
        return payment_methods

from . import util
from .JuspayException import InvalidArguementException

class Wallets:

    def __init__(self):
        return 

    class Wallet:

        def __init__(self, kwargs):
            self.id = util.get_arg(kwargs, 'id')
            self.object = util.get_arg(kwargs, 'object')
            self.wallet = util.get_arg(kwargs, 'wallet')
            self.token = util.get_arg(kwargs, 'token')
            self.linked = util.get_arg(kwargs, 'linked')
            self.current_balance = util.get_arg(kwargs, 'current_balance')
            self.last_refreshed = util.get_arg(kwargs, 'last_refreshed')

    @staticmethod
    def create(**kwargs):
        customer_id = util.get_arg(kwargs,'customer_id')
        gateway = util.get_arg(kwargs,'gateway')
        if customer_id is None or gateway is None:
            raise InvalidArguementException('`customer_id` & `gateway` are required arguments for Wallets.create()\n')

        method = 'POST'
        url = '/customers/%s/wallets' % (customer_id)

        response = util.request(method, url, kwargs).json()
        wallet = Wallets.Wallet(response)
        return wallet

    @staticmethod
    def create_and_authenticate(**kwargs):
        customer_id = util.get_arg(kwargs,'customer_id')
        gateway = util.get_arg(kwargs,'gateway')
        if customer_id is None or gateway is None:
            raise InvalidArguementException('`customer_id` & `gateway` are required arguments for '
                                            'Wallets.create_and_authenticate()\n')

        method = 'POST'
        url = '/customers/%s/wallets' % (customer_id)
        kwargs['command'] = 'authenticate'

        response = util.request(method, url, kwargs).json()
        wallet = Wallets.Wallet(response)
        return wallet

    @staticmethod
    def list(**kwargs):
        customer_id= util.get_arg(kwargs,'customer_id')
        order_id = util.get_arg(kwargs,'order_id')

        if customer_id is None and order_id is None:
            raise InvalidArguementException('`customer_id` or `order_id` is a required argument for Wallets.list()\n')

        method = 'GET'
        if customer_id is not None:
            url = '/customers/%s/wallets' % (customer_id)
        else:
            url = '/orders/%s/wallets' % (order_id)

        response = util.request(method, url, {}).json()
        response = util.get_arg(response,'list')
        wallets = []
        if response is not None:
            for wallet in response:
                wallet = Wallets.Wallet(wallet)
                wallets.append(wallet) 
        return wallets

    @staticmethod
    def refreshBalance(**kwargs):
        customer_id = util.get_arg(kwargs,'customer_id')
        if customer_id is None:
            raise InvalidArguementException('`customer_id` is a required argument for Wallets.refreshBalance()\n')

        method = 'GET'
        url = '/customers/%s/wallets/refresh-balances' % (customer_id)

        response = util.request(method, url, {}).json()
        response = util.get_arg(response,'list')
        wallets = []
        if response is not None:
            for wallet in response:
                wallet = Wallets.Wallet(wallet)
                wallets.append(wallet) 
        return wallets

    @staticmethod
    def authenticate(**kwargs):
        wallet_id = util.get_arg(kwargs,'wallet_id')
        if wallet_id is None:
            raise InvalidArguementException('`wallet_id` is a required argument for Wallets.authenticate()\n')

        method = 'POST'
        url = '/wallets/%s' % (wallet_id)
        parameters = {
            'command' : 'authenticate'
        }
        response = util.request(method, url, parameters).json()
        wallet = Wallets.Wallet(response)
        return wallet

    @staticmethod
    def refresh_by_wallet_id(**kwargs):
        wallet_id = util.get_arg(kwargs,'wallet_id')
        if wallet_id is None:
            raise InvalidArguementException('`wallet_id` is a required argument for Wallets.refresh()\n')

        method = 'GET'
        url = '/wallets/%s' % (wallet_id)
        parameters = {
            'command' : 'refresh'
        }
        response = util.request(method, url, parameters).json()
        wallet = Wallets.Wallet(response)
        return wallet

    @staticmethod
    def link(**kwargs):
        wallet_id = util.get_arg(kwargs,'wallet_id')
        otp = util.get_arg(kwargs,'otp')
        if wallet_id is None or otp is None:
            raise InvalidArguementException('`wallet_id` & `otp` are required arguments for Wallets.link()\n')

        method = 'POST'
        url = '/wallets/%s' % (wallet_id)
        kwargs['command'] = 'link'
        response = util.request(method, url, kwargs).json()
        wallet = Wallets.Wallet(response)
        return wallet

    @staticmethod
    def delink(**kwargs):
        wallet_id = util.get_arg(kwargs,'wallet_id')
        if wallet_id is None:
            raise InvalidArguementException('`wallet_id` is a required argument for Wallets.delink()\n')

        method = 'POST'
        url = '/wallets/%s' % (wallet_id)
        parameters = {
            'command' : 'delink'
        }
        response = util.request(method, url, parameters).json()
        wallet = Wallets.Wallet(response)
        return wallet

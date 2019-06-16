from . import util
import sys
from .JuspayException import InvalidArguementException

class Cards:

    def __init__(self):
        return

    class Card:

        def __init__(self, kwargs):
            self.name = util.get_arg(kwargs, 'name_on_card')
            self.exp_year = util.get_arg(kwargs, 'card_exp_year')
            self.reference = util.get_arg(kwargs, 'card_reference')
            self.exp_month = util.get_arg(kwargs, 'card_exp_month')
            self.expired = util.get_arg(kwargs, 'expired')
            self.fingerprint = util.get_arg(kwargs, 'card_fingerprint')
            self.isin = util.get_arg(kwargs, 'card_isin')
            self.type = util.get_arg(kwargs, 'card_type')
            self.issuer = util.get_arg(kwargs, 'card_issuer')
            self.brand = util.get_arg(kwargs, 'card_brand')
            self.token = util.get_arg(kwargs, 'card_token')
            self.nickname = util.get_arg(kwargs, 'nickname')
            self.number = util.get_arg(kwargs, 'card_number')
            self.deleted = util.get_arg(kwargs, 'deleted')

    @staticmethod
    def create(**kwargs):
        if kwargs is None or len(kwargs) == 0:
            raise InvalidArguementException()

        method = 'POST'
        url = '/card/add'
        response = util.request(method, url, kwargs).json()
        card = Cards.Card(response)
        return card

    @staticmethod
    def list(**kwargs):
        customer_id = util.get_arg(kwargs,'customer_id')
        if customer_id is None:
            raise InvalidArguementException('`customer_id` is a required argument for Cards.list()\n')

        method = 'GET'
        url = '/card/list'
        response = util.request(method, url, kwargs).json()
        response = util.get_arg(response,'cards')
        cards = []
        if response is not None:
            for card in response:
                card = Cards.Card(card)
                cards.append(card)
        return cards

    @staticmethod
    def delete(**kwargs):
        card_token = util.get_arg(kwargs,'card_token')
        if card_token is None:
            raise InvalidArguementException('`card_token` is a required argument for Cards.delete()\n')

        method = 'POST'
        url = '/card/delete'
        response = util.request(method, url, kwargs).json()
        card = Cards.Card(response)
        return card

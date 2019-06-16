from . import util
import sys
from .Cards import Cards
from .JuspayException import InvalidArguementException


class Orders:

    def __init__(self):
        return

    all_input_params = ['order_id', 'amount', 'currency', 'customer_id', 'customer_email', 'customer_phone',
                        'description', 'product_id', 'gateway_id', 'return_url', 'billing_address_first_name',
                        'billing_address_last_name', 'billing_address_line1', 'billing_address_line2',
                        'billing_address_line3', 'billing_address_city', 'billing_address_state',
                        'billing_address_country', 'billing_address_postal_code', 'billing_address_phone',
                        'billing_address_country_code_iso', 'shipping_address_first_name',
                        'shipping_address_last_name', 'shipping_address_line1', 'shipping_address_line2',
                        'shipping_address_line3', 'shipping_address_city', 'shipping_address_state',
                        'shipping_address_country', 'shipping_address_postal_code', 'shipping_address_phone',
                        'shipping_address_country_code_iso', 'udf1', 'udf2', 'udf3', 'udf4', 'udf5', 'udf6', 'udf7',
                        'udf8', 'udf9', 'udf10']

    class Order:

        class Address:

            def __init__(self, address_type, kwargs):
                self.type = address_type
                self.first_name = util.get_arg(kwargs, self.type + '_address_first_name')
                self.last_name = util.get_arg(kwargs, self.type + '_address_last_name')
                self.line1 = util.get_arg(kwargs, self.type + '_address_line1')
                self.line2 = util.get_arg(kwargs, self.type + '_address_line2')
                self.line3 = util.get_arg(kwargs, self.type + '_address_line3')
                self.city = util.get_arg(kwargs, self.type + '_address_city')
                self.state = util.get_arg(kwargs, self.type + '_address_state')
                self.country = util.get_arg(kwargs, self.type + '_address_country')
                self.postal_code = util.get_arg(kwargs, self.type + '_address_postal_code')
                self.phone = util.get_arg(kwargs, self.type + '_address_phone')
                self.country_code_iso = util.get_arg(kwargs, self.type + '_address_country_code_iso')

        class Refund:

                def __init__(self, kwargs):
                    self.id = util.get_arg(kwargs, 'refund_id')
                    self.ref = util.get_arg(kwargs, 'ref')
                    self.amount = util.get_arg(kwargs, 'amount')
                    self.created = util.get_arg(kwargs, 'created')
                    self.status = util.get_arg(kwargs, 'status')

        class GatewayResponse:

                def __init__(self, kwargs):
                    self.rrn = util.get_arg(kwargs, 'rrn')
                    self.epg_txn_id = util.get_arg(kwargs, 'epg_txn_id')
                    self.auth_id_code = util.get_arg(kwargs, 'auth_id_code')
                    self.txn_id = util.get_arg(kwargs, 'txn_id')
                    self.resp_code = util.get_arg(kwargs, 'resp_code')
                    self.resp_message = util.get_arg(kwargs, 'resp_message')

        class PaymentLink:
                def __init__(self, kwargs):
                    self.web = util.get_arg(kwargs, 'web')
                    self.mobile = util.get_arg(kwargs, 'mobile')
                    self.iframe = util.get_arg(kwargs, 'iframe')

        def __init__(self, kwargs):

            if util.check_param(kwargs,'billing_address'):
                billing_address = Orders.Order.Address("billing", kwargs)
            else:
                billing_address = None
            if util.check_param(kwargs,'shipping_address'):
                shipping_address = Orders.Order.Address("shipping", kwargs)
            else:
                shipping_address = None
            if util.get_arg(kwargs, 'card') is not None:
                card = Cards.Card(util.get_arg(kwargs, 'card'))
            else:
                card = None
            if util.get_arg(kwargs, 'payment_gateway_response') is not None:
                gateway_response = Orders.Order.GatewayResponse(util.get_arg(kwargs, 'payment_gateway_response'))
            else:
                gateway_response = None
            if 'refunds' in kwargs:
                refunds = []
                for refund in kwargs['refunds']:
                    refund_obj = Orders.Order.Refund(refund)
                    refunds.append(refund_obj)
            else:
                refunds = None

            self.id = util.get_arg(kwargs, 'id')
            self.merchant_id = util.get_arg(kwargs, 'merchant_id')
            self.order_id = util.get_arg(kwargs, 'order_id')
            self.status = util.get_arg(kwargs, 'status')
            self.status_id = util.get_arg(kwargs, 'status_id')
            self.amount = util.get_arg(kwargs, 'amount')
            self.currency = util.get_arg(kwargs, 'currency')
            self.customer_id = util.get_arg(kwargs, 'customer_id')
            self.customer_email = util.get_arg(kwargs, 'customer_email')
            self.customer_phone = util.get_arg(kwargs, 'customer_phone')
            self.product_id = util.get_arg(kwargs, 'product_id')
            self.return_url = util.get_arg(kwargs, 'return_url')
            self.description = util.get_arg(kwargs, 'description')
            self.billing_address = billing_address
            self.shipping_address = shipping_address
            self.udf1 = util.get_arg(kwargs, 'udf1')
            self.udf2 = util.get_arg(kwargs, 'udf2')
            self.udf3 = util.get_arg(kwargs, 'udf3')
            self.udf4 = util.get_arg(kwargs, 'udf4')
            self.udf5 = util.get_arg(kwargs, 'udf5')
            self.udf6 = util.get_arg(kwargs, 'udf6')
            self.udf7 = util.get_arg(kwargs, 'udf7')
            self.udf8 = util.get_arg(kwargs, 'udf8')
            self.udf9 = util.get_arg(kwargs, 'udf9')
            self.udf10 = util.get_arg(kwargs, 'udf10')
            self.txn_id = util.get_arg(kwargs, 'txn_id')
            self.gateway_id = util.get_arg(kwargs, 'gateway_id')
            self.bank_error_code = util.get_arg(kwargs, 'bank_error_code')
            self.bank_error_message = util.get_arg(kwargs, 'bank_error_message')
            self.refunded = util.get_arg(kwargs, 'refunded')
            self.amount_refunded = util.get_arg(kwargs, 'amount_refunded')
            self.payment_method_type = util.get_arg(kwargs, 'payment_method_type')
            self.payment_method = util.get_arg(kwargs, 'payment_method')
            self.card = card
            self.gateway_response = gateway_response
            self.refunds = refunds
            self.payment_links = Orders.Order.PaymentLink(kwargs['payment_links'])

    @staticmethod
    def create(**kwargs):
        order = util.get_arg(kwargs,'order_id')
        if order is None:
            raise InvalidArguementException('`order_id` is a required argument for Order.create()\n')

        method = 'POST'
        url = '/order/create'
        response = util.request(method, url, kwargs).json()
        order = Orders.Order(response)
        return order

    @staticmethod
    def status(**kwargs):
        order = util.get_arg(kwargs,'order_id')
        if order is None:
            raise InvalidArguementException('`order_id` is a required argument for Order.status()\n')

        method = 'GET'
        url = '/order/status'
        response = util.request(method, url, kwargs).json()
        order = Orders.Order(response)
        return order

    @staticmethod
    def list(**kwargs):
        method = 'GET'
        url = '/order/list'

        response = util.request(method, url, kwargs or {}).json()
        returned_list = []
        for order in response['list']:
            order = Orders.Order(order)
            returned_list.append(order)
        order_list_response = {'count' : response['count'],
                               'offset': response['offset'],
                               'total' : response['total'],
                               'list' :returned_list}
        return order_list_response

    @staticmethod
    def update(**kwargs):
        order_id = util.get_arg(kwargs,'order_id')
        if order_id is None:
            raise InvalidArguementException('`order_id` is a required argument for Order.update()\n')

        method = 'POST'
        url = '/order/create'
        response = util.request(method, url, kwargs).json()
        order = Orders.Order(response)
        return order

    @staticmethod
    def refund(**kwargs):
        order_id = util.get_arg(kwargs,'order_id')
        unique_request_id = util.get_arg(kwargs, 'unique_request_id')
        if order_id is None or unique_request_id is None:
            raise InvalidArguementException('`order_id` & `unique_request_id` is a required argument for Order.refund()\n')

        method = 'POST'
        url = '/order/refund'
        response = util.request(method, url, kwargs).json()
        order = Orders.Order(response)
        return order

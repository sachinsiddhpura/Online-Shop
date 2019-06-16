import util
import sys

from JuspayException import InvalidArguementException

class Customers:

    def __init__(self):
        return

    class Customer:

        def __init__(self, kwargs):
            self.id = util.get_arg(kwargs, 'id')
            self.object = util.get_arg(kwargs, 'object')
            self.date_created = util.get_arg(kwargs, 'date_created')
            self.last_updated = util.get_arg(kwargs, 'last_updated')
            self.email_address = util.get_arg(kwargs, 'email_address')
            self.first_name = util.get_arg(kwargs, 'first_name')
            self.last_name = util.get_arg(kwargs, 'last_name')
            self.mobile_country_code = util.get_arg(kwargs, 'mobile_country_code')
            self.mobile_number = util.get_arg(kwargs, 'mobile_number')
            self.object_reference_id = util.get_arg(kwargs, 'object_reference_id')

    @staticmethod
    def create(**kwargs):
        if kwargs is None or len(kwargs) == 0:
            raise InvalidArguementException()

        method = 'POST'
        url = '/customers'
        response = util.request(method, url, kwargs).json()
        customer = Customers.Customer(response)
        return customer

    @staticmethod
    def list(**kwargs):
        method = 'GET'
        url = '/customers'
    	offset = util.get_arg(kwargs,'offset')
    	count = util.get_arg(kwargs,'count')

    	if count is None and offset is None:
            sys.stderr.write('`count` & `offset` can be passed if required.\n')

        response = util.request(method, url, kwargs or {}).json()
        response_list = util.get_arg(response,'list')
        customers_list = []
        customer_list_response = {}
        if response is not None:
            for customer in response_list:
                customer = Customers.Customer(customer)
                customers_list.append(customer)
            customer_list_response = {
                'count' : response['count'],
                'offset': response['offset'],
                'total' : response['total'],
                'list' :customers_list
            }
        return customer_list_response

    @staticmethod
    def get(**kwargs):
        id = util.get_arg(kwargs,'id')

        if id is None:
            raise InvalidArguementException(message='`id` is a required argument for Customers.list()\n')

        method = 'GET'
        url = '/customers/%s' % (id)

        response = util.request(method, url, kwargs).json()
        customer = Customers.Customer(response)
        return customer

    @staticmethod
    def update(**kwargs):
        id = util.get_arg(kwargs,'id')

        if id is None:
            raise InvalidArguementException(message='`id` is a required argument for Customers.update()\n')

        method = 'POST'
        url = '/customers/%s' % (id)

        response = util.request(method, url, kwargs).json()
        customer = Customers.Customer(response)
        return customer

    @staticmethod
    def delete(**kwargs):
        raise NotImplementedError()

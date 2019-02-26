#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import socket
import urllib
import hashlib
import requests

from .exceptions import RequiredField


class NicePayV1(object):
    """
    Docs: https://docs.nicepay.co.id/api-v1-EN.html

    nicepay = NicePayV1()
    nicepay.api_url = 'https://docs.nicepay.co.id/foobar.egg'
    nicepay.api_notification_url = 'https://foobar.baz'
    nicepay.api_key = 'xxx-xxx-xxx'
    nicepay.imid = 'xxx-xxx-xxx'
    nicepay.get_*stuff()
    """
    api_notification_url = ''
    api_callback_url = ''
    api_url = None
    api_key = None
    imid = None

    def __init__(self):
        self.merchant_token = None

    def __repr__(self):
        return '%s(merchant_token="%s")' % (self.__class__.__name__, self.merchant_token)

    def send(self, to_json=True, **kwargs):
        if not all([self.api_url, self.api_key, self.imid]):
            message = 'Please fill all `api_url`, `api_key` and `imid`'
            raise RequiredField(message)

        response_data = {}
        response_data['merchant_token'] = kwargs.get('merchantToken')
        response_data['baskets'] = kwargs.get('baskets')

        if 'baskets' in kwargs:
            del kwargs['baskets']

        params = urllib.parse.urlencode(kwargs)
        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        response = requests.post(self.api_url, headers=headers, params=params)
        response_data['status_code'] = response.status_code

        if to_json:
            response = json.loads(response.text[4:])
            response_data.update(**response)
        else:
            response_data['content'] = response.content

        return response_data

    @property
    def get_client_ip(self):
        return socket.gethostbyname(socket.gethostname())

    def check_required_fields(self, required_fields, exist_fields):
        for field in required_fields:
            if field not in exist_fields:
                raise RequiredField('Field `%s` is required!' % field)

    def get_merchant_token(self, **kwargs):
        required_fields = ['referenceNo', 'amt']
        exist_fields = kwargs.keys()
        self.check_required_fields(required_fields, exist_fields)

        token = '%s%s%s%s' % (self.imid, kwargs['referenceNo'],
                              kwargs['amt'], self.api_key)
        return hashlib.sha256(token.encode('ascii')).hexdigest()

    def request_credit_card(self, **kwargs):
        """
        https://docs.nicepay.co.id/api-v1-EN.html?python#credit-card

        request_data = {
            'currency': 'IDR',
            'amt': '10000',
            'instmntType': '1',
            'instmntMon': '1',
            'referenceNo': 'IV02318',
            'goodsNm': 'IV02318',
            'billingNm': 'John Doe',
            'billingPhone': '02112345678',
            'billingEmail': 'foobar@mail.com',
            'billingAddr': "Jl. Jend. Sudirman No. 28",
            'billingCity': "Jakarta Pusat",
            'billingState': "DKI Jakarta",
            'billingPostCd': "10210",
            'billingCountry': "Indonesia",
            'description': 'Payment Of Ref IV02318',
            'cartData': '{}'
        }
        nicepay.request_credit_card(**request_data)
        """
        required_fields = ['currency', 'amt', 'instmntType', 'instmntMon',
                           'referenceNo',  'goodsNm', 'billingNm', 'billingPhone',
                           'billingEmail', 'billingCity',  'billingState', 'billingPostCd',
                           'billingCountry', 'description', 'cartData']
        request_data = {}
        request_data.update(**kwargs)
        request_data['iMid'] = self.imid
        request_data['payMethod'] = '01'
        request_data['instmntType'] = kwargs.get('instmntType', '1')
        request_data['instmntMon'] = kwargs.get('instmntMon', '1')
        request_data['callBackUrl'] = self.api_callback_url
        request_data['dbProcessUrl'] = self.api_notification_url
        request_data['merchantToken'] = self.get_merchant_token(**request_data)
        request_data['userIP'] = kwargs.get('userIP') or self.get_client_ip

        return self.send(**request_data)

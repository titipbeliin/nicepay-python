#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import socket
import hashlib
import requests


class RequiredField(Exception):
    pass


class NicePay(object):
    """
    Docs: https://docs.nicepay.co.id

    nicepay = NicePay()
    nicepay.api_url = 'https://docs.nicepay.co.id/foobar.egg'
    nicepay.api_notification_url = 'https://foobar.baz'
    nicepay.api_key = 'xxx-xxx-xxx'
    nicepay.imid = 'xxx-xxx-xxx'
    nicepay.get_*stuff()
    """
    api_notification_url = ''
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

        headers = {'Accept': 'application/json',
                   'Content-Type': 'application/json'}
        response = requests.post(self.api_url, headers=headers,
                                 data=json.dumps(kwargs))
        response_data = {}

        if to_json:
            response_data = response.json()
            response_data['status_code'] = response.status_code
        else:
            response_data['content'] = response.content
            response_data['status_code'] = response.status_code
        return response_data

    @property
    def get_client_ip(self):
        return socket.gethostbyname(socket.gethostname())

    def check_required_fields(self, required_fields, exist_fields):
        for field in required_fields:
            if field not in exist_fields:
                raise RequiredField('Field `%s` is required!' % field)

    def get_merchant_token(self, **kwargs):
        required_fields = ['timeStamp', 'referenceNo', 'amt']
        exist_fields = kwargs.keys()
        self.check_required_fields(required_fields, exist_fields)

        token = '%s%s%s%s%s' % (kwargs['timeStamp'], self.imid,
                                kwargs['referenceNo'], kwargs['amt'],
                                self.api_key)
        return hashlib.sha256(token.encode('ascii')).hexdigest()

    def request_registration(self, **kwargs):
        """
        request_data = {
            'userIP': '192.168.23.87',                # or None
            'timeStamp': '20180109181300',
            'payMethod': '02',
            'currency': 'IDR',
            'amt': '10000',
            'referenceNo': 'ADETEST02',
            'goodsNm': 'ADEJULIANTO2',
            'billingNm': 'ADETEST01',
            'billingPhone': '08123456789',
            'billingEmail': 'ADETEST01@GMAIL.COM',
            'billingCity': 'JAKARTA',
            'billingState': 'JAKARTA',
            'billingPostCd': '14350',
            'billingCountry': 'INDONESIA',
            'cartData': '{}'
        }
        nicepay.request_registration(**request_data)
        """
        required_fields = ['timeStamp', 'payMethod', 'currency', 'amt',
                           'referenceNo', 'goodsNm', 'billingNm', 'billingPhone',
                           'billingEmail', 'billingCity', 'billingState',
                           'billingPostCd', 'billingCountry', 'cartData']
        exist_fields = kwargs.keys()
        self.check_required_fields(required_fields, exist_fields)

        request_data = {}
        request_data.update(**kwargs)
        request_data['iMid'] = self.imid
        request_data['dbProcessUrl'] = self.api_notification_url
        request_data['merchantToken'] = self.get_merchant_token(**request_data)
        request_data['userIP'] = kwargs.get('userIP') or self.get_client_ip

        return self.send(**request_data)

    def request_inquiry(self, **kwargs):
        """
        request_data = {'timeStamp': '20180109181300',
                        'tXid': 'IONPAYTEST02201801121146555531',
                        'referenceNo': 'ADETEST02',
                        'amt': '10000'}
        nicepay.request_inquiry(**request_data)
        """
        required_fields = ['timeStamp', 'referenceNo', 'amt']
        exist_fields = kwargs.keys()
        self.check_required_fields(required_fields, exist_fields)

        token = self.get_merchant_token(timeStamp=kwargs['timeStamp'],
                                        referenceNo=kwargs['referenceNo'],
                                        amt=kwargs['amt'])

        # first assign into self mode
        self.merchant_token = token

        request_data = {}
        request_data.update(**kwargs)
        request_data['iMid'] = self.imid
        request_data['merchantToken'] = token

        return self.send(**request_data)

    def request_cancel(self, **kwargs):
        """
        request_data = {'timeStamp': '20180109181300',
                        'tXid': 'IONPAYTEST02201801121146555531',
                        'payMethod': '02',
                        'cancelType': '01',
                        'amt': '10000',
                        'preauthToken': ''}
        nicepay.request_cancel(**request_data)
        """
        required_fields = ['timeStamp', 'payMethod', 'tXid', 'cancelType', 'amt']
        exist_fields = kwargs.keys()
        self.check_required_fields(required_fields, exist_fields)

        token_cancel = '%s%s%s%s%s' % (kwargs['timeStamp'], self.imid, kwargs['tXid'],
                                       kwargs['amt'], self.api_key)
        token_cancel = hashlib.sha256(token_cancel.encode('ascii')).hexdigest()

        request_data = {}
        request_data.update(**kwargs)
        request_data['iMid'] = self.imid
        request_data['merchantToken'] = token_cancel

        return self.send(**request_data)

    def request_payment(self, **kwargs):
        """
        request_data = {
            'timeStamp': '20180109181300',
            'tXid': 'IONPAYTEST02201802051512483907',  # get tXid from register first
            'cardNo': '5409120028181901',
            'cardExpYymm': '2012',                     # format Yymm
            'cardCvv': '111',
            'recurringToken': '',
            'preauthToken': '',
            'clickPayNo': '',
            'dataField3': '',
            'clickPayToken': '',
            'merchantToken': '52a5c5bd8020xxxxxx',
            'callBackUrl': '20180109181300'
        }
        nicepay.request_payment(**request_data)
        """
        required_fields = ['timeStamp', 'tXid', 'cardNo',
                           'cardExpYymm', 'cardCvv']
        exist_fields = kwargs.keys()
        self.check_required_fields(required_fields, exist_fields)

        request_data = {}
        request_data.update(**kwargs)
        request_data['callBackUrl'] = kwargs.get('callBackUrl') or kwargs['timeStamp']

        return self.send(to_json=False, **request_data)

    def request_installment_info(self, **kwargs):
        """
        request_data = {'timeStamp': '20180109181300',
                        'merchantToken': '52a5c5bd8020xxxxxx',
                        'cardBin': '406810'}
        nicepay.request_installment_info(**request_data)
        """
        required_fields = ['timeStamp', 'merchantToken', 'cardBin']
        exist_fields = kwargs.keys()
        self.check_required_fields(required_fields, exist_fields)

        request_data = {}
        request_data.update(**kwargs)
        request_data['iMid'] = self.imid

        return self.send(**request_data)

    def request_vacct_inquiry(self, **kwargs):
        """
        request_data = {
            'vacctNo': '1146555531',
            'startDt': '20180101',
            'endDt': '20180111'
        }
        nicepay.request_vacct_inquiry(**request_data)
        """
        required_fields = ['vacctNo', 'startDt']
        exist_fields = kwargs.keys()
        self.check_required_fields(required_fields, exist_fields)

        token_vacct = '%s%s%s%s' % (self.imid, kwargs['vacctNo'],
                                    kwargs['startDt'], self.api_key)
        token_vacct = hashlib.sha256(token_vacct.encode('ascii')).hexdigest()

        request_data = {}
        request_data.update(**kwargs)
        request_data['iMid'] = self.imid
        request_data['merchantToken'] = token_vacct

        return self.send(**request_data)

    def request_vacct_inquiry_customer(self, **kwargs):
        """
        request_data = {'customerId': '70003507',
                        'startDt': '20180110',
                        'endDt': '20180111'}
        nicepay.request_vacct_inquiry_customer(**request_data)
        """
        required_fields = ['customerId', 'startDt']
        exist_fields = kwargs.keys()
        self.check_required_fields(required_fields, exist_fields)

        token_customer = '%s%s%s%s' % (self.imid, kwargs['customerId'],
                                       kwargs['startDt'], self.api_key)
        token_customer = hashlib.sha256(token_customer.encode('ascii')).hexdigest()

        request_data = {}
        request_data.update(**kwargs)
        request_data['iMid'] = self.imid
        request_data['merchantToken'] = token_customer

        return self.send(**request_data)

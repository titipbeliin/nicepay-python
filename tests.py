#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import unittest

from nicepay.nicepay import NicePay


class NicePayV2TestCase(unittest.TestCase):
    show_print = False

    def setUp(self):
        nicepay = NicePay()
        nicepay.api_url = None
        nicepay.api_notification_url = 'http://127.0.0.1:8000/nicepay/test3/dbProcess.do'
        nicepay.api_key = '33F49GnCMS1mFYlGXisbUDzVf2ATWCl9k3R++d5hDd3Frmuos/XLx8XhXpe+LDYAbpGKZYSwtlyyLOtS/8aD7A=='
        nicepay.imid = 'IONPAYTEST'

        self.nicepay = nicepay

        self.registration_url = 'https://api.nicepay.co.id/nicepay/direct/v2/registration'
        self.inquiry_url = 'https://api.nicepay.co.id/nicepay/direct/v2/inquiry'
        self.cancel_url = 'https://api.nicepay.co.id/nicepay/direct/v2/cancel'
        self.payment_url = 'https://api.nicepay.co.id/nicepay/direct/v2/payment'
        self.installment_url = 'https://api.nicepay.co.id/nicepay/direct/v2/instInfoInquiry'
        self.vacct_inquiry_url = 'https://api.nicepay.co.id/nicepay/api/vacctInquiry.do'
        self.vacct_inquiry_customer_url = 'https://api.nicepay.co.id/nicepay/api/vacctCustomerIdInquiry.do'

    def test_registration(self):
        request_data = {
            'timeStamp': '20180109181300',
            'payMethod': '02',
            'bankCd': 'BMRI',
            'vacctValidDt': '20180112',
            'vacctValidTm': '235959',
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
            'cartData': '{"count": "1","item": [{"img_url": "https://www.lecs.com/image/introduction/img_vmd020101.jpg","goods_name": "Jam Tangan Army","goods_detail": "jumlah 1","goods_amt": "400"}]}'
        }
        self.nicepay.api_url = self.registration_url
        response = self.nicepay.request_registration(**request_data)
        if self.show_print:
            print(response)
        self.assertTrue(isinstance(response, dict))

    def test_inquiry(self):
        request_data = {'timeStamp': '20180109181300',
                        'tXid': 'IONPAYTEST02201801121146555531',
                        'referenceNo': 'ADETEST02',
                        'amt': '10000'}
        self.nicepay.api_url = self.inquiry_url
        response = self.nicepay.request_inquiry(**request_data)
        if self.show_print:
            print(response)
        self.assertTrue(isinstance(response, dict))

    def test_cancel(self):
        request_data = {'timeStamp': '20180109181300',
                        'tXid': 'IONPAYTEST02201801121146555531',
                        'payMethod': '02',
                        'cancelType': '01',
                        'amt': '10000',
                        'preauthToken': ''}
        self.nicepay.api_url = self.cancel_url
        response = self.nicepay.request_cancel(**request_data)
        if self.show_print:
            print(response)
        self.assertTrue(isinstance(response, dict))

    def test_payment(self):
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
            'merchantToken': '52a5c5bd8020e809e3dd01b603f0b9ec89dc4c084d5392763b5bb2f690d074c7',
            'callBackUrl': '20180109181300'
        }
        self.nicepay.api_url = self.payment_url
        response = self.nicepay.request_payment(**request_data)
        if self.show_print:
            print(response)
        self.assertTrue(isinstance(response, dict))

    def test_installment(self):
        request_data = {'timeStamp': '20180109181300',
                        'merchantToken': '52a5c5bd8020e809e3dd01b603f0b9ec89dc4c084d5392763b5bb2f690d074c7',
                        'cardBin': '406810'}
        self.nicepay.api_url = self.installment_url
        response = self.nicepay.request_installment_info(**request_data)
        if self.show_print:
            print(response)
        self.assertTrue(isinstance(response, dict))

    def test_vacct_inquiry(self):
        request_data = {'vacctNo': '1146555531',
                        'startDt': '20180101',
                        'endDt': '20180111'}
        self.nicepay.api_url = self.vacct_inquiry_url
        response = self.nicepay.request_vacct_inquiry(**request_data)
        if self.show_print:
            print(response)
        self.assertTrue(isinstance(response, dict))

    def test_vacct_customer_inquiry(self):
        request_data = {'customerId': '70003507',
                        'startDt': '20180110',
                        'endDt': '20180111'}
        self.nicepay.api_url = self.vacct_inquiry_customer_url
        response = self.nicepay.request_vacct_inquiry_customer(**request_data)
        if self.show_print:
            print(response)
        self.assertTrue(isinstance(response, dict))

    def test_vacct_customer_inquiry(self):
        request_data = {'customerId': '70003507',
                        'startDt': '20180110',
                        'endDt': '20180111'}
        self.nicepay.api_url = self.vacct_inquiry_customer_url
        response = self.nicepay.request_vacct_inquiry_customer(**request_data)
        if self.show_print:
            print(response)
        self.assertTrue(isinstance(response, dict))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        NicePayV2TestCase.show_print = sys.argv.pop()
    unittest.main()

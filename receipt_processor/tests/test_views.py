from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from ..models import *
from ..serializer import *
import json

# Testing POST and GET api's and also testing each rule inside our POST api
class TestViews(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.posturl = reverse('process')
    
    # Check weather the api can handle valid and invalid recipts, also check if points are calculated correctly
    def test_post_api_with_receipt(self):
        valid_receipt = {
            "retailer": "Test Retailer",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {"shortDescription": "Test Item 1", "price": "10.00"},
                {"shortDescription": "Test Item 2", "price": "5.00"},
            ],
            "total": "15.00"
        }
        invalid_receipt = {
            "retailer": "Test Retailer",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "total": "15.00"
        }

        valid_response = self.client.post(self.posturl, valid_receipt, format='json')
        invalid_response = self.client.post(self.posturl, invalid_receipt, format='json')
        
        self.assertEqual(valid_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(invalid_response.status_code, status.HTTP_400_BAD_REQUEST)

        receipt = Receipt.objects.get()
        self.assertEqual(receipt.points, 98)  

    # Here on check all rules are functioning as intended.
    # For each rule these tests will send a POST request with values that are correct for only that rule. Then we check the points to make sure our logic is correct
    def test_post_api_rule1(self):
        test_receipt = {
            "retailer": "Test Retailer",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "13:01",
            "items": [
                {"shortDescription": "Test Item 1", "price": "10.00"},
            ],
            "total": "15.01"
        }

        response = self.client.post(self.posturl, test_receipt, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        receipt = Receipt.objects.get()
        self.assertEqual(receipt.points, 12)        # 12 len of chars in retailer


    def test_post_api_rule2(self):
        test_receipt = {
            "retailer": "#@#$!",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "13:01",
            "items": [
                {"shortDescription": "Test Item 1", "price": "10.00"},
            ],
            "total": "10.00"
        }

        response = self.client.post(self.posturl, test_receipt, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        receipt = Receipt.objects.get()
        self.assertEqual(receipt.points, 75)        # 75 because 50 + 25 (R2+R3)

    
    def test_post_api_rule3(self):
        test_receipt = {
            "retailer": "#@#$!",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "13:01",
            "items": [
                {"shortDescription": "Test Item 1", "price": "10.00"},
            ],
            "total": "12.25"
        }

        response = self.client.post(self.posturl, test_receipt, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        receipt = Receipt.objects.get()
        self.assertEqual(receipt.points, 25)        # 12.25 is divisible by .25 so 25 points


    def test_post_api_rule4(self):
        test_receipt = {
            "retailer": "#@#$!",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "13:01",
            "items": [
                {"shortDescription": "Test Item 1", "price": "10.00"},
                {"shortDescription": "Test Item 1", "price": "10.00"},
            ],
            "total": "1.51"
        }

        response = self.client.post(self.posturl, test_receipt, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        receipt = Receipt.objects.get()
        self.assertEqual(receipt.points, 5)         # 2 items in the list so 5 points
    

    def test_post_api_rule5(self):
        test_receipt = {
            "retailer": "#@#$!",
            "purchaseDate": "2022-01-02",
            "purchaseTime": "13:01",
            "items": [
                {"shortDescription": "Test Item 1a", "price": "10.00"},
            ],
            "total": "1.51"
        }

        response = self.client.post(self.posturl, test_receipt, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        receipt = Receipt.objects.get()
        self.assertEqual(receipt.points, 2)         # item desc is multiple of 3 so 10*0.2==2
    

    def test_post_api_rule6(self):
        test_receipt = {
            "retailer": "#@#$!",
            "purchaseDate": "2022-01-03",
            "purchaseTime": "13:01",
            "items": [
                {"shortDescription": "Test Item 1", "price": "10.00"},
            ],
            "total": "1.51"
        }

        response = self.client.post(self.posturl, test_receipt, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        receipt = Receipt.objects.get()
        self.assertEqual(receipt.points, 6) 

    
    def test_post_api_rule6(self):
        test_receipt = {
            "retailer": "#@#$!",
            "purchaseDate": "2022-01-12",
            "purchaseTime": "14:01",
            "items": [
                {"shortDescription": "Test Item 1", "price": "10.00"},
            ],
            "total": "1.51"
        }

        response = self.client.post(self.posturl, test_receipt, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        receipt = Receipt.objects.get()
        self.assertEqual(receipt.points, 10)

    # Check if our GET api returns correct points for a valid receipt
    def test_get_api(self):
        test_receipt = {
            "retailer": "Test Retailer",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {"shortDescription": "Test Item 1", "price": "10.00"},
                {"shortDescription": "Test Item 2", "price": "5.00"},
            ],
            "total": "15.00"
        }

        self.client.post(self.posturl, test_receipt, format='json')
        receipt = Receipt.objects.get()
        url = reverse('retrive', args=[receipt.id])
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['points'], 98)
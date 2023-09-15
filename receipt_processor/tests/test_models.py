from django.test import TestCase
from ..models import *
from decimal import Decimal
from datetime import date, time

# Check if the receipts are being created successfully
class TestModels(TestCase):

    def test_receipt_creation(self):
        receipt = Receipt.objects.create(
            retailer="Test Retailer",
            purchaseDate=date(2022, 1, 1),
            purchaseTime=time(13, 1),
            total=Decimal('15.00'),
            points=0                            
        )

        self.assertEqual(receipt.retailer, "Test Retailer")
        self.assertEqual(receipt.purchaseDate, date(2022, 1, 1))
        self.assertEqual(receipt.purchaseTime, time(13, 1))
        self.assertEqual(receipt.total, Decimal('15.00'))
        self.assertEqual(receipt.points, 0)


    def test_item_creation(self):
        receipt = Receipt.objects.create(
            retailer="Test Retailer",
            purchaseDate=date(2022, 1, 1),
            purchaseTime=time(13, 1),
            total=Decimal('15.00'),
            points=0
        )

        # Creating test items related to the receipt
        item1 = Items.objects.create(
            receipt=receipt,
            shortDescription=" Item desc 1",
            price=Decimal('10.00')
        )
        item2 = Items.objects.create(
            receipt=receipt,
            shortDescription="Item desc 2",
            price=Decimal('5.00')
        )

        self.assertEqual(item1.receipt, receipt)
        self.assertEqual(item1.shortDescription, " Item desc 1")
        self.assertEqual(item1.price, Decimal('10.00'))

        self.assertEqual(item2.receipt, receipt)
        self.assertEqual(item2.shortDescription, "Item desc 2")
        self.assertEqual(item2.price, Decimal('5.00'))
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from receipt_processor.views import *

# Testing weather each URL is mapped to intended views
class TestUrls(SimpleTestCase):

    def test_process_url_is_resolved(self):
        url = reverse('process')
        self.assertEquals(resolve(url).func, processReceipt)
    
    def test_retrive_url_is_resolved(self):
        url = reverse('retrive', args=['some-slug'])
        self.assertEquals(resolve(url).func, getPoints)
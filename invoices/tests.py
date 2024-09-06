from rest_framework.test import APITestCase
from rest_framework import status
from .models import Invoice, InvoiceDetail

class InvoiceAPITestCase(APITestCase):
    def setUp(self):
        self.invoice = Invoice.objects.create(date='2024-01-01', customer_name='Pushpendra Maurya')

    def test_get_invoices(self):
        response = self.client.get('/api/invoices/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invoice_detail(self):
        response = self.client.get(f'/api/invoices/{self.invoice.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_invoice(self):
        data = {'date': '2024-02-01', 'customer_name': 'Jane Doe'}
        response = self.client.post('/api/invoices/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 2)

    def test_update_invoice(self):
        data = {'date': '2024-03-01', 'customer_name': 'Updated Name'}
        response = self.client.put(f'/api/invoices/{self.invoice.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.invoice.refresh_from_db()
        self.assertEqual(self.invoice.customer_name, 'Updated Name')

    def test_delete_invoice(self):
        response = self.client.delete(f'/api/invoices/{self.invoice.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Invoice.objects.count(), 0)

class InvoiceDetailAPITestCase(APITestCase):
    def setUp(self):
        self.invoice = Invoice.objects.create(date='2024-01-01', customer_name='Pushpendra Maurya')

    def test_create_invoice_detail(self):
        data = {'invoice': self.invoice.id, 'description': 'Product A', 'quantity': 2, 'unit_price': 10.0, 'price': 20.0}
        response = self.client.post('/api/invoice_details/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InvoiceDetail.objects.count(), 1)

    def test_update_invoice_detail(self):
        invoice_detail = InvoiceDetail.objects.create(invoice=self.invoice, description='Product B', quantity=3, unit_price=15.0, price=45.0)
        data = {'description': 'Updated Product B', 'quantity': 4, 'unit_price': 18.0, 'price': 72.0}
        response = self.client.put(f'/api/invoice_details/{invoice_detail.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        invoice_detail.refresh_from_db()
        self.assertEqual(invoice_detail.description, 'Updated Product B')

    def test_delete_invoice_detail(self):
        invoice_detail = InvoiceDetail.objects.create(invoice=self.invoice, description='Product C', quantity=1, unit_price=25.0, price=25.0)
        response = self.client.delete(f'/api/invoice_details/{invoice_detail.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(InvoiceDetail.objects.count(), 0)
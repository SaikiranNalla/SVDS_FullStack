from django.db import models


class Orders(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

    date = models.DateField()

    # Vehicle details
    vehicle_number = models.CharField(max_length=50)
    vehicle_charge = models.IntegerField()

    # consignment details
    transit_from = models.CharField(max_length=255)
    transit_to = models.CharField(max_length=255)
    consignor = models.CharField(max_length=100)
    consignee = models.CharField(max_length=100)
    value = models.IntegerField()
    packages = models.IntegerField()
    description = models.TextField(blank=True)
    eway_bill = models.CharField(max_length=100)
    consignment_invoice = models.CharField(max_length=100)
    actual_weight = models.IntegerField()
    charged_weight = models.IntegerField()
    freight_charges = models.IntegerField(default=0)

    # bill specific
    invoice_number = models.CharField(max_length=50, blank=True)
    other_charges = models.IntegerField(default=0)
    total_charge = models.IntegerField(default=0)

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Order {self.id} - {self.status.title()}"
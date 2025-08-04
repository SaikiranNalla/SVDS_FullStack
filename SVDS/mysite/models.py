from django.db import models
import string
from django.contrib.auth.models import User

# Characters for base‑36: 0–9 then A–Z
LETTER_SEQ = string.ascii_uppercase            # 'A'..'Z'
MAX_LETTER_COUNT = len(LETTER_SEQ) * 1000      # 26 * 1000 = 26000 codes
MAX_NUMERIC = 10000                            # 0000..9999


class Orders(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('paid', 'Paid')
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
    consignment_value = models.IntegerField()
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
    svds_bill_no = models.CharField(
        max_length=4,
        unique=True,
        editable=False,
        blank=True,
        help_text="Auto‑generated 4‑char alphanumeric bill number"
    )

    # predefined choices
    delivery_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS, default='pending')

    def _next_bill(self, last: str) -> str:
        """
        Given the last code, returns the next in sequence:
        A000…A999→B000…Z999→0000…9999→0000…
        """
        # Letter‑first block
        if len(last) == 4 and last[0].isalpha() and last[1:].isdigit():
            letter = last[0]
            num = int(last[1:])
            if num < 999:
                return f"{letter}{num + 1:03d}"
            else:
                # move to next letter
                idx = LETTER_SEQ.index(letter)
                if idx < len(LETTER_SEQ) - 1:
                    return f"{LETTER_SEQ[idx + 1]}000"
                else:
                    # exhausted A000–Z999, jump to numeric block
                    return "0000"

        # Numeric‑only block
        if len(last) == 4 and last.isdigit():
            num = int(last)
            if num < MAX_NUMERIC - 1:
                return f"{num + 1:04d}"
            else:
                # wrap around
                return "0000"

        # Fallback (shouldn't happen)
        return "A000"

    def save(self, *args, **kwargs):
        # On first save, generate the next svds_bill_no
        if not self.svds_bill_no:
            # grab the highest existing code in lexicographic order
            last = Orders.objects.order_by('-svds_bill_no').first()
            if last and last.svds_bill_no:
                self.svds_bill_no = self._next_bill(last.svds_bill_no)
            else:
                # nothing exists yet—start with A000
                self.svds_bill_no = "A000"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"SVDS-{self.svds_bill_no} ({self.delivery_status.title()})"


from django.core.validators import MaxValueValidator, RegexValidator
from django.db import models
from django.utils import timezone

from accounts.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Institution(models.Model):
    KIND_CHOICES = (
        (0, 'fundacja'),
        (1, 'organizacja pozarządowa'),
        (2, 'zbiórka lokalna')
    )

    name = models.CharField(max_length=50)
    description = models.TextField()
    kind = models.IntegerField(choices=KIND_CHOICES, default=0)
    categories = models.ManyToManyField(Category)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.PositiveIntegerField(validators=[MaxValueValidator(100)])
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=30,
                                    validators=[
                                        RegexValidator(
                                            regex='(^|\W)(\(?(\+|00)?48\)?)?[ -]?\d{3}[ -]?\d{3}[ -]?\d{3}(?!\w)',
                                            message='Numer telefonu jest nieprawidłowy.')])
    city = models.CharField(max_length=50)
    zip_code = models.CharField(max_length=6,
                                validators=[
                                    RegexValidator(
                                        '[0-9]{2}\-[0-9]{3}',
                                        message='Kod pocztowy jest nieprawidłowy.')])
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField(blank=True)
    is_taken = models.BooleanField(default=False)
    taken_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        if self.is_taken and self.taken_date is None:
            self.taken_date = timezone.now()
        elif not self.is_taken and self.taken_date is not None:
            self.taken_date = None
        super().save(*args, **kwargs)

from django.db import models
from students.models import BaseClass
# Create your models here.
from multiselectfield import MultiSelectField
class ModeChoices(models.TextChoices):

    ONLINE = 'Online','Online'

    OFLINE = "Ofline", "Ofline"

    HYBRID = "Hybrid", "Hybrid"

class Course(BaseClass):

    name = models.CharField(max_length=25)

    code = models.CharField(max_length=15)

    fee = models.FloatField()
    
    offer_percent = models.IntegerField()
    
    mode = MultiSelectField(max_length=15, choices=ModeChoices.choices)
    
    @property
    def get_offer_fee(self):

        # print(self.offer_percent)

        offer_fee = self.fee- (self.fee * self.offer_percent/100)

        return offer_fee



    class Meta:

        verbose_name = 'Course'

        verbose_name_plural = 'Courses'

    def __str__(self):
        
        return self.name
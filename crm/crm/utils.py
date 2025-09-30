import random

import string

from students.models import Students
def generate_admission_number():


    while True:
        five_number = ''.join(random.choices(string.digits,k=5))

        adm_num =  f"LM-{five_number}"

        if not Students.objects.filter(adm_num=adm_num).exists():

            return adm_num




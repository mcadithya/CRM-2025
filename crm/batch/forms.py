from django import forms

from course.models import Course
from trainer.models import Trainer
from .models import Batch

class AddBatchForm(forms.ModelForm):

    class Meta :

        model  =  Batch

        exclude = ['uuid', 'active_status','end_date','code']

        widgets = {
            'name' : forms.TextInput(attrs={'class': "form-control",'required':'required'}),

            'start_date' : forms.DateInput(attrs={'class': "form-control",'required':'required','type':'date'}),

        }
    course =forms.ModelChoiceField(queryset= Course.objects.all(), widget = forms.Select(attrs={'class':'form-select'}) )

    trainer = forms.ModelMultipleChoiceField(queryset= Trainer.objects.all(), widget = forms.SelectMultiple(attrs={'class':'form-select'}))

    
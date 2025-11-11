from django import forms
from .models import Course

class AddCourseForm(forms.ModelForm):

    class Meta :

        model  =  Course

        exclude = ['uuid', 'active_status']

        widgets = {

            'code' : forms.TextInput(attrs={'class': "form-control"}),

            'name' : forms.TextInput(attrs={'class': "form-control"}),

            'fee' : forms.TextInput(attrs={'class': "form-control"}),

            'offer_percent': forms.TextInput(attrs={'class': "form-control"}),
            'mode': forms.CheckboxSelectMultiple(attrs={'class': "form-control"}),
        }


    # def clean(self):

    #     cleaned_data =  super().clean()

    #     mode = cleaned_data.get('mode')

    #     if mode:

    #         self.add_error('mode','choose atleast one mode')        
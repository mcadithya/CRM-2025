from django import forms
import re
from course.models import Course
from batch.models import Batch
from trainer.models import Trainer
from .models import Students ,EducationChoices, BatchChoices,DistrictChoices,TrainerChoices,CourseChoices

class AddStudentForm(forms.ModelForm):

    class Meta :

        model  =  Students

        exclude = ['join_date','adm_num','uuid', 'active_status','profile']

        widgets = {

            'first_name' : forms.TextInput(attrs={'class': "form-control"}),

            'last_name' : forms.TextInput(attrs={'class': "form-control"}),

            'email' : forms.EmailInput(attrs={'class': "form-control"}),

            'contact_num': forms.TextInput(attrs={'class': "form-control"}),

            'photo' : forms.FileInput(attrs={'class': "form-control"}),

            'dob' : forms.DateInput(attrs={'class': "form-control",'type':"date"}),

            'address': forms.TextInput(attrs={'class': "form-control"}),

            'place': forms.TextInput(attrs={'class': "form-control"}),
            
            'pincode': forms.TextInput(attrs={'class': "form-control"}),

        }
    
    education = forms.ChoiceField(choices=EducationChoices.choices, widget= forms.Select(attrs={'class':'form-select'}))

    # batch = forms.ChoiceField(choices=BatchChoices.choices,widget= forms.Select(attrs={'class' : 'form-select'}))

    batch = forms.ModelChoiceField(queryset= Batch.objects.all(),widget= forms.Select(attrs={'class' : 'form-select'}))

    # course = forms.ChoiceField(choices=CourseChoices.choices,widget=forms.Select(attrs={'class' : 'form-select'}))

    course = forms.ModelChoiceField(queryset= Course.objects.all(),widget=forms.Select(attrs={'class' : 'form-select'}))

    # trainer = forms.ChoiceField(choices=TrainerChoices.choices,widget=forms.Select(attrs={'class' : 'form-select'}))

    trainer = forms.ModelChoiceField(queryset= Trainer.objects.all(),widget=forms.Select(attrs={'class' : 'form-select'}))

    district = forms.ChoiceField(choices= DistrictChoices.choices,widget=forms.Select(attrs={'class' : 'form-select'}))

    def clean(self):

        cleaned_data =  super().clean()

        pincode = cleaned_data.get('pincode')

        contact_num = cleaned_data.get('contact_num')

        email = cleaned_data.get('email')

        if len(pincode) < 6:

            self.add_error('pincode','pincode must be 6 digits')

        if Students.objects.filter(email= email).exists() and not self.instance:

            self.add_error('email','This email is already taken')

        username, domian = email.split('@')

        doamin_list = ["gmail.com",
                        "yahoo.com",
                        "outlook.com",
                        "hotmail.com",
                        "icloud.com",
                        "aol.com",
                        "protonmail.com",
                        "zoho.com",
                        "yandex.com",
                        "mail.com",
                        'mailinator.com']
        
        if domian not in doamin_list:

            self.add_error('email','Invalid email address')


        if Students.objects.filter(contact_num=contact_num).exists() and not self.instance:

            self.add_error('contact_num','This phone number is already taken')
        
        pattern = '(\\+91)?\\d{10}' 

        match = re.fullmatch(pattern,contact_num)

        if not match:

            self.add_error("contact_num",'invaid phone number')


    # def __init__(self,*args,**kwargs):

    #     super(AddStudentForm,self).__init__(*args,**kwargs)

    #     if not self.instance:

    #         self.fields.get('email').widget.attrs['required'] = 'required'

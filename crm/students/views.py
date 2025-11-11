from django.shortcuts import render, redirect

from django.views import View

from .forms import AddStudentForm 

from .models import Students,CourseChoices,BatchChoices,TrainerChoices

from django.db.models import Q
# we are created all separate application 
from course.models import Course

from trainer.models import Trainer

from batch.models import Batch

from django.db import transaction

from authentication.models import Profile,OTP

from decouple import config

from crm.utils import generate_admission_number,generate_password,sent_email
# Create your views here.
# threading for parallel process exicution - 
import threading 

# permission
# from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

from authentication.permissions import permitted_users
# @method_decorator(login_required(login_url='login'),name='dispatch')



class DashBoardView(View):

    def get(self,request,*args,**kwargs):

        data = {'title':"Dashboard"}

        return render(request,'students/dashboard.html', context=data)


@method_decorator(permitted_users(['Admin','Sales']), name='dispatch')   

class StudentView(View):

    def get(self,request,*args,**kwargs):

        query = request.GET.get('query')

        course = request.GET.get('course')

        batch = request.GET.get("batch")

        trainer = request.GET.get('trainer')

        students = Students.objects.filter(active_status = True)

        if query:

            students=students.filter(Q(first_name__icontains=query)|
                                     Q(last_name__icontains=query)|
                                     Q(email__icontains=query)|
                                     Q(contact_num__icontains=query)|
                                     Q(education__icontains=query)|
                                     Q(trainer__icontains=query)|
                                     Q(address__icontains=query)|
                                     Q(place__icontains=query)|
                                     Q(dictrict__icontains=query)|
                                     Q(course__icontains=query)|
                                     Q(batch__icontains=query)|
                                     Q(pincode__icontains=query)
                                     )
        elif course:

            students = students.filter(course__name=course) # in orm . replaced by __ (double underscore)

            # students = students.filter(course=course)

        elif batch:

            students.filter(batch=batch)

        elif trainer:

            students.filter(trainer=trainer)

        

        # data = {"title" : "Students List","students":students,
        #        'CourseChoices':CourseChoices,'BatchChoices':BatchChoices,
        #        'TrainerChoices':TrainerChoices,"query":query,
        #        'course':course,'batch':batch,'trainer': trainer}

        # separate apllication then 
        data = {"title" : "Students List","students":students,
               'CourseChoices':Course.objects.all(),'BatchChoices':Batch.objects.all(),
               'TrainerChoices':Trainer.objects.all(),"query":query,
               'course':course,'batch':batch,'trainer': trainer}

        return render(request,'students/students_list.html', context=data)
@method_decorator(permitted_users(['Admin','Sales']), name='dispatch')    
class StudentDetailsView(View):

    def get(self,request,*args,**kwargs):


        uuid  = kwargs.get("uuid")

        student = Students.objects.get(uuid=uuid)

        data = {'title':"Student Details" , 'student': student }

        return render(request,"students/student_details.html",data)

# Perform Hard Delete 

# class StudentDeleteView(View):

#     def get(self,request,*args,**kwargs):

#         uuid = kwargs.get('uuid')

#         student = Students.objects.get(uuid=uuid)

#         student.delete()

#         return redirect('students-list')



# Perform Soft Delete
@method_decorator(permitted_users(['Admin','Sales']), name='dispatch') 
class StudentDeleteView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        student = Students.objects.get(uuid=uuid)

        student.active_status = False

        student.save()

        return redirect('students-list')

@method_decorator(permitted_users(['Admin','Sales']), name='dispatch') 
class AddStudentView(View):

    form_class = AddStudentForm

    def get(self,request,*args,**kwargs):

        form  = self.form_class()

        # print(request.user._meta.get_fields())   

        data = {"form":form,'title':"Add Student"}

        return render(request,'students/add-student.html',context = data)
    

    def post(self,request,*args,**kwargs):
        
        form =self.form_class(request.POST,request.FILES)

        if form.is_valid():

            with transaction.atomic():

                student = form.save(commit=False)

                adm_num = generate_admission_number()

                student.adm_num = adm_num

                email = form.cleaned_data.get('email')

                password = generate_password()

                print(password)

                profile = Profile.objects.create_user(username = email, password = password, role = "Student")

                OTP.objects.create(profile=profile)

                student.profile = profile

                # student.batch = 'hello' 

            # student.batch = 'hello' thenn try to create student then get error but profile will created but student record is not created 
            
                student.save()

                recepient = student.email

                template  ='email/credentials.html'

                site_link  = config('SITE_LINK')

                context = {'username': student.email, 'password': password , 'name' :f'{student.first_name}{student.last_name}','site_link':site_link}

                title = "Login Credentials"

                thread = threading.Thread(target=sent_email,args=(recepient,template,title,context)) #create thread object , in target function have parameter then add args other wise skip args. args is tuple. 

                thread.start()
                # sent_email(recepient,template,title,context)

                return redirect("students-list")
        
        data = {'form':form}
        
        return render(request,'students/add-student.html',context = data)

        # post_data = request.POST

        # first_name = post_data.get("first_name")

        # last_name = post_data.get("last_name")

        # adm_num  = post_data.get('adm_num')

        # email = post_data.get('email')

        # contact_num =post_data.get('contact_num')

        # photo =request.FILES.get('photo')

        # dob = post_data.get('dob')

        # education = post_data.get("education")

        # address = post_data.get("address")

        # place = post_data.get("place")

        # course = post_data.get("course")

        # district = post_data.get("district")

        # pincode = post_data.get("pincode")

        # batch = post_data.get("batch")

        # trainer = post_data.get("trainer")

        # place = post_data.get("place")
      
        # student = Students.objects.create(first_name =  first_name ,last_name = last_name,adm_num  = adm_num ,course=course,  email = email , contact_num = contact_num, photo = photo,  dob = dob , education = education,address  = address, place = place , district =  district, pincode = pincode ,batch = batch ,trainer = trainer )
@method_decorator(permitted_users(['Admin','Sales']), name='dispatch') 
class EditStudentView(View):
     
     form_class = AddStudentForm

     def get(self,request,*args,**kwargs):
         
         uuid = kwargs.get('uuid')

         student = Students.objects.get(uuid=uuid)

         form = self.form_class(instance = student)

         data = {'form' : form ,'title':"Edit Student"}

         
         return render(request,"students/edit-student.html",data)
    
     def post(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')
    
        student = Students.objects.get(uuid=uuid)

        form =self.form_class(request.POST,request.FILES,instance = student)

        if form.is_valid():

            form.save()

            return redirect("students-list")

        data = {'form':form}

        return render(request,"students/edit-student.html",data)
    
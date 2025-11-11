from django.shortcuts import render,redirect

from django.utils.decorators import method_decorator

from authentication.permissions import permitted_users

from django.views import View
from .models import Batch
from .forms import AddBatchForm

from crm.utils import get_batch_code,get_end_date

# Create your views here.

class BatchListView(View):

    def get(self,request,*args,**kwargs):

        query = request.GET.get('quesry')

        batches = Batch.objects.filter(active_status = True)

        # if query:

        #     batches= batches.filter(Q(code__icontainer = query)|Q(name__icontainer = query)|Q(mode__icontainer = query))

        data = {'batches': batches}

        print(batches)

        return render(request,'batch/batch-list.html', data )
@method_decorator(permitted_users(['Admin','Sales']), name='dispatch')
class AddBatchView(View):

    form_class = AddBatchForm

    def get(self,request,*args,**kwargs):

        form  = self.form_class()

        # print(request.user._meta.get_fields())   

        data = {"form":form,'title':"Add Batch"}

        return render(request,'batch/add-batch.html',context = data)
    

    def post(self,request,*args,**kwargs):
        
        form =self.form_class(request.POST)

        if form.is_valid():

            batch = form.save(commit = False)

            start_date = form.cleaned_data.get('start_date')

            batch_code = get_batch_code(batch.course,start_date)

            print(batch_code)

            end_date = get_end_date(start_date)

            print(end_date)

            batch.code = batch_code

            batch.end_date = end_date

            batch.save()

            form.save_m2m()

            return redirect('batch-list')

        
        data = {'form':form}
        
        return render(request,'batch/add-batch.html',context = data)
    
@method_decorator(permitted_users(['Admin','Sales']), name='dispatch')
class EditBatchView(View):
     
     form_class = AddBatchForm

     def get(self,request,*args,**kwargs):
         
         uuid = kwargs.get('uuid')

         batch = Batch.objects.get(uuid=uuid)

         form = self.form_class(instance = batch)

         data = {'form' : form ,'title':"Edit batch"}

         
         return render(request,"batch/edit-batch.html",data)
    
     def post(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')
    
        batch = Batch.objects.get(uuid=uuid)

        form =self.form_class(request.POST,instance = batch)

        if form.is_valid():

            form.save()

            return redirect("batch-list")

        data = {'form':form}

        return render(request,"batch/edit-batch.html",data)



@method_decorator(permitted_users(['Admin','Sales']), name='dispatch') 
class BatchDeleteView(View):

    def get(self,request,*args,**kwargs):

        uuid = kwargs.get('uuid')

        batch = Batch.objects.get(uuid=uuid)

        batch.active_status = False

        batch.save()

        return redirect('batch-list')
    
@method_decorator(permitted_users(['Admin','Sales']), name='dispatch')    
class BatchDetailsView(View):

    def get(self,request,*args,**kwargs):


        uuid  = kwargs.get("uuid")

        batch = Batch.objects.get(uuid=uuid)

        data = {'title':"Batch Details" , 'batch': batch }

        return render(request,"batch/batch_details.html",data)
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse
from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.hashers import check_password
from .models import Admin, Student, Landlord, Properties, Rental , Service
# Create your views here.

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

#landlord
def landRegister(request):

    if request.method == 'POST':

        land_ID = request.POST['landID'] #refer models vars
        land_name = request.POST['landName']
        land_pass = request.POST['landPass']
        land_no = request.POST['landNo']
        confirm_pass = request.POST['confirmPass']

        if land_pass != confirm_pass:  # Check if passwords match
            messages.error(request, 'Passwords do not match.')
            return render(request, 'landRegister.html')
        
        if Landlord.objects.filter(landID=land_ID).exists():
            messages = 'Landlord account already existed.'
            return render(request, 'landlog.html', {'messages': messages})

        new_landlord = Landlord(
            landID = land_ID,
            landName = land_name,
            landPass = land_pass,
            landNo = land_no)
        
        new_landlord.save()

        message = 'Registration successful. You can now login.'
        return render(request, 'landlog.html', {'message':message})

    return render(request, 'landRegister.html')

def landlog(request):
    if request.method == 'POST':
        land_ID = request.POST.get('landID')
        land_pass = request.POST.get('landPass')

        # Check if the landlord exists
        try:
            landlord = Landlord.objects.get(landID=land_ID)  # Use get() to retrieve a single object
        except Landlord.DoesNotExist:
            message = 'Landlord Account does not exist. Please register.'
            return render(request, 'landlog.html', {'message': message})

        if landlord.landPass == land_pass:
            
            request.session['landID'] = landlord.landID  # Save landID in session     
            return redirect('houserental:landDash')
        else:
            message = 'Incorrect password. Please try again.'
            return render(request, 'landlog.html', {'message': message})

    return render(request, 'landlog.html')


def landDash(request):
    
    if 'landID' not in request.session:
        return redirect('houserental:landlog')  
    
    land_ID = request.session['landID']  
    
    landlord = Landlord.objects.filter(landID=land_ID)

    if landlord.exists():  # check if the landlord exists
        return render(request, 'landDash.html', {'landlord': landlord})
    else:
        message = 'No Data or Invalid ID'
        return render(request, 'landDash.html', {'message': message})

       
   
def landProp(request):
    if 'landID' not in request.session:
        return redirect('houserental:landlog')  

    land_ID = request.session['landID']
    

    properties = Properties.objects.filter(landID=land_ID)

    if properties.exists():  
        paginator = Paginator(properties, 10)  # show 10 properties per page
        page_number = request.GET.get('page')  # get the page number from the request
        page_obj = paginator.get_page(page_number) 

        return render(request, 'landProp.html', {'page_obj': page_obj})
    else:
        message = 'No Data or Invalid ID'
        return render(request, 'landProp.html', {'message': message})
     

def landAddprop(request):
    
    if 'landID' not in request.session:
        return redirect('houserental:landlog') 

    
    land_ID = request.session['landID']
  
    try:
        landlord = Landlord.objects.get(landID=land_ID)
    except Landlord.DoesNotExist:
        return redirect('houserental:landlog')  

    if request.method == 'POST':
        prop_ID = request.POST['propID']
        prop_name = request.POST['propName']
        prop_loc = request.POST['propLoc']
        prop_size = request.POST['propSize']
        prop_price = request.POST['propPrice']
        
        
        data = Properties(
            propID=prop_ID,
            propType=prop_name,
            propLoc=prop_loc,
            propSize=prop_size,
            propPrice=prop_price,
            landID=landlord  
        )
        data.save()

        return redirect('houserental:landProp')
    
    return render(request, 'landAddprop.html', {'landlordID': land_ID})

def landTenant(request):

    if 'landID' not in request.session:
        return redirect('houserental:landlog') 

    land_ID = request.session['landID']  

    properties = Properties.objects.filter(landID=land_ID)    
    rentals = Rental.objects.filter(propID__in=properties)  # Use __in to filter by a queryset

    
    paginator = Paginator(rentals, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    return render(request, 'landTenant.html', {'page_obj': page_obj, 'properties': properties})
  

def landReport(request):
    return render(request, 'landReport.html')


#student
def studRegister(request):

    if request.method == 'POST':

        stud_ID = request.POST['studID'] # <--refer html page name vars
        stud_name = request.POST['studName']
        stud_pass = request.POST['studPass']
        confirm_pass = request.POST['confirmPass']
        stud_no = request.POST['studNo']
        guard_no = request.POST['guardNo']
        stud_address = request.POST['studAddress']
        

        if stud_pass != confirm_pass:  # Check if passwords match
            messages.error(request, 'Passwords do not match.')
            return render(request, 'landRegister.html')

        if Student.objects.filter(studID=stud_ID).exists():
            messages = 'Student already existed.'
            return render(request, 'studlog.html', {'messages': messages})

        new_student = Student(
            studID = stud_ID,  # <--refer models.py
            studName = stud_name,
            studPass = stud_pass,
            studNo = stud_no,
            guardNo = guard_no,
            studAddress = stud_address)
        
        new_student.save()

        message = 'Registration successful. You can now login.'
        return render(request, 'studlog.html', {'message':message})

    return render(request, 'studRegister.html')
     

def studlog(request):
    if request.method == 'POST':
        stud_ID = request.POST.get('studID')
        stud_pass = request.POST.get('studPass')

        try:
            student = Student.objects.get(studID=stud_ID)  
        except Student.DoesNotExist:
            message = 'Student Account does not exist. Please register.'
            return render(request, 'studlog.html', {'message': message})

        
        if student.studPass == stud_pass:            
            request.session['studID'] = student.studID           
            return redirect('houserental:studDash')
        else:
            message = 'Incorrect password. Please try again.'
            return render(request, 'studlog.html', {'message': message})

    return render(request, 'studlog.html')

def studDash(request):
   
    if 'studID' not in request.session:
        return redirect('houserental:studlog') 

    stud_ID = request.session['studID'] 


    rental = Rental.objects.filter(studID=stud_ID)
    service = Service.objects.filter(studID=stud_ID)
    

    if rental.exists():
        context = {'rental': rental}        
       
        if service.exists():
            context['service'] = service  
            
        return render(request, 'studDash.html', context)
    else:
        message = 'No Data or Invalid ID'
        return render(request, 'studDash.html', {'message': message})
  

def studRent(request):
    properties = Properties.objects.all()

    if 'studID' not in request.session:
        return redirect('houserental:studlog') 

    stud_ID = request.session['studID'] 

    if request.method == 'POST':
        stud_ID = request.POST['studID']  #from the form
        prop_ID = request.POST['propID']   

      
        try:
            stud_instance = Student.objects.get(pk=stud_ID)
        except Student.DoesNotExist:
            message = 'Student ID does not exist.'
            return render(request, 'studDash.html', {'message': message})

        try:
            prop_instance = Properties.objects.get(pk=prop_ID)
        except Properties.DoesNotExist:
            message = 'Property ID does not exist.'
            return render(request, 'studDash.html', {'message': message})
        
        existing_rental = Rental.objects.filter(studID=stud_instance, propID=prop_instance).exists()
        if existing_rental:
            message = 'You have already applied for this property.'
            return render(request, 'studDash.html', {'message': message})

       
        rental_instance = Rental(
            studID=stud_instance,
            propID=prop_instance,
        )

        rental_instance.save() 
        message = 'Rental application has been submitted. Check the status in the dashboard.'
        return render(request, 'studDash.html', {'message': message})

    # Pagination setup
    paginator = Paginator(properties, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'studRent.html', {'page_obj': page_obj, 'properties': properties ,'stud_ID': stud_ID })



def studService(request):
    
    if 'studID' not in request.session:
        return redirect('houserental:studlog')

    stud_ID = request.session['studID']

   
    if request.method == 'POST':
        prop_ID = request.POST.get('propID')  
        details = request.POST.get('details', '')  
         
        stud_instance = Student.objects.get(pk=stud_ID)
        prop_instance = Properties.objects.get(pk=prop_ID)

        
        if not Rental.objects.filter(studID=stud_instance, propID=prop_instance).exists():
            return render(request, 'studService.html', {'message': 'You can only submit a request for properties you have rented.'})

        
        service_instance = Service(
            studID=stud_instance,
            propID=prop_instance,
            details=details
        )
        service_instance.save()

        return render(request, 'studService.html', {'message': 'Service request has been submitted. Check the status in the dashboard.'})

    return render(request, 'studService.html', {'message': 'Invalid request method.'})






def payment(request):
    return render(request, 'payment.html')
   

def landMonthly(request):

    return render(request, 'monthlyReport.html')

def mainSummary(request):

    return render(request, 'mainSummary.html')





def deleteProp(request, propID):
    data = Properties.objects.get(propID=propID)
    data.delete()

    return HttpResponseRedirect(reverse('houserental:landProp'))
 
def studProfile(request):
    
    if 'studID' not in request.session:
        return redirect('houserental:studlog')  

    stud_ID = request.session['studID'] 

    try:
        student = Student.objects.get(studID=stud_ID)  
    except Student.DoesNotExist:
        messages.error(request, 'Student not found.')
        return redirect('houserental:studlog') 
    
    if request.method == 'POST':
        
        student.studName = request.POST.get('full_name')  
        student.studGender = request.POST.get('gender')  
        student.studNo = request.POST.get('studNo')
        student.guardNo = request.POST.get('guardNo')
        student.studAddress = request.POST.get('address') 
        
        student.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('houserental:studProfile')  

    return render(request, 'studProfile.html', {'student': student})


def adminlog(request):

    if request.method == 'POST':
        staff_id = request.POST.get('staffid')
        staff_pass = request.POST.get('staffpass')

        try:
            admin = Admin.objects.get(staffid=staff_id)  
        except Admin.DoesNotExist:
            message = 'Login for staff only. '
            return render(request, 'adminlog.html', {'message': message})

        
        if admin.staffpass == staff_pass:
                                
            return redirect('houserental:admin')
        else:
            message = 'Incorrect password. Please try again.'
            return render(request, 'adminlog.html', {'message': message})

    return render(request, 'adminlog.html')


def admin(request):

    rental = Rental.objects.all()  

    paginator = Paginator(rental, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'admin.html', {'page_obj':page_obj})   
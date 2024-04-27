import traceback
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User,Group
from .models import *
from django.contrib.auth import authenticate,logout,login
from django.utils import timezone



def homepage(request):
    return render(request, 'index.html')

def aboutpage(request):
    return render(request, 'about.html')

def login_admin(request):
    error = ""
    if request.method == 'POST':
        u=request.POST['username']
        p=request.POST['password']
        user = authenticate(username=u,password=p)
        try:
            if user.is_staff:
                login(request,user)
                error="no"
            else:
                error ="yes"
        except:
            error="yes"
    d={'error':error}
    return render(request, 'adminlogin.html',d)

def loginpage(request):
    error=""
    page= ""
    if  request.method=='POST':
        u=request.POST['email']
        p=request.POST['password']
        user = authenticate(request,username=u,password=p)
        try:
            if user is not None:
                login(request,user)

                if user.groups.exists():
                    error="no"
                    g=user.groups.all()[0].name
 
                    if g=='Doctor':
                        page="doctor"
                        d={'error':error,'page':page}
                        return render(request,'doctorhome.html',d)

                    elif g=='Receptionist':
                        page="reception"
                        d={'error':error,'page':page}
                        return render(request,'receptionhome.html',d)
                
                    elif g=='Patient':
                        page="patient"
                        d={'error':error,'page':page}
                        return render(request,'patienthome.html',d)
                else:
                    print("User has no groups.")
            else:
                error="yes"
        except Exception as e:
            print(e)
            # print(traceback.print_exc())
            error="yes"
            raise

    return render(request,'login.html')

def createaccountpage(request):
    error=""
    pat_group=""
    user="none"
    if request.method =="POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        repeatpassword = request.POST.get('repeatpassword')
        gender = request.POST.get('gender')
        phonenumber = request.POST.get('phonenumber')
        address = request.POST.get('address')
        birthdate = request.POST.get('dateofbirth')
        bloodgroup = request.POST.get('bloodgroup')

        try:
            if password == repeatpassword:
                Patient.objects.create(name=name,email=email,password=password,gender=gender,phonenumber=phonenumber,address=address,birthdate=birthdate,bloodgroup=bloodgroup)
                user = User.objects.create_user(first_name=name,email=email,password=password,username=email)
                pat_group = Group.objects.get_or_create(name='Patient')
                print(type(pat_group))
                pat_group[0].user_set.add(user)

                user.save()

                error="no"
            else:
                error="yes"
        except Exception as e:
            error="yes"

    d={'error':error}

    return render(request,'createaccount.html',d)


def adminaddDoctor(request):
    error = ""
    user="none"
    if not request.user.is_staff:
        return redirect('logn_admin')
    
    if request.method == "POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        repeatpassword=request.POST.get('repeatpassword')
        gender=request.POST.get('gender')
        phonenumber=request.POST.get('phonenumber')
        address=request.POST.get('address')
        birthdate=request.POST.get('dateofbirth')
        bloodgroup=request.POST.get('bloodgroup')
        specialization=request.POST.get('specialization')

        try:
            if password==repeatpassword:
                Doctor.objects.create(name=name,email=email,password=password,gender=gender,phonenumber=phonenumber,address=address,birthdate=birthdate,bloodgroup=bloodgroup,specialization=specialization)
                user=User.objects.create_user(first_name=name,email=email,password=password,username=email)
                doc_group, created = Group.objects.get_or_create(name='Doctor')
                doc_group.user_set.add(user)
                user.save()
                error="no"
            else:
                error="yes"
        except Exception as e:
            error="yes"
    d={'error':error}
    return render(request,'adminadddoctor.html',d)

def adminviewDoctor(request):
    if not request.user.is_staff:
        return redirect('login_admin')
    doc = Doctor.objects.all()
    d={'doc':doc}
    return render(request, 'adminviewDoctors.html',d) 

def admin_delete_doctor(request,pid,email):
    if not request.user.is_staff:
        return redirect('login_admin')
    doctor = Doctor.objects.get(id=pid)
    doctor.delete()
    users=User.objects.filter(username=email)
    users.delete()
    return redirect('adminviewDoctor')

def patient_delete_appointment(request,pid):
    if not request.user.is_active:
        return redirect('loginpage')
    appointment = Appointment.objects.get(id=pid)
    appointment.delete()
    return redirect('viewappointments')

def adminaddReceptionist(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login_admin')
    
    if request.method == 'POST':
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']
        repeatpassword=request.POST['repeatpassword']
        gender=request.POST['gender']
        phonenumber=request.POST['phonenumber']
        address=request.POST['address']
        birthdate=request.POST['dateofbirth']
        bloodgroup=request.POST['bloodgroup']

        try:
            if password == repeatpassword:
                Recepcionist.objects.create(name=name,email=email,password=password,gender=gender,phonenumber=phonenumber,address=address,birthdate=birthdate,bloodgroup=bloodgroup)
                user = User.objects.create_user(first_name=name,email=email,password=password,username=email)
                rec_group = Group.objects.get_or_create(name='Receptionist')
                rec_group.user_set.add(user)

                user.save()

                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    d={'error':error}
    return render (request,'adminaddreceptionist.html',d)

def adminviewReceptionist(request):
    if not request.user.is_staff:
        return redirect('login_admin')
    rec = Recepcionist.objects.all()
    r={'rec':rec}
    return render (request, 'adminviewreceptionists.html',r)

def admin_delete_receptionist(request,pid,email):
    if not request.user.is_staff:
        return redirect('login_admin')
    reception = Recepcionist.objects.get(id=pid)
    reception.delete()
    users = User.objects.filter(username=email)
    users.delete()
    return redirect('adminviewReceptionist')

def adminviewAppointment(request):
    if not request.user.is_staff:
        return redirect('login_admin')
    upcoming_appointments = Appointment.objects.filter(appointmentdate__gte=timezone.now(), status=True).order_by('appointmentdate')

    previous_appointments = Appointment.objects.filter(appointmentdate__lt=timezone.now()).order_by('-appointmentdate') | Appointment.objects.filter(status=False).order_by('-appointmentdate')

    d={"upcomming_appoingments":upcoming_appointments,"previous_appointmens":previous_appointments}
    return render(request,'adminviewappointments.html',d)


def Logout(request):
    if not request.user.is_active:
        return redirect('loginpage')
    logout(request)
    return redirect('loginpage')

def Logout_admin(request):
    if not request.user.is_staff:
        return redirect('login_admin')
    logout(request)
    return redirect('login_admin')

def AdminHome(request):

    if not request.user.is_staff:
        return redirect('login_admin')
    return render(request,'adminhome.html')

def Home(request):
    if not request.user.is_active:
        return redirect('loginpage')
    
    g=request.user.groups.all()[0].name
    if g=='Doctor':
        return render(request,'doctorhome.html')
    elif g=='Receptionist':
        return render(request,'receptionhome.html')
    elif g=='Patient':
        return render(request,'patienthome.html')
    
def profile(request):
    if not request.user.is_active:
        return redirect('loginpage')
    
    g=request.user.groups.all()[0].name
    if g=='Patient':
        patient_detials = Patient.objects.all().filter(email=request.user)
        d={'patient_detials':patient_detials}
        return render(request, 'patientprofile.html',d)
    
    elif g=='Doctor':
        doctor_detials=Doctor.objects.all().filter(email=request.user)
        d={'doctor_detials':doctor_detials}
        return render(request,'doctorprofile.html',d)
    elif g=='Receptionist':
        reception_details=Recepcionist.objects.all().filter(email=request.user)
        d={'reception_details':reception_details}
        return render(request,'receptionprofile.html',d)
        
def MakeAppointments(request):
    error=""
    if not request.user.is_active:
        return request('loginpage')
    
    if not Doctor.objects.exists():
        error = "yes"
        return render(request, "patientmakeappointments.html")
    
    alldoctors=Doctor.objects.all()
    d={'alldoctors':alldoctors}
    g=request.user.groups.all()[0].name
    if g == 'Patient':
        if request.method == 'POST':
            doctoremail = request.POST['doctoremail']
            doctorname = request.POST['doctorname']
            patientname = request.POST['patientname']
            patientemail = request.POST['patientemail']
            appointmentdate = request.POST['appointmentdate']
            appointmenttime = request.POST['appointmenttime']
            symptoms = request.POST['symptoms']
            try:
                Appointment.objects.create(doctorname=doctorname,doctoremail=doctoremail,patientname=patientname,patientemail=patientemail,appointmentdate=appointmentdate,appointmenttime=appointmenttime,symptomps=symptoms, status=True)
                error="no"
            except:
                raise
                error="yes"
            e={'error':error}
            return render(request,'patientMakeAppointments.html',e)
        elif request.method == "GET":
            return render(request,'patientMakeAppointments.html',d)
        
def viewappointments(request):
    if not request.user.is_active:
        return redirect('loginpage')
    
    g=request.user.groups.all()[0].name
    if g=='Patient':
        upcomming_appointments = Appointment.objects.filter(patientemail=request.user, appointmentdate__gte=timezone.now(),status=True).order_by('appointmentdate')

        previous_appointments = Appointment.objects.filter(patientemail=request.user,appointmentdate__lt=timezone.now()).order_by('-appointmentdate') | Appointment.objects.filter(patientemail=request.user, status=False).order_by('-appointmentdate')

        d={"upcomming_appointments":upcomming_appointments,"previous_appointments":previous_appointments}
        return render(request,'patientviewappointments.html',d)
    elif g=='Doctor':
        if request.method=='POST':
            prescriptiondata = request.POST['prescription']
            idvalue=request.POST['idofappointment']
            Appointment.objects.filter(id=idvalue).update(precription=prescriptiondata, status=False)

            upcomming_appointments=Appointment.objects.filter(doctoremail=request.user, appointmentdate__gte=timezone.now(),status=True).order_by('apointmentdate')

            previous_appointments=Appointment.objects.filter(doctoremail=request.user,appointmentdate__lt=timezone.now()).order_by('-appointmentdate') | Appointment.objects.filter(doctoremail=request.user, status=False).order_by('-appointmentdate')

            d={"upcomming_appointments":upcomming_appointments, "previous_appointments":previous_appointments} 
            return render(request,'doctorviewappointment.html',d)
        elif g=='REceptionist':
            upcomming_appointments=Appointment.objects.filter(appointmentdate__gte=timezone.now(),status=True).order_by('appointmentdate')
            
            previous_appointments=Appointment.objects.filter(appointmentdate__lt=timezone.now()).order_by('-appointmentdate') | Appointment.objects.filter(status=False).order_by('-appointmentdate')

            d={"upcomming_appointments":upcomming_appointments,"previous_appointments":previous_appointments}
            return render (request,'receptionviewappointments.html',d)

def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)

    # print(appointment.patient.first_name)

    context = {
        'test': 'Hola',
        'appointment': appointment,
        'alldoctors': Doctor.objects.all(),
        'user': request.user,
        'error': None
    }
    return render(request, 'viewappointment.html', context)
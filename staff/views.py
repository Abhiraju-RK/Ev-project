from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from . models import Staff,Station,AvailableSlot,Booking
from user.models import Client
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User

# Create your views here.
def staff_home(request):
    return render(request,'app/staff_home.html')

def staff_register(request):
    if request.method == "POST":
        username=request.POST.get("username")
        email=request.POST.get('email')
        password=request.POST.get('password')
        confrim_pass=request.POST.get('confirm_pass')
        phone=request.POST.get('phone')

        if not username or not email or not password or not confrim_pass or not phone:
            messages.error(request,"All feild requires  !!")
            return redirect('staff_register')
        if User.objects.filter(email=email).exists():
            messages.error(request,"Email Already exists !!")
            return redirect('staff_register')
        if not phone.isdigit() or len(phone)!=10:
            messages.error(request,"Phone number must have 10 digit !!")
            return redirect('staff_register')
        if confrim_pass!=password:
            messages.error(request,"Password doesnt match !!")
            return redirect('staff_register')
        
        user=User.objects.create_user(username=username,email=email,password=password)
        user.save()
        Staff.objects.create(user=user,email=email,phone=phone)

        messages.success(request,"Register Successfully")
        return redirect('staff_login')
    return render(request, 'app/staff_register.html') 

def staff_login(request):
    if request.method == "POST":
        email=request.POST.get('email')
        password=request.POST.get('password')

        try:
            user_obj=Staff.objects.get(email=email)
        except Staff.DoesNotExist:
            messages.error(request,'You are  not registerd')
            return redirect('staff_register')
        
        user=authenticate(request,username=user_obj.user.username,password=password)
        
        if user is not None:
            login(request,user)
            messages.success(request,f'{user.username} successfully login ')
            return redirect('staff_home')
        else:
            messages.error(request, 'Invalid email or password!')
    return render(request,'app/staff_login.html')

def staff_logout(request):
    logout(request)
    return redirect('index')

@login_required
def staff_profile(request):
    user=request.user
    if request.method == "POST":
        if "staff_update" in request.POST:
            user.username=request.POST.get('username',user.username)
        
            user.email=request.POST.get('email',user.email)
            user.phone=request.POST.get('phone',user.phone)
            user.save()
            messages.success(request,'Profile update successfully ')
            return redirect('staff_profile')
        elif "staff_pass" in request.POST:
            current_password=request.POST.get('current_password')
            new_password=request.POST.get('new_password')
            confirm_password=request.POST.get('confirm_password')

            if confirm_password!=new_password:
                messages.error(request,'Invalid password !!')
                return redirect('staff_profile')
            if not user.check_password(current_password):
                messages.error(request, "Current password is incorrect!")
                return redirect('staff_profile')
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "Password changed successfully!")

        return redirect('staff_profile')
    
    return render(request, 'app/staff_profile.html',)

@login_required
def station_list(request):
    stations=Station.objects.all().order_by('city')
    return render(request,'app/station_list.html',{'stations':stations})


@login_required
def add_station(request):
    if request.method == "POST":
        name=request.POST.get("name")
        location=request.POST.get('location')
        city=request.POST.get('city')
        quik_map=request.POST.get('quik_map')

        staffs=Staff.objects.get(email=request.user.email)

        Station.objects.create(user=staffs,name=name,location=location,city=city,quik_map=quik_map)

        messages.success(request, "Station added successfully!")
        return redirect('station_list')
    else:
        messages.error(request,"Station dint addedd !!")
    return render(request,'app/add_station.html')


def edit_station(request,station_id):
    staff = Staff.objects.get(user=request.user)
    try:
        station = Station.objects.get(id=station_id, user=staff)
    except Station.DoesNotExist:
        messages.error(request, "Station not found or you don't have permission to edit it.")
        return redirect('station_list')
    if request.method == "POST":
        station.name=request.POST.get('name')
        station.location=request.POST.get('location')
        station.city=request.POST.get('city')
        station.quik_map=request.POST.get('quik_map')

        station.save()
        messages.success(request,'Station edited Successfully ')
        return redirect('station_list')
    return render(request,'app/staff_edit_station.html')



@login_required
def add_slot(request):
    if request.method == "POST":
        name=request.POST.get('name')   
        price=request.POST.get('price')
        station_id=request.POST.get('station')

        try:
            station=Station.objects.get(id=station_id)
            AvailableSlot.objects.create(station=station,name=name,price=price,is_booked=False)
            messages.success(request, "Slot added successfully!")
            return redirect('slot_list',station_id=station.id)
        except Station.DoesNotExist:
            messages.error(request,"Slot dint addedd !!")
    stations=Station.objects.all()
    return render(request,'app/add_slot.html',{'stations':stations})

@login_required
def slot_list(request,station_id):
    station = get_object_or_404(Station, id=station_id)
    slots = AvailableSlot.objects.filter(station=station)
    return render(request,'app/slot_list.html',{'slots':slots})

@login_required
def slot_bookings(request):
    bookings=Booking.objects.all()
    return render(request,'app/slot_bookings.html',{'bookings':bookings})
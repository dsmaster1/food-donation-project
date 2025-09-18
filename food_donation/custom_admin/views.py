from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from home.models import *
from home.forms import *
from django.utils import timezone
from django.utils.timezone import now
# Create your views here.

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user and user.is_superuser:
            login(request, user)
            return redirect('index_admin')
        else:
            messages.error(request, 'Access denied! Only Admin can log in')  
            return redirect('admin_login')  
    return render(request, 'admin_login.html')

def logoutpage(request):
    logout(request)
    messages.error(request, 'user has logged out')
    return redirect(admin_login)

@login_required(login_url='admin_login')
def admin_dashboard(request):
    totalvolunteers = StaffProfile.objects.count()
    totaldonations = Donation.objects.count()
    totaldonors = Donor.objects.count()
    totalpendingdonations = Donation.objects.filter(status="pending").count()
    totalaccepteddonations = Donation.objects.filter(status="accept").count()
    totalgiven = Donation.objects.filter(status="Donation Given").count()
    totaldonationareas = Location.objects.all().count()

    context = {
        "totalvolunteers": totalvolunteers,
        "totaldonations": totaldonations,
        "totaldonors": totaldonors,
        "totalpendingdonations": totalpendingdonations,
        "totalaccepteddonations": totalaccepteddonations,
        "totalgiven": totalgiven,
        "totaldonationareas": totaldonationareas,
    }

    return render(request, "index-admin.html", context)

@login_required(login_url='admin_login')
def manage_donor(request):
    donor = Donor.objects.all()
    return render(request, 'manage_donor.html', {'donor':donor})

@login_required(login_url='admin_login')
def new_volunteer(request):
    volunteer = StaffProfile.objects.filter(status='pending')
    return render(request, 'new_volunteer.html', {'volunteer': volunteer})

def accepted_volunteers(request):
    volunteer = StaffProfile.objects.filter(status='accept')
    return render(request, 'accepted_volunteer.html', {'volunteer': volunteer}) 

def rejected_volunteers(request):
    volunteer = StaffProfile.objects.filter(status='reject')
    return render(request, 'rejected_volunteer.html', {'volunteer': volunteer}) 


def all_volunteers(request):
    volunteer = StaffProfile.objects.all()
    return render(request, 'all_volunteer.html', {'volunteer': volunteer}) 

@login_required(login_url='admin_login')
def all_donations(request):
    donation = Donation.objects.all()
    return render(request, 'all_donations.html', {'donation': donation})

@login_required(login_url='admin_login')
def pending_donation(request):
    donation = Donation.objects.filter(status='pending')
    return render(request, 'pending_donation.html', {'donation':donation})

@login_required(login_url='admin_login')
def accepted_donation(request):
    donation = Donation.objects.filter(status='accept')
    return render(request, 'accepted_donation.html', {'donation':donation} )

@login_required(login_url='admin_login')
def rejected_donation(request):
    donation = Donation.objects.filter(status='reject')
    return render(request, 'rejected_donation.html', {'donation':donation} )

@login_required(login_url='admin_login')
def donation_given(request):
    donation = Donation.objects.filter(status='Donation Given')
    return render(request, 'donationgiven_admin.html', {'donation': donation})

@login_required(login_url='admin_login')
def view_donationdetail(request, pid):
    donation = get_object_or_404(Donation, id=pid)
    booking = donation.bookings.first()

    if request.method == 'POST':
        status = request.POST.get('status')
        adminremark = request.POST.get('admin_remark')

        if not status:
            messages.error(request, 'Status is required' )
        else:

            try:
                donation.admin_remark = adminremark
                donation.status = status
                donation.last_update = timezone.now().date()
                donation.save()
                messages.success(request, 'Status & Remark Updated Successfully' )

                return redirect('view_donationdetail', pid=pid)
            except Exception as e:

                messages.warning(request, f'Failed to Update Status & Remark: {e}')
    return render(request, "view_donationdetail.html", {'donation':donation, 'booking':booking})

@login_required(login_url='admin_login')
def donationrec_admin(request):
    donation = Donation.objects.filter(status='Donation Received')
    return render(request, 'donationrec_admin.html', {'donation':donation} )

@login_required(login_url='admin_login')
def donationnotrec_admin(request):
    donation = Donation.objects.filter(status='Donation Not Received')
    return render(request, 'donationnotrec_admin.html', {'donation':donation} )



def delete_donation(request, pid):
    donation = Donation.objects.get(id=pid)
    donation.delete()
    return redirect('alldonations')

def delete_volunteer(request, pid):
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('all_volunteers')

def delete_donor(request, pid):
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('managedonor')

@login_required(login_url='admin_login')
def donor_details(request, pid):
    donor = get_object_or_404(Donor, id=pid)
    
    return render(request, 'view_donordetail.html', {'donor': donor})

@login_required(login_url='admin_login')
def view_volunteerdetails(request, pid):
    staff = get_object_or_404(StaffProfile, id=pid)
    if request.method == 'POST':
        status = request.POST['status']
        admin_remark = request.POST['admin_remark']
        try:
            staff.admin_remark = admin_remark
            staff.status = status
            staff.last_updated = timezone.now().date()
            staff.save()
            messages.success(request, 'Volunteer Updated Successfully')
        except:
            messages.warning(request,'Volunteer Update Failed')    
    return render(request, 'view_volunteerdetail.html', {'staff':staff })

@login_required(login_url='admin_login')
def add_area(request):
    if request.method == 'POST':
        form = DonationAreaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Area Added Successfully')
            return redirect('addarea') 
        else:
            messages.error(request, 'Invalid Form Data')
    else:
        form = DonationAreaForm() 

    return render(request, 'add_area.html', {'form': form})

@login_required(login_url='admin_login')
def manage_area(request):
    area = Location.objects.all()
    return render(request, 'manage_area.html', {'area':area})

@login_required(login_url='admin_login')
def edit_area(request, pid):
    area = get_object_or_404(Location, id=pid)
    if request.method == 'POST':
        form = DonationAreaForm(request.POST, instance=area)
        if form.is_valid():
            try:
                form.save()
                
                return redirect('managearea')
            except:
                messages.warning(request, 'Area Not Updated')
        else:
            messages.warning(request, 'Invalid form data')
    else:
        form = DonationAreaForm(instance=area)


    return render(request, 'edit_area.html', {'form':form, 'area':area})

@login_required(login_url='admin_login')
def delete_area(request, pid):
    area = Location.objects.get(id=pid)
    area.delete()
    return redirect('managearea')

@login_required(login_url='admin_login')
def incomingdonationdetails_admin(request, pid):
    donation = get_object_or_404(Donation, id=pid)

    if request.method == 'POST':
        status = request.POST.get('status')
        adminremark = request.POST.get('admin_remark')

        try:
            donation.status = status
            donation.admin_remark = adminremark
            donation.last_update = timezone.now().date()
            donation.save()
            messages.success(request, 'Admin Remark updated successfully')
        except:
            messages.warning(request, 'Failed to update Admin Remark')    

    return render(request, 'donationcollectiondetails_admin.html', {'donation':donation})

@login_required
def donateditemdetails_admin(request, pid):
    donation = get_object_or_404(Donation, id=pid)
    booking = donation.bookings.first() 
    return render(request, 'donateditemdetails_admin.html', {'donation':donation, 'booking':booking})

@login_required(login_url='admin_login')
def donationrecdetail_admin(request, pid):
    donation = get_object_or_404(Donation, id=pid)
    booking = donation.bookings.first()  

    if request.method == 'POST':
        status = request.POST.get('status')
        try:
            donation.status = status
            donation.last_update = now().date()
            donation.save()
            messages.success(request, f"Donation status updated to {status}")
        except Exception as e:
            messages.warning(request, f"Error: {e}")    

    return render(request,'donationrecdetails_admin.html',{'donation': donation,'booking': booking,})
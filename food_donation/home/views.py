from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404,HttpResponseRedirect
from .forms import *
from django.contrib.auth import login,authenticate,logout,update_session_auth_hash
from .models import Donor
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date
from django.utils import timezone
from django.utils.timezone import now
# Create your views here.

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def user_register(request): 
    if request.method == 'POST':
        user_form = UserRegistration(request.POST)
        donor_form = DonorSignupForm(request.POST, request.FILES)
        if user_form.is_valid() and donor_form.is_valid() :
            user = user_form.save()

            donor = donor_form.save(commit=False)
            donor.user = user
            donor.save()

            messages.success(request, 'Registration successful!')
            return redirect('userlogin')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserRegistration()
        donor_form = DonorSignupForm()

    context = {
        'user_form': user_form,
        'donor_form': donor_form,

    }        
    return render(request, 'user_register.html', context)

def staff_register(request):
    if request.method == 'POST':
        user_form = UserRegistration(request.POST)
        staff_form = StaffSignupForm(request.POST, request.FILES)
        if user_form.is_valid() and staff_form.is_valid() :
            user = user_form.save()

            staff = staff_form.save(commit=False)
            staff.user = user
            staff.status = 'pending'
            staff.save()

            messages.success(request, 'Registration successful!')
            return redirect('stafflogin')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserRegistration()
        staff_form = StaffSignupForm()

    context = {
        'user_form': user_form,
        'donor_form': staff_form,

    }      
    return render(request, 'staff_register.html',context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            donor_user = Donor.objects.filter(user_id=user.id)
            if donor_user:
                login(request, user)
                return redirect('userhome')
            else:
                messages.warning(request, 'Invalid Donor User')
        else:
            messages.warning(request, 'Invalid username and password')        
    return render(request, 'user_login.html')

@login_required
def user_dashboard(request):
    profile = Donor.objects.get(user=request.user)
    return render(request, 'index-donor.html', {'profile':profile})

@login_required
def profile_donor(request):
    donor = get_object_or_404(Donor, user=request.user)

    user_form = UserRegistration(instance=request.user)
    donor_form = DonorSignupForm(instance=donor)

    if request.method == 'POST':
        try:
          
            user = request.user
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.save()
            
            donor.contact = request.POST.get('contact', donor.contact)
            donor.address = request.POST.get('address', donor.address)
            
            if 'profilepic' in request.FILES:
                donor.profilepic = request.FILES['profilepic']
            
            donor.save()
            
            messages.success(request, 'Profile updated successfully!', extra_tags='profile')
            return redirect('donorprofile')
            
        except Exception as e:
            messages.error(request, f'Profile update failed. Error: {str(e)}')

    context = {
        'user_form': user_form,
        'donor_form': donor_form,
        'donor': donor,
    }
    return render(request, 'profile_donor.html', context)     

@login_required
def index_donor(request):
    user = request.user
    donor = get_object_or_404(Donor, user=user)
    donation_count = Donation.objects.filter(donor=donor).count()
    accepted_count = Donation.objects.filter(donor=donor, status='accept').count()
    rejected_count = Donation.objects.filter(donor=donor, status='reject').count()
    pending_count = Donation.objects.filter(donor=donor, status='pending').count()
    given_count = Donation.objects.filter(donor=donor, status='Donation Given').count()

    context = {
        'donor':donor,
        'donation_count':donation_count,
        'accepted_count':accepted_count,
        'rejected_count':rejected_count,
        'pending_count':pending_count,
        'given_count':given_count
    }
    return render(request, 'index-donor.html', context)

def staff_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            staff_user = StaffProfile.objects.filter(user_id=user.id)
            if staff_user:
                login(request, user)
                return redirect('staffdash')
            else:
                messages.warning(request, 'Invalid Staff User')
        else:
            messages.warning(request, 'Invalid username and password')        
    return render(request, 'staff_login.html')

@login_required
def staff_dashboard(request):
    user = request.user
    staff = get_object_or_404(StaffProfile, user=user)
    totalDonations = Donation.objects.all().count()
    acceptedDonations = Donation.objects.filter(status='accept').count()
    pendingDonations = Donation.objects.filter( status='pending').count()
    totalDonationGiven = Donation.objects.filter( status='Donation Given').count()


    context = {
        'staff':staff,
        'totalDonations':totalDonations,
        'acceptedDonations':acceptedDonations,
        'pendingDonations':pendingDonations,
        'totalDonationGiven':totalDonationGiven
    }

    return render(request, 'staff_index.html', context)

@login_required
def profile_staff(request):
    staff = get_object_or_404(StaffProfile, user=request.user)

    staff_form = StaffSignupForm(instance=staff)

    if request.method == 'POST':
        try:

            user = request.user
            user.first_name = request.POST.get('first_name', user.first_name)
            user.last_name = request.POST.get('last_name', user.last_name)
            user.save()

            staff.contact = request.POST.get('contact', staff.contact)
            staff.address = request.POST.get('address', staff.address)
            staff.about = request.POST.get('about', staff.about)

            if 'profilepic' in request.FILES:
                staff.profilepic = request.FILES['profilepic']

            if 'idpic' in request.FILES:
                staff.idpic = request.FILES['idpic']

            staff.save()

            messages.success(request, 'Profile updated successfully!')
            return redirect('staffprofile')

        except Exception as e:
            messages.error(request, f'Profile update failed. Error: {str(e)}')

    context = {
        'staff_form': staff_form,
        'staff': staff,
    }
    return render(request, 'profile_staff.html', context)



def userlogout(request):
    logout(request)
    messages.success(request, 'Logout successful', extra_tags='auth')
    return redirect('home')

@login_required
def changepwd_donor(request):
    if request.method == 'POST':
        form = ChangePassword(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "✅ Your password has been successfully changed.")
            staff_user = StaffProfile.objects.filter(user_id=user.id)
            if user.is_superuser:
                return redirect('admin_dashboard')
            elif staff_user:
                return redirect('staffdash')
            else:
                return redirect('userdash')
       
    else:
        form = ChangePassword(user=request.user)

   
    return render(request, 'changepwd.html', {'form':form})

@login_required
def donate_now(request):
    if request.method == "POST":
        form = DonateNowForm(request.POST, request.FILES)
        if form.is_valid():
            donation = form.save(commit=False)
            donor = Donor.objects.get(user=request.user) 
            donation.donor = donor
            donation.status = "pending"
            donation.donation_date = date.today()
            donation.save()
            messages.success(request, "Donation submitted successfully", extra_tags='donate' )
            return redirect("donorindex")
    else:
        form = DonateNowForm()

    return render(request, "donatenow.html", {"form": form})       



@login_required(login_url='userlogin')
def donation_history(request):
    donor = Donor.objects.get(user=request.user)
    donations = Donation.objects.filter(donor=donor).order_by('-donation_date')
    
    context = {
        'donor': donor,
        'donations': donations
    }
    
    return render(request, 'donation_history.html', context)

@login_required(login_url='userlogin')
def rejecteddonation_donor(request):
    donor = Donor.objects.get(user=request.user)
    donations = Donation.objects.filter(donor=donor, status = 'reject')
    
    context = {
        'donor': donor,
        'donations': donations
    }
    
    return render(request, 'rejecteddonation_donor.html', context)

@login_required(login_url='userlogin')
def pendingdonation_donor(request):
    donor = get_object_or_404(Donor, user=request.user)
    donations = Donation.objects.filter(donor=donor, status = 'pending')
    context = {
        'donor': donor,
        'donations': donations
    }
    return render(request, 'pendingdonation_donor.html', context)

login_required(login_url='userlogin')
def accepteddonation_donor(request):
    donor = Donor.objects.get(user=request.user)
    donations = Donation.objects.filter(donor=donor, status='accept')
    
    context = {
        'donor': donor,
        'donations': donations
    }
    
    return render(request, 'accepteddonation_donor.html', context)

@login_required(login_url='userlogin')
def donationgiven_donor(request):
    donor = Donor.objects.get(user=request.user)
    donations = Donation.objects.filter(donor=donor, status='Donation Given')
    
    context = {
        'donor': donor,
        'donations': donations
    }
    
    return render(request, 'donationgiven_donor.html', context)

@login_required(login_url='userlogin')
def donation_details_donor(request, pid):
    donor_profile = Donor.objects.get(user=request.user)

    donation = get_object_or_404(Donation, id=pid, donor=donor_profile)
    return render(request, 'donationdetail_donor.html', {'donation': donation})

@login_required
def donationrec_staff(request):
    user = request.user
    staff = get_object_or_404(StaffProfile, user=user)
    donation = Donation.objects.filter(status='Donation Received')

    context = {
        'staff':staff,
        'donation':donation
    }
    return render(request, 'donationrec_volunteer.html', context)

@login_required
def donationnotrec_staff(request):
    user = request.user
    staff = get_object_or_404(StaffProfile, user=user)
    donation = Donation.objects.filter(staff=staff, status='Donation not Received')

    context = {
        'staff':staff,
        'donation':donation
    }
    return render(request, 'donationnotrec_volunteer.html', context)

@login_required
def donated_staff(request):
    user = request.user
    staff = get_object_or_404(StaffProfile, user=user)
    donation = Donation.objects.filter(status='Donation Given')

    context = {
        'staff':staff,
        'donation':donation
    }
    return render(request, 'donated_volunteer.html', context)

@login_required(login_url='stafflogin')
def incomingdonation_details(request, pid):
    donation = get_object_or_404(Donation, id=pid)

    if request.method == 'POST':
        status = request.POST.get('status')
        staffremark = request.POST.get('staffremark')

        try:
            donation.status = status
            donation.staffremark = staffremark
            donation.last_update = date.today()
            donation.save()
            messages.success(request, 'Staff Remark updated successfully')
        except:
            messages.warning(request, 'Failed to update Staff Remark')    

    return render(request, 'donationcollection_detail.html', {'donation':donation})

@login_required(login_url='stafflogin')
def donationrec_detail(request, pid):
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

    return render(request,'donationrec_detail.html',{'donation': donation,'booking': booking,})

@login_required
def viewdonationdetail_staff(request, pid):
    donation = get_object_or_404(Donation, id=pid)

    if request.method == 'POST':
        status = request.POST.get('status')
        staffremark = request.POST.get('staffremark')

        if not status:
            messages.error(request, 'Status is required' )
        else:

            try:
                donation.staffremark = staffremark
                donation.status = status
                donation.last_update = timezone.now().date()
                donation.save()
                messages.success(request, 'Status & Remark Updated Successfully' )

                return redirect('viewdonationdetail_staff', pid=pid)
            except Exception as e:

                messages.warning(request, f'Failed to Update Status & Remark: {e}')
    return render(request, "viewdonationdetail_staff.html", {'donation':donation})

@login_required(login_url='stafflogin')
def alldonations_staff(request):
    donation = Donation.objects.all()
    return render(request, 'alldonations_staff.html', {'donation': donation})

@login_required(login_url='stafflogin')
def pendingdonation_staff(request):
    donation = Donation.objects.filter(status='pending')
    return render(request, 'pendingdonation_staff.html', {'donation':donation})

@login_required(login_url='stafflogin')
def accepteddonation_staff(request):
    donation = Donation.objects.filter(status='accept')
    return render(request, 'accepteddonation_staff.html', {'donation':donation} )

@login_required(login_url='stafflogin')
def rejecteddonation_staff(request):
    donation = Donation.objects.filter(status='reject')
    return render(request, 'rejecteddonation_staff.html', {'donation':donation} )


@login_required
def available_donations(request):
    current_donor = request.user.donor

    donations = Donation.objects.filter(status="Donation Received").exclude(donor=current_donor)
    context = {
        "donations": donations
    }
    return render(request, "userhome.html", context)


@login_required
def book_donation(request, donation_id):
    donor = request.user.donor
    donation = get_object_or_404(Donation, id=donation_id, status="Donation Received")

    if donation.donor == donor:
        messages.error(request, "You cannot book your own donation.")
        return redirect("userhome")

    if hasattr(donation, "booking"):
        messages.error(request, "This donation has already been booked.")
        return redirect("userhome")

    Booking.objects.create(donation=donation, booked_by=donor)
    messages.success(request, "You have successfully booked this donation.")
    return redirect("userhome")

@login_required
def mark_reached(request, pid):
    donation = get_object_or_404(Donation, id=pid, donor__user=request.user)

    if request.method == 'POST':
        donation.reached_location = True
        donation.last_update = now().today()
        donation.save()
        messages.success(request, "Marked as reached donation center.", extra_tags="donation")

    return redirect("dondetails", pid=donation.id)    

@login_required
def donateditemdetails_staff(request, pid):
    donation = get_object_or_404(Donation, id=pid)
    booking = donation.bookings.first() 
    return render(request, 'donateditemdetails_staff.html', {'donation':donation, 'booking':booking})

@login_required
def donateditemdetails_donor(request, pid):
    donation = get_object_or_404(Donation, id=pid)
    booking = donation.bookings.first() 
    return render(request, 'donateditemdetails_donor.html', {'donation':donation, 'booking':booking})


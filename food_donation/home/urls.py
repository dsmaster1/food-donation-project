from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', home, name='home'),
    path('about', about, name='about'),
    path('contact', contact, name='contact'),
    path('userlogin', user_login, name='userlogin'),
    path('stafflogin', staff_login, name='stafflogin'),
    path('userregister', user_register, name='uregister'),
    path('staffregister', staff_register, name='sregister'),
    path('userdashboard', user_dashboard, name='userdash'),
    path('donorindex', index_donor, name='donorindex'),
    path('staffdashboard', staff_dashboard, name='staffdash'),
    path('userhome', available_donations, name='userhome'),
    path('logout', userlogout, name='logout'),
    path('passchangedonor', changepwd_donor, name='dpwdchange'),
    path('donatenow', donate_now, name='donnow'),
    path('donatehistory', donation_history, name='donhistory'),
    path('donatedetails/<int:pid>/', donation_details_donor, name='dondetails'),
    path('donorprofile', profile_donor, name='donorprofile'),
    path('donationreceived_staff', donationrec_staff, name='donreceived'),
    path('donnotreceived_staff', donationnotrec_staff, name='donnorec'),
    path('donated_staff', donated_staff, name='donatedstaff'),
    path('staffprofile', profile_staff, name='staffprofile'),
    path('donationincoming/<int:pid>', incomingdonation_details, name='donationincoming'),
    path('donationrec_detail/<int:pid>', donationrec_detail, name='donationrec_detail'),
    path('alldonation_staff',alldonations_staff, name='alldonation_staff' ),
    path('pendingdonation_staff', pendingdonation_staff, name='pendingdonation_staff'),
    path('pendingdonation_donor', pendingdonation_donor, name='pendingdonation_donor'),
    path('accepteddonation_staff', accepteddonation_staff, name='accepteddonation_staff'),
    path("book-donation/<int:donation_id>/", book_donation, name="book_donation"),
    path('rejecteddonation_staff', rejecteddonation_staff, name='rejecteddonation_staff'),
    path("viewdonationdetail_staff/<int:pid>",viewdonationdetail_staff,name="viewdonationdetail_staff"),
    path('rejecteddonation_donor', rejecteddonation_donor, name='rejecteddonation_donor'),
    path('accepteddonation_donor', accepteddonation_donor, name='accepteddonation_donor'),
    path('donation/<int:pid>/reached/', mark_reached, name='mark_reached'),
    path('donateditemdetails_staff/<int:pid>', donateditemdetails_staff, name='donateditemdetails_staff'),
    path('donateditemdetails_donor/<int:pid>', donateditemdetails_donor, name='donateditemdetails_donor'),
    path('donationgiven_donor', donationgiven_donor, name='donationgiven_donor'),


    #Password Reset

    # Password reset - request email
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html'
    ), name='password_reset'),

    # Email sent page
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),

    # Password reset confirm (link from email)
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    # Password reset complete page
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.urls import path
from .views import *
urlpatterns = [
    path('', admin_login, name='admin_login'),
    path('admin_dashboard/', admin_dashboard, name='index_admin'),
    path('admin-logout', logoutpage, name='adlogout'),
    path('managedonor', manage_donor, name='managedonor'),
    path('accepted_volunteer', accepted_volunteers, name='accvolunteer'),
    path('new_volunteer', new_volunteer, name='new_volunteer'),
    path('all_donations', all_donations, name='alldonations'),
    path('rejected_volunteer', rejected_volunteers, name='rejected_volunteer'),
    path('all_volunteers', all_volunteers, name='all_volunteers'),
    path('manage_area', manage_area, name='managearea'),
    path('pending_donation', pending_donation, name='pendingdonation'),
    path('accepted_donation', accepted_donation, name='accepteddonation'),
    path('rejected_donation', rejected_donation, name='rejected_donation'),
    path('donationgivenadmin', donation_given, name='donationgivenad'),
    path("view-donationdetail/<int:pid>",view_donationdetail,name="view_donationdetail"),
    path('donationrec_admin', donationrec_admin, name='donationrec_admin'),
    path('donationnotrec_admin', donationnotrec_admin, name='donationnotrec_admin'),
    path('donationincoming_admin/<int:pid>', incomingdonationdetails_admin, name='donationincoming_admin'),
    
    
    path('viewdonor_details/<int:pid>', donor_details, name='viewdonor_details'),
    path('view_volunteerdetails/<int:pid>/', view_volunteerdetails, name='view_volunteerdetail'),
    
    path('add_area', add_area, name='addarea'),
    path('edit_area/<int:pid>', edit_area, name='editarea'),
    path('donateditem_details/<int:pid>', donateditemdetails_admin, name='donateditem_details'),
    path('donationrecdetails_admin/<int:pid>', donationrecdetail_admin, name='donationrecdetails_admin'),
  
    # delete
    path('delete_area/<int:pid>',delete_area, name='deletearea'),
    path('delete_donor/<int:pid>', delete_donor, name='deletedonor'),
    path('delete_volunteer/<int:pid>/', delete_volunteer, name='delete_volunteer'),
    path('delete_donation/<int:pid>', delete_donation, name='delete_donation'),

]
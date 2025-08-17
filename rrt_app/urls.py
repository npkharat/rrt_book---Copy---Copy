from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_issue, name='create_issue'),
    path('list/', views.issue_list, name='issue_list'),
    path('approve/<int:pkt_id>/', views.approve_issue, name='approve_issue'),
    path('disapprove/<int:pkt_id>/', views.disapprove_issue, name='disapprove_issue'),
    path('delete/<int:pkt_id>/', views.delete_issue, name='delete_issue'),
    path('edit/<int:pkt_id>/', views.edit_issue, name='edit_issue'),
    path('view_data/', views.view_data, name='view_data'),
    path('dashboard/', views.troubleshooting_dashboard, name='troubleshooting_dashboard'),
    path('ajax/search/', views.ajax_issue_search, name='ajax_issue_search'),
]

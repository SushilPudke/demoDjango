from django.urls import path

from .views import EmployeeListView, EmployeeManagementView, InviteUserAPIView

urlpatterns = [
    path('invite/', InviteUserAPIView.as_view(), name='invite_employee'),
    path('employees/', EmployeeListView.as_view(), name='employees_list'),
    path('employees/<int:pk>/', EmployeeManagementView.as_view(), name='employees_detail'),
]

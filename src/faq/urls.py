from django.urls import path

from .views import QuestionListView, ContactFormApiView


urlpatterns = [
    path('questions/', QuestionListView.as_view(), name='question-list'),
    path('contact_form/', ContactFormApiView.as_view(), name='contact_form'),
]

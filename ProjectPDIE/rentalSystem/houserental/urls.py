from django.urls import path
from . import views

app_name = 'houserental'

urlpatterns = [
    path('index/', views.index, name= 'test'),
    path('index/landlog/', views.landlog , name = 'landlog'),
    path('index/landRegister/', views.landRegister, name='landRegister'),
    path('index/landlog/landDash/', views.landDash , name='landDash'),
    path('index/landlog/landTenant/', views.landTenant , name='landTenant'),
    path('index/landlog/landProp/', views.landProp , name='landProp'),
    path('index/landlog/landProp/landAddprop/', views.landAddprop , name='landAddprop'),
    path('index/landlog/landReport/', views.landReport , name='landReport'),
    path('index/landlog/landReport/monthlyReport/',views.landMonthly, name='montlyreport'),
    path('index/landlog/landReport/mainSummary/',views.mainSummary, name='mainSummary'),
    path('index/landlog/landProp/deleteProp/<str:propID>/', views.deleteProp , name='deleteProp'),
    path('index/landlog/landProp/deleteProp/<str:propID>/', views.deleteProp , name='deleteProp'),
    
    path('index/studlog/', views.studlog , name = 'studlog'),
    path('index/studRegister/', views.studRegister, name='studRegister'),    
    path('index/studlog/studDash/', views.studDash , name='studDash'),    
    path('index/studlog/studRent/', views.studRent , name='studRent'),
    path('index/studlog/studService/', views.studService , name='studService'),
    path('index/studlog/studProfile/', views.studProfile , name='studProfile'),
    path('index/studlog/studDash/payment/', views.payment , name='payment'),

    path('index/admin/', views.admin , name='admin'),
     path('index/adminlog/', views.adminlog , name='adminlog'),


] 
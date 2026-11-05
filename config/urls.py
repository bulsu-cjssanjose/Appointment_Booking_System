from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/appointments/')), 
    path('admin/', admin.site.urls),
    path('appointments/', include('appointments.urls')),
]
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from boxes.views import BoxStatusListView, BoxDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/boxes/status/', BoxStatusListView.as_view(), name='box-status'),
    path('api/boxes/<int:idBox>/detail/', BoxDetailView.as_view(), name='box-detail'),
]

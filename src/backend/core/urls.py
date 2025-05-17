from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from boxes.views import boxes_stream, BoxDetalleView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("api/boxes/stream/", boxes_stream),
    path("api/boxes/<int:idBox>/detalle/", BoxDetalleView.as_view()),
]
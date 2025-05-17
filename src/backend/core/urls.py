from django.contrib import admin
from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView

from boxes.views import BoxStatusListView, boxes_stream, ReporteKPIView, BoxDetailView
#

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("api/boxes/status/", BoxStatusListView.as_view()),
    path("api/boxes/stream/", boxes_stream),
    path("api/boxes/<int:idBox>/detalle/", BoxDetailView.as_view()),
    path("api/boxes/reportes/", ReporteKPIView.as_view()),
]

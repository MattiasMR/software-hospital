from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from boxes.views import (
  boxes_stream, 
  BoxDetalleView, 
  BoxStatusListView, 
  ReportesView,
  ResumenDashboardView,
  BuscarMedicosView,
  BoxDetalleV2View
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("api/boxes/status/", BoxStatusListView.as_view(), name="boxes-status"),
    path("api/boxes/stream/", boxes_stream, name="boxes-stream"),
    path("api/boxes/<int:idBox>/detalle/", BoxDetalleView.as_view(), name="box-detalle"),
    path('api/boxes/reportes/', ReportesView.as_view(),    name='boxes-reportes'),
    path("api/resumen/", ResumenDashboardView.as_view(), name="resumen-dashboard"),
    path("api/medicos/", BuscarMedicosView.as_view(), name="buscar-medicos"),
    path('api/boxes/<int:idBox>/detalle-v2/', BoxDetalleV2View.as_view(), name='box-detalle-v2'),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'mappings', views.MappingViewSet, basename='mapping')

urlpatterns = [
    path('', include(router.urls)),
    path('mappings/by-patient/<int:patient_id>/', views.PatientDoctorsView.as_view({'get': 'list'}), name='patient-doctors'),
]

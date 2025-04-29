from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'job-postings', views.JobPostingViewSet)
router.register(r'applications', views.JobApplicationViewSet)
router.register(r'interviews', views.InterviewViewSet)
router.register(r'marital-status', views.MaritalStatusViewSet)
router.register(r'family-policy-types', views.FamilyPolicyTypeViewSet)
router.register(r'genders', views.GenderViewSet)
router.register(r'education-levels', views.EducationLevelViewSet)

# Public API endpoints
public_router = DefaultRouter()
public_router.register(r'job-postings', views.PublicJobPostingViewSet)
public_router.register(r'applications', views.PublicJobApplicationCreateView)
public_router.register(r'marital-status', views.MaritalStatusViewSet)
public_router.register(r'family-policy-types', views.FamilyPolicyTypeViewSet)
public_router.register(r'genders', views.GenderViewSet)
public_router.register(r'education-levels', views.EducationLevelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('public/', include(public_router.urls)),
    path('public/departments/', views.public_departments, name='public-departments'),
    path('public/factories/', views.public_factories, name='public-factories'),
    path('dashboard/stats/', views.dashboard_stats, name='dashboard-stats'),
]

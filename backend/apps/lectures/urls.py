from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .viewsets import LectureViewSet, LectureCategoryViewSet

app_name = 'blog'

urlpatterns = [
    path('lectures/', views.LectureListView.as_view(), name='lectures'),
    path('lecture/create/', views.create_lecture, name='create_lecture'),
    path('lecture/<int:pk>/edit/', views.edit_lecture, name='edit_lecture'),
    path('lecture/<int:pk>/delete/', views.delete_lecture, name='delete_lecture'),
    path('lecture/import/', views.import_lecture, name='import_lecture'),
    path('lecture/import-directory/', views.import_lectures_from_directory, name='import_lectures_from_directory'),
]

# REST API routes for frontend (Vue)Vite
router = DefaultRouter()
router.register(r'api/lecture-categories', LectureCategoryViewSet, basename='lecture-category')
router.register(r'api/lectures', LectureViewSet, basename='lecture')

urlpatterns += router.urls



from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count
from .models import Lecture, LectureCategory
from .serializers import LectureSerializer, LectureCategorySerializer


class LectureCategoryViewSet(ModelViewSet):
    queryset = LectureCategory.objects.all().order_by('name')
    serializer_class = LectureCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @action(detail=False, methods=['get'])
    def with_counts(self, request):
        data = Lecture.objects.filter(is_active=True).values('category__id', 'category__name', 'category__slug').annotate(count=Count('id')).order_by('category__name')
        return Response(data)


class LectureViewSet(ModelViewSet):
    queryset = Lecture.objects.filter(is_active=True).select_related('category', 'author')
    serializer_class = LectureSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(author=user)



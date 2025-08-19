from django.db.models import Count
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import GutierrezTemplate, RossiTemplate
from .serializers import GutierrezTemplateSerializer, RossiTemplateSerializer


class GutierrezTemplateViewSet(viewsets.ModelViewSet):
    queryset = GutierrezTemplate.objects.filter(is_active=True)
    serializer_class = GutierrezTemplateSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "category", "content"]
    ordering = ["-updated_at"]

    def get_queryset(self):
        queryset = super().get_queryset()
        created_by_id = self.request.query_params.get('created_by_id', None)
        if created_by_id is not None:
            if created_by_id == 'null':
                queryset = queryset.filter(created_by_id__isnull=True)
            else:
                queryset = queryset.filter(created_by_id=created_by_id)
        return queryset

    @action(detail=False, methods=["get"], url_path="categories")
    def categories(self, request):
        queryset = self.get_queryset()
        categories = (
            queryset.values("category")
            .annotate(count=Count("id"))
            .order_by("category")
        )
        return Response(list(categories))

    def destroy(self, request, *args, **kwargs):
        # Soft delete: mark is_active=False
        instance = self.get_object()
        instance.is_active = False
        instance.save(update_fields=["is_active", "updated_at"])
        return Response(status=status.HTTP_204_NO_CONTENT)


class RossiTemplateViewSet(viewsets.ModelViewSet):
    queryset = RossiTemplate.objects.filter(is_active=True)
    serializer_class = RossiTemplateSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "category", "content"]
    ordering = ["-updated_at"]

    @action(detail=False, methods=["get"], url_path="categories")
    def categories(self, request):
        categories = (
            self.queryset.values("category")
            .annotate(count=Count("id"))
            .order_by("category")
        )
        return Response(list(categories))

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.is_active = False
        instance.save(update_fields=["is_active", "updated_at"])
        return Response(status=status.HTTP_204_NO_CONTENT)


# Create your views here.

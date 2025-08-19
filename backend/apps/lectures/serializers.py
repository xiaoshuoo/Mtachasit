from rest_framework import serializers
from .models import Lecture, LectureCategory


class LectureCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LectureCategory
        fields = ["id", "name", "slug", "icon", "description", "created_at"]


class LectureSerializer(serializers.ModelSerializer):
    lines_count = serializers.SerializerMethodField()
    category = LectureCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=LectureCategory.objects.all(), source='category', write_only=True, allow_null=True, required=False
    )

    class Meta:
        model = Lecture
        fields = [
            "id", "title", "content", "category", "category_id", "author", "created_at", "updated_at", "is_active", "lines_count"
        ]
        read_only_fields = ("author", "created_at", "updated_at")

    def get_lines_count(self, obj):
        return len([l for l in (obj.content or '').split('\n') if l.strip()])



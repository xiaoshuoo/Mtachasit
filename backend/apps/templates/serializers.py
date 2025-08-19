from rest_framework import serializers
from .models import GutierrezTemplate, RossiTemplate


class GutierrezTemplateSerializer(serializers.ModelSerializer):
    lines_count = serializers.SerializerMethodField()

    class Meta:
        model = GutierrezTemplate
        fields = [
            'id',
            'title',
            'category',
            'content',
            'created_by_id',
            'slug',
            'created_at',
            'updated_at',
            'lines_count',
        ]

    def get_lines_count(self, obj):
        return len([line for line in (obj.content or '').split('\n') if line.strip()])


class RossiTemplateSerializer(serializers.ModelSerializer):
    lines_count = serializers.SerializerMethodField()

    class Meta:
        model = RossiTemplate
        fields = [
            'id', 'title', 'category', 'content', 'slug', 'created_at', 'updated_at', 'lines_count'
        ]

    def get_lines_count(self, obj):
        return len([line for line in (obj.content or '').split('\n') if line.strip()])



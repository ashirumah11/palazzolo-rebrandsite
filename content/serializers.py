from rest_framework import serializers
from .models import Announcement, StaffMember, EventItem, Testimonial, GalleryItem, HeroCarouselItem, EventRegistration


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class StaffMemberSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = StaffMember
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        try:
            if obj.image and hasattr(obj.image, 'url'):
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(obj.image.url)
                return obj.image.url
            return None
        except Exception:
            return None


class EventItemSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = EventItem
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        try:
            if obj.image and hasattr(obj.image, 'url'):
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(obj.image.url)
                return obj.image.url
            return None
        except Exception:
            return None


class TestimonialSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Testimonial
        fields = '__all__'
        read_only_fields = ['id', 'created_at']

    def get_image_url(self, obj):
        try:
            if obj.image and hasattr(obj.image, 'url'):
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(obj.image.url)
                return obj.image.url
            return None
        except Exception:
            return None


class GalleryItemSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    media_type = serializers.CharField(read_only=True)
    is_youtube_video = serializers.BooleanField(read_only=True)
    youtube_video_id = serializers.CharField(read_only=True)
    embed_url = serializers.SerializerMethodField()
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = GalleryItem
        fields = [
            'id', 'title', 'image', 'image_url', 'video_url',
            'media_type', 'is_youtube_video', 'youtube_video_id', 'embed_url',
            'caption', 'alt_text', 'category', 'category_display',
            'is_active', 'order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'media_type',
                            'is_youtube_video', 'youtube_video_id', 'embed_url', 'category_display']

    def get_image_url(self, obj):
        try:
            if obj.image and hasattr(obj.image, 'url'):
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(obj.image.url)
                return obj.image.url
            return None
        except Exception:
            return None

    def get_embed_url(self, obj):
        try:
            return obj.get_embed_url()
        except Exception:
            return None


class HeroCarouselItemSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = HeroCarouselItem
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        try:
            if obj.image and hasattr(obj.image, 'url'):
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(obj.image.url)
                return obj.image.url
            return None
        except Exception:
            return None


class EventRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRegistration
        fields = '__all__'
        read_only_fields = ['id', 'registered_at']
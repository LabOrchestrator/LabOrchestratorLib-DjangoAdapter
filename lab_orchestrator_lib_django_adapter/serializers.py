from django.contrib.auth import get_user_model
from rest_framework import serializers

from lab_orchestrator_lib_django_adapter.models import LabModel, LabInstanceModel, DockerImageModel


class FixedRelatedField(serializers.PrimaryKeyRelatedField):
    """The PrimaryKeyRelatedField has a bug, that doesn't allow you to save the object if you only refer to the id of
    an attribute. That's due to the to_internal_value method returning an object instead of the id."""

    def to_internal_value(self, data):
        """The base implementation converts the pk to an object and this breaks the saving."""
        data = super().to_internal_value(data)
        return data.id


class DockerImageModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = DockerImageModel
        fields = '__all__'


class LabModelDockerImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DockerImageModel
        fields = '__all__'


class LabModelSerializer(serializers.ModelSerializer):
    docker_image = LabModelDockerImageSerializer(many=False, read_only=True)
    docker_image_id = FixedRelatedField(queryset=DockerImageModel.objects.all(), write_only=False, many=False,
                                        read_only=False, label='Docker Image', required=True)

    class Meta:
        model = LabModel
        fields = '__all__'


class LabInstanceModelLabSerializer(serializers.ModelSerializer):
    docker_image = LabModelDockerImageSerializer(many=False, read_only=True)

    class Meta:
        model = LabModel
        fields = '__all__'


class LabInstanceModelUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username']


class LabInstanceModelSerializer(serializers.ModelSerializer):
    lab = LabInstanceModelLabSerializer(many=False, read_only=True)
    user = LabInstanceModelUserSerializer(many=False, read_only=True)

    class Meta:
        model = LabInstanceModel
        fields = '__all__'


class LabInstanceKubernetesSerializer(serializers.Serializer):
    lab = LabInstanceModelLabSerializer(many=False, read_only=True)
    user = LabInstanceModelUserSerializer(many=False, read_only=True)
    lab_id = FixedRelatedField(queryset=LabModel.objects.all(), write_only=False, many=False,
                               read_only=False, label='Lab', required=True)
    user_id = FixedRelatedField(many=False, read_only=True, label='User', required=False)
    jwt_token = serializers.CharField(read_only=True)

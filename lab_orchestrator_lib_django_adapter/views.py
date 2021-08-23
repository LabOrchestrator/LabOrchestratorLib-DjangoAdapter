from rest_framework import viewsets, permissions

from lab_orchestrator_lib_django_adapter.controller_collection import get_default_cc
from lab_orchestrator_lib_django_adapter.models import LabInstanceModel, LabModel, DockerImageModel
from lab_orchestrator_lib_django_adapter.serializers import LabInstanceModelSerializer, LabInstanceKubernetesSerializer, \
    LabModelSerializer, DockerImageModelSerializer


class DockerImageViewSet(viewsets.ModelViewSet):
    #permission_classes = [permissions.IsAuthenticated]
    queryset = DockerImageModel.objects.all()
    serializer_class = DockerImageModelSerializer


class LabViewSet(viewsets.ModelViewSet):
    #permission_classes = [permissions.IsAuthenticated]
    queryset = LabModel.objects.all()
    serializer_class = LabModelSerializer


class LabInstanceViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = LabInstanceModel.objects.all()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cc = get_default_cc()

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        if not bool(self.request.user and self.request.user.is_staff):
            # all memberships that i'm allowed to see
            queryset = queryset.filter(user_id=self.request.user.id)
        return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return LabInstanceKubernetesSerializer
        return LabInstanceModelSerializer

    def create(self, request, *args, **kwargs):
        lab_id = request.POST.get("lab_id")
        lab_instance_kubernetes = self.cc.lab_instance_ctrl.create(lab_id=lab_id, user_id=request.user.id)
        serializer = LabInstanceKubernetesSerializer(lab_instance_kubernetes)
        return self.get_serializer(serializer.data, many=False)

    def destroy(self, request, *args, **kwargs):
        mod = self.get_object()
        obj = self.cc.lab_instance_ctrl.adapter.to_obj(mod)
        self.cc.lab_instance_ctrl.delete(obj)

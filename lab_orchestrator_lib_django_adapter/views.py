from rest_framework import viewsets, permissions

from lab_orchestrator_lib_django_adapter.controller_collection import get_default_cc
from lab_orchestrator_lib_django_adapter.models import LabInstanceModel, LabModel, DockerImageModel
from lab_orchestrator_lib_django_adapter.serializers import LabInstanceModelSerializer, LabInstanceKubernetesSerializer, \
    LabModelSerializer, DockerImageModelSerializer


class IsAdminOrReadOnly(BasePermission):
    """
    The request is authenticated as an admin, or is a read-only request.
    """

    def has_permission(self, request, view):
        return bool(request.method in SAFE_METHODS or (request.user and request.user.is_staff))


class DockerImageViewSet(viewsets.ModelViewSet):
    """Example ViewSet for docker images.

    Only admins can edit and add docker images. Everyone (even not authenticated users) can use the list and retrieve
    methods.

    This doesn't need to use the docker image controller, because the controller has no special implementation of the
    create or delete methods and it's save to manipulate the database objects directly without the controller.
    """
    permission_classes = [IsAdminOrReadOnly]
    queryset = DockerImageModel.objects.all()
    serializer_class = DockerImageModelSerializer


class LabViewSet(viewsets.ModelViewSet):
    """Example ViewSet for labs.

    Only admins can edit and add labs. Everyone (even not authenticated users) can use the list and retrieve
    methods.

    This doesn't need to use the lab controller, because the controller has no special implementation of the
    create or delete methods and it's save to manipulate the database objects directly without the controller.
    """
    permission_classes = [IsAdminOrReadOnly]
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

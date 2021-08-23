from django.conf import settings
from lab_orchestrator_lib.controller.controller_collection import create_controller_collection, ControllerCollection
from lab_orchestrator_lib.kubernetes.api import APIRegistry
from lab_orchestrator_lib.kubernetes.config import get_development_config, get_kubernetes_config, get_registry, \
    KubernetesConfig

from lab_orchestrator_lib_django_adapter.adapter import UserDjangoAdapter, LabInstanceDjangoAdapter, LabDjangoAdapter, \
    DockerImageDjangoAdapter


def create_django_controller_collection(registry: APIRegistry, secret_key: str):
    user_adapter = UserDjangoAdapter()
    docker_image_adapter = DockerImageDjangoAdapter()
    lab_adapter = LabDjangoAdapter()
    lab_instance_adapter = LabInstanceDjangoAdapter()
    return create_controller_collection(
        registry=registry,
        user_adapter=user_adapter,
        docker_image_adapter=docker_image_adapter,
        lab_adapter=lab_adapter,
        lab_instance_adapter=lab_instance_adapter,
        secret_key=secret_key,
    )


def get_default_cc(kubernetes_config: KubernetesConfig = None, registry: APIRegistry = None,
                   controller_collection: ControllerCollection = None, secret_key: str = None):
    if secret_key is None:
        secret_key = settings.SECRET_KEY
    if kubernetes_config is None:
        if settings.DEVELOPMENT:
            kubernetes_config = get_development_config()
        else:
            kubernetes_config = get_kubernetes_config()
    if registry is None:
        registry = get_registry(kubernetes_config)
    if controller_collection is None:
        return create_django_controller_collection(registry, secret_key)
    return controller_collection

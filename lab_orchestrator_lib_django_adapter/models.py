from django.db import models
from django.contrib.auth import get_user_model


class DockerImageModel(models.Model):
    name = models.CharField(max_length=32, unique=True, null=False)
    description = models.CharField(max_length=128, null=True)
    url = models.CharField(max_length=256, null=False)

    def __str__(self):
        return f"{self.name}: {self.url} ({self.pk})"


class LabModel(models.Model):
    name = models.CharField(max_length=32, unique=True, null=False)
    namespace_prefix = models.CharField(max_length=32, unique=True, null=False)
    description = models.CharField(max_length=128, null=True)
    docker_image = models.ForeignKey(DockerImageModel, on_delete=models.DO_NOTHING, null=False, related_name="labs")
    docker_image_name = models.CharField(max_length=32, null=False)

    def __str__(self):
        return f"{self.name}: {self.docker_image} ({self.docker_image_name}) ({self.pk})"


class LabInstanceModel(models.Model):
    lab = models.ForeignKey(LabModel, on_delete=models.CASCADE, null=False, related_name="lab_instances")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=False, related_name="lab_instances")

    def __str__(self):
        return f"{self.lab.name} - {self.user.pk} ({self.pk})"

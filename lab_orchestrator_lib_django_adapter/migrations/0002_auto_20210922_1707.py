# Generated by Django 3.2.6 on 2021-09-22 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lab_orchestrator_lib_django_adapter', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='labmodel',
            name='docker_image',
        ),
        migrations.RemoveField(
            model_name='labmodel',
            name='docker_image_name',
        ),
        migrations.CreateModel(
            name='LabDockerImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docker_image_name', models.CharField(max_length=32)),
                ('docker_image', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='lab_docker_images', to='lab_orchestrator_lib_django_adapter.dockerimagemodel')),
                ('lab', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='lab_docker_images', to='lab_orchestrator_lib_django_adapter.labmodel')),
            ],
        ),
    ]

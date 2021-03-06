# Generated by Django 3.2.6 on 2021-09-28 09:19

from django.db import migrations, models
import lab_orchestrator_lib_django_adapter.models


class Migration(migrations.Migration):

    dependencies = [
        ('lab_orchestrator_lib_django_adapter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dockerimagemodel',
            name='description',
            field=models.CharField(max_length=128, null=True, validators=[lab_orchestrator_lib_django_adapter.models.not_empty]),
        ),
        migrations.AlterField(
            model_name='dockerimagemodel',
            name='name',
            field=models.CharField(max_length=32, unique=True, validators=[lab_orchestrator_lib_django_adapter.models.not_empty]),
        ),
        migrations.AlterField(
            model_name='dockerimagemodel',
            name='url',
            field=models.CharField(max_length=256, validators=[lab_orchestrator_lib_django_adapter.models.not_empty]),
        ),
        migrations.AlterField(
            model_name='labdockerimagemodel',
            name='docker_image_name',
            field=models.CharField(max_length=32, validators=[lab_orchestrator_lib_django_adapter.models.validate_dns_subdomain, lab_orchestrator_lib_django_adapter.models.not_empty]),
        ),
        migrations.AlterField(
            model_name='labmodel',
            name='description',
            field=models.CharField(max_length=128, null=True, validators=[lab_orchestrator_lib_django_adapter.models.not_empty]),
        ),
        migrations.AlterField(
            model_name='labmodel',
            name='name',
            field=models.CharField(max_length=32, unique=True, validators=[lab_orchestrator_lib_django_adapter.models.not_empty]),
        ),
        migrations.AlterField(
            model_name='labmodel',
            name='namespace_prefix',
            field=models.CharField(max_length=32, unique=True, validators=[lab_orchestrator_lib_django_adapter.models.validate_dns_label, lab_orchestrator_lib_django_adapter.models.not_empty]),
        ),
    ]

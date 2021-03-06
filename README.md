[![Status](https://img.shields.io/pypi/status/lab-orchestrator-lib-django-adapter)](https://pypi.org/project/lab-orchestrator-lib-django-adapter/)
[![Version](https://img.shields.io/pypi/v/lab-orchestrator-lib-django-adapter?label=release)](https://pypi.org/project/lab-orchestrator-lib-django-adapter/)
[![License](https://img.shields.io/github/license/laborchestrator/laborchestratorlib-djangoadapter)](https://github.com/LabOrchestrator/laborchestratorlib-djangoadapter/blob/main/LICENSE)
[![Issues](https://img.shields.io/github/issues/laborchestrator/laborchestratorlib-djangoadapter)](https://github.com/laborchestrator/laborchestratorlib-djangoadapter/issues)
[![Downloads](https://img.shields.io/pypi/dw/lab-orchestrator-lib-django-adapter)](https://pypi.org/project/lab-orchestrator-lib-django-adapter/)
[![Dependencies](https://img.shields.io/librariesio/release/pypi/lab-orchestrator-lib-django-adapter)](https://libraries.io/pypi/lab-orchestrator-lib-django-adapter)
[![Docs](https://img.shields.io/readthedocs/laborchestratorlib-djangoadapter)](https://laborchestratorlib-djangoadapter.readthedocs.io/en/latest/)

# Lab Orchestrator Lib Django Adapter

This package implements the adapters to use the
[lab orchestrator library](https://github.com/LabOrchestrator/LabOrchestratorLib)
in django projects. That means that some data of the lab orchestrator library will be saved
in the django database.

[Github](https://github.com/LabOrchestrator/LabOrchestratorLib-DjangoAdapter)  
[PyPi](https://pypi.org/project/lab-orchestrator-lib-django-adapter/)  
[Read The Docs](https://laborchestratorlib-djangoadapter.readthedocs.io/en/latest/index.html)


## Setup
### Installation
Install this library with: `pip install lab-orchestrator-lib-django-adapter`.

### Project setup
Assuming you have a django application, first define the following variables in your `settings.py`:

- `DEVELOPMENT` (bool): If this is true the development mode is activated. This means, that no cacert is used and
  insecure certs are allowed. If false this assumes you are running this inside a Kubernetes cluster.
- `SECRET_KEY` (str): This key is used to create jwt tokens. Create a random key for this and keep this key safe.

After that add `lab_orchestrator_lib_django_adapter` to the `INSTALLED_APPS` variable in your `settings.py`.

### Environment Variables
The library makes use of some environment variables that you need to set:
- `KUBERNETES_SERVICE_HOST` (str): Host of your Kubernetes API (if you run `kubectl proxy`: `localhost`)
- `KUBERNETES_SERVICE_PORT` (int): Port of your Kubernetes API (if you run `kubectl proxy`: `8001`)
- `DEVELOPMENT` (bool): If this is true the development mode is activated. This means, that no cacert is used and
  insecure certs are allowed. If false this assumes you are running this inside a Kubernetes cluster.

## Usage

You have three Model classes:

- `DockerImageModel`
- `LabModel`
- `LabInstanceModel`

Those three models are used to save data from the library in the django database and those can all be used safely in
read only view sets. The `DockerImageModel` and `LabModel` can also be used safely in a delete, update and create view
sets. To create and delete a `LabInstanceModel` you need to use the lab instance controller. Updating a
`LabInstanceModel` is not allowed.

To get extra information from Kubernetes resources you need to use the controllers.

A default `ControllerCollection` can be got with the `get_default_cc` method in
`lab_orchestrator_lib_django_adapter.controller_collection` module. The controllers are part of the lab orchestrator lib
and there you can find documentation about how to use this.

An example on how to use this library in `ViewSets` can be found in the
[views.py](https://github.com/LabOrchestrator/LabOrchestratorLib-DjangoAdapter/blob/main/lab_orchestrator_lib_django_adapter/views.py).

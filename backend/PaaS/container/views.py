import docker
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

# set docker client
from django.views.decorators.http import require_GET, require_POST

from container.container_controller import *

docker_client = docker.from_env()


#
@require_GET
def _container(request):
    container_id = str(request.GET.get('container_id'))
    try:
        return JsonResponse({'errno': 0})
    except:
        return JsonResponse({'errno': 1})


# 查看容器列表
@require_GET
def list_container(request):
    try:
        container_list = ctn_list()
        return JsonResponse({'errno': 0, 'container_list': container_list})
    except:
        return JsonResponse({'errno': 1, 'container_list': []})


# 查看容器信息
@require_GET
def get_container(request):
    container_id = str(request.GET.get('container_id'))
    try:
        res = ctn_get(container_id)
        return JsonResponse({'errno': 0, 'res': res})
    except:
        return JsonResponse({'errno': 1})


# 新建容器
@require_POST
def create_container(request):
    image_name = str(request.GET.get('image_name'))
    inner_port = str(request.GET.get('inner_port'))
    outer_port = str(request.GET.get('outer_port'))
    ports = {inner_port + '/tcp': outer_port}
    try:
        res = ctn_create(image_name, ports)
        return JsonResponse({'errno': 0, "res": res})
    except:
        return JsonResponse({'errno': 1})


# 运行容器
@require_GET
def run_container(request):
    image_name = str(request.GET.get('image_name'))
    inner_port = str(request.GET.get('inner_port'))
    outer_port = str(request.GET.get('outer_port'))
    ports = {inner_port + '/tcp': outer_port}
    try:
        res = ctn_create(image_name, ports)
        return JsonResponse({'errno': 0, "res": res})
    except:
        return JsonResponse({'errno': 1})


# 停止容器
@require_GET
def stop_container(request):
    container_id = str(request.GET.get('container_id'))
    try:
        res = ctn_stop(container_id)
        return JsonResponse({'errno': 0})
    except:
        return JsonResponse({'errno': 1})

# 删除容器
@require_GET
def remove_container(request):
    container_id = str(request.GET.get('container_id'))
    try:
        res = ctn_remove(container_id)
        return JsonResponse({'errno': 0})
    except:
        return JsonResponse({'errno': 1})
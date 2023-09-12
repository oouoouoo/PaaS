from django.http import JsonResponse
from django.shortcuts import render
import docker

# Create your views here.

# set docker client
docker_client = docker.from_env()


#
def _image(request):
    if request.method == 'GET':
        uid = request.POST.get('uid')
        return JsonResponse({'errno': 0, })
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


# 新建镜像
def build_image(request):
    if request.method == 'GET':
        dockerfile = request.FILES.get('dockerfile')
        docker_client.images.build(fileobj=dockerfile)
        return JsonResponse({'errno': 0, })
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


# 拉取镜像
def pull_image(request):
    if request.method == 'GET':
        repository = request.POST.get('repository')
        docker_client.images.pull(repository=repository)
        return JsonResponse({'errno': 0, })
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


# 查看镜像列表
def list_image(request):
    if request.method == 'GET':
        images = docker_client.images.list()
        image_list = []
        for image in images:
            dic = {}
            dic["attrs"] = image.attrs
            dic["id"] = image.id
            dic["labels"] = image.labels
            dic["short_id"] = image.short_id
            dic["tags"] = image.tags
            image_list.append(dic)
        return JsonResponse({'errno': 0, 'image_list': image_list})
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


# 删除镜像
def delete_image(request):
    if request.method == 'GET':
        image_id = request.POST.get('image_id')
        docker_client.images.remove(image_id)
        return JsonResponse({'errno': 0, })
    else:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})

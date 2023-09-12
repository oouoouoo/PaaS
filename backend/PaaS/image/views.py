from django.http import JsonResponse
from django.shortcuts import render
import docker

# Create your views here.

# set docker client
from django.views.decorators.http import require_GET, require_POST

docker_client = docker.from_env()


#
@require_GET
def _image(request):
    image_id = str(request.GET.get('image_id'))
    try:
        return JsonResponse({'errno': 0})
    except:
        return JsonResponse({'errno': 1})


# 查看镜像列表
@require_GET
def list_image(request):
    try:
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
    except:
        return JsonResponse({'errno': 1})


# 查看镜像
@require_GET
def get_image(request):
    image = str(request.GET.get('image'))   # ?image是镜像名还是Id
    try:
        image = docker_client.images.get(image)
        # 提取镜像的相关信息
        image_info = {
            'Id': image.id,
            'Tags': image.tags,
            'Created': image.attrs['Created'],
            'Size': image.attrs['Size'],
            'Architecture': image.attrs['Architecture'],
            # 可以根据需要提取更多信息
        }
        return JsonResponse({'errno': 0, 'res': image_info})
    except:
        return JsonResponse({'errno': 1})


# 新建镜像
@require_POST
def build_image(request):
    dockerfile = request.FILES.get('dockerfile')
    try:
        docker_client.images.build(fileobj=dockerfile)
        return JsonResponse({'errno': 0, })
    except:
        return JsonResponse({'errno': 1, 'msg': "请求方式错误"})


# 拉取镜像
@require_GET
def pull_image(request):
    repository = str(request.GET.get('repository'))
    try:
        docker_client.images.pull(repository=repository)
        return JsonResponse({'errno': 0})
    except:
        return JsonResponse({'errno': 1})


# 修改镜像
@require_POST
def modify_image(request):
    image_id = str(request.POST.get('image_id'))
    try:
        dockerfile = request.FILES.get("dockerfile")
        res = docker_client.images.build(
            fileobj=dockerfile,
            tag=image_id,  # 使用原有的镜像标识符作为标签，并替换原有的镜像
        )
        return JsonResponse({'errno': 0})
    except:
        return JsonResponse({'errno': 1})


# 删除镜像
@require_GET
def delete_image(request):
    image_id = str(request.GET.get('image_id'))
    try:
        docker_client.images.remove(image_id)
        return JsonResponse({'errno': 0})
    except:
        return JsonResponse({'errno': 1})

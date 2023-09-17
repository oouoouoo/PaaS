import os

from django.http import JsonResponse
from django.shortcuts import render
import docker

# Create your views here.

# set docker client
from django.views.decorators.http import require_GET, require_POST

from PaaS import settings

docker_client = docker.from_env()


#
@require_GET
def _image(request):
    image_id = str(request.GET.get('image_id'))
    try:
        return JsonResponse({'errno': 0})
    except Exception as e:
        print(e)
        return JsonResponse({'errno': 1})


def load_image(file_path, re_name=None, re_tag=None):
    try:
        fp = open(file=file_path, mode='rb')
        result = docker_client.images.load(data=fp)
        fp.close()
        print(result)
        return 'ok'
    except Exception as e:
        print(e)
        raise Exception(e)


# 登录
@require_POST
def login(request):
    username = str(request.GET.get('username'))
    password = str(request.GET.get('password'))
    try:
        if username == 'CR7' and password == '123456':
            return JsonResponse({'errno': 0})
        else:
            return JsonResponse({'errno': 2})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'errno': 1, 'msg': str(e)})


# 创建镜像  -Dockerfile Done
@require_POST
def build_image(request):
    try:
        # 获取上传的Dockerfile文件
        dockerfile = request.FILES.get('dockerfile')
        # 创建dockerfile子文件夹（如果不存在）
        dockerfile_dir = os.path.join(settings.MEDIA_ROOT, 'dockerfile')
        os.makedirs(dockerfile_dir, exist_ok=True)
        # 构建文件保存路径
        file_path = os.path.join(dockerfile_dir, dockerfile.name)
        # dockerfile.save(file_path)
        # 使用 write 方法将文件保存到文件系统
        with open(file_path, 'wb') as destination:
            for chunk in dockerfile.chunks():
                destination.write(chunk)

        docker_client.images.build(path=dockerfile_dir, quiet=False)
        return JsonResponse({'errno': 0, 'msg': "通过Dockerfile创建镜像成功"})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'errno': 1, 'msg': str(e)})


# 上传镜像  tar Done
@require_POST
def upload_image(request):
    try:
        # 获取上传的tar文件
        tar_file = request.FILES.get('tar_file')
        # 创建tar子文件夹（如果不存在）
        tarfile_dir = os.path.join(settings.MEDIA_ROOT, 'tar')
        os.makedirs(tarfile_dir, exist_ok=True)
        # 构建文件保存路径
        file_path = os.path.join(tarfile_dir, tar_file.name)
        tar_file.save(file_path)
        res = load_image(file_path=file_path)
        return JsonResponse({'errno': 0, 'msg': "上传新建镜像成功", 'res': res})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'errno': 1, 'msg': str(e)})


# 拉取镜像  Done
@require_POST
def pull_image(request):
    try:
        repository = str(request.POST.get('repository'))
        tag = str(request.POST.get('tag', 'latest'))
        print("POST is :" + str(request.POST))
        print("repository is " + repository)
        print("tag is " + tag)
        docker_client.images.pull(repository=repository, tag=tag)
        return JsonResponse({'errno': 0, 'msg': "拉取镜像成功"})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'errno': 1, 'msg': str(e)})


# 查看镜像列表 Done
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
        return JsonResponse({'errno': 0, 'msg': "获取镜像列表成功", 'image_list': image_list})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'errno': 1, 'msg': str(e)})


# 查看镜像 Done
@require_GET
def get_image(request):
    image = str(request.GET.get('image_id'))  # ?image是镜像名还是Id
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
        return JsonResponse({'errno': 0, 'msg': "获取镜像信息成功", 'image_info': image_info})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'errno': 1, 'msg': str(e)})


# 删除镜像 Done
@require_POST
def delete_image(request):
    # 删除所有镜像
    image_id = str(request.POST.get('image_id'))
    try:
        print("POST is :" + str(request.POST))
        image = docker_client.images.get(image_id)
        print("tags len is", len(image.tags))
        print("tags are", image.tags)
        for tag in image.tags:
            parts = tag.split(":")
            image_name = parts[0]
            print("delete tag ", image_name)
            docker_client.images.remove(image_name)
        return JsonResponse({'errno': 0, 'msg': "删除镜像成功"})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'errno': 1, 'msg': str(e)})


# 删除镜像标签 Done
@require_POST
def delete_image_by_tag(request):
    image_id = str(request.POST.get('image_id'))
    tag = str(request.POST.get('tag'))
    try:
        print("POST is :" + str(request.POST))
        image = docker_client.images.get(image_id)
        parts = tag.split(":")
        image_name = parts[0]
        print("delete tag ", image_name)
        docker_client.images.remove(image_name)
        # docker_client.images.remove(image_id)
        return JsonResponse({'errno': 0, 'msg': "删除镜像标签成功"})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'errno': 1, 'msg': str(e)})


# 修改镜像 Done
@require_POST
def modify_image(request):
    try:
        image_id = str(request.POST.get('image_id'))
        new_image_name = str(request.POST.get('new_image_name'))
        # 获取上传的Dockerfile文件
        dockerfile = request.FILES.get('dockerfile')
        # 创建dockerfile子文件夹（如果不存在）
        dockerfile_dir = os.path.join(settings.MEDIA_ROOT, 'dockerfile')
        os.makedirs(dockerfile_dir, exist_ok=True)
        # 构建文件保存路径
        file_path = os.path.join(dockerfile_dir, dockerfile.name)
        # dockerfile.save(file_path)
        # 使用 write 方法将文件保存到文件系统
        with open(file_path, 'wb') as destination:
            for chunk in dockerfile.chunks():
                destination.write(chunk)
        docker_client.images.remove(image_id)
        res = docker_client.images.build(
            path=dockerfile_dir,
            # tag=image_id,  # 使用原有的镜像标识符作为标签，并替换原有的镜像
            tag=new_image_name,
        )
        # 设置新的镜像标签
        # docker_client.images.get(image_id).tag(new_image_name)
        return JsonResponse({'errno': 0, 'msg': "修改镜像成功"})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'errno': 1, 'msg': str(e)})

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


# 新建运行容器
@require_POST
def run_container(request):
    try:
        # 获取请求中的参数，例如容器名称、镜像、容器端口、环境变量等
        container_name = request.POST.get('container_name')
        image_name = request.POST.get('image_name')
        # command = request.values.getlist('command[]')
        container_port = request.POST.get('container_port')
        env_var1 = request.POST.get('ENV_VAR1')
        print(request.POST)
        # 创建环境变量字典，只包含 ENV_VAR1（可以扩展多个）
        environment_vars = {
            'ENV_VAR1': env_var1
        }
        # container = client.containers.run(image='nginx', name='test-myself', command=["nginx", "-g", "daemon off;"],
        # detach=True, ports={80: 30090})
        container = client.containers.run(image=image_name, name=container_name,
                                          command=["nginx", "-g", "daemon off;"],
                                          ports={80: container_port},
                                          environment={'ENV_VAR1': env_var1},
                                          detach=True)
        return JsonResponse({'errno': 0, 'msg': "新建容器成功"})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'errno': 1, 'msg': str(e)})


# 查看容器列表    Done
@require_GET
def list_container(request):
    try:
        containers = client.containers.list(all=True)
        container_list = []
        for container in containers:
            res = ctn_get(container.id)
            container_list.append(res)
            '''
            dic = {}
            dic["id"] = container.id
            dic["short_id"] = container.short_id
            dic["name"] = container.name
            dic["status"] = container.status
            dic["image"] = container.image.tags[0] if container.image.tags else ""
            dic["ports"] = container.ports
            container_list.append(dic)
            '''
        return JsonResponse({'errno': 0, 'msg': "获取容器列表成功", 'container_list': container_list})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'errno': 1, 'msg': str(e)})


# 查看容器信息    Done
@require_GET
def get_container(request):
    container_id = str(request.GET.get('container_id'))
    try:
        res = ctn_get(container_id)
        return JsonResponse({'errno': 0, 'msg': "获取容器信息成功", 'res': res})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'errno': 1, 'msg': str(e)})


# 停止容器  Done
@require_POST
def stop_container(request):
    container_id = str(request.POST.get('container_id'))
    try:
        print("POST :"+ str(request.POST))
        print("ID is "+ container_id)
        # 容器状态由Up变成Exited，容器不再运行
        container = client.containers.get(container_id)
        container.stop()
        return JsonResponse({'errno': 0, 'msg': "停止容器成功"})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'errno': 1, 'msg': str(e)})


# 重启容器  Done
@require_POST
def start_container(request):
    container_id = str(request.POST.get('container_id'))
    try:
        # 容器状态由Exited变成Up，容器重新启动并运行
        container = client.containers.get(container_id)
        container.start()
        return JsonResponse({'errno': 0, 'msg': "重启容器成功"})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'errno': 1, 'msg': str(e)})


# 删除容器  Done
@require_POST
def remove_container(request):
    container_id = str(request.POST.get('container_id'))
    try:
        container = client.containers.get(container_id)
        container.stop()
        container.remove()
        return JsonResponse({'errno': 0, 'msg': "删除容器成功"})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'errno': 1, 'msg': str(e)})


# 新建容器  Done
@require_POST
def create_container2(request):
    image_name = str(request.POST.get('image_name'))
    inner_port = str(request.POST.get('inner_port'))
    outer_port = str(request.POST.get('outer_port'))
    ports = {inner_port + '/tcp': outer_port}
    try:
        res = ctn_create(image_name, ports)
        return JsonResponse({'errno': 0, 'msg': "新建容器成功", "res": res})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'errno': 1, 'msg': str(e)})


# 运行容器  Done
@require_POST
def run_container2(request):
    image_name = str(request.POST.get('image_name'))
    inner_port = str(request.POST.get('inner_port'))
    outer_port = str(request.POST.get('outer_port'))
    ports = {inner_port + '/tcp': outer_port}
    try:
        res = ctn_run(image_name, ports)
        return JsonResponse({'errno': 0, 'msg': "运行容器成功", "res": res})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'errno': 1, 'msg': str(e)})

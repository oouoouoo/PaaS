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
        if container_port is not None:
            container_port = int(container_port)
        else:
            # 如果未提供 container_port 参数，可以为其设置一个默认值
            container_port = 80
        print("container_port is :", container_port)
        # print("container_port is :" + request.POST.get('container_port'))
        env_var1 = request.POST.get('ENV_VAR1')
        # 创建环境变量字典，只包含 ENV_VAR1（可以扩展多个）
        environment_vars = {
            'ENV_VAR1': env_var1
        }
        '''
        # 创建容器配置
        container_config = {
            'image': image_name,
            'name': container_name,
            'ports': {container_port: container_port},
            'environment': environment_vars,
            'detach': True,  # 后台模式运行容器
            # 'command': 'nginx',  # 指定要运行的命令
        }
        '''
        cmd = ["/bin/sh", "-c", "#(nop) ", "CMD [\"nginx\" \"-g\" \"daemon off;\"]"],
        # 创建并启动容器
        # container = client.containers.run(**container_config)
        container = client.containers.run(image=image_name, name=container_name,
                                          # command='nginx',
                                          # command='/usr/sbin/nginx',
                                          # command="/docker-entrypoint.sh nginx -g 'daemon off;'",
                                          # command=["nginx", "-g", "daemon off;"],
                                          # command="CMD [\"nginx\" \"-g\" \"daemon off;\"]",
                                          # command= ["CMD [\"nginx\" \"-g\" \"daemon off;\"]"],
                                          # command=["\"nginx\" \"-g\" \"daemon off;\""],
                                          command=["/bin/sh", "-c", "#(nop) ", "CMD [\"nginx\" \"-g\" \"daemon off;\"]"],
                                          environment={'NGINX_ENV_VAR': 'my_value'},
                                          # environment=environment_vars,
                                          ports={container_port: container_port},
                                          detach=True)  # 后台模式运行容器
        return JsonResponse({'errno': 0})
    except Exception as e:
        # 捕获异常并打印异常信息
        print(f"Error: {str(e)}")
        # 将异常信息包含在返回的 JSON 数据中
        return JsonResponse({'errno': 1, 'error_message': str(e)})


# 查看容器列表    Done
@require_GET
def list_container(request):
    try:
        containers = client.containers.list(all=True)
        container_list = []
        for container in containers:
            dic = {}
            dic["id"] = container.id
            dic["name"] = container.name
            dic["status"] = container.status
            dic["image"] = container.image.tags[0] if container.image.tags else ""
            dic["ports"] = container.ports
            container_list.append(dic)
        return JsonResponse({'errno': 0, 'container_list': container_list})
    except:
        return JsonResponse({'errno': 1, 'container_list': []})


# 查看容器信息    Done
@require_GET
def get_container(request):
    container_id = str(request.GET.get('container_id'))
    try:
        res = ctn_get(container_id)
        return JsonResponse({'errno': 0, 'res': res})
    except:
        return JsonResponse({'errno': 1})


# 停止容器  Done
@require_GET
def stop_container(request):
    container_id = str(request.GET.get('container_id'))
    try:
        # 容器状态由Up变成Exited，容器不再运行
        container = client.containers.get(container_id)
        container.stop()
        return JsonResponse({'errno': 0})
    except:
        return JsonResponse({'errno': 1})


# 重启容器  Done
@require_GET
def start_container(request):
    container_id = str(request.GET.get('container_id'))
    try:
        # 容器状态由Exited变成Up，容器重新启动并运行
        container = client.containers.get(container_id)
        container.start()
        return JsonResponse({'errno': 0})
    except:
        return JsonResponse({'errno': 1})


# 删除容器  Done
@require_GET
def remove_container(request):
    container_id = str(request.GET.get('container_id'))
    try:
        container = client.containers.get(container_id)
        container.stop()
        container.remove()
        return JsonResponse({'errno': 0})
    except:
        return JsonResponse({'errno': 1})


# 新建容器  Done
@require_POST
def create_container2(request):
    image_name = str(request.GET.get('image_name'))
    inner_port = str(request.GET.get('inner_port'))
    outer_port = str(request.GET.get('outer_port'))
    ports = {inner_port + '/tcp': outer_port}
    try:
        res = ctn_create(image_name, ports)
        return JsonResponse({'errno': 0, "res": res})
    except:
        return JsonResponse({'errno': 1})


# 运行容器  Done
@require_GET
def run_container2(request):
    image_name = str(request.GET.get('image_name'))
    inner_port = str(request.GET.get('inner_port'))
    outer_port = str(request.GET.get('outer_port'))
    ports = {inner_port + '/tcp': outer_port}
    try:
        res = ctn_run(image_name, ports)
        return JsonResponse({'errno': 0, "res": res})
    except:
        return JsonResponse({'errno': 1})

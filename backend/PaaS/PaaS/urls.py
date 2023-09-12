"""PaaS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import container.views
import image.views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 镜像管理
    path("image/list", image.views.list_image),     # 查看镜像列表
    path("image/build", image.views.build_image),   # 新建镜像
    path("image/pull", image.views.pull_image),     # 拉取镜像
    path("image/delete", image.views.delete_image), # 删除镜像

    # 容器管理
    path("container/list", container.views.list_container),     # 查看容器列表
    path("container/get", container.views.get_container),       # 查看容器信息
    path("container/create", container.views.create_container), # 新建容器
    path("container/run", container.views.run_container),       # 运行容器
    path("container/stop", container.views.stop_container),     # 停止容器
    path("container/remove", container.views.remove_container), # 删除容器

    # 应用管理

]

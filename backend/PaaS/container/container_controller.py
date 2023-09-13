import os
import random
import docker

client = docker.from_env()


def ctn_list():
    ctns = client.containers.list(all=True)
    res = []
    for ctn in ctns:
        res.append(ctn.id)
    return res


def ctn_search(keyword, key):
    ctns = client.containers.list(all=True)
    res = []
    for ctn in ctns:
        if key == 'Name' and keyword in ctn.name:
            res.append(ctn.id)
        if key == 'Status' and keyword in ctn.status:
            res.append(ctn.id)
        if key == 'Image' and keyword in ctn.image.tags[0]:
            res.append(ctn.id)
    return res


def ctn_get(ctn_id):
    ctn = client.containers.get(ctn_id)
    ctn_attr = {}
    ctn_attr['Id'] = ctn.id
    ctn_attr['Created'] = list(ctn.attrs.items())[1][1]
    ctn_attr['Port'] = list(ctn.attrs.items())[18][1]['PortBindings']
    try:
        for key in ctn_attr['Port'].keys():
            ctn_attr['Port'][key] = ctn_attr['Port'][key][0]['HostPort']
    except:
        ctn_attr['Port'] = {}
    try:
        ctn_attr['Image'] = ctn.image.tags[0]
    except:
        ctn_attr['Image'] = 'unknown'
    ctn_attr['Name'] = ctn.name
    ctn_attr['Status'] = ctn.status
    return ctn_attr


def getPort():
    pscmd = "netstat -ntl |grep -v Active| grep -v Proto|awk '{print $4}'|awk -F: '{print $NF}'"
    procs = os.popen(pscmd).read()
    procarr = procs.split("\n")
    tt = random.randint(15000, 20000)
    if tt not in procarr:
        return tt
    else:
        getPort()


def ctn_create(im, ports):
    if ports == {'22/tcp': '22'}:
        ports['22/tcp'] = str(getPort())
        ctn = client.containers.create(im, ports=ports)
    else:
        ctn = client.containers.create(im, ports=ports)
    return {'Id': ctn.id}


def ctn_run(im, ports):
    if ports == {'22/tcp': '22'}:
        ports['22/tcp'] = str(getPort())
        ctn = client.containers.create(im, detach=True, ports=ports)
    else:
        ctn = client.containers.run(im, detach=True, ports=ports)
    return {'Id': ctn.id}


# def ctn_prune():
#     client.containers.prune()

def ctn_start(ctn_id):
    ctn = client.containers.get(ctn_id)
    ctn.start()


def ctn_stop(ctn_id):
    ctn = client.containers.get(ctn_id)
    ctn.stop()


def ctn_remove(ctn_id):
    ctn = client.containers.get(ctn_id)
    ctn.stop()
    ctn.remove()


def ctn_exec(ctn_id, command):
    ctn = client.containers.get(ctn_id)
    res = ctn.exec_run(command)
    return res

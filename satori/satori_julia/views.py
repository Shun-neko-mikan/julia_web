from django.views.generic import View
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
import os
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.colors import Normalize              
from numba import jit                                
matplotlib.use('Agg')                                


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "satori_julia/index.html")


async def cal_julia(request):
    req_val= [request.GET['min_x'], request.GET['max_x'], request.GET['min_y'], request.GET['max_y'], request.GET['comp_const']]
    response = check_input(req_val)

    if response.status_code != 200:
        return response
    else:
        req_val = [float(i) for i in req_val[0:4]] + [req_val[4]]
        comp_const = req_val[4].split(" ")
        req_val.append(comp_const[0])
        req_val.append(comp_const[1])
        req_val[5] = float(req_val[5])
        req_val[6] = float(req_val[6][:-1])


    resolution = 1000
    n_max = 100
    z_real = np.linspace(req_val[0], req_val[1], resolution)
    z_imag = np.linspace(req_val[2], req_val[3], resolution)
    result = julia(z_real, z_imag, n_max, req_val[5], req_val[6])


    data = create_graph(result,req_val[0], req_val[1], req_val[2], req_val[3])
    return HttpResponse(data, content_type="image/jpeg", status=200)


# 入力が正しいかどうかを確認する関数
def check_input(req_val):
    if req_val[0] == "" or req_val[1] == "" or req_val[2] == "" or req_val[3] == "" or req_val[4] == "":
            msg = "Please input currect value."
            msg = msg.encode('utf-8')
            return HttpResponse(msg, status = 400)
    try:
        req_val = [float(i) for i in req_val[0:4]] + [req_val[4]]
    except:
        msg = "Please input float value."
        msg = msg.encode('utf-8')
        return HttpResponse(msg, status = 400)
    

    if abs(req_val[0]) > 2 or abs(req_val[1]) > 2 or abs(req_val[2]) > 2 or abs(req_val[3]) > 2:
        msg = "Please input min_x, min_y, max_x, max_y between -2 and 2."
        msg = msg.encode('utf-8')
        return HttpResponse(msg, status = 400)
    

    if req_val[0] > req_val[1] or req_val[2] > req_val[3]:
        msg = "Please input min_x < max_x, min_y < max_y."
        msg = msg.encode('utf-8')
        return HttpResponse(msg, status = 400)
    

    try:
        comp_const = req_val[4].split(" ")
        req_val.append(comp_const[0])
        req_val.append(comp_const[1])
        req_val[5] = float(req_val[5])
        if req_val[6][-1] == "j":
            req_val[6] = float(req_val[6][:-1])
        else:
            msg = "Please input 'a+bj' in comp_const."
            msg = msg.encode('utf-8')
            return HttpResponse(msg, status = 400)
    except:
        msg = "Please input 'a+bj' in comp_const."
        msg = msg.encode('utf-8')
        return HttpResponse(msg, status = 400)
    msg = "OK"
    return HttpResponse(msg, status = 200)





@jit                                                 
def julia(z_real, z_imag, n_max, a,  b):
    Re, Im = np.meshgrid(z_real, z_imag)              
    n_grid = len(Re.ravel())                           
    z = np.zeros(n_grid)                             
    c = complex(a, b)                                

    for i in range(n_grid):

        
        n = 0
        z0 = complex(Re.ravel()[i], Im.ravel()[i])


        while np.abs(z0) < 1e20 and not n == n_max:
            z0 = z0 ** 2 + c                         
            n += 1                                   


        if n == n_max:
            z[i] = 0
        else:
            z[i] = n


    z = np.reshape(z, Re.shape)                      
    z = z[::-1]                                      
    return z

# グラフ作成用関数
def create_graph(result,min_x, max_x, min_y, max_y):

    fig = plt.figure()
    ax = fig.add_subplot(111)
    mapplt = ax.imshow(result, cmap='jet', norm=Normalize(vmin=0, vmax=100),extent=[min_x, max_x, min_y, max_y])


    image_path = os.path.join(settings.BASE_DIR, "static", "media", "julia.jpeg")
    plt.savefig(image_path,dpi=800)
    plt.close()


    image_path = os.path.join(settings.BASE_DIR, "static", "media", "julia.jpeg")
    with open(image_path, "rb") as f:
        data = f.read()


    os.remove(image_path)
    return data
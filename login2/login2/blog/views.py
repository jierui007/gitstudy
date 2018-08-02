# 导入框架自带的用户验证应用的用户模型User
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from .models import Article, Anthology
import random
import time
import json

#首页
def index(request):
    articles = Article.objects.all()
    return render(request, 'index.html', {'articles': articles})

#注册
def register(request):
    """
    注册业务
    :param request:
    :return: GET请求时，返回注册页面。POST请求时，处理注册并返回结果。
    """
    # 判断请求方式是不是GET，如果是GET就返回注册页面，否则执行获取数据创建用户
    if request.method == 'GET':
        # 渲染并返回注册页面
        return render(request, 'register.html')
    else:
        # 通过用户模型User创建用户插入数据库
        user = User.objects.create_user(request.POST['username'], password=request.POST['password'],
                                        email=request.POST['email'])
        # 判断是否添加用户成功，成功则跳转到登录页面，否则返回错误信息
        if user is not None:
            return redirect('login')

        else:
            return HttpResponse('注册失败，请重新注册。')
#登录
def do_login(request):
    """
    登录业务
    :param request:
    :return: GET请求时，返回登录页面。POST请求时，处理登录请求并返回结果。
    """
    if request.method == 'GET':
        next_url = request.GET.get('next', '')
        print(next_url)
        return render(request, 'login.html', {'next': next_url})
    else:
        # 通过auth模块对authenticate方法验证用户账号密码是否正确
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        # 如果用户验证通过
        if user is not None:#用户存在
            # 判断用户是否是处于激活状态，如果是则使用login方法执行登录操作
            if user.is_active:
                login(request, user)
                #判断有没有next参数，有调到原来请求的的页面，没有则跳转到首页
                if request.POST['next']:
                     return redirect(request.POST['next'])
                else:
                     return redirect('index')
            else:
                return HttpResponse('账号未激活')
        else:
            return HttpResponse('未注册账号')

#退出登录
def do_logout(request):
    """退出登录"""
    logout(request)
    return redirect('index')

#------------------------------文集-------------------------------

@login_required(login_url='login')
def write(request):
    """
    用户访问文章发布页面，通过装饰器login_required限制必须登录才能访问
    """
    # 查询所有文集列表
    ant_list = Anthology.objects.filter(user=request.user)
    data = {'ant_list': ant_list}
    if ant_list:
        # 获取当前选中的文集id，如果用户提交则使用的，如果没有提交则使用默认第一个
        active_ant_id = request.GET.get('active_ant_id', ant_list[0].id)
        data['active_ant_id'] = int(active_ant_id)
        art_list = Article.objects.filter(anthology_id=active_ant_id)
        if art_list:
            active_art_id = request.GET.get('active_art_id', art_list[0].id)
            art_current = Article.objects.get(pk=active_art_id)
            data.update({
                'art_list': art_list,
                'art_current': art_current
            })
    return render(request, 'write.html', data)

def anthology_create(request):
    """创建文集"""
    name = request.POST['name'] # 从POST请求中获取文集name值
    # 创建一个文集，用户为当前登录的用户
    anthology = Anthology.objects.create(user=request.user, name=name)
    # 如果创建文集成功，返回成功，失败则返回失败，其中json.dump将python格式的转换成字符串格式的
    if anthology is not None:
        return HttpResponse(json.dumps({
            'ant_id': anthology.id
        }), content_type='application/json')
    else:
        return HttpResponse('创建失败')


def anthology_update(request):
    id = request.POST['id']
    name = request.POST['name']
    Anthology.objects.filter(id=id).update(name=name)
    return redirect('write')


def anthology_delete(request):
    ant_id = request.GET['id']
    Anthology.objects.get(id = ant_id).delete()
    return redirect('write')
def anthology_list(request):
    """渲染文集列表"""
    data_list = Anthology.objects.all()
    return render(request, 'write', {'list': data_list})

#-----------------------------写文章---------------------------------

def article(request):
    return render(request, 'article.html')

def article_create(request):
    """创建文章"""
    ant_id = request.POST['ant_id'] # 从POST请求中获取文集ID
    # 创建一个文章
    article_new = Article.objects.create(anthology_id=ant_id,
                                         title=time.strftime("%Y-%m-%d"))#文章标题以时间格式创建
    # 如果创建文章成功，返回成功，失败则返回失败
    if article_new is not None:
        return HttpResponse(json.dumps({
            'ant_id': ant_id,
            'art_id': article_new.id
        }), content_type='application/json')
    else:
        return HttpResponse('创建失败')


def article_post(request):
    """
    文章发布
    :param request:
    :return:
    """
    art_id = request.POST['art_id']
    ant_id = request.POST['ant_id']
    title = request.POST['title']
    content = request.POST['content']
    res = Article.objects.update_or_create(id=art_id, anthology_id=ant_id, defaults={'title': title, 'content': content})
    if res is not None:
        return HttpResponse('发布成功')
    else:
        return HttpResponse('发布失败')


def article_delete(request):
    art_id = request.GET['id']
    Article.objects.get(id = art_id).delete()
    return redirect('write')


def upload_ajax(request):
    """
    处理文章发布中的图片ajax上传
    :param request:
    :return:
    """
    if request.method == 'POST':
        file = FileSystemStorage()
        filename = str(int(time.time()*1000)) + str(random.randint(1000, 9999)) + '.png'
        file.save(file.location + '/' + filename, content=request.FILES['img'])
        res = {
            "errno": 0,
            "data": [
                file.base_url + filename
            ]
        }
    return HttpResponse(json.dumps(res), content_type="application/json")

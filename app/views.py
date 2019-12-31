from django.shortcuts import render,HttpResponse
from django.shortcuts import redirect
from app.models import *
from django.core import serializers
import json



def check(func):
    def wra(req,*arg,**kwargs):
        if not req.session.get('username'):
            return redirect("/login/")
        return func(req,*arg,**kwargs)
    return wra


#返回验证码
def get_code(request):
    from PIL import Image, ImageDraw, ImageFont
    #引入随机函数模块
    import random,os
    #定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), random.randrange(20, 100))
    width = 100
    height = 50
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str = '1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str[random.randrange(0, len(str))]
    #构造字体对象
    ttrFile = os.path.join(os.path.dirname(__file__),'kt.ttf')
    font = ImageFont.truetype(ttrFile, 40)
    #构造字体颜色
    fontcolor1 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor2 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor3 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor4 = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor1)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor2)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor3)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor4)
    #释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    #内存文件操作
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        passwd = request.POST['password']
        j_captcha = request.POST['j_captcha'].upper()
        code = request.session.get('verifycode').upper()
        if code != j_captcha:
            return HttpResponse("2")
        user = UserManager.objects.filter(username=username,password=passwd)
        if user:
            request.session["username"] = username
            return HttpResponse("0")
        else:
            return HttpResponse("1")
    else:
        return render(request,'login.html')

@check
#用户注销
def logout(request):
    request.session.flush()
    response = HttpResponse("注销成功")
    response['Refresh']="2;/index/"
    return response



def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        passwd = request.POST['password']
        j_captcha = request.POST['j_captcha'].upper()
        code = request.session.get('verifycode').upper()
        if code != j_captcha:
            return HttpResponse("2")
        user = UserManager.objects.filter(username=username)
        if user:
            return HttpResponse("1")
        else:
            UserManager.objects.create(username=username,password=passwd).save()
            return HttpResponse("0")
    else:
        return render(request,'register.html')


@check
def index(request):
    # dateTime_p = datetime.datetime.strptime("2019-10-31", '%Y-%m-%d')
    # airs = Airquality.objects.filter(date__year=2019).filter(date__month=11)
    return render(request,"index.html")

@check
def getInfoByYearMonth(request,year,month):
    # dateTime_p = datetime.datetime.strptime(year-month, '%Y-%m')
    airs = Airquality.objects.filter(date__year=year).filter(date__month=month)
    json_data = serializers.serialize('json',airs,ensure_ascii=False)
    return HttpResponse(json_data, content_type="application/json,charset=utf-8")


@check
def getLast(request):
    air = Airquality.objects.all().last().date
    year = air.year
    month = air.month
    return HttpResponse(json.dumps({"year":year,"month":month}), content_type="application/json,charset=utf-8")


@check
def dataPrediction(request):
    airs = Airquality.objects.all()
    air = airs.last().date
    year = air.year
    month = air.month
    if month > 3:
        airs = airs.filter(date__year=year)
    else:
        airs = airs.filter(date__year=year-1)

    AQI,PM25,PM10,SO2,CO,NO2,O3 = 0,0,0,0,0,0,0
    level = "优"
    # level 0-50  51-100 101-150  151-200

    for i in airs:
        AQI+=i.AQI
        PM25+=i.PM25
        PM10+=i.PM10
        SO2+=i.SO2
        CO+=float(i.CO)
        NO2+=i.NO2
        O3+=i.O3
    AQI = int(AQI/len(airs))
    PM25 = int(PM25/len(airs))
    PM10 = int(PM10/len(airs))
    SO2 = int(SO2/len(airs))
    CO = round(CO/len(airs),2)
    NO2 = int(NO2/len(airs))
    O3 = int(O3/len(airs))
    #预测年月
    if month == 12:
        year+=1
    month = 1
    if AQI > 150:
        level = "中等污染"
    if AQI > 100 and AQI <= 150:
        level = "一般污染"
    if AQI > 50 and AQI <= 100:
        level = "良好"


    return HttpResponse(json.dumps({"year":year,"month":month,"AQI":AQI,level:level,
                                    "PM25":PM25,"PM10":PM10,"SO2":SO2,"CO":CO,"NO2":NO2,"O3":O3
                                    }), content_type="application/json,charset=utf-8")

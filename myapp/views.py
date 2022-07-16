from django.shortcuts import render

# Create your views here.
from django.db.models import Max
from .models import user_login

def index(request):
    return render(request, './myapp/index.html')


def about(request):
    return render(request, './myapp/about.html')


def contact(request):
    return render(request, './myapp/contact.html')

############################# ADMIN ###################################
def admin_login(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        pwd = request.POST.get('pwd')
        #print(un,pwd)
        #query to select a record based on a condition
        ul = user_login.objects.filter(uname=un, passwd=pwd, u_type='admin')

        if len(ul) == 1:
            request.session['user_name'] = ul[0].uname
            request.session['user_id'] = ul[0].id
            return render(request,'./myapp/admin_home.html')
        else:
            msg = '<h1> Invalid Uname or Password !!!</h1>'
            context ={ 'msg1':msg }
            return render(request, './myapp/admin_login.html',context)
    else:
        msg = ''
        context ={ 'msg1':msg }
        return render(request, './myapp/admin_login.html',context)


def admin_home(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)
    else:
        return render(request,'./myapp/admin_home.html')


def admin_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return admin_login(request)
    else:
        return admin_login(request)

def admin_changepassword(request):
    if request.method == 'POST':
        opasswd = request.POST.get('opasswd')
        npasswd = request.POST.get('npasswd')
        cpasswd = request.POST.get('cpasswd')
        uname = request.session['user_name']
        try:
            ul = user_login.objects.get(uname=uname,passwd=opasswd,u_type='admin')
            if ul is not None:
                ul.passwd=npasswd
                ul.save()
                context = {'msg': 'Password Changed'}
                return render(request, './myapp/admin_changepassword.html', context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/admin_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Err Not Changed'}
            return render(request, './myapp/admin_changepassword.html', context)
    else:
        context = {'msg': ''}
        return render(request, './myapp/admin_changepassword.html', context)


import pandas as pd
from django.core.files.storage import FileSystemStorage
from .models import book_details
from datetime import datetime

def admin_book_file_add(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        book_file = fs.save(uploaded_file.name, uploaded_file)
        filename = f'./myapp/static/myapp/media/{book_file}'
        books = pd.read_csv(filename, sep=';', encoding="latin-1", error_bad_lines=False)
        for row in books.itertuples():
            bd = book_details(isbn=row[1], title=row[2], author=row[3], pub_year=row[4],
                              publisher=row[5], urls=row[6], urlm=row[7], urll=row[8],
                              file_path='none', status='none')
            bd.save()
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')
        context = {'msg': 'Record Added'}
        return render(request, 'myapp/admin_book_file_add.html',context)
    else:
        context = {}

        return render(request, 'myapp/admin_book_file_add.html',context)


def admin_book_details_add(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        book_file = fs.save(uploaded_file.name, uploaded_file)
        bid = request.POST.get('bid')
        bd = book_details.objects.get(id=int(bid))
        bd.file_path = book_file
        bd.save()

        context = {'msg': 'Record Added','bid':bid}
        return render(request, 'myapp/admin_book_details_add.html',context)
    else:
        bid = request.GET.get('bid')
        context = {'bid':bid}

        return render(request, 'myapp/admin_book_details_add.html',context)

def admin_book_details_delete(request):

    id = request.GET.get('id')
    print('id = '+id)
    cm = book_details.objects.get(id=int(id))
    cm.delete()
    msg = 'Record Deleted'
    cm_l = book_details.objects.all()
    context = {'book_list': cm_l,'msg':msg}
    return render(request, './myapp/admin_book_details_view.html',context)

def admin_book_details_view(request):
    msg = ''
    cnt = request.GET.get('cnt')
    ocnt = 0
    if cnt == None:
        cnt = int('100')
    elif int(cnt) <=0:
        cnt = 100
        ocnt = 0
    else:
        ocnt = int(cnt)
        cnt = int(cnt) + 100

    cm_l = book_details.objects.all()
    ncm_l =[]
    c = 0
    if len(cm_l) >= cnt:
        ncm_l = cm_l[ocnt:cnt]
    #for book in cm_l:
    #    if c >= ocnt and c <= cnt:
    #        ncm_l.append(book)
    #    c +=1
    context = {'book_list': ncm_l, 'msg': msg, 'cnt':cnt, 'pcnt':ocnt-100}
    return render(request, './myapp/admin_book_details_view.html', context)

def admin_user_details_view(request):
    user_list = user_details.objects.all()
    context = {'user_list': user_list}
    return render(request, './myapp/admin_user_details_view.html', context)

def admin_user_details_delete(request):
    try:
        uname = request.session['user_name']
        print(uname)
    except:
        return admin_login(request)

    id = request.GET.get('id')
    print('id = '+id)
    up = user_details.objects.get(id=int(id))
    user_id = up.user_id
    up.delete()
    ul = user_login.objects.get(id=int(user_id))
    ul.delete()

    msg = 'Record Deleted'

    user_list = user_details.objects.all()
    context = {'user_list': user_list,'msg':msg}
    return render(request, './myapp/admin_user_details_view.html', context)

def admin_book_search(request):
    if request.method == 'POST':
        query = request.POST.get('query')
        cm_l = book_details.objects.filter(title__contains=query)
        context = {'book_list': cm_l, 'msg': ''}
        return render(request, './myapp/admin_book_search_view.html', context)
    else:
        return render(request, 'myapp/admin_book_search.html')

from .book_algo import train_model
def admin_train_model(request):
    ####################################
    train_model(root_path='./dataset/')

    ######################################
    context = { 'msg': 'Dataset Trained and Model File Created'}
    return render(request, './myapp/admin_messages.html', context)


################################ USER #########################################
from .models import user_details

def user_login_check(request):
    if request.method == 'POST':
        uname = request.POST.get('uname')
        passwd = request.POST.get('passwd')

        ul = user_login.objects.filter(uname=uname, passwd=passwd, u_type='user')
        print(len(ul))
        if len(ul) == 1:
            request.session['user_id'] = ul[0].id
            request.session['user_name'] = ul[0].uname
            context = {'uname': request.session['user_name']}

            return render(request, 'myapp/user_home.html',context)
        else:
            context = {'msg': 'Invalid Credentials'}
            return render(request, 'myapp/user_login.html',context)
    else:
        return render(request, 'myapp/user_login.html')

def user_home(request):

    context = {'uname':request.session['user_name']}
    return render(request,'./myapp/user_home.html',context)


def user_details_add(request):
    if request.method == 'POST':

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')

        gender = request.POST.get('gender')
        dob = request.POST.get('age')
        addr = request.POST.get('addr')
        pin = request.POST.get('pin')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('pwd')
        uname=email
        #status = "new"

        ul = user_login(uname=uname, passwd=password, u_type='user')
        ul.save()
        user_id = user_login.objects.all().aggregate(Max('id'))['id__max']

        ud = user_details(user_id=user_id,fname=fname, lname=lname, gender=gender,
                          dob=dob,addr=addr, pin=pin, contact=contact, email=email ,
                          status='new')
        ud.save()

        print(user_id)
        context = {'msg': 'User Registered'}
        return render(request, 'myapp/user_login.html',context)

    else:
        return render(request, 'myapp/user_details_add.html')

def user_changepassword(request):
    if request.method == 'POST':
        uname = request.session['user_name']
        new_password = request.POST.get('new_password')
        current_password = request.POST.get('current_password')
        print("username:::" + uname)
        print("current_password" + str(current_password))

        try:

            ul = user_login.objects.get(uname=uname, passwd=current_password)

            if ul is not None:
                ul.passwd = new_password  # change field
                ul.save()
                context = {'msg':'Password Changed Successfully'}
                return render(request, './myapp/user_changepassword.html',context)
            else:
                context = {'msg': 'Password Not Changed'}
                return render(request, './myapp/user_changepassword.html', context)
        except user_login.DoesNotExist:
            context = {'msg': 'Password Not Changed'}
            return render(request, './myapp/user_changepassword.html', context)
    else:
        return render(request, './myapp/user_changepassword.html')


def user_logout(request):
    try:
        del request.session['user_name']
        del request.session['user_id']
    except:
        return user_login_check(request)
    else:
        return user_login_check(request)


from .models import user_search
def user_book_search(request):
    if request.method == 'POST':
        user_id = int(request.session['user_id'])
        query = request.POST.get('query')
        dt = datetime.today().strftime('%Y-%m-%d')
        tm = datetime.today().strftime('%H:%M:%S')

        us = user_search(user_id=user_id, query=query, dt=dt, tm=tm, status='none')
        us.save()

        cm_l = book_details.objects.filter(title__contains=query)
        context = {'book_list': cm_l, 'msg': ''}
        return render(request, './myapp/user_book_search_view.html', context)
    else:
        return render(request, 'myapp/user_book_search.html')

def user_search_view(request):
    if request.method == 'GET':
        user_id = int(request.session['user_id'])

        us_l = user_search.objects.filter(user_id=user_id)
        context = {'search_list': us_l, 'msg': ''}
        return render(request, './myapp/user_search_view.html', context)
    else:
        return render(request, 'myapp/user_home.html')

def user_book_search_results(request):
    if request.method == 'GET':
        query = request.GET.get('query')

        cm_l = book_details.objects.filter(title__contains=query)
        context = {'book_list': cm_l, 'msg': ''}
        return render(request, './myapp/user_book_search_view.html', context)
    else:
        return render(request, 'myapp/user_book_search.html')


from .book_algo import predict, predict_from_model

def user_book_ml_results(request):
    if request.method == 'GET':
        bid = request.GET.get('bid')
        bd = book_details.objects.get(id=int(bid))
        title = bd.title


        # print(title)
        book_list = []
        ############## ML ALGO PART #####################
        # result_list = predict_from_model(root_path='./dataset/', in_title=title)
        result_list = predict_from_model(root_path='./dataset/', in_title=title)
        print('lenofresultlist',len(result_list))
        if len(result_list) == 0:
            context = {'book_list': book_list, 'msg': 'Prediction is empty'}
            return render(request, './myapp/user_book_ml_view.html', context)
        else:
            for result in result_list:
                #print(result)
                #print('############')
                try:
                    bt = book_details.objects.get(isbn=result[1])
                    book_list.append(bt)
                except:
                    print('error book not loaded')

        #################################
        context = {'book_list': book_list, 'msg': ''}
        return render(request, './myapp/user_book_ml_view.html', context)

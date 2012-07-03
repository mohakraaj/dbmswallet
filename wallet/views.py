from django.http import HttpResponse
from model_signup import userprofile
from django.core.mail import send_mail
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from json import dumps
from model_loan import loan_data,budget,transactions
def mainpage(request):
    '''url^/$'''
     
    return render_to_response('mainpage.html',{'login':True,'signup':False})

def showlogin(request):

    '''url ^login/$ '''
    error=True
    return render_to_response("loginf.html",{'error':error})


def showsignup(request):
    '''url ^signup/$ '''

    err=True
    return render_to_response('signupf.html',{'err':err})
#    data={'login':True,'signup':False} 
 #   return HttpResponse(dumps(data))

def loginp(request):
    '''url ^loginfill/ '''
    if request.method=='POST':
        try:
            name=request.POST['firstName'] 
            ipassword=request.POST['password']         
           # person=userprofile.objects.get(name=request.POST['firstName'],password=request.POST['password'])
            user=authenticate(username=name, password=ipassword)
            if user is not None:
                if user.is_active:
                    login(request,user)
                    request.session['k']=1
                    return render_to_response('budget.html')
            else:
                    return HttpResponse("Invalid User name and Password ;)")
        except:
            return HttpResponse('Sorry we have a problem.. we are solving the problem')
        
    return HttpResponse('Page doesn exist ;)')



def signup(request):
    ''' url ^/signupfill/ all the validations are done at client side so no need to validate :)'''
    if request.method=='POST':
        iname=request.POST['firstName']
        iwebsite=request.POST['website']
        iemail=request.POST['email']
        ibirthdate=request.POST['bday']
        ibirthdate=yearformater(ibirthdate)
        isex=request.POST['sex']
        icountry=request.POST['country']
        ipassword=request.POST['password']
    try:
        person=userprofile(name=iname,website=iwebsite,email=iemail,birth_date=ibirthdate,sex=isex,country=icountry,password=ipassword,mailing=True)
        person.save()

        send_mail('eWALLET','thanks for registering','mohakraaj@gmail.com',[iemail],fail_silently=True)
        user=User.objects.create_user(iname,iemail,ipassword)
        user.save()
    except:
        return render_to_response('signupf.html',{'error':True})
    return loginp(request)    


def yearformater(year):
    """ to format the year type to date type in data base .. calendar librar        y used in client side is not stable"""
    k=year.split('/')
    if len(k)>1:
        yearformatted=k[2]+'-'+k[1]+'-'+k[0]
    else:
        yearformatted=k[0]    
    return yearformatted


@login_required
def loan_caller(request):
    return render_to_response('loan.html')

@login_required
def loan(request):
    ''' url ^/loan/ '''
    if request.method=='POST':
        user=request.user
        ifname=request.POST['fName']
        iemail=request.POST['email']
        icurrency=request.POST['currency']
        iamount=request.POST['amount']
        iinterest=request.POST['interest']
        ideadline=request.POST['bday']
        ideadline=yearformater(ideadline)
        
        send_mail('eWALLET','Hey u own me cash me remember ;)','mohakraaj@gmail.com',[iemail],fail_silently=True)
        try:
            m=loan_data.objects.filter(created_by=request.user,fname=ifname)
            if len(m)==0:
                k=loan_data(created_by=user,fname=ifname,email=iemail,currency=icurrency,amount=iamount,interest=iinterest,deadline=ideadline)
                k.save()
                return render_to_response('loan.html',{'error':True})
            else:
                m[0].amount+=iamount
        except:
            return HttpResponse("Sorry there is some error")
    return HttpResponse("Page doesn exist ;)")

@login_required
def transaction_display(request):
    trans=[]
    k=transactions.objects.filter(created_by=request.user)
    s=[]
    print k
    request.session['k']=1
    for ele in k:
        s.append(ele.id)
        t={}
        t['id']=ele.id
        t['category']=ele.category
        t['amount']=ele.amount
        t['date']=ele.created_date.strftime('%Y-%m-%d')
        trans.append(t)
    return render_to_response('showtrans.html',{'t':trans})

@login_required
def loan_display(request):
    loan=[]
    k=loan_data.objects.filter(created_by=request.user)
    s=[]
    for ele in k:
        s.append(ele.id)
        t={}
        t['id']=ele.id
        t['name']=ele.fname
        t['amount']=ele.amount
        t['deadline']=ele.deadline.strftime('%Y-%m-%d')
        print t['deadline']
        t['email']=ele.email
        loan.append(t)
    print loan,s
    return render_to_response('loan_display.html',{'loan':loan,'s':s})

@login_required
def show_budget(request):
    '''url ^/showbudget/'''
    print request.user
    return render_to_response('budget.html') 

@login_required
def budgetset(request):
    '''url ^/budget_set/'''
    if request.method=='POST':
        created_by=request.user
        icategory=request.POST['category']
        imonth=(request.POST['month'])
        iyear=(request.POST['year'])
        iamount=request.POST['amount']
        l=budget.objects.filter(created_by=request.user,category=icategory,month=imonth,year=iyear) 
        if len(l)==0:
            k=budget(created_by=request.user,category=icategory,month=imonth,year=iyear,amount=iamount) 
            k.save()
            print k
        else:
            l[0].amount=iamount
            print l
        return render_to_response('budget.html',{'error':True})
@login_required
def budget_display(request):
    '''url /budget_display'''
    return render_to_response('budget_display.html')

@login_required
def budget_cdata(request):
    ''' url /budgetcdata '''
    categories=["automobile","entertainment","family","health","food","household","insurance","office","travel","personal"]
#   amount_distribution a_d
    a_d=[]
    for ele in categories:
        
        k=budget.objects.filter(created_by=request.user,category=ele)
        sum=0
        for bud in k:
            sum+=bud.amount
        a_d.append(sum)
    print a_d
    b=dumps(a_d)
    print b
    return HttpResponse(b)

@login_required
def budget_m_display(request):
    '''url /budget_m_display'''
    return render_to_response('budget_m_display.html')

@login_required
def budget_mdata(request):
    ''' url /budgetmdata '''
    categories=['january','February','March','April','May','June','July','August','September','October','November','December']
#   amount_distribution a_d
    a_d=[]
    for ele in categories:
        k=budget.objects.filter(created_by=request.user,month__iexact=ele)
        sum=0
        for bud in k:
            sum+=bud.amount

        a_d.append(sum)
    print a_d
    b=dumps(a_d)
    print b
    return HttpResponse(b)

@login_required
def budget_y_display(request):
    '''url /budget_m_display'''
    return render_to_response('budget_y_display.html')


@login_required
def budget_ydata(request):
    ''' url /budgetydata '''
    categories=['2009','2010','2011','2012','2013','2014','2015']
#   amount_distribution a_d
    print request.user
    a_d=[]
    for ele in categories:
        k=budget.objects.filter(created_by=request.user,year__iexact=ele)
        sum=0
        for bud in k:
            sum+=bud.amount

        a_d.append(sum)
    print a_d
    b=dumps(a_d)
    print b
    return HttpResponse(b)
@login_required
def budget_check(request):
    '''url budget check'''
    return render_to_response('budget_left.html')
@login_required
def budget_left(request):
    '''url budget_left'''
    if request.method=='POST':
        imonth=request.POST['month']
        iyear=request.POST['year']
        icat=["automobile","entertainment","family","health","food","household","insurance","office","travel","personal"]
        info=[]
        for icategory in icat:
            h={}
            l=budget.objects.filter(created_by=request.user,category=icategory,month=imonth,year=iyear)
            s=iyear+'-'+imonth+'-'+'01'
            f=iyear+'-'+imonth+'-'+'30'
            print s
            print f
            t=transactions.objects.filter(created_by=request.user,category=icategory,created_date__gte=f,created_date__lte=s)
            print t
            sum=0
            for ele in t:
                sum+=ele.amount        
            h['name']=icategory
            h['spent']=sum
            if len(l)>0:
                h['bspent']=l[0].amount
            else:
                h['bspent']=0
            info.append(h)
        info=dumps(info)
        print info
        return HttpResponse(info)
@login_required
def transaction_show(request):
    '''url ^/show_transaction'''
    return render_to_response('transaction.html')

@login_required
def transaction(request):
    '''url ^/transaction '''
    if request.method=='POST':
        k=transactions(created_by=request.user,category=request.POST['category'],amount=request.POST['amount'],created_date=request.POST['date'])
        k.save()
        print k
        return render_to_response('transaction.html')
    else:
        return HttpResponse('Page doesn exist')


@login_required
def logout_view(request):
    logout(request)
    return render_to_response("loginf.html")




# Create your views here.

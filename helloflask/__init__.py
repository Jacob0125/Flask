from flask import Flask, g, request, Response, make_response,session
from flask import session, render_template, Markup, url_for
from datetime import date, datetime, timedelta
import os
from dateutil.relativedelta import relativedelta

# from helloflask.init_db import init_database, db_session

app = Flask(__name__)

app.config.update(
    SECRET_KEY='X1243yRH!mMwf',
    SESSION_COOKIE_NAME='pyweb_flask_session',
    PERMANENT_SESSION_LIFETIME=timedelta(31) # 31 days cf. minutes=30
    )


app.debug = True # use only debug!!
app.jinja_env.trim_blocks = True
# app.config['SERVER_NAME'] = 'local.com:5000'
# @app.route("/sd")
# def helloworld_local():
#     return "Hello Local.com!"
# @app.route("/sd", subdomain="g")
# def helloworld22():
#     return "Hello G.Local.com!!!"

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

    
@app.template_filter('ymd') # cf. Handlebars' helper
def datetime_ymd(dt, fmt='%m-%d'):
    if isinstance(dt, date):
        return "<strong>%s</strong>" % dt.strftime(fmt)
        # return dt.strftime(fmt)
    else:
        return dt
    
@app.template_filter('symd') # cf. Handlebars' helper
def datetime_symd(dt):

    if not isinstance(dt,date):
        dt = datetime.strptime(dt,'%Y-%m-%d %H:%M')

    # if (datetime.now() - dt) <1:            
    if (datetime.now() - dt).days < 1:
        fmt = "%H:%M"
    else:
        fmt = "%m/%d"

    return "<strong>%s</strong>" % dt.strftime(fmt)
  

def make_date(dt,fmt):
    if not isinstance(dt,date):
        return datetime.strptime(dt,fmt)
    else:
        return dt

@app.template_filter('sdt')
def sdt(dt,fmt='%Y-%m-%d'):
    d = make_date(dt,fmt)
    wd = d.weekday() * -1
    # if wd == 6:
    #     return 1
    # else :
    #     return wd
    return 1 if wd == -6 else wd


@app.template_filter('month')
def month(dt,fmt='%Y-%m-%d'):
    d = make_date(dt,fmt)
    return d.month

@app.template_filter('edt')
def edt(dt,fmt='%Y-%m-%d'):
    d = make_date(dt,fmt)
    nextmonth = d + relativedelta(months=1)
    return (nextmonth - timedelta(1)).day + 1

app.config.update(
    connect_args={"options": "-c timezone=utc"},
	SECRET_KEY='X1243yRH!mMwf',
	SESSION_COOKIE_NAME='pyweb_flask_session',
	PERMANENT_SESSION_LIFETIME=timedelta(31)      # 31 days
)


class FormInput:
    def __init__(self, id='',name='',value='',checked='',text='',type='text'):
        self.id =id
        self.name = name
        self.value = value
        self.checked = checked
        self.text = text
        self.type = type
class Nav:
    def __init__(self, title, url='# ', children=[]):
        self.title =title
        self.url = url
        self.children = children

@app.route('/')
def idx():
    rds= []
    for i in [1,2,3]:
        id = 'r' + str(i)
        name = 'radiotest'
        value = i
        checked = ''
        if i==2:
            cheched ='checked'
        text = 'RadioTest'+str(i)
        rds.append(FormInput(id,name,value,checked,text))

    today = '2023-02-20 09:22' 
    # today = datetime.strptime('2023-02-20 09:22' '%Y-%m-%d %H:%M')
    # today = datetime.now()
    # today = date.today()
    d = datetime.strptime('2023-03-01', '%Y-%m-%d')
    mm = d.month
    nextmonth = d + relativedelta(months=1)
    sdt = d.weekday() * -1
    edt = (nextmonth - timedelta(1)).day + 1
    # year = 2023
    year = request.args.get('year', date.today().year, int)
    return render_template('app_main.html',year = year, ttt="wisconsin",radioList = rds, today = today)

@app.route('/top100')
def top100():
    return render_template('application.html',title = 'MAIN!!')




@app.route("/tmpl3")
def tmpl3():
    py = Nav("파이선", "https://naver.com");
    ja = Nav("자바", "https://daum.com");
    pr= Nav("프로그램1", "https://goole.com",[py,ja]);

    jin = Nav("파이선", "https://naver.com");
    gc = Nav("자바", "https://daum.com");
    web= Nav("프로그램2", "https://goole.com",[jin,gc]);

    spr = Nav("파이선", "https://naver.com");
    nd = Nav("자바", "https://daum.com");
    oth= Nav("프로그램3", "https://goole.com",[jin,gc,nd,spr]);

    return render_template('index.html', navs =[pr,web,oth])


@app.route("/tmpl1")
def tmp1():
    a = (1, "만남1", "김건모", False, []);
    b = (2, "만남2", "노사연", True, [a]);
    c = (3, "만남3", "익명", False, [a,b]);
    d = (4, "만남4", "익명", False, [a,b,c])

    return render_template("index.html", lst1=[a,b,c,d])

@app.route("/tmpl")
def tmpl():
    tit = Markup("<strong>Title</strong>")
    mu = Markup("<h1>iii = <i>%s</i></h1>")
    h = mu % "Italic"
    # print("h=", h)
    # lst = [ ("만남1", "김건모"), ("만남2", "노사연") ]

       # data의 세번째 인자로 숨김 여부 추가
    # lst = [ ( "만남", "김건모", False), ( "만남", "노사연", True), ( "만남", "익명", False) ]
    # lst = [ (1, "만남", "김건모", False), (2, "만남", "노사연", True), (3, "만남", "익명", False) ]

    # loop(data)
    a = (1, "만남1", "김건모", False, [])
    b = (2, "만남2", "노사연", True, [a])
    c = (3, "만남3", "익명", False, [a,b])
    d = (4, "만남4", "익명", False, [a,b,c])

    return render_template("index.html", lst=[a,b,c,d])

    # return render_template("index.html", lst=[])
    # return render_template("index.html", lst=lst)
    # return render_template("index.html", title = tit, mu=Markup(h))
    # return render_template('index.html', title='title')

# @app.route("/")
# def helloworld():
#     return "Hello Flask World!!!!!!!!!!!"

@app.route("/main")
def main():
    return render_template('main.html',title = "Jabcob cho")

@app.route("/ymt")
# request 처리 용 함수
def ymd(fmt):
    def trans(date_str):
        return datetime.strptime(date_str, fmt)
    return trans

@app.route("/cookie")
def wc():
    key = request.args.get('key')
    val = request.args.get('value')
    res = Response("SET COOKIE")
    res.set_cookie( key, val)
    session['Token'] = '123X'
    return make_response(res)
    # other request
@app.route("/rcookie")
def rc():
    key = request.args.get('key')
    val =  request.cookies.get(key)
    # val =  request.cookies.get('UserToken', 'default token')
    return "cookie["+key+"] ="+val+session.get("Token")

@app.route('/delsess')
def delsess():
    if session.get('Token'):
        del session['Token']
    return "Session이 삭제되었습니다!"

@app.route('/dt')
def dt():
    datestr = request.values.get('date', date.today(), type=ymd('%Y-%m-%d'))
    return "우리나라 시간 형식: " + str(datestr)

@app.route('/res1')
def res1( ):
    custom_res = Response("Custom Response", 200, {'test': 'ttt'})
    return make_response(custom_res)

# @app.before_request
# def before_request():
#     print("before_request!!!")
#     g.str = "한글"

# @app.route("/gg")
# def helloworld1():
#     return "Hello World!" + getattr(g, 'str', '111')


@app.route( '/rp' )
def rp( ):
    q = request.args.getlist('q')
    # q = request.args.get('q')
    # p = request.args.getlist('p')
    return "q=%s" % str(q)
    # return "p=%s" % str(p)

# WSGI(WebSe rver Gateway Interface)
@app.route('/test_wsgi')
def wsgi_test():
    def application(environ, start_response):
        body = 'The request method was %s' % environ['REQUEST_METHOD']
        headers = [ ('Content-Type', 'text/plain'), 
                           ('Content-Length', str(len(body))) ]
        start_response('200 OK', headers)
        return [body]
    return make_response(application)

@app.route("/rqen")
def rqen():
        return ('REQUEST_METHOD: %(REQUEST_METHOD) s <br>'
    'SCRIPT_NAME: %(SCRIPT_NAME) s <br>'
    'PATH_INFO: %(PATH_INFO) s <br>'
    'QUERY_STRING: %(QUERY_STRING) s <br>'
    'SERVER_NAME: %(SERVER_NAME) s <br>'
    'SERVER_PORT: %(SERVER_PORT) s <br>'
    'SERVER_PROTOCOL: %(SERVER_PROTOCOL) s <br>'
    'wsgi.version: %(wsgi.version) s <br>'
    'wsgi.url_scheme: %(wsgi.url_scheme) s <br>'
    'wsgi.input: %(wsgi.input) s <br>'
    'wsgi.errors: %(wsgi.errors) s <br>'
    'wsgi.multithread: %(wsgi.multithread) s <br>'
    'wsgi.multiprocess: %(wsgi.multiprocess) s <br>'
    'wsgi.run_once: %(wsgi.run_once) s') % request.environ

# import helloflask.views
# import helloflask.tests
# import helloflask.filters

# app.debug = True
# app.jinja_env.trim_blocks = True

# # config["connect_args"] = {"options": "-c timezone=utc"}


# @app.before_first_request
# def beforeFirstRequest():
#     print(">> before_first_request!!")
#     init_database()   # initialize database 


# @app.after_request
# def afterReq(response):
#     print(">> after_request!!")
#     return response


# @app.teardown_request
# def teardown_request(exception):
#     print(">>> teardown request!!", exception)


# @app.teardown_appcontext
# def teardown_context(exception):
#     print(">>> teardown context!!", exception)
#     db_session.remove()   # remove used db-session



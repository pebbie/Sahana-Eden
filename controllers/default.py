# -*- coding: utf-8 -*-

"""
    Default Controllers

    @author: Fran Boon
"""

module = "default"

# Options Menu (available in all Functions)
response.menu_options = [
    #[T("About Sahana"), False, URL(r=request, f="about")],
]

def call():
    "Call an XMLRPC, JSONRPC or RSS service"
    # If webservices don't use sessions, avoid cluttering up the storage
    #session.forget()
    return service()

def download():
    "Download a file"
    return response.download(request, db)

# Add newly-registered users to Person Registry & 'Authenticated' role
auth.settings.register_onaccept = lambda form: auth.shn_register(form)

_table_user = auth.settings.table_user
_table_user.first_name.comment = SPAN("*", _class="req")
_table_user.email.comment = SPAN("*", _class="req")
_table_user.password.comment = SPAN("*", _class="req")
_table_user.language.label = T("Language")
_table_user.language.default = "en"
_table_user.language.comment = DIV(_class="tooltip", _title=Tstr("Language") + "|" + Tstr("The language to use for notifications."))
_table_user.language.represent = lambda opt: shn_languages.get(opt, UNKNOWN_OPT)

def index():
    "Module's Home Page"

    modules = deployment_settings.modules

    module_name = modules[module].name_nice

    settings = db(db.s3_setting.id == 1).select(limitby=(0, 1)).first()
    admin_name = settings.admin_name
    admin_email = settings.admin_email
    admin_tel = settings.admin_tel
    response.title = T("Sahana FOSS Disaster Management System")
    self_registration = settings.self_registration

    form=None
    
    if self_registration:
        request.args = ["register"]
        form = auth()
    else:
        request.args = ["login"]
        auth.settings.login_next = None
        form = auth()

    return dict(module_name=module_name, modules=modules, admin_name=admin_name, admin_email=admin_email, admin_tel=admin_tel, self_registration=self_registration, form=form)

def user():
    "Auth functions based on arg. See gluon/tools.py"

    auth.settings.on_failed_authorization = URL(r=request, f="error")
    
    if request.args and request.args(0) == "login_next":
        # Can redirect the user to another page on first login for workflow (set in 00_settings.py)
        # Note the timestamp of last login through the browser
        if auth.is_logged_in():
            db(db.auth_user.id == auth.user.id).update(timestamp = request.utcnow)

    _table_user = auth.settings.table_user
    if request.args and request.args(0) == "profile":
        #_table_user.organisation.writable = False
        _table_user.utc_offset.readable = True
        _table_user.utc_offset.writable = True

    form = auth()

    self_registration = db().select(db.s3_setting.self_registration, limitby=(0, 1)).first().self_registration

    # Use Custom Ext views
    # Best to not use an Ext form for login: can't save username/password in browser & can't hit 'Enter' to submit!
    #if request.args(0) == "login":
    #    response.title = T("Login")
    #    response.view = "auth/login.html"

    return dict(form=form, self_registration=self_registration)

def source():
    "RESTful CRUD controller"
    return shn_rest_controller("s3", "source")

# NB These 4 functions are unlikely to get used in production
def header():
    "Custom view designed to be pulled into an Ext layout's North Panel"
    return dict()
def footer():
    "Custom view designed to be pulled into an Ext layout's South Panel"
    return dict()
def menu():
    "Custom view designed to be pulled into the 1st item of an Ext layout's Center Panel"
    return dict()
def list():
    "Custom view designed to be pulled into an Ext layout's Center Panel"
    return dict()

# About Sahana
def apath(path=""):
    "Application path"
    import os
    from gluon.fileutils import up
    opath = up(request.folder)
    #TODO: This path manipulation is very OS specific.
    while path[:3] == "../": opath, path=up(opath), path[3:]
    return os.path.join(opath,path).replace("\\", "/")

def about():
    """
    The About page provides details on the software
    depedencies and versions available to this instance
    of Sahana Eden.
    """
    import sys
    import subprocess
    import string
    python_version = sys.version
    web2py_version = open(apath("../VERSION"), "r").read()[8:]
    sahana_version = open(os.path.join(request.folder, "VERSION"), "r").read()
    try:
        sqlite_version = (subprocess.Popen(["sqlite3", "-version"], stdout=subprocess.PIPE).communicate()[0]).rstrip()
    except:
        sqlite_version = T("Not installed or incorectly configured.")
    try:
        mysql_version = (subprocess.Popen(["mysql", "--version"], stdout=subprocess.PIPE).communicate()[0]).rstrip()[10:]
    except:
        mysql_version = T("Not installed or incorrectly configured.")
    try:
        pgsql_reply = (subprocess.Popen(["psql", "--version"], stdout=subprocess.PIPE).communicate()[0])
        pgsql_version = string.split(pgsql_reply)[2]
    except:
        pgsql_version = T("Not installed or incorrectly configured.")
    try:
        import MySQLdb
        pymysql_version = MySQLdb.__revision__
    except:
        pymysql_version = T("Not installed or incorrectly configured.")
    try:
        import reportlab
        reportlab_version = reportlab.Version
    except:
        reportlab_version = T("Not installed or incorrectly configured.")
    try:
        import xlwt
        xlwt_version = xlwt.__VERSION__
    except:
        xlwt_version = T("Not installed or incorrectly configured.")
    return dict(
                python_version=python_version,
                sahana_version=sahana_version,
                web2py_version=web2py_version,
                sqlite_version=sqlite_version,
                mysql_version=mysql_version,
                pgsql_version=pgsql_version,
                pymysql_version=pymysql_version,
                reportlab_version=reportlab_version,
                xlwt_version=xlwt_version
                )

def help():
    "Custom View"
    response.title = T("Help")
    return dict()

def contact():
    "Custom View"
    response.title = T("Contact us")
    return dict()

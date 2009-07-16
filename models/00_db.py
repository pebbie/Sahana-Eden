# -*- coding: utf-8 -*-

import os, traceback, datetime
import re

# Switch to 'False' in Production for a Performance gain
# (need to set to 'True' again when amending Table definitions)
migrate = True

#if request.env.web2py_runtime_gae:            # if running on Google App Engine
#    db = DAL('gae')                           # connect to Google BigTable
#    session.connect(request, response, db=db) # and store sessions and tickets there
    ### or use the following lines to store sessions in Memcache
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db=MEMDB(Client())
#else:                                         # else use a normal relational database
db = DAL('sqlite://storage.db')       # if not, use SQLite or other DB
#db = DAL('mysql://root:password@localhost/db', pools=10) # or other DB
#db = DAL('postgres://postgres:password@localhost/db', pools=10)

# Default strings are in English
T.current_languages = ['en', 'en-en']

# Custom classes which extend default Gluon & T2
from applications.sahana.modules.sahana import *
#from applications.sahana.modules.ldapconnect import AuthLDAP

t2 = S3(request, response, session, cache, T, db)

mail = Mail()
# These settings should be made configurable as part of the Messaging Module
mail.settings.server = 'mail:25'
mail.sender = 'sahana@sahanapy.org'

auth = AuthS3(globals(),db)
auth.define_tables()
# Require Admin approval for self-registered users
auth.settings.registration_requires_approval = False
# Require captcha verification for registration
#auth.settings.captcha = RECAPTCHA(request,public_key='RECAPTCHA_PUBLIC_KEY',private_key='RECAPTCHA_PRIVATE_KEY')
# Require Email Verification
auth.settings.registration_requires_verification = False
# Email settings for registration verification
auth.settings.mailer = mail
# ** Amend this to your Publically-accessible URL ***
auth.messages.verify_email = 'Click on the link http://.../verify_email/%(key)s to verify your email'
# Allow use of LDAP accounts for login
# (NB These are not automatically added to PR or to Authenticated role since they enter via the login() method not register())
#from gluon.contrib.login_methods.ldap_auth import ldap_auth
# Active Directory
#auth.settings.login_methods.append(ldap_auth(mode='ad', server='dc.domain.org', base_dn='ou=Users,dc=domain,dc=org'))
# or if not wanting local users at all (no passwords saved within DB):
#auth.settings.login_methods=[ldap_auth(mode='ad', server='dc.domain.org', base_dn='ou=Users,dc=domain,dc=org')]
# Domino
#auth.settings.login_methods.append(ldap_auth(mode='domino', server='domino.domain.org'))
# OpenLDAP
#auth.settings.login_methods.append(ldap_auth(server='demo.sahanapy.org', base_dn='ou=users,dc=sahanapy,dc=org'))
# Allow use of Email accounts for login
#auth.settings.login_methods.append(email_auth("smtp.gmail.com:587", "@gmail.com"))
# We don't wish to clutter the groups list with 1 per user.
auth.settings.create_user_groups = False
# We need to allow basic logins for Webservices
auth.settings.allow_basic_login = False

crud = CrudS3(globals(),db)
# Breaks refresh of List after Create: http://groups.google.com/group/web2py/browse_thread/thread/d5083ed08c685e34
#crud.settings.keepvalues = True

from gluon.tools import Service
service = Service(globals())

# Reusable timestamp fields
timestamp = SQLTable(None, 'timestamp',
            Field('created_on', 'datetime',
                          readable=False,
                          writable=False,
                          default=request.now),
            Field('modified_on', 'datetime',
                          readable=False,
                          writable=False,
                          default=request.now,
                          update=request.now)
            ) 

# Reusable author fields
authorstamp = SQLTable(None, 'authorstamp',
            Field('created_by', db.auth_user,
                          writable=False,
                          default=session.auth.user.id if auth.is_logged_in() else 0,
                          represent = lambda id: (id and [db(db.auth_user.id==id).select()[0].first_name] or ["None"])[0],
                          ondelete='RESTRICT'),
            Field('modified_by', db.auth_user,
                          writable=False,
                          default=session.auth.user.id if auth.is_logged_in() else 0,
                          update=session.auth.user.id if auth.is_logged_in() else 0,
                          represent = lambda id: (id and [db(db.auth_user.id==id).select()[0].first_name] or ["None"])[0],
                          ondelete='RESTRICT')
            ) 

# Reusable UUID field (needed as part of database synchronization)
import uuid
uuidstamp = SQLTable(None, 'uuidstamp',
            Field('uuid', length=64,
                          notnull=True,
                          unique=True,
                          readable=False,
                          writable=False,
                          default=uuid.uuid4()))

# Reusable Deletion status field (needed as part of database synchronization)
# Q: Will this be moved to a separate table? (Simpler for module writers but a performance penalty)
deletion_status = SQLTable(None, 'deletion_status',
            Field('deleted', 'boolean',
                          readable=False,
                          writable=False,
                          default=False))

# Reusable Admin field
admin_id = SQLTable(None, 'admin_id',
            Field('admin', db.auth_group,
                requires = IS_NULL_OR(IS_IN_DB(db, 'auth_group.id', 'auth_group.role')),
                represent = lambda id: (id and [db(db.auth_group.id==id).select()[0].role] or ["None"])[0],
                comment = DIV(A(T('Add Role'), _class='popup', _href=URL(r=request, c='admin', f='group', args='create', vars=dict(format='plain')), _target='top'), A(SPAN("[Help]"), _class="tooltip", _title=T("Admin|The Group whose members can edit data in this record."))),
                ondelete='RESTRICT'
                ))
    
# Custom validators
from applications.sahana.modules.validators import *

from gluon.storage import Storage
# Keep all S3 framework-level elements stored off here, so as to avoid polluting global namespace & to make it clear which part of the framework is being interacted with
# Avoid using this where a method parameter could be used: http://en.wikipedia.org/wiki/Anti_pattern#Programming_anti-patterns
s3 = Storage()
s3.crud_strings = Storage()
s3.display = Storage()

table = 'auth_user'
title_create = T('Add User')
title_display = T('User Details')
title_list = T('List Users')
title_update = T('Edit User')
title_search = T('Search Users')
subtitle_create = T('Add New User')
subtitle_list = T('Users')
label_list_button = T('List Users')
label_create_button = T('Add User')
msg_record_created = T('User added')
msg_record_modified = T('User updated')
msg_record_deleted = T('User deleted')
msg_list_empty = T('No Users currently registered')
s3.crud_strings[table] = Storage(title_create=title_create,title_display=title_display,title_list=title_list,title_update=title_update,title_search=title_search,subtitle_create=subtitle_create,subtitle_list=subtitle_list,label_list_button=label_list_button,label_create_button=label_create_button,msg_record_created=msg_record_created,msg_record_modified=msg_record_modified,msg_record_deleted=msg_record_deleted,msg_list_empty=msg_list_empty)

table = 'auth_group'
title_create = T('Add Role')
title_display = T('Role Details')
title_list = T('List Roles')
title_update = T('Edit Role')
title_search = T('Search Roles')
subtitle_create = T('Add New Role')
subtitle_list = T('Roles')
label_list_button = T('List Roles')
label_create_button = T('Add Role')
msg_record_created = T('Role added')
msg_record_modified = T('Role updated')
msg_record_deleted = T('Role deleted')
msg_list_empty = T('No Roles currently defined')
s3.crud_strings[table] = Storage(title_create=title_create,title_display=title_display,title_list=title_list,title_update=title_update,title_search=title_search,subtitle_create=subtitle_create,subtitle_list=subtitle_list,label_list_button=label_list_button,label_create_button=label_create_button,msg_record_created=msg_record_created,msg_record_modified=msg_record_modified,msg_record_deleted=msg_record_deleted,msg_list_empty=msg_list_empty)

table = 'auth_membership'
title_create = T('Add Membership')
title_display = T('Membership Details')
title_list = T('List Memberships')
title_update = T('Edit Membership')
title_search = T('Search Memberships')
subtitle_create = T('Add New Membership')
subtitle_list = T('Memberships')
label_list_button = T('List Memberships')
label_create_button = T('Add Membership')
msg_record_created = T('Membership added')
msg_record_modified = T('Membership updated')
msg_record_deleted = T('Membership deleted')
msg_list_empty = T('No Memberships currently defined')
s3.crud_strings[table] = Storage(title_create=title_create,title_display=title_display,title_list=title_list,title_update=title_update,title_search=title_search,subtitle_create=subtitle_create,subtitle_list=subtitle_list,label_list_button=label_list_button,label_create_button=label_create_button,msg_record_created=msg_record_created,msg_record_modified=msg_record_modified,msg_record_deleted=msg_record_deleted,msg_list_empty=msg_list_empty)

module = 's3'
# Settings - systemwide
resource = 'setting'
table = module + '_' + resource
db.define_table(table, timestamp, uuidstamp,
                Field('admin_name'),
                Field('admin_email'),
                Field('admin_tel'),
                Field('debug', 'boolean'),
                Field('security_policy'),
                Field('self_registration', 'boolean'),
                Field('audit_read', 'boolean'),
                Field('audit_write', 'boolean'),
                migrate=migrate)
db[table].security_policy.requires = IS_IN_SET(['simple', 'full'])
# Populate table with Default options
# - deployments can change these live via appadmin
if not len(db().select(db[table].ALL)): 
   db[table].insert(
        admin_name = T("Sahana Administrator"),
        admin_email = T("support@Not Set"),
        admin_tel = T("Not Set"),
        # Debug => Load all JS/CSS independently & uncompressed. Change to True for Production deployments (& hence stable branches)
        debug = True,
        # Change to enable a customised security policy
        security_policy = 'simple',
        # Change to False to disable Self-Registration
        self_registration = True,
        # Change to True to enable Auditing at the Global level (if False here, individual Modules can still enable it for them)
        audit_read = False,
        audit_write = False
    )
# Define CRUD strings (NB These apply to all Modules' 'settings' too)
title_create = T('Add Setting')
title_display = T('Setting Details')
title_list = T('List Settings')
title_update = T('Edit Setting')
title_search = T('Search Settings')
subtitle_create = T('Add New Setting')
subtitle_list = T('Settings')
label_list_button = T('List Settings')
label_create_button = T('Add Setting')
msg_record_created = T('Setting added')
msg_record_modified = T('Setting updated')
msg_record_deleted = T('Setting deleted')
msg_list_empty = T('No Settings currently defined')
s3.crud_strings[resource] = Storage(title_create=title_create, title_display=title_display, title_list=title_list, title_update=title_update, subtitle_create=subtitle_create, subtitle_list=subtitle_list, label_list_button=label_list_button, label_create_button=label_create_button, msg_record_created=msg_record_created, msg_record_modified=msg_record_modified, msg_record_deleted=msg_record_deleted, msg_list_empty=msg_list_empty)

# Auth Menu (available in all Modules)
if not auth.is_logged_in():
    self_registration = db().select(db.s3_setting.self_registration)[0].self_registration
    if self_registration:
        response.menu_auth = [
            [T('Login'), False, URL(request.application, 'default', 'user/login'),
             [
                    [T('Register'), False,
                     URL(request.application, 'default', 'user/register')],
                    [T('Lost Password'), False,
                     URL(request.application, 'default', 'user/retrieve_password')]]
             ],
            ]
    else:
        response.menu_auth = [
            [T('Login'), False, URL(request.application, 'default', 'user/login'),
             [
                    [T('Lost Password'), False,
                     URL(request.application, 'default', 'user/retrieve_password')]]
             ],
            ]
else:
    response.menu_auth = [
        ['Logged-in as: ' + auth.user.first_name + ' ' + auth.user.last_name, False, None,
         [
                [T('Logout'), False, 
                 URL(request.application, 'default', 'user/logout')],
                [T('Edit Profile'), False, 
                 URL(request.application, 'default', 'user/profile')],
                [T('Change Password'), False,
                 URL(request.application, 'default', 'user/change_password')]]
         ],
        ]

# Modules
resource = 'module'
table = module + '_' + resource
db.define_table(table,
                Field('name', notnull=True, unique=True),
                Field('name_nice', notnull=True, unique=True),
                Field('access'),  # Hide modules if users don't have the required access level (NB Not yet implemented either in the Modules menu or the Controllers)
                Field('priority', 'integer', notnull=True, unique=True),
                Field('description', length=256),
                Field('enabled', 'boolean', default=True),
                migrate=migrate)
db[table].name.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, '%s.name' % table)]
db[table].name_nice.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, '%s.name_nice' % table)]
db[table].access.requires = IS_NULL_OR(IS_IN_DB(db, 'auth_group.id', 'auth_group.role', multiple=True))
db[table].priority.requires = [IS_NOT_EMPTY(), IS_NOT_IN_DB(db, '%s.priority' % table)]
# Populate table with Default modules
if not len(db().select(db[table].ALL)):
	db[table].insert(
        name="default",
        name_nice="Sahana Home",
        priority=0,
        access='',
        description="",
        enabled='True'
	)
	db[table].insert(
        name="admin",
        name_nice="Administration",
        priority=1,
        access='|1|',        # Administrator
        description="Site Administration",
        enabled='True'
	)
	db[table].insert(
        name="gis",
        name_nice="Mapping",
        priority=2,
        access='',
        description="Situation Awareness & Geospatial Analysis",
        enabled='True'
	)
	db[table].insert(
        name="pr",
        name_nice="Person Registry",
        priority=3,
        access='',
        description="Central point to record details on People",
        enabled='True'
	)
	db[table].insert(
        name="mpr",
        name_nice="Missing Person Registry",
        priority=4,
        access='',
        description="Helps to report and search missing person",
        enabled='True'
	)
	db[table].insert(
        name="dvr",
        name_nice="Disaster Victim Registry",
        priority=5,
        access='',
        description="Traces internally displaced people (IDPs) and their needs",
        enabled='False'
	)
	db[table].insert(
        name="or",
        name_nice="Organization Registry",
        priority=6,
        access='',
        description="Lists 'who is doing what & where'. Allows relief agencies to self organize the activities rendering fine coordination among them",
        enabled='True'
	)
	db[table].insert(
        name="cr",
        name_nice="Shelter Registry",
        priority=7,
        access='',
        description="Tracks the location, distibution, capacity and breakdown of victims in shelter",
        enabled='True'
	)
	db[table].insert(
        name="vol",
        name_nice="Volunteer Registry",
        priority=8,
        access='',
        description="Allows managing volunteers by capturing their skills, availability and allocation",
        enabled='False'
	)
	db[table].insert(
        name="ims",
        name_nice="Inventory Management",
        priority=9,
        access='',
        description="Effectively and efficiently manage relief aid, enables transfer of inventory items to different inventories and notify when items are required to refill",
        enabled='False'
	)
	db[table].insert(
        name="rms",
        name_nice="Request Management",
        priority=10,
        access='',
        description="Tracks requests for aid and matches them against donors who have pledged aid",
        enabled='False'
	)
	db[table].insert(
        name="vita",
        name_nice="Person Tracking and Tracing",
        priority=11,
        access='',
        description="Person Tracking and Tracing",
        enabled='True'
	)
	db[table].insert(
        name="msg",
        name_nice="Messaging Module",
        priority=12,
        access='',
        description="Sends & Receives Alerts via Email & SMS",
        enabled='True'
	)
	db[table].insert(
        name="budget",
        name_nice="Budgeting Module",
        priority=13,
        access='',
        description="Allows a budget to be drawn up",
        enabled='True'
	)

# Authorization
# User Roles (uses native Web2Py Auth Groups)
table = auth.settings.table_group_name
# 1st-run initialisation
if not len(db().select(db[table].ALL)):
    auth.add_group('Administrator', description = 'System Administrator - can access & make changes to any data')
    # Doesn't work on Postgres!
    auth.add_membership(1, 1) # 1st person created will be System Administrator (can be changed later)
    auth.add_group('Anonymous', description = 'Anonymous - dummy group to grant permissions')
    auth.add_group('Authenticated', description = 'Authenticated - all logged-in users')
    auth.add_group('Editor', description = 'Editor - can access & make changes to any unprotected data')
    
# Auditing
# ToDo: consider using native Web2Py log to auth_events
resource = 'audit'
table = module + '_' + resource
db.define_table(table,timestamp,
                Field('person', db.auth_user, ondelete='RESTRICT'),
                Field('operation'),
                Field('representation'),
                Field('module'),
                Field('resource'),
                Field('record', 'integer'),
                Field('old_value'),
                Field('new_value'),
                migrate=migrate)
db[table].operation.requires = IS_IN_SET(['create', 'read', 'update', 'delete', 'list', 'search'])

# Settings - appadmin
module = 'appadmin'
resource = 'setting'
table = module + '_' + resource
db.define_table(table,
                Field('audit_read', 'boolean'),
                Field('audit_write', 'boolean'),
                migrate=migrate)
# Populate table with Default options
# - deployments can change these live via appadmin
if not len(db().select(db[table].ALL)): 
   db[table].insert(
        # If Disabled at the Global Level then can still Enable just for this Module here
        audit_read = False,
        audit_write = False
    )

def shn_sessions(f):
    """
    Extend session to support:
        Multiple flash classes
        Settings
            Debug mode
            Audit modes
    """
    response.error = session.error
    response.confirmation = session.confirmation
    response.warning = session.warning
    session.error = []
    session.confirmation = []
    session.warning = []
    # Keep all our configuration options in a single global variable
    if not session.s3:
        session.s3 = Storage()
    # Are we running in debug mode?
    session.s3.debug = db().select(db.s3_setting.debug)[0].debug
    # We Audit if either the Global or Module asks us to (ignore gracefully if module author hasn't implemented this)
    try:
        session.s3.audit_read = db().select(db.s3_setting.audit_read)[0].audit_read or db().select(db['%s_setting' % request.controller].audit_read)[0].audit_read
    except:
        session.s3.audit_read = db().select(db.s3_setting.audit_read)[0].audit_read
    try:
        session.s3.audit_write = db().select(db.s3_setting.audit_write)[0].audit_write or db().select(db['%s_setting' % request.controller].audit_write)[0].audit_write
    except:
        session.s3.audit_write = db().select(db.s3_setting.audit_write)[0].audit_write
    return f()
response._caller = lambda f: shn_sessions(f)

# Modules Menu (available in all Controllers)
response.menu_modules = []
modules = db(db.s3_module.enabled=='Yes').select(db.s3_module.ALL,orderby=db.s3_module.priority)
for module in modules:
    if not module.access:
        response.menu_modules.append([T(module.name_nice), False, URL(r=request, c='default', f='open_module', vars=dict(id='%d' % module.id))])
    else:
        authorised = False
        groups = re.split('\|', module.access)[1:-1]
        for group in groups:
            if auth.has_membership(group):
                authorised = True
        if authorised == True:
            response.menu_modules.append([T(module.name_nice), False, URL(r=request, c='default', f='open_module', vars=dict(id='%d' % module.id))])

#
# Widgets
#

# See test.py

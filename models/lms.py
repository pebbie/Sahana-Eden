﻿# -*- coding: utf-8 -*-

module = 'lms'

# Settings
resource = 'setting'
table = module + '_' + resource
db.define_table(table,
                db.Field('audit_read', 'boolean'),
                db.Field('audit_write', 'boolean'),
                migrate=migrate)
# Populate table with Default options
# - deployments can change these live via appadmin
if not len(db().select(db[table].ALL)): 
   db[table].insert(
        # If Disabled at the Global Level then can still Enable just for this Module here
        audit_read = False,
        audit_write = False
    )

# Sites
resource = 'site'
table = module + '_' + resource
db.define_table(table,timestamp,uuidstamp,
                db.Field('name', notnull=True),
                db.Field('description', length=256),
                admin_id,
                location_id,
                person_id,
                db.Field('address', 'text'),
                db.Field('area'),
                migrate=migrate)
db[table].uuid.requires = IS_NOT_IN_DB(db,'%s.uuid' % table)
db[table].name.requires = IS_NOT_EMPTY()   # Sites don't have to have unique names
db[table].name.label = T("Site Name")
db[table].name.comment = SPAN("*", _class="req")
db[table].admin.label = T("Site Manager")
db[table].person_id.label = T("Contact Person")
title_create = T('Add Site ')
title_display = T('Site Details')
title_list = T('List Sites')
title_update = T('Edit Site')
title_search = T('Search Site(s)')
subtitle_create = T('Add New Site')
subtitle_list = T('Shelters')
label_list_button = T('List Sites')
label_create_button = T('Add Site')
msg_record_created = T('Site added')
msg_record_modified = T('Site updated')
msg_record_deleted = T('Site deleted')
msg_list_empty = T('No Sites currently registered')
s3.crud_strings[table] = Storage(title_create=title_create,title_display=title_display,title_list=title_list,title_update=title_update,title_search=title_search,subtitle_create=subtitle_create,subtitle_list=subtitle_list,label_list_button=label_list_button,label_create_button=label_create_button,msg_record_created=msg_record_created,msg_record_modified=msg_record_modified,msg_record_deleted=msg_record_deleted,msg_list_empty=msg_list_empty)

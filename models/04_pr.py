# -*- coding: utf-8 -*-

#
# Sahanapy Person Registry
#
# created 2009-07-23 by nursix
#
# This part defines PR joined resources:
#       - Address
#       - Contact
#       - Image
#       - Presence Log
#       - Identity
#       - Role
#       - Group Membership
#       - Network (network)         - a social network layer of a person
#       - Network Membership
#       - Case
#       - Finding

module = 'pr'

# *****************************************************************************
# Address (address)
#
pr_address_type_opts = {
    1:T('Home Address'),
    2:T('Office Address'),
    3:T('Holiday Address'),
    99:T('other')
    }

opt_pr_address_type = SQLTable(None, 'opt_pr_address_type',
                        Field('opt_pr_address_type','integer',
                            requires = IS_IN_SET(pr_address_type_opts),
                            default = 99,
                            label = T('Address Type'),
                            represent = lambda opt: opt and pr_address_type_opts[opt]))

#
# address table ---------------------------------------------------------------
#
resource = 'address'
table = module + '_' + resource
db.define_table(table, timestamp, uuidstamp, deletion_status,
                    pr_pe_id,                           # Person Entity ID
                    opt_pr_address_type,                # Address type
                    Field('co_name'),                   # c/o Name
                    Field('street1'),                   # Street Address 1
                    Field('street2'),                   # Street Address 2
                    Field('postcode'),                  # ZIP or postal code
                    Field('city'),                      # City
                    Field('state'),                     # State or Province
                    opt_pr_country,                     # Country
                    location_id,                        # Link to GIS location
                    Field('lat'),                       # Latitude
                    Field('lon'),                       # Longitude
                    Field('comment'),                   # Comment
                    migrate=migrate)

# Joined Resource
jrlayer.add_jresource(module, resource,
    multiple=True,
    joinby='pr_pe_id',
    deletable=True,
    editable=True,
    list_fields = ['id', 'opt_pr_address_type', 'co_name', 'street1', 'postcode', 'city', 'opt_pr_country'])

# Field validation
db[table].uuid.requires = IS_NOT_IN_DB(db, '%s.uuid' % table)
db[table].pr_pe_id.requires = IS_ONE_OF(db, 'pr_pentity.id', shn_pentity_represent, filterby='opt_pr_entity_type', filter_opts=(1, 2))
db[table].lat.requires = IS_NULL_OR(IS_LAT())
db[table].lon.requires = IS_NULL_OR(IS_LON())

# Field representation

# Field labels
db[table].co_name.label = T('c/o Name')
db[table].street1.label = T('Street')
db[table].street2.label = T('Street (add.)')
db[table].postcode.label = T('ZIP/Postcode')
db[table].opt_pr_country.label = T('Country')

# CRUD Strings
title_create = T('Add Address')
title_display = T('Address Details')
title_list = T('List Addresses')
title_update = T('Edit Address')
title_search = T('Search Addresses')
subtitle_create = T('Add New Address')
subtitle_list = T('Addresses')
label_list_button = T('List Addresses')
label_create_button = T('Add Address')
msg_record_created = T('Address added')
msg_record_modified = T('Address updated')
msg_record_deleted = T('Address deleted')
msg_list_empty = T('No Addresses currently registered')
s3.crud_strings[table] = Storage(title_create=title_create,title_display=title_display,title_list=title_list,title_update=title_update,title_search=title_search,subtitle_create=subtitle_create,subtitle_list=subtitle_list,label_list_button=label_list_button,label_create_button=label_create_button,msg_record_created=msg_record_created,msg_record_modified=msg_record_modified,msg_record_deleted=msg_record_deleted,msg_list_empty=msg_list_empty)

# *****************************************************************************
# Contact (contact)
#

#
# Contact Methods -------------------------------------------------------------
#
pr_contact_method_opts = {
    1:T('E-Mail'),
    2:T('Telephone'),
    3:T('Mobile Phone'),
    4:T('Fax'),
    99:T('other')
    }

opt_pr_contact_method = SQLTable(None, 'opt_pr_contact_method',
                        Field('opt_pr_contact_method', 'integer',
                            requires = IS_IN_SET(pr_contact_method_opts),
                            default = 99,
                            label = T('Contact Method'),
                            represent = lambda opt: opt and pr_contact_method_opts[opt]))

#
# contact table ---------------------------------------------------------------
#
resource = 'contact'
table = module + '_' + resource
db.define_table(table, timestamp, uuidstamp, deletion_status,
                pr_pe_id,                               # Person Entity ID
                Field('name'),                          # Contact name (optional)
                opt_pr_contact_method,                  # Contact Method
                Field('person_name'),                   # Contact person name
                Field('priority'),                      # Priority
                Field('value', notnull=True),
                Field('comment'),                       # Comment
                migrate=migrate)

# Joined Resource
jrlayer.add_jresource(module, resource,
    multiple=True,
    joinby='pr_pe_id',
    deletable=True,
    editable=True,
    list_fields = ['id', 'name', 'person_name', 'opt_pr_contact_method', 'value', 'priority'])

# Field validation
db[table].uuid.requires = IS_NOT_IN_DB(db, '%s.uuid' % table)
db[table].pr_pe_id.requires = IS_ONE_OF(db, 'pr_pentity.id', shn_pentity_represent, filterby='opt_pr_entity_type', filter_opts=(1, 2))
db[table].value.requires = IS_NOT_EMPTY()
db[table].priority.requires = IS_IN_SET([1,2,3,4,5,6,7,8,9])

# Field representation

# Field labels

# CRUD Strings
title_create = T('Add Contact')
title_display = T('Contact Details')
title_list = T('List Contacts')
title_update = T('Edit Contact')
title_search = T('Search Contacts')
subtitle_create = T('Add New Contact')
subtitle_list = T('Contacts')
label_list_button = T('List Contacts')
label_create_button = T('Add Contact')
msg_record_created = T('Contact added')
msg_record_modified = T('Contact updated')
msg_record_deleted = T('Contact deleted')
msg_list_empty = T('No Contacts currently registered')
s3.crud_strings[table] = Storage(title_create=title_create,title_display=title_display,title_list=title_list,title_update=title_update,title_search=title_search,subtitle_create=subtitle_create,subtitle_list=subtitle_list,label_list_button=label_list_button,label_create_button=label_create_button,msg_record_created=msg_record_created,msg_record_modified=msg_record_modified,msg_record_deleted=msg_record_deleted,msg_list_empty=msg_list_empty)

# *****************************************************************************
# Image (image)
#

#
# Image Types -----------------------------------------------------------------
#
pr_image_type_opts = {
    1:T('Photograph'),
    2:T('Sketch'),
    3:T('Fingerprint'),
    4:T('X-Ray'),
    5:T('Document Scan'),
    99:T('other')
    }

opt_pr_image_type = SQLTable(None, 'opt_pr_image_type',
                    db.Field('opt_pr_image_type', 'integer',
                    requires = IS_IN_SET(pr_image_type_opts),
                    default = 1,
                    label = T('Image Type'),
                    represent = lambda opt: opt and pr_image_type_opts[opt]))

#
# image table -----------------------------------------------------------------
#
resource = 'image'
table = module + '_' + resource
db.define_table(table, timestamp, uuidstamp, deletion_status,
                pr_pe_id,
                opt_pr_image_type,
                Field('title'),
                Field('image', 'upload', autodelete=True),
                Field('description'),
                Field('comment'),
                migrate=migrate)

# Joined Resource
jrlayer.add_jresource(module, resource,
    multiple=True,
    joinby='pr_pe_id',
    deletable=True,
    editable=True,
    list_fields = ['id', 'opt_pr_image_type', 'image', 'title','description'])

# Field validation
db[table].uuid.requires = IS_NOT_IN_DB(db, '%s.uuid' % table)

# Field representation
db[table].image.represent = lambda image: DIV(IMG(_src=URL(r=request, c='default', f='download', args=image),_height=60))

# Field labels

# CRUD Strings
title_create = T('Image')
title_display = T('Image Details')
title_list = T('List Images')
title_update = T('Edit Image Details')
title_search = T('Search Images')
subtitle_create = T('Add New Image')
subtitle_list = T('Images')
label_list_button = T('List Images')
label_create_button = T('Add Image')
msg_record_created = T('Image added')
msg_record_modified = T('Image updated')
msg_record_deleted = T('Image deleted')
msg_list_empty = T('No Images currently registered')
s3.crud_strings[table] = Storage(title_create=title_create,title_display=title_display,title_list=title_list,title_update=title_update,title_search=title_search,subtitle_create=subtitle_create,subtitle_list=subtitle_list,label_list_button=label_list_button,label_create_button=label_create_button,msg_record_created=msg_record_created,msg_record_modified=msg_record_modified,msg_record_deleted=msg_record_deleted,msg_list_empty=msg_list_empty)

# *****************************************************************************
# Presence Log (presence)
#

#
# Presence Conditions ---------------------------------------------------------
#
pr_presence_condition_opts = vita.presence_conditions

opt_pr_presence_condition = SQLTable(None, 'opt_pr_presence_condition',
                        Field('opt_pr_presence_condition', 'integer',
                            requires = IS_IN_SET(pr_presence_condition_opts),
                            default = vita.DEFAULT_PRESENCE,
                            label = T('Presence Condition'),
                            represent = lambda opt: opt and pr_presence_condition_opts[opt]))

#
# presence table --------------------------------------------------------------
#
resource = 'presence'
table = module + '_' + resource
db.define_table(table, timestamp, uuidstamp, deletion_status,
                pr_pe_id,                           # Personal Entity Reference
                Field('observer'),                  # Person observing
                Field('reporter'),                  # Person reporting
                location_id,                        # Named Location Reference
                Field('location_details'),          # Details on Location
                Field('lat'),                       # Latitude
                Field('lon'),                       # Longitude
                Field('time', 'datetime'),          # Time
                opt_pr_presence_condition,          # Presence Condition
                Field('procedure'),                 # Procedure description (for procedure) TODO: replace by option field?
                Field('origin'),                    # Origin (for transfer and transit) TODO: replace by location reference?
                Field('destination'),               # Destination (for transfer and transit) TODO: replace by location reference?
                Field('comment'),                   # a comment (optional)
                migrate=migrate)

# RSS
def shn_pr_presence_rss(record):
    if record:
        if record.location_details and len(record.location_details.strip())>0:
            location_details = record.location_details.strip()
        else:
            location_details = None
        return "<b>%s</b>: %s %s<br/>[Lat: %s Lon: %s]<br/>%s" % (
            pr_presence_condition_opts[record.opt_pr_presence_condition],
            record.location and location_id.location.represent(record.location) or "Unknown location",
            location_details and "/ %s" % location_details or "",
            record.lat and "Lat: %s " % record.lat or "",
            record.lon and "Lon: %s " % record.lon or "",
#            opt_pr_presence_condition.opt_pr_presence_condition.represent(record.opt_pr_presence_condition),
            record.procedure or "-")
    else:
        return None

# Joined Resource
jrlayer.add_jresource(module, resource,
    multiple=True,
    joinby='pr_pe_id',
    deletable=True,
    editable=True,
    main='time', extra='location_details',
    rss=dict(
        title="%(time)s",
        description=shn_pr_presence_rss
    ),
    list_fields = ['id','time','location','location_details','lat','lon','opt_pr_presence_condition','origin','destination'])

# Field validation
db[table].uuid.requires = IS_NOT_IN_DB(db, '%s.uuid' % table)
db[table].lat.requires = IS_NULL_OR(IS_LAT())
db[table].lon.requires = IS_NULL_OR(IS_LON())

# Field representation
db[table].observer.requires = IS_NULL_OR(IS_ONE_OF(db, 'pr_person.id', shn_pr_person_represent))
db[table].observer.represent = lambda id: (id and [shn_pr_person_represent(id)] or ["None"])[0]

db[table].observer.comment = DIV(A(T('Add Person'), _class='popup', _href=URL(r=request, c='pr', f='person', args='create', vars=dict(format='plain')), _target='top'), A(SPAN("[Help]"), _class="tooltip", _title=T("Create Person Entry|Create a person entry in the registry."))),
db[table].observer.ondelete = 'RESTRICT'

db[table].reporter.requires = IS_NULL_OR(IS_ONE_OF(db, 'pr_person.id', shn_pr_person_represent))
db[table].reporter.represent = lambda id: (id and [shn_pr_person_represent(id)] or ["None"])[0]
db[table].reporter.comment = DIV(A(T('Add Person'), _class='popup', _href=URL(r=request, c='pr', f='person', args='create', vars=dict(format='plain')), _target='top'), A(SPAN("[Help]"), _class="tooltip", _title=T("Create Person Entry|Create a person entry in the registry."))),
db[table].reporter.ondelete = 'RESTRICT'

db[table].time.requires = IS_UTC_DATETIME(utc_offset=shn_user_utc_offset(), allow_future=False)
db[table].time.represent = lambda value: shn_as_local_time(value)

# Field labels
db[table].time.label = T('Date/Time')

# CRUD Strings
title_create = T('Add Log Entry')
title_display = T('Log Entry Details')
title_list = T('Presence Log')
title_update = T('Edit Log Entry')
title_search = T('Search Log Entry')
subtitle_create = T('Add New Log Entry')
subtitle_list = T('Current Log Entries')
label_list_button = T('List Log Entries')
label_create_button = T('Add Log Entry')
msg_record_created = T('Log entry added')
msg_record_modified = T('Log entry updated')
msg_record_deleted = T('Log entry deleted')
msg_list_empty = T('No Presence Log Entries currently registered')
s3.crud_strings[table] = Storage(title_create=title_create,title_display=title_display,title_list=title_list,title_update=title_update,title_search=title_search,subtitle_create=subtitle_create,subtitle_list=subtitle_list,label_list_button=label_list_button,label_create_button=label_create_button,msg_record_created=msg_record_created,msg_record_modified=msg_record_modified,msg_record_deleted=msg_record_deleted,msg_list_empty=msg_list_empty)

# *****************************************************************************
# Physical Description (pd_xxx)
#   - for identification purposes
#   - following Interpol DVI Forms http://www.interpol.int/Public/DisasterVictim/Forms
#   - appliable for both Missing Persons and Dead Bodies
#
#   TODO: elaborate on field types and field options!
#

#
# Field options ---------------------------------------------------------------
#
pr_bodily_constitution_opts = {
    1:T('light'),
    2:T('medium'),
    3:T('heavy'),
    99:T('unspecified')
    }

opt_pr_bodily_constitution = SQLTable(None, 'opt_pr_bodily_constitution',
                                db.Field('opt_pr_bodily_constitution', 'integer',
                                requires = IS_IN_SET(pr_bodily_constitution_opts),
                                default = 99,
                                label = T('Bodily Constitution'),
                                represent = lambda opt: opt and pr_bodily_constitution_opts[opt]))

#
# Physical Description Tables -------------------------------------------------
#
resource = 'pd_general'
table = module + '_' + resource
db.define_table(table, timestamp, uuidstamp, deletion_status,
                pr_pe_id,
                Field('est_age'),                       # D1-31A   Estimated Age
                Field('height'),                        # D1-32    Height
                Field('weight'),                        # D1-33    Weight
                opt_pr_bodily_constitution,             # D1-34/01 Bodily Constitution
                Field('race_group'),                    # D1-35/01 Race, group
                Field('race_type'),                     # D1-35/01 Race, type
                Field('race_complexion'),               # D1-35/01 Race, complexion
                Field('specific_details_head'),         # D3-53    Specific Details
                Field('specific_details_throat'),       # D3-53    Specific Details
                Field('specific_details_arm_left'),     # D3-53    Specific Details
                Field('specific_details_arm_right'),    # D3-53    Specific Details
                Field('specific_details_hand_left'),    # D3-53    Specific Details
                Field('specific_details_hand_right'),   # D3-53    Specific Details
                Field('specific_details_body_front'),   # D3-53    Specific Details
                Field('specific_details_body_back'),    # D3-53    Specific Details
                Field('specific_details_leg_left'),     # D3-53    Specific Details
                Field('specific_details_leg_right'),    # D3-53    Specific Details
                Field('specific_details_foot_left'),    # D3-53    Specific Details
                Field('specific_details_foot_right'),   # D3-53    Specific Details
                Field('other_peculiarities', 'text'),   # D3-55    Other Peculiarities
                Field('body_sketch'),                   # D4       Body Sketch
                migrate=migrate)

# Joined Resource
jrlayer.add_jresource(module, resource, multiple=False, joinby='pr_pe_id', deletable=False, editable=True)

resource = 'pd_head'
table = module + '_' + resource
db.define_table(table, timestamp, uuidstamp, deletion_status,
                pr_pe_id,
                Field('head_form_front'),               # D1-34/02 Head form, front
                Field('head_form_profile'),             # D1-34/03 Head form, profile
                Field('hair_head_type'),                # D1-36/01 Hair of the head, Type
                Field('hair_head_length'),              # D1-36/02 Hair of the head, Length
                Field('hair_head_colour'),              # D1-36/03 Hair of the head, Colour
                Field('hair_head_shade'),               # D1-36/04 Hair of the head, Shade of colour
                Field('hair_head_thickness'),           # D1-36/05 Hair of the head, Thickness
                Field('hair_head_style'),               # D1-36/06 Hair of the head, Style
                Field('hair_head_parting'),             # D1-36/06 Hair of the head, Parting
                Field('hair_head_baldness_ext'),        # D1-36/07 Hair of the head, Baldness (extent)
                Field('hair_head_baldness_loc'),        # D1-36/07 Hair of the head, Baldness (location)
                Field('hair_head_other'),               # D1-36/08 Hair of the head, Other information
                migrate=migrate)

# Joined Resource
jrlayer.add_jresource(module, resource, multiple=False, joinby='pr_pe_id', deletable=False, editable=True)

resource = 'pd_face'
table = module + '_' + resource
db.define_table(table, timestamp, uuidstamp, deletion_status,
                pr_pe_id,
                Field('forehead_height'),               # D2-37/01 Forehead, Height
                Field('forehead_width'),                # D2-37/01 Forehead, Width
                Field('forehead_inclination'),          # D2-37/02 Forehead, Inclination
                Field('eyebrows_shape'),                # D2-38/01 Eyebrows, Shape
                Field('eyebrows_thickness'),            # D2-38/01 Eyebrows, Thickness
                Field('eyebrows_peculiarities'),        # D2-38/02 Eyebrows, Peculiarities
                Field('eyes_colour'),                   # D2-39/01 Eyes, Colour
                Field('eyes_shade'),                    # D2-39/02 Eyes, Shade
                Field('eyes_distance'),                 # D2-39/03 Eyes, Distance between Eyes
                Field('eyes_peculiarities'),            # D2-39/04 Eyes, Peculiarities
                Field('nose_size'),                     # D2-40/01 Nose, size
                Field('nose_shape'),                    # D2-40/01 Nose, shape
                Field('nose_spectacle_marks'),          # D2-40/02 Nose, Peculiarities - Marks of spectacles
                Field('nose_misshapen'),                # D2-40/02 Nose, Peculiarities - Misshapen
                Field('nose_peculiarities'),            # D2-40/02 Nose, Peculiarities
                Field('nose_curve'),                    # D2-40/03 Nose, Curve
                Field('nose_angle'),                    # D2-40/03 Nose, Angle
                Field('hair_facial_type'),              # D2-41/01 Facial hair, Type
                Field('hair_facial_colour'),            # D2-41/02 Facial hair, Colour
                Field('ears_size'),                     # D2-42/01 Ears, size
                Field('ears_angle'),                    # D2-42/01 Ears, angle
                Field('ears_lobes_attached'),           # D2-42/02 Ears, Ear Lobes
                Field('ears_piercings_left'),           # D2-42/02 Ears, Number of Piercings, left
                Field('ears_piercings_right'),          # D2-42/02 Ears, Number of Piercings, right
                Field('mouth_size'),                    # D2-43/01 Mouth, Size
                Field('mouth_other'),                   # D2-43/01 Mouth, Other
                Field('lips_shape'),                    # D2-44/01 Lips, Shape
                Field('lips_other'),                    # D2-44/01 Lips, Other
                Field('chin_size'),                     # D3-47/01 Chin, Size
                Field('chin_inclination'),              # D3-47/01 Chin, Inclination
                Field('chin_shape'),                    # D3-47/02 Chin, Shape
                migrate=migrate)

# Joined Resource
jrlayer.add_jresource(module, resource, multiple=False, joinby='pr_pe_id', deletable=False, editable=True)

resource = 'pd_teeth'
table = module + '_' + resource
db.define_table(table, timestamp, uuidstamp, deletion_status,
                pr_pe_id,
                Field('teeth_natural', 'boolean', default=True),        # D2-45/01 Teeth, Conditions
                Field('teeth_treated', 'boolean', default=False),       # D2-45/01 Teeth, Conditions
                Field('teeth_crowns', 'boolean', default=False),        # D2-45/01 Teeth, Conditions
                Field('teeth_bridges', 'boolean', default=False),       # D2-45/01 Teeth, Conditions
                Field('teeth_implants', 'boolean', default=False),      # D2-45/01 Teeth, Conditions
                Field('teeth_gaps'),                    # D2-45/02 Teeth, Gaps between front teeth
                Field('teeth_missing'),                 # D2-45/02 Teeth, Missing teeth
                Field('teeth_toothless'),               # D2-45/02 Teeth, Toothless
                Field('teeth_dentures_lower'),          # D2-45/03 Teeth, Dentures
                Field('teeth_dentures_upper'),          # D2-45/03 Teeth, Dentures
                Field('teeth_dentures_id'),             # D2-45/03 Teeth, Dentures, ID-number
                migrate=migrate)

# Joined Resource
jrlayer.add_jresource(module, resource, multiple=False, joinby='pr_pe_id', deletable=False, editable=True)

resource = 'pd_body'
table = module + '_' + resource
db.define_table(table, timestamp, uuidstamp, deletion_status,
                pr_pe_id,
                Field('neck_length'),                   # D3-48/01 Neck, Length
                Field('neck_shape'),                    # D3-48/01 Neck, Shape
                Field('neck_peculiarities'),            # D3-48/02 Neck, Peculiarities
                Field('neck_collar_size'),              # D3-48/02 Neck, Collar Size
                Field('neck_circumference'),            # D3-48/02 Neck, Circumference
                Field('hands_shape'),                   # D3-49/01 Hands, Shape
                Field('hands_size'),                    # D3-49/01 Hands, Size
                Field('hands_nails_length'),            # D3-49/02 Hands, Nail length
                Field('hands_nails_peculiarities'),     # D3-49/03 Hands, Nail peculiarities
                Field('hands_nicotine'),                # D3-49/03 Hands, Nicotine
                Field('feet_shape'),                    # D3-50/01 Feet, Shape
                Field('feet_size'),                     # D3-50/01 Feet, Size
                Field('feet_condition'),                # D3-50/02 Feet, Condition
                Field('feet_nails'),                    # D3-50/02 Feet, Nails
                Field('feet_peculiarities'),            # D3-50/03 Feet, Peculiarities
                Field('hair_body_extent'),              # D3-51/01 Body hair, Extent
                Field('hair_body_colour'),              # D3-51/02 Body hair, Colour
                Field('hair_pubic_extent'),             # D3-52/01 Pubic hair, Extent
                Field('hair_pubic_colour'),             # D3-52/02 Pubic hair, Colour
                Field('circumcision'),                  # D3-54    Circumcision
                Field('smoking_habits'),                # D2-46/01 Smoking Habits, Type
                Field('smoking_stains'),                # D2-46/01 Smoking Habits, Stains Found
                migrate=migrate)

# Joined Resource
jrlayer.add_jresource(module, resource, multiple=False, joinby='pr_pe_id', deletable=False, editable=True)

# *****************************************************************************
# Identity (identity)
#

#
# ID Types --------------------------------------------------------------------
#
pr_id_type_opts = {
    1:T('Passport'),
    2:T('National ID Card'),
    3:T('Driving License'),
    99:T('other')
    }

opt_pr_id_type = SQLTable(None, 'opt_pr_id_type',
                    Field('opt_pr_id_type', 'integer',
                        requires = IS_IN_SET(pr_id_type_opts),
                        default = 1,
                        label = T('ID type'),
                        represent = lambda opt: opt and pr_id_type_opts[opt]))

#
# identitiy table -------------------------------------------------------------
#
resource = 'identity'
table = module + '_' + resource
db.define_table(table, timestamp, uuidstamp, deletion_status,
                person_id,                          # Reference to person
                opt_pr_id_type,                     # ID type
                Field('type'),                      # Description for type 'Other'
                Field('value'),                     # ID value
                Field('country_code', length=4),    # Country Code (for National ID Cards)
                Field('ia_name'),                   # Name of issuing authority
#                Field('ia_subdivision'),            # Name of issuing authority subdivision
#                Field('ia_code'),                   # Code of issuing authority (if any)
                Field('comment'))                   # a comment (optional)

# Joined Resource
jrlayer.add_jresource(module, resource,
    multiple=True,
    joinby=dict(pr_person='person_id'),
    deletable=True,
    editable=True,
    list_fields = ['id', 'opt_pr_id_type', 'type', 'value', 'country_code', 'ia_name'])

# Field validation
db[table].uuid.requires = IS_NOT_IN_DB(db, '%s.uuid' % table)

# Field representation

# Field labels
db[table].ia_name.label = T("Issuing Authority")

# CRUD Strings
title_create = T('Add Identity')
title_display = T('Identity Details')
title_list = T('Known Identities')
title_update = T('Edit Identity')
title_search = T('Search Identity')
subtitle_create = T('Add New Identity')
subtitle_list = T('Current Identities')
label_list_button = T('List Identities')
label_create_button = T('Add Identity')
msg_record_created = T('Identity added')
msg_record_modified = T('Identity updated')
msg_record_deleted = T('Identity deleted')
msg_list_empty = T('No Identities currently registered')
s3.crud_strings[table] = Storage(title_create=title_create,title_display=title_display,title_list=title_list,title_update=title_update,title_search=title_search,subtitle_create=subtitle_create,subtitle_list=subtitle_list,label_list_button=label_list_button,label_create_button=label_create_button,msg_record_created=msg_record_created,msg_record_modified=msg_record_modified,msg_record_deleted=msg_record_deleted,msg_list_empty=msg_list_empty)

# *****************************************************************************
# Role (role)
#

#
# role table ------------------------------------------------------------------
#
resource = 'role'
table = module + '_' + resource
db.define_table(table, timestamp, deletion_status,
                person_id,
                Field('description'),
                migrate=migrate)

# *****************************************************************************
# Group membership (group_membership)
#

#
# group_membership table ------------------------------------------------------
#
resource = 'group_membership'
table = module + '_' + resource
db.define_table(table, timestamp, deletion_status,
                group_id,
                person_id,
                Field('group_head', 'boolean', default=False),
                Field('description'),
                Field('comment'),
                migrate=migrate)

# Joined Resource
jrlayer.add_jresource(module, resource,
    multiple=True,
    joinby=dict(pr_group='group_id', pr_person='person_id'),
    deletable=True,
    editable=True,
    list_fields = ['id', 'group_id', 'person_id', 'group_head', 'description'])

# Field validation

# Field representation
db[table].group_head.represent = lambda group_head: (group_head and [T('yes')] or [''])[0]

# Field labels

# CRUD Strings
title_create = T('Add Group Membership')
title_display = T('Group Membership Details')
title_list = T('Group Memberships')
title_update = T('Edit Membership')
title_search = T('Search Membership')
subtitle_create = T('Add New Group Membership')
subtitle_list = T('Current Group Memberships')
label_list_button = T('List All Group Memberships')
label_create_button = T('Add Group Membership')
msg_record_created = T('Group Membership added')
msg_record_modified = T('Group Membership updated')
msg_record_deleted = T('Group Membership deleted')
msg_list_empty = T('No Group Memberships currently registered')
s3.crud_strings[table] = Storage(title_create=title_create,title_display=title_display,title_list=title_list,title_update=title_update,title_search=title_search,subtitle_create=subtitle_create,subtitle_list=subtitle_list,label_list_button=label_list_button,label_create_button=label_create_button,msg_record_created=msg_record_created,msg_record_modified=msg_record_modified,msg_record_deleted=msg_record_deleted,msg_list_empty=msg_list_empty)

# *****************************************************************************
# Network (network)
#
pr_network_type_opts = {
    1:T('Family'),
    2:T('Friends'),
    3:T('Colleagues'),
    99:T('other')
    }

opt_pr_network_type = SQLTable(None, 'opt_pr_network_type',
                    Field('opt_pr_network_type','integer',
                        requires = IS_IN_SET(pr_network_type_opts),
                        default = 99,
                        label = T('Network Type'),
                        represent = lambda opt: opt and pr_network_type_opts[opt]))

#
# network table ---------------------------------------------------------------
#
resource = 'network'
table = module + '_' + resource
db.define_table(table, timestamp, uuidstamp, deletion_status,
                person_id,                          # Reference to person (owner)
                opt_pr_network_type,                # Network type
                Field('comment'),                   # a comment (optional)
                migrate=migrate)

# Joined Resource
jrlayer.add_jresource(module, resource,
    multiple=True,
    joinby=dict(pr_person='person_id'),
    deletable=True,
    editable=True,
    list_fields = ['id', 'opt_pr_network_type', 'comment'])

# Field validation
db[table].uuid.requires = IS_NOT_IN_DB(db, '%s.uuid' % table)

# Field representation

# Field labels

# CRUD Strings

#
# network_id: reusable field for other tables to reference ----------------------
#
network_id = SQLTable(None, 'network_id',
                Field('network_id', db.pr_network,
                requires = IS_NULL_OR(IS_ONE_OF(db, 'pr_network.id', '%(id)s')),
                represent = lambda id: (id and [db(db.pr_network.id==id).select()[0].id] or ["None"])[0],
                comment = DIV(A(T('Add Network'), _class='popup', _href=URL(r=request, c='pr', f='network', args='create', vars=dict(format='plain')), _target='top'), A(SPAN("[Help]"), _class="tooltip", _title=T("Create Network|Create a social network layer for a person."))),
                ondelete = 'RESTRICT'
                ))

# *****************************************************************************
# Network membership (network_membership)
#

#
# network_membership table ----------------------------------------------------
#
resource = 'network_membership'
table = module + '_' + resource
db.define_table(table, timestamp, deletion_status,
                network_id,
                person_id,
                Field('description'),
                Field('comment'),
                migrate=migrate)

# Joined Resource
jrlayer.add_jresource(module, resource,
    multiple=True,
    joinby=dict(pr_person='person_id'),
    deletable=True,
    editable=True,
    list_fields = ['id','network_id','person_id','description','comment'])

# Field validation

# Field representation

# Field labels

# CRUD Strings

# *****************************************************************************
# Case (case)
#

#
# case table ------------------------------------------------------------------
#
resource = 'case'
table = module + '_' + resource
db.define_table(table, timestamp, uuidstamp, deletion_status,
                Field('description'),               # Short Description
                Field('details','text'),            # Detailed Description
                Field('comment'),                   # a comment (optional)
                migrate=migrate)
db[table].uuid.requires = IS_NOT_IN_DB(db, '%s.uuid' % table)

# Reusable field for other tables to reference
pcase_id = SQLTable(None, 'pcase_id',
                Field('pcase_id', db.pr_case,
                requires = IS_NULL_OR(IS_ONE_OF(db, 'pr_case.id', '%(description)s')),
                represent = lambda id: (id and [db(db.pr_case.id==id).select()[0].description] or ["None"])[0],
                comment = DIV(A(T('Add Case'), _class='popup', _href=URL(r=request, c='pr', f='case', args='create', vars=dict(format='plain')), _target='top'), A(SPAN("[Help]"), _class="tooltip", _title=T("Case|Add new case."))),
                ondelete = 'RESTRICT'
                ))

# *****************************************************************************
# Finding (finding)
#

#
# finding table ---------------------------------------------------------------
#
resource = 'finding'
table = module + '_' + resource
db.define_table(table, timestamp, uuidstamp, deletion_status,
                pr_pe_id,                      # about which entity?
#                opt_pr_findings_type,           # Finding type
                Field('description'),           # Descriptive title
                Field('module'),                # Access module
                Field('resource'),              # Access resource
                Field('resource_id'),           # Access ID
                migrate=migrate)

db[table].uuid.requires = IS_NOT_IN_DB(db, '%s.uuid' % table)
db[table].module.requires = IS_NULL_OR(IS_ONE_OF(db, 's3_module.name', '%(name_nice)s'))
db[table].module.represent = lambda name: (name and [db(db.s3_module.name==name).select()[0].name_nice] or ["None"])[0]

# *****************************************************************************
# Functions:
#

#
# shn_pr_person_pfif ----------------------------------------------------------
#
def shn_pr_person_pfif(person, domain):

    domain = request.env.server_name

    if person:
        pe = vita.pentity(person)

        person_record_id = "%s/%s" % (domain, pe.uuid)
        pfif = dict(person_record_id=person_record_id)

        entry_date = str(person.modified_on)
        source_date = str(person.created_on)
        pfif.update(entry_date=entry_date, source_date=source_date)

        first_name = person.first_name.upper()
        last_name = person.last_name.upper()
        pfif.update(first_name=first_name, last_name=last_name)

        # Get home address of that person
        query = (db.pr_address.deleted==False)
        query = (db.pr_address.pr_pe_id==pe.id) & query
        query = (db.pr_address.opt_pr_address_type==1) & query

        rows = db(query).select(db.pr_address.ALL)
        if rows:
            home_address = rows[0]
            home_city = home_address.city
            if home_address.opt_pr_country == 184: # United States?
                home_state = home_address.state
            else:
                home_state = shn_list_of_nations[home_address.opt_pr_country]

            home_neighborhood = '' # not available
            home_street = home_address.street1
            home_zip = home_address.postcode
        else:
            home_city = ''
            home_state = ''
            home_neighborhood = ''
            home_street = ''
            home_zip = ''

        pfif.update(
            home_city = home_city,
            home_state = home_state,
            home_neighborhood = home_neighborhood,
            home_street = home_street,
            home_zip = home_zip
            )

        # Get photograph of that person
        query = (db.pr_image.deleted==False)
        query = (db.pr_image.pr_pe_id==pe.id) & query
        query = (db.pr_image.opt_pr_image_type==1) & query

        rows = db(query).select(db.pr_image.ALL)
        if rows:
            photo = rows[0]
            photo_url = "%s/%s/pr/download/%s" % (S3_PUBLIC_URL, request.application, photo.image)
        else:
            photo_url = ''

        pfif.update(photo_url=photo_url)

        # Get admin data
        try:
            admin_data = db(db.s3_setting.id==1).select(
                                    db.s3_setting.admin_name,
                                    db.s3_setting.admin_email,
                                    db.s3_setting.admin_tel)[0]

            author_name = admin_data.admin_name
            author_email = admin_data.admin_email
            author_phone = admin_data.admin_tel
        except:
            author_name = ''
            author_email = ''
            author_phone = ''

        pfif.update(author_name=author_name, author_email=author_email, author_phone=author_phone)
            
        # Add source data
        source_name = domain
        source_url = "%s/%s/%s/person/%s.pfif" % (S3_PUBLIC_URL, request.application, module, person.id)
        pfif.update(source_name=source_name, source_url=source_url)

        return dict(person=pfif)

    else:
        return None

#
# shn_pr_presence_pfif --------------------------------------------------------
#
def shn_pr_presence_pfif(record, domain):

    if record:
        note_record_id = "%s/%s" % (domain, record.uuid)
        pfif = dict(note_record_id=note_record_id)

        return dict(note=pfif)
    else:
        return None

#
# End
# *****************************************************************************

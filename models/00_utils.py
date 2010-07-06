# -*- coding: utf-8 -*-

"""
    Utilities
"""

def shn_sessions():
    """
    Extend session to support:
        Multiple flash classes
        Settings
            Debug mode
            Security mode
            Restricted mode
            Theme
            Audit modes
    """
    response.error = session.error
    response.confirmation = session.confirmation
    response.warning = session.warning
    session.error = []
    session.confirmation = []
    session.warning = []
    # Keep all our configuration options in a single pair of global variables
    # Use session for persistent variables
    if not session.s3:
        session.s3 = Storage()
    # Use response for one-off variables which are visible in views without explicit passing
    response.s3 = Storage()
    response.s3.formats = Storage()
    
    roles = []
    try:
        user_id = auth.user.id
        _memberships = db.auth_membership
        memberships = db(_memberships.user_id == user_id).select(_memberships.group_id) # Cache this & invalidate when memberships are changed?
        for membership in memberships:
            roles.append(membership.group_id)
    except:
        # User not authenticated therefore has no roles other than '0'
        pass
    session.s3.roles = roles

    controller_settings_table = "%s_setting" % request.controller
    controller_settings = controller_settings_table in db.tables and \
       db(db[controller_settings_table].id > 0).select(limitby=(0, 1)).first()
    
    settings = db(db.s3_setting.id > 0).select(db.s3_setting.debug, db.s3_setting.security_policy, db.s3_setting.self_registration, db.s3_setting.audit_read, db.s3_setting.audit_write, limitby=(0, 1)).first()
    # Are we running in debug mode?
    session.s3.debug = "debug" in request.vars or settings and settings.debug
    session.s3.self_registration = (settings and settings.self_registration) or 1
    session.s3.security_policy = (settings and settings.security_policy) or 1

    # We Audit if either the Global or Module asks us to
    # (ignore gracefully if module author hasn't implemented this)
    session.s3.audit_read = (settings and settings.audit_read) \
        or (controller_settings and controller_settings.audit_read)
    session.s3.audit_write = (settings and settings.audit_write) \
        or (controller_settings and controller_settings.audit_write)
    return settings

s3_settings = shn_sessions()

#
# List of supported languages
#
shn_languages = {
    "en": T("English"),
    "fr": T("French")
}
auth.settings.table_user.language.requires = IS_IN_SET(shn_languages, zero=None)

#
# List of Nations - added by nursix
#
shn_list_of_nations = {
    1:T("Afghanistan"),
    2:T("Albania"),
    3:T("Algeria"),
    4:T("Andorra"),
    5:T("Angola"),
    6:T("Antigua and Barbuda"),
    7:T("Argentina"),
    8:T("Armenia"),
    9:T("Australia"),
    10:T("Austria"),
    11:T("Azerbaijan"),
    12:T("Bahamas"),
    13:T("Bahrain"),
    14:T("Bangladesh"),
    15:T("Barbados"),
    16:T("Belarus"),
    17:T("Belgium"),
    18:T("Belize"),
    19:T("Benin"),
    20:T("Bhutan"),
    21:T("Bolivia"),
    22:T("Bosnia and Herzegovina"),
    23:T("Botswana"),
    24:T("Brazil"),
    25:T("Brunei"),
    26:T("Bulgaria"),
    27:T("Burkina Faso"),
    28:T("Burundi"),
    29:T("Cambodia"),
    30:T("Cameroon"),
    31:T("Canada"),
    32:T("Cape Verde"),
    33:T("Central African Republic"),
    34:T("Chad"),
    35:T("Chile"),
    36:T("China"),
    37:T("Colombia"),
    38:T("Comoros"),
    39:T("Congo, Democratic Republic of the (Congo-Kinshasa)"),
    40:T("Congo, Republic of the (Congo-Brazzaville)"),
    41:T("Costa Rica"),
    42:T("Côte d'Ivoire"),
    43:T("Croatia"),
    44:T("Cuba"),
    45:T("Cyprus"),
    46:T("Czech Republic"),
    47:T("Denmark"),
    48:T("Djibouti"),
    49:T("Dominica"),
    50:T("Dominican Republic"),
    51:T("East Timor"),
    52:T("Ecuador"),
    53:T("Egypt"),
    54:T("El Salvador"),
    55:T("Equatorial Guinea"),
    56:T("Eritrea"),
    57:T("Estonia"),
    58:T("Ethiopia"),
    59:T("Fiji"),
    60:T("Finland"),
    61:T("France"),
    62:T("Gabon"),
    63:T("The Gambia"),
    64:T("Georgia"),
    65:T("Germany"),
    66:T("Ghana"),
    67:T("Greece"),
    68:T("Grenada"),
    69:T("Guatemala"),
    70:T("Guinea"),
    71:T("Guinea-Bissau"),
    72:T("Guyana"),
    73:T("Haiti"),
    74:T("Honduras"),
    75:T("Hungary"),
    76:T("Iceland"),
    77:T("India"),
    78:T("Indonesia"),
    79:T("Iran"),
    80:T("Iraq"),
    81:T("Ireland"),
    82:T("Israel"),
    83:T("Italy"),
    84:T("Jamaica"),
    85:T("Japan"),
    86:T("Jordan"),
    87:T("Kazakhstan"),
    88:T("Kenya"),
    89:T("Kiribati"),
    90:T("Korea, North"),
    91:T("Korea, South"),
    92:T("Kuwait"),
    93:T("Kyrgyzstan"),
    94:T("Laos"),
    95:T("Latvia"),
    96:T("Lebanon"),
    97:T("Lesotho"),
    98:T("Liberia"),
    99:T("Libya"),
    100:T("Liechtenstein"),
    101:T("Lithuania"),
    102:T("Luxembourg"),
    103:T("Macedonia"),
    104:T("Madagascar"),
    105:T("Malawi"),
    106:T("Malaysia"),
    107:T("Maldives"),
    108:T("Mali"),
    109:T("Malta"),
    110:T("Marshall Islands"),
    111:T("Mauritania"),
    112:T("Mauritius"),
    113:T("Mexico"),
    114:T("Micronesia"),
    115:T("Moldova"),
    116:T("Monaco"),
    117:T("Mongolia"),
    118:T("Montenegro"),
    119:T("Morocco"),
    120:T("Mozambique"),
    121:T("Myanmar"),
    122:T("Namibia"),
    123:T("Nauru"),
    124:T("Nepal"),
    125:T("Netherlands"),
    126:T("New Zealand"),
    127:T("Nicaragua"),
    128:T("Niger"),
    129:T("Nigeria"),
    130:T("Norway"),
    131:T("Oman"),
    132:T("Pakistan"),
    133:T("Palau"),
    134:T("Panama"),
    135:T("Papua New Guinea"),
    136:T("Paraguay"),
    137:T("Peru"),
    138:T("Philippines"),
    139:T("Poland"),
    140:T("Portugal"),
    141:T("Qatar"),
    142:T("Romania"),
    143:T("Russia"),
    144:T("Rwanda"),
    145:T("Saint Kitts and Nevis"),
    146:T("Saint Lucia"),
    147:T("Saint Vincent and the Grenadines"),
    148:T("Samoa"),
    149:T("San Marino"),
    150:T("São Tomé and Príncipe"),
    151:T("Saudi Arabia"),
    152:T("Senegal"),
    153:T("Serbia"),
    154:T("Seychelles"),
    155:T("Sierra Leone"),
    156:T("Singapore"),
    157:T("Slovakia"),
    158:T("Slovenia"),
    159:T("Solomon Islands"),
    160:T("Somalia"),
    161:T("South Africa"),
    162:T("Spain"),
    163:T("Sri Lanka"),
    164:T("Sudan"),
    165:T("Suriname"),
    166:T("Swaziland"),
    167:T("Sweden"),
    168:T("Switzerland"),
    169:T("Syria"),
    170:T("Tajikistan"),
    171:T("Tanzania"),
    172:T("Thailand"),
    173:T("Togo"),
    174:T("Tonga"),
    175:T("Trinidad and Tobago"),
    176:T("Tunisia"),
    177:T("Turkey"),
    178:T("Turkmenistan"),
    179:T("Tuvalu"),
    180:T("Uganda"),
    181:T("Ukraine"),
    182:T("United Arab Emirates"),
    183:T("United Kingdom"),
    184:T("United States"),
    185:T("Uruguay"),
    186:T("Uzbekistan"),
    187:T("Vanuatu"),
    188:T("Vatican City"),
    189:T("Venezuela"),
    190:T("Vietnam"),
    191:T("Yemen"),
    192:T("Zambia"),
    193:T("Zimbabwe"),
    194:T("Abkhazia"),
    195:T("Kosovo"),
    196:T("Nagorno-Karabakh"),
    197:T("Northern Cyprus"),
    198:T("Somaliland"),
    199:T("South Ossetia"),
    200:T("Taiwan"),
    201:T("Transnistria"),
    999:T("unknown")
    }

# User Time Zone Operations:

from datetime import timedelta
import time

def shn_user_utc_offset():
    """
        returns the UTC offset of the current user or None, if not logged in
    """

    if auth.is_logged_in():
        return db(db.auth_user.id == session.auth.user.id).select(db.auth_user.utc_offset, limitby=(0, 1)).first().utc_offset
    else:
        try:
            offset = db().select(db.s3_setting.utc_offset, limitby=(0, 1)).first().utc_offset
        except:
            offset = None
        return offset


def shn_as_local_time(value):
    """
        represents a given UTC datetime.datetime object as string:

        - for the local time of the user, if logged in
        - as it is in UTC, if not logged in, marked by trailing +0000
    """

    format="%Y-%m-%d %H:%M:%S"

    offset = IS_UTC_OFFSET.get_offset_value(shn_user_utc_offset())

    if offset:
        dt = value + timedelta(seconds=offset)
        return dt.strftime(str(format))
    else:
        dt = value
        return dt.strftime(str(format))+" +0000"

# Make URLs clickable
shn_url_represent = lambda url: (url and [A(url, _href=url, _target="blank")] or [""])[0]

# Phone number requires
shn_phone_requires = IS_NULL_OR(IS_MATCH('\+?\s*[\s\-\.\(\)\d]+(?:(?: x| ext)\s?\d{1,5})?$'))
        
def Tstr(text):
    """Convenience function for non web2py modules"""
    return str(T(text))


def myname(user_id):
    user = db.auth_user[user_id]
    return user.first_name if user else "None"


def shn_last_update(table, record_id):

    if table and record_id:
        record = table[record_id]
        if record:
            mod_on_str  = T(" on ")
            mod_by_str  = T(" by ")

            modified_on = ""
            if "modified_on" in table.fields:
                modified_on = "%s%s" % (mod_on_str, shn_as_local_time(record.modified_on))

            modified_by = ""
            if "modified_by" in table.fields:
                user = auth.settings.table_user[record.modified_by]
                if user:
                    person = db(db.pr_person.uuid == user.person_uuid).select(limitby=(0, 1)).first()
                    if person:
                        modified_by = "%s%s" % (mod_by_str, vita.fullname(person))

            if len(modified_on) or len(modified_by):
                last_update = "%s%s%s" % (T("Record last updated"), modified_on, modified_by)
                return last_update
    return None

def shn_compose_message(data, template):
    " Compose an SMS Message from an XSLT "
    from lxml import etree
    if data:
        root = etree.Element("message")
        for k in data.keys():
            entry = etree.SubElement(root, k)
            entry.text = s3xrc.xml.xml_encode(str(data[k]))

        message = None
        tree = etree.ElementTree(root)

        if template:
            template = os.path.join(request.folder, "static", template)
            if os.path.exists(template):
                message = s3xrc.xml.transform(tree, template)

        if message:
            return str(message)
        else:
            return s3xrc.xml.tostring(tree, pretty_print=True)


def shn_crud_strings(table_name,
                     table_name_plural = None):
    """
    @author: Michael Howden (michael@aidiq.com)

    @description:
        Creates the strings for the title of/in the various CRUD Forms.

    @arguments:
        table_name - string - The User's name for the resource in the table - eg. "Person"
        table_name_plural - string - The User's name for the plural of the resource in the table - eg. "People"

    @returns:
        class "gluon.storage.Storage" (Web2Py)

    @example
        s3.crud_strings[<table_name>] = shn_crud_strings(<table_name>, <table_name_plural>)
    """
    
    if not table_name_plural:
        table_name_plural = table_name + "s"

    ADD = T("Add " + table_name)
    LIST = T("List "+ table_name_plural)

    table_strings = Storage(
    title = T(table_name),
    title_plural = T(table_name_plural),
    title_create = ADD,
    title_display = T(table_name + " Details"),
    title_list = LIST,
    title_update = T("Edit "+ table_name) ,
    title_search = T("Search " + table_name_plural) ,
    subtitle_create = T("Add New " + table_name) ,
    subtitle_list = T(table_name_plural),
    label_list_button = LIST,
    label_create_button = ADD,
    msg_record_created =  T(table_name +" added"),
    msg_record_modified =  T(table_name + " updated"),
    msg_record_deleted = T( table_name + " deleted"),
    msg_list_empty = T("No " + table_name_plural + " currently registered"))

    return table_strings


def shn_get_crud_strings(tablename):

    """ Get the CRUD strings for a table """

    return s3.crud_strings.get(tablename, s3.crud_strings)


def shn_import_table(table_name,
                     import_if_not_empty = False):
    """
    @author: Michael Howden (michael@aidiq.com)

    @description:
        If a table is empty, it will import values into that table from:
        /private/import/tables/<table>.csv.

    @arguments:
        table_name - string - The name of the table
        import_if_not_empty - bool
    """

    table = db[table_name]
    if not db(table.id).count() or import_if_not_empty:
        import_file = os.path.join(request.folder,
                                   "private", "import", "tables",
                                   table_name + ".csv")
        table.import_from_csv_file(open(import_file,"r"))


def shn_represent_file(file_name,
                       table,
                       field = "file"):
    """
    @author: Michael Howden (michael@aidiq.com)

    @description:
        Represents a file (stored in a table) as the filename with a link to that file
    """
    import base64
    url_file = crud.settings.download_url + "/" + file_name

    if db[table][field].uploadfolder:
        path = db[table][field].uploadfolder
    else:
        path = os.path.join(db[table][field]._db._folder, "..", "uploads")
    pathfilename = os.path.join(path, file_name)

    try:
        #f = open(pathfilename,"r")
        #filename = f.filename
        regex_content = re.compile("([\w\-]+\.){3}(?P<name>\w+)\.\w+$")
        regex_cleanup_fn = re.compile('[\'"\s;]+')

        m = regex_content.match(file_name)
        filename = base64.b16decode(m.group("name"), True)
        filename = regex_cleanup_fn.sub("_", filename)
    except:
        filename = file_name

    return A(filename, _href = url_file)


def shn_rheader_tabs(jr, tabs=[]):

    """ Constructs a DIV of component links for a S3RESTRequest """

    rheader_tabs = []
    for (title, component) in tabs:
        _class = "rheader_tab_other"
        if component:
            if jr.component and jr.component.name == component:
                _class = "rheader_tab_here"
            args = [jr.id, component]
            _href = URL(r=request, f=jr.name, args=args)
        else:
            if not jr.component:
                _class = "rheader_tab_here"
            args = [jr.id]
            _next = URL(r=request, f=jr.name, args=[jr.id])
            _href = URL(r=request, f=jr.name, args=args, vars = {"_next": _next})
        tab = SPAN(A(title, _href=_href), _class=_class)
        rheader_tabs.append(tab)

    if rheader_tabs:
        rheader_tabs = DIV(rheader_tabs, _id="rheader_tabs")
    else:
        rheader_tabs = ""

    return rheader_tabs

def shn_action_buttons(jr, deletable=True):
    """ Provide the usual Action Buttons for Column views. Designed to be called from a postp """

    if not jr.component:
        if auth.is_logged_in():
            # Provide the ability to delete records in bulk
            if deletable:
                response.s3.actions = [
                    dict(label=str(UPDATE), _class="action-btn", url=str(URL(r=request, args=["[id]", "update"]))),
                    dict(label=str(DELETE), _class="action-btn", url=str(URL(r=request, args=["[id]", "delete"])))
                ]
            else:
                response.s3.actions = [
                    dict(label=str(UPDATE), _class="action-btn", url=str(URL(r=request, args=["[id]", "update"])))
                ]
        else:
            response.s3.actions = [
                dict(label=str(READ), _class="action-btn", url=str(URL(r=request, args=["[id]"])))
            ]

    return

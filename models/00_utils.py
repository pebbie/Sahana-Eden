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
    settings = db(db.s3_setting.id > 0).select().first()
    controller_settings_table = '%s_setting' % request.controller
    controller_settings = controller_settings_table in db.tables and \
       db(db[controller_settings_table].id > 0).select().first()
    # Are we running in debug mode?
    session.s3.debug = 'debug' in request.vars or settings and settings.debug
    session.s3.security_policy = (settings and settings.security_policy) or 1

    # Are we running in restricted mode?
    #session.s3.restricted = auth.has_membership(auth.id_group('Restricted'))
    # Select the theme
    if not session.s3.theme:
        session.s3.theme = Storage()
    admin_theme = db().select(db.admin_theme.footer).first()
    session.s3.theme.footer = admin_theme and admin_theme.footer or 'footer.html'
    # We Audit if either the Global or Module asks us to 
    # (ignore gracefully if module author hasn't implemented this)
    session.s3.audit_read = (settings and settings.audit_read) \
        or (controller_settings and controller_settings.audit_read)
    session.s3.audit_write = (settings and settings.audit_write) \
        or (controller_settings and controller_settings.audit_write)
    return settings

s3_settings = shn_sessions()


#
# Widgets
#

# See test.py

#
# List of Nations - added by nursix
#
shn_list_of_nations = {
    1:T('Afghanistan'),
    2:T('Albania'),
    3:T('Algeria'),
    4:T('Andorra'),
    5:T('Angola'),
    6:T('Antigua and Barbuda'),
    7:T('Argentina'),
    8:T('Armenia'),
    9:T('Australia'),
    10:T('Austria'),
    11:T('Azerbaijan'),
    12:T('Bahamas'),
    13:T('Bahrain'),
    14:T('Bangladesh'),
    15:T('Barbados'),
    16:T('Belarus'),
    17:T('Belgium'),
    18:T('Belize'),
    19:T('Benin'),
    20:T('Bhutan'),
    21:T('Bolivia'),
    22:T('Bosnia and Herzegovina'),
    23:T('Botswana'),
    24:T('Brazil'),
    25:T('Brunei'),
    26:T('Bulgaria'),
    27:T('Burkina Faso'),
    28:T('Burundi'),
    29:T('Cambodia'),
    30:T('Cameroon'),
    31:T('Canada'),
    32:T('Cape Verde'),
    33:T('Central African Republic'),
    34:T('Chad'),
    35:T('Chile'),
    36:T('China'),
    37:T('Colombia'),
    38:T('Comoros'),
    39:T('Congo, Democratic Republic of the (Congo-Kinshasa)'),
    40:T('Congo, Republic of the (Congo-Brazzaville)'),
    41:T('Costa Rica'),
    42:T('C�te d\'Ivoire'),
    43:T('Croatia'),
    44:T('Cuba'),
    45:T('Cyprus'),
    46:T('Czech Republic'),
    47:T('Denmark'),
    48:T('Djibouti'),
    49:T('Dominica'),
    50:T('Dominican Republic'),
    51:T('East Timor'),
    52:T('Ecuador'),
    53:T('Egypt'),
    54:T('El Salvador'),
    55:T('Equatorial Guinea'),
    56:T('Eritrea'),
    57:T('Estonia'),
    58:T('Ethiopia'),
    59:T('Fiji'),
    60:T('Finland'),
    61:T('France'),
    62:T('Gabon'),
    63:T('The Gambia'),
    64:T('Georgia'),
    65:T('Germany'),
    66:T('Ghana'),
    67:T('Greece'),
    68:T('Grenada'),
    69:T('Guatemala'),
    70:T('Guinea'),
    71:T('Guinea-Bissau'),
    72:T('Guyana'),
    73:T('Haiti'),
    74:T('Honduras'),
    75:T('Hungary'),
    76:T('Iceland'),
    77:T('India'),
    78:T('Indonesia'),
    79:T('Iran'),
    80:T('Iraq'),
    81:T('Ireland'),
    82:T('Israel'),
    83:T('Italy'),
    84:T('Jamaica'),
    85:T('Japan'),
    86:T('Jordan'),
    87:T('Kazakhstan'),
    88:T('Kenya'),
    89:T('Kiribati'),
    90:T('Korea, North'),
    91:T('Korea, South'),
    92:T('Kuwait'),
    93:T('Kyrgyzstan'),
    94:T('Laos'),
    95:T('Latvia'),
    96:T('Lebanon'),
    97:T('Lesotho'),
    98:T('Liberia'),
    99:T('Libya'),
    100:T('Liechtenstein'),
    101:T('Lithuania'),
    102:T('Luxembourg'),
    103:T('Macedonia'),
    104:T('Madagascar'),
    105:T('Malawi'),
    106:T('Malaysia'),
    107:T('Maldives'),
    108:T('Mali'),
    109:T('Malta'),
    110:T('Marshall Islands'),
    111:T('Mauritania'),
    112:T('Mauritius'),
    113:T('Mexico'),
    114:T('Micronesia'),
    115:T('Moldova'),
    116:T('Monaco'),
    117:T('Mongolia'),
    118:T('Montenegro'),
    119:T('Morocco'),
    120:T('Mozambique'),
    121:T('Myanmar'),
    122:T('Namibia'),
    123:T('Nauru'),
    124:T('Nepal'),
    125:T('Netherlands'),
    126:T('New Zealand'),
    127:T('Nicaragua'),
    128:T('Niger'),
    129:T('Nigeria'),
    130:T('Norway'),
    131:T('Oman'),
    132:T('Pakistan'),
    133:T('Palau'),
    134:T('Panama'),
    135:T('Papua New Guinea'),
    136:T('Paraguay'),
    137:T('Peru'),
    138:T('Philippines'),
    139:T('Poland'),
    140:T('Portugal'),
    141:T('Qatar'),
    142:T('Romania'),
    143:T('Russia'),
    144:T('Rwanda'),
    145:T('Saint Kitts and Nevis'),
    146:T('Saint Lucia'),
    147:T('Saint Vincent and the Grenadines'),
    148:T('Samoa'),
    149:T('San Marino'),
    150:T('S�o Tom� and Pr�ncipe'),
    151:T('Saudi Arabia'),
    152:T('Senegal'),
    153:T('Serbia'),
    154:T('Seychelles'),
    155:T('Sierra Leone'),
    156:T('Singapore'),
    157:T('Slovakia'),
    158:T('Slovenia'),
    159:T('Solomon Islands'),
    160:T('Somalia'),
    161:T('South Africa'),
    162:T('Spain'),
    163:T('Sri Lanka'),
    164:T('Sudan'),
    165:T('Suriname'),
    166:T('Swaziland'),
    167:T('Sweden'),
    168:T('Switzerland'),
    169:T('Syria'),
    170:T('Tajikistan'),
    171:T('Tanzania'),
    172:T('Thailand'),
    173:T('Togo'),
    174:T('Tonga'),
    175:T('Trinidad and Tobago'),
    176:T('Tunisia'),
    177:T('Turkey'),
    178:T('Turkmenistan'),
    179:T('Tuvalu'),
    180:T('Uganda'),
    181:T('Ukraine'),
    182:T('United Arab Emirates'),
    183:T('United Kingdom'),
    184:T('United States'),
    185:T('Uruguay'),
    186:T('Uzbekistan'),
    187:T('Vanuatu'),
    188:T('Vatican City'),
    189:T('Venezuela'),
    190:T('Vietnam'),
    191:T('Yemen'),
    192:T('Zambia'),
    193:T('Zimbabwe'),
    194:T('Abkhazia'),
    195:T('Kosovo'),
    196:T('Nagorno-Karabakh'),
    197:T('Northern Cyprus'),
    198:T('Somaliland'),
    199:T('South Ossetia'),
    200:T('Taiwan'),
    201:T('Transnistria'),
    999:T('unknown')
    }
    
# User Time Zone Operations:
# TODO: don't know if that fits here, should perhaps be moved into sahana.py

from datetime import timedelta
import time

def shn_user_utc_offset():
    """
        returns the UTC offset of the current user or None, if not logged in
    """

    if auth.is_logged_in():
        return db(db.auth_user.id==session.auth.user.id).select()[0].utc_offset
    else:
        try:
            offset = db().select(db.s3_setting.utc_offset)[0].utc_offset
        except:
            offset = None
        return offset

def shn_as_local_time(value):
    """
        represents a given UTC datetime.datetime object as string:

        - for the local time of the user, if logged in
        - as it is in UTC, if not logged in, marked by trailing +0000
    """

    format='%Y-%m-%d %H:%M:%S'

    offset = IS_UTC_OFFSET.get_offset_value(shn_user_utc_offset())

    if offset:
        dt = value + timedelta(seconds=offset)
        return dt.strftime(str(format))
    else:
        dt = value
        return dt.strftime(str(format))+' +0000'

def Tstr(text):
    """Convenience function for non web2py modules"""
    return str(T(text))

def myname(user_id):
    user = db.auth_user[user_id]
    return user.first_name if user else 'None'

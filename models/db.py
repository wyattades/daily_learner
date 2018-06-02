# -*- coding: utf-8 -*-

# -------------------------------------------------------------------------
# AppConfig configuration made easy. Look inside private/appconfig.ini
# Auth is for authenticaiton and access control
# -------------------------------------------------------------------------
from gluon.contrib.appconfig import AppConfig
from gluon.tools import Auth

# -------------------------------------------------------------------------
# This scaffolding model makes your app work on Google App Engine too
# File is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

if request.global_settings.web2py_version < '2.15.5':
    raise HTTP(500, 'Requires web2py 2.15.5 or newer')

# -------------------------------------------------------------------------
# if SSL/HTTPS is properly configured and you want all HTTP requests to
# be redirected to HTTPS, uncomment the line below:
# -------------------------------------------------------------------------
# request.requires_https()

# -------------------------------------------------------------------------
# once in production, remove reload=True to gain full speed
# -------------------------------------------------------------------------
configuration = AppConfig(reload=True)

if not request.env.web2py_runtime_gae:
    # ---------------------------------------------------------------------
    # if NOT running on Google App Engine use SQLite or other DB
    # ---------------------------------------------------------------------
    db = DAL(configuration.get('db.uri'),
            pool_size=configuration.get('db.pool_size'),
            migrate_enabled=True,
            lazy_tables=True,
            # migrate=True,
            # auto_import=True,
            # check_reserved=['all']
        )
else:
    # ---------------------------------------------------------------------
    # connect to Google BigTable (optional 'google:datastore://namespace')
    # ---------------------------------------------------------------------
    db = DAL('google:datastore+ndb')
    # ---------------------------------------------------------------------
    # store sessions and tickets there
    # ---------------------------------------------------------------------
    session.connect(request, response, db=db)
    # ---------------------------------------------------------------------
    # or store session in Memcache, Redis, etc.
    # from gluon.contrib.memdb import MEMDB
    # from google.appengine.api.memcache import Client
    # session.connect(request, response, db = MEMDB(Client()))
    # ---------------------------------------------------------------------

# -------------------------------------------------------------------------
# by default give a view/generic.extension to all actions from localhost
# none otherwise. a pattern can be 'controller/function.extension'
# -------------------------------------------------------------------------
response.generic_patterns = [] 
if request.is_local and not configuration.get('app.production'):
    response.generic_patterns.append('*')

# -------------------------------------------------------------------------
# choose a style for forms
# -------------------------------------------------------------------------

# TODO: clean this up a bit
def formstyle_bulma(form, fields):
    col_label_size = 3

    label_col_class = 'col-sm-%d' % col_label_size
    col_class = 'col-sm-%d' % (12 - col_label_size)
    offset_class = 'col-sm-offset-%d' % col_label_size
    parent = CAT()

    for id, label, controls, help in fields:
        # wrappers
        _help = [SPAN(help, _class='help')] if help else []

        # embed _help into _controls
        _controls = DIV(controls, *_help, _class='control %s' % (col_class))
        if isinstance(controls, INPUT):
            if controls['_type'] == 'submit':
                controls = BUTTON(controls['_value'], _class='button is-primary', **controls.attributes)
                _controls = DIV(controls, _class='control %s %s' % (col_class, offset_class))
            if controls['_type'] == 'button':
                controls.add_class('button is-link')
            elif controls['_type'] == 'file':
                controls.add_class('file')
            elif controls['_type'] in ('text', 'password'):
                controls.add_class(' input')
            elif controls['_type'] == 'checkbox':
                label['_for'] = None
                controls.attributes['_class'] = 'checkbox'
                label.insert(0, controls)
                label.insert(1, ' ')
                _controls = DIV(DIV(label, *_help, _class='checkbox'),
                                _class='%s %s' % (offset_class, col_class))
                label = ''
            elif isinstance(controls, SELECT):
                first_option = controls.components[0]
                if first_option['_value'] == '':
                    first_option.append('Select {}'.format(label.components[0]))
                    first_option['_disabled'] = True
                _controls.components[0] = DIV(controls, _class='select')
            elif isinstance(controls, TEXTAREA):
                controls.add_class('textarea')

        elif isinstance(controls, SPAN):
            _controls = P(controls.components,
                            _class='control-static %s' % col_class)
        elif isinstance(controls, UL):
            def replace_li(li):
                li.components[0].add_class('input')
                return LI(DIV(li.components[0],
                    _class='control is-expanded'),
                    _class='field is-grouped')
            controls.elements('li', replace=replace_li) 
        elif isinstance(controls, CAT) and isinstance(controls[0], INPUT):
                controls[0].add_class('control')
        if isinstance(label, LABEL):
            label.add_class('label {}'.format(label_col_class))

        parent.append(DIV(label, _controls, _class='field', _id=id))
    return parent

response.formstyle = formstyle_bulma
# response.form_label_separator = ''

# -------------------------------------------------------------------------
# (optional) optimize handling of static files
# -------------------------------------------------------------------------
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

# -------------------------------------------------------------------------
# (optional) static assets folder versioning
# -------------------------------------------------------------------------
# response.static_version = '0.0.0'

# -------------------------------------------------------------------------
# Here is sample code if you need for
# - email capabilities
# - authentication (registration, login, logout, ... )
# - authorization (role based authorization)
# - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
# - old style crud actions
# (more options discussed in gluon/tools.py)
# -------------------------------------------------------------------------

# host names must be a list of allowed host names (glob syntax allowed)
auth = Auth(db, host_names=configuration.get('host.names'))

# Define redirects after login & register
auth.settings.login_next = auth.settings.register_next = URL('default','session')

# -------------------------------------------------------------------------
# create all tables needed by auth, maybe add a list of extra fields
# -------------------------------------------------------------------------
auth.settings.extra_fields['auth_user'] = []
auth.define_tables(username=False, signature=False)

# Add admin account
if len(db(db.auth_user.email == configuration.get('admin.email')).select()) == 0:
    admin_user = db.auth_user.insert(
        password = db.auth_user.password.validate(configuration.get('admin.password'))[0],
        email = configuration.get('admin.email'),
        first_name = 'System',
        last_name = 'Administrator',
    )
    admin_group = db.auth_group.insert(
        role = 'admin',
    )
    db.auth_membership.insert(
        group_id = admin_group.id,
        user_id = admin_user.id,
    )

# -------------------------------------------------------------------------
# configure email
# -------------------------------------------------------------------------
# mail = auth.settings.mailer
# mail.settings.server = 'logging' if request.is_local else configuration.get('smtp.server')
# mail.settings.sender = configuration.get('smtp.sender')
# mail.settings.login = configuration.get('smtp.login')
# mail.settings.tls = configuration.get('smtp.tls') or False
# mail.settings.ssl = configuration.get('smtp.ssl') or False

# -------------------------------------------------------------------------
# configure auth policy
# -------------------------------------------------------------------------
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

# -------------------------------------------------------------------------  
# read more at http://dev.w3.org/html5/markup/meta.name.html               
# -------------------------------------------------------------------------
response.meta.author = configuration.get('app.author')
response.meta.description = configuration.get('app.description')
response.meta.keywords = configuration.get('app.keywords')
response.meta.generator = configuration.get('app.generator')

# -------------------------------------------------------------------------
# your http://google.com/analytics id                                      
# -------------------------------------------------------------------------
response.google_analytics_id = configuration.get('google.analytics_id')

# -------------------------------------------------------------------------
# maybe use the scheduler
# -------------------------------------------------------------------------
# if configuration.get('scheduler.enabled'):
#     from gluon.scheduler import Scheduler
#     scheduler = Scheduler(db, heartbeat=configure.get('heartbeat'))

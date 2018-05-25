# -*- coding: utf-8 -*-

from gluon.sqlhtml import ExporterCSV, ExporterJSON
from import_parser import get_parser
from pprint import pprint

export_formats = dict(
    csv_with_hidden_cols=False,
    json=(ExporterJSON, 'JSON'),
    csv=(ExporterCSV, 'CSV'),
    xml=False,
    html=False,
    tsv_with_hidden_cols=False,
    tsv=False,
)

ui = dict(
    widget='',
    header='',
    content='',
    default='',
    cornerall='',
    cornertop='',
    cornerbottom='',
    button='button',
    buttontext='',
    buttonadd='fas fa-plus',
    buttonback='fas fa-arrow-left',
    buttonexport='fas fa-cloud-download-alt',
    buttondelete='fas fa-trash',
    buttonedit='fas fa-edit',
    buttontable='fas fa-arrow-right',
    buttonview='fas fa-list-ul',
)

# Static pages
def index():
    return dict()
def about():
    return dict()
def tutorial():
    return dict()

# User login/register/etc (required for auth)
def user():
    return dict(form=auth())

# Database admin access: '/admin_panel'
@auth.requires_membership('admin')
def admin_panel():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename:
        return dict(links=[A(tablename, _href=URL('default', 'admin_panel/' + tablename)) for tablename in db.tables])
    if not tablename in db.tables:
        raise HTTP(404)
    grid = SQLFORM.smartgrid(db[tablename],
        _class='table',
        ui={table: ui for table in db.tables},
        csv=False,
    )
    
    # Set up breadcrumbs
    crumbs = [ LI(A('Admin Panel', _href=URL('default', 'admin_panel'))) ]
    crumbs += [ LI(A(el[0], _href=el['_href'])) for el in grid.elements('.web2py_breadcrumbs li a') ]
    crumbs[-1].add_class('is-active')
    grid.element('.web2py_breadcrumbs', replace=lambda el: DIV(UL(*crumbs), _class='breadcrumb'))
    
    return dict(grid=grid)

# ---- action to server uploaded static content (required) ---
# @cache.action()
# def download():
#     return response.download(request, db)

def _view_button(row):
    return A(
        SPAN('Go to this Session'),
        SPAN(I(_class='fas fa-arrow-right'), _class='icon'),
        _class='button is-primary', _href=URL('default', 'session/%d' % row.id)
    )

def _view_session(session_record):
    action = request.args(1)

    # TODO
    # if action and action not in ['new','delete','edit']:
    #     raise HTTP(404)

    table = get_session_table(session_record.id)        

    crumbs = [
        ('Sessions', URL('default', 'session')),
        (session_record.name, URL('default', 'session/%d' % session_record.id)),
    ]
    title = session_record.name

    # Calculate page
    if action == 'predict':
        crumbs.append(('Predict', ''))
        return dict(grid='Placeholder', title='Predict', crumbs=crumbs)

    # Data upload page
    if action == 'import':
        crumbs.append(('Import', ''))

        labels = list(session_record.labels)
        labels.append(session_record.result_label)

        response.view = 'default/import.html'

        data_import = FORM(
            INPUT(_type='file', _name='file', _required=True, _class='file-input', _accept=".json,.csv"),
        )

        def validate(data_import):
            print('validatin')
            filedata = data_import.vars.file
            parser = get_parser(filedata.type)
            if parser:
                try:
                    rows = parser(labels, filedata.file)
                    if rows:
                        table.bulk_insert(rows)
                        session.flash = 'Successfully imported {} entries'.format(len(rows))
                    else:
                        data_import.errors.file = 'Invalid labels/values provided'
                except Exception as e:
                    print('Parsing error:', e)
                    data_import.errors.file = 'Failed to parse file'
            else:
                data_import.errors.file = 'Unsupported filetype: ' + filedata.type

        if data_import.process(
            formname='import',
            onvalidation=validate,
            onsuccess=None,
            onfailure=None,
            next=URL('default', 'session/{}'.format(session_record.id)),
        ).accepted:
            print('form accepted!')

        return dict(labels=labels, title='Import', crumbs=crumbs, form=data_import)
        
    grid = SQLFORM.grid(table,
        args=[session_record.id],
        exportclasses=export_formats,
        ui=ui,
        _class='table is-striped is-hoverable',
        searchable=False,
        user_signature=False,
        details=False,
        paginate=10,
    )

    if grid.update_form:
        crumbs.append(('Edit', ''))
        title = 'Edit Record'
    elif grid.create_form:
        crumbs.append(('New', ''))
        title = 'New Record'

    return dict(grid=grid, crumbs=crumbs, title=title, session_data=not action and session_record,
                analytics=not action and DIV('Placeholder'))

@auth.requires_login()
def session():
    session_id = request.args(0)

    # If args[0], then find session id matching args[0]
    session_record = None
    if session_id and session_id not in ['new', 'delete', 'edit']:
        session_record = db.sessions(session_id)
        if session_record == None or session_record.owner_id != auth.user_id:
            raise HTTP(403)
        return _view_session(session_record)

    # Create sessions grid
    query = (db.sessions.owner_id == auth.user_id)
    tl = db.sessions
    grid = SQLFORM.grid(query, 
        csv=False,
        ui=ui,
        searchable=False,
        oncreate=lambda form: create_session_table(form.vars),
        ondelete=lambda table,id: drop_session_table(id),
        _class='table',
        details=False,
        fields = [tl.name, tl.description, tl.created_on],
        user_signature=False,
        links=[dict(header='', body=_view_button)],
        links_placement='left',
    )

    # Fix form formatting in create_form
    if grid.create_form is not None:
        error = grid.create_form.errors.labels
        grid.create_form.errors.labels = None
        def replace_li(li):
            input = li.element('input')
            input.add_class('input')
            return LI(DIV(input,
                    _class='control is-expanded'),
                    _class='field is-grouped')
        grid.create_form.elements('ul li', replace=replace_li)
        grid.create_form.elements('ul', replace=lambda ul: (CAT(ul, DIV(error, _class='error')) if error else ul))

    # Replace 'Add Record' button text
    addspan = grid.element(_title='Add record to database')
    if addspan: addspan[0] = addspan['_title'] = 'New Session'

    # Remove 'records found' message
    grid.element('.web2py_counter', replace=None)

    # Set title
    crumbs = None
    if grid.create_form:
        title = 'New Session'
        crumbs = [
            ('Sessions', URL('default', 'session')),
            ('New', ''),
        ]
    elif grid.update_form:
        session_record = grid.update_form.record
        title = 'Edit Session'
        grid.element('#sessions_labels__row').add_class('is-displaynone')
        grid.element('#sessions_result_label__row').add_class('is-displaynone')
        crumbs = [
            ('Sessions', URL('default', 'session')),
            (session_record.name, URL('default', 'session/%d' % session_record.id)),
            ('Edit', ''),
        ]
    else:
        title = 'Sessions'

    return dict(grid=grid, title=title, crumbs=crumbs)
    
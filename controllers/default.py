# -*- coding: utf-8 -*-

from gluon.sqlhtml import ExporterCSV, ExporterXML, ExporterHTML, ExporterJSON

export_formats = dict(
    csv_with_hidden_cols=False,
    json=(ExporterJSON, 'JSON'),
    csv=(ExporterCSV, 'CSV'),
    xml=(ExporterXML, 'XML'),
    html=(ExporterHTML, 'HTML'),
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
    return A(SPAN('Go to this Session'), SPAN(I('', _class='fas fa-arrow-right'), _class='icon'), _class='button is-primary', _href=URL('default', 'session/%d' % row.id))

def _view_session(session_record):
    action = request.args(1)

    # if action and action not in ['new','delete','edit']:
    #     raise HTTP(404)

    table = get_session_table(session_record.id)        

    crumbs = [
        ('Sessions', URL('default', 'session')),
        (session_record.name, URL('default', 'session/%d' % session_record.id)),
    ]
    title = session_record.name

    # Calculate page
    if action == 'calculate':
        crumbs.append(('Calculator', ''))
        return dict(grid='Placeholder', title='Calculator', crumbs=crumbs)

    grid = SQLFORM.grid(table,
        args=[session_record.id],
        exportclasses=export_formats,
        ui=ui,
        _class='table',
        searchable=False,
        user_signature=False,
        details=False,
    )

    if action == 'edit':
        crumbs.append(('Edit', ''))
        title = 'Edit Record'
    if action == 'new':
        crumbs.append(('New', ''))
        title = 'New Record'

    return dict(grid=grid, crumbs=crumbs, title=title, description=not action and session_record.description,
                analytics=not action and DIV('Placeholder'))

@auth.requires_login()
def session():
    session_id = request.args(0)

    # If args[0], then find session id matching args[0]
    session_record = None
    if session_id and session_id not in ['new', 'delete']:
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
        editable=False,
        searchable=False,
        oncreate=lambda form: create_session_table(form.vars.id, form.vars.labels, form.vars.result_label),
        ondelete=lambda table,id: drop_session_table(id),
        _class='table',
        details=False,
        fields = [tl.name, tl.description, tl.created_on],
        user_signature=False,
        links=[dict(header='', body=_view_button)],
        links_placement='left',
    )

    # Replace 'Add Record' button text
    addspan = grid.element(_title='Add record to database')
    if addspan: addspan[0] = addspan['_title'] = 'New Session'

    # Remove 'records found' message
    grid.element('.web2py_counter', replace=None)

    return dict(grid=grid, crumbs=[('Sessions', '')], title='New Session' if session_id == 'new' else 'Sessions')
    
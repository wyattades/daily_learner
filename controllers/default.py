# -*- coding: utf-8 -*-

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

# ---- Action for login/register/etc (required for auth) -----
def user():
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
# @cache.action()
# def download():
#     return response.download(request, db)

def _view_button(row):
    return A(SPAN('Go to this Session'), SPAN(I('', _class='fas fa-arrow-right'), _class='icon'), _class='button is-primary', _href=URL('default', 'session/%d' % row.id))

def _entry_fields(labels, vals, error):
    fields = [ DIV(
                LABEL(labels[i], _class='label'),
                INPUT(_type='number', _step=0.0001, _name='vals', _class='input', _value=vals and vals[i], requires=IS_DECIMAL_IN_RANGE(0.0, 1.0)),
                _class='field'
            ) for i in range(len(labels)) ]
    if error:
        fields.append(DIV(error, _class='error'))

    return CAT(*fields)

def _delete_entries(_, session_id):
    query = (db.entries.session_id == session_id)
    db(query).delete()

def _view_session(session_record):
    action = request.args(1)

    # if action and action not in ['new','delete','edit']:
    #     raise HTTP(404)

    crumbs = [
        ('Sessions', URL('default', 'session')),
        (session_record.name, URL('default', 'session/%d' % session_record.id)),
    ]
    title = session_record.name


    # Enforce that the number of vals equals the number of labels
    rq = db.entries.vals.requires
    rq.minimum = rq.maximum = len(session_record.labels)

    tl = db.entries
    query = (db.entries.session_id == session_record.id)

    # Calculate page
    if action == 'calculate':
        crumbs.append(('Calculator', ''))
        return dict(grid='Placeholder', title='Calculator', crumbs=crumbs)

    grid = SQLFORM.grid(query,
        args=[session_record.id],
        csv=False,
        ui=ui,
        _class='table',
        searchable=False,
        user_signature=False,
        details=False,
    )

    prev_vals = None
    vals_error = None

    if action == 'edit': # Get previous vals and errors
        prev_vals = grid.update_form.record.vals
        vals_error = grid.update_form.errors.vals

        crumbs.append(('Edit', ''))
        title = 'Edit Record'
    if action == 'new':
        crumbs.append(('New', ''))
        title = 'New Record'
    if action in ['new','edit']: # Replace fields with user's custom fields
        grid.element('#entries_vals__row.field', replace=lambda el: _entry_fields(session_record.labels, prev_vals, vals_error))
        grid.element('#entries_result_val__label').components = [session_record.result_label]

    return dict(grid=grid, crumbs=crumbs, title=title, analytics=not action and DIV('Placeholder'))

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
        ondelete=_delete_entries,
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
    
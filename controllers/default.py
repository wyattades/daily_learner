# -*- coding: utf-8 -*-


# Static pages
def index():
    return dict()
def about():
    return dict()
def tutorial():
    return dict()

# ---- API (example) -----
# @auth.requires_login()
# def api_get_user_email():
#     if not request.env.request_method == 'GET': raise HTTP(403)
#     return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
# @auth.requires_membership('admin') # can only be accessed by members of admin groupd
# def grid():
#     response.view = 'generic.html' # use a generic view
#     tablename = request.args(0)
#     if not tablename in db.tables: raise HTTP(403)
#     grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
#     return dict(grid=grid)

# ---- Embedded wiki (example) ----
# def wiki():
#     auth.wikimenu() # add the wiki to the menu
#     return auth.wiki() 

# ---- Action for login/register/etc (required for auth) -----
def user():
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
# @cache.action()
# def download():
#     return response.download(request, db)

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
    buttonview='fas fa-list-ul')

def _view_button(row):
    return A(SPAN(I('', _class='fas fa-list'), _class='icon'), SPAN('View'), _class='button is-link', _href=URL('default', 'session/%d' % row.id))

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

@auth.requires_login()
def session():
    session_id = request.args(0)
    session_record = None
    if session_id:
        session_record = db.sessions(session_id)
        if session_record != None and session_record.owner_id != auth.user_id:
            raise HTTP(403)

    if session_record:
        # Enforce that the number of vals equals the number of labels
        rq = db.entries.vals.requires
        rq.minimum = rq.maximum = len(session_record.labels)

        query = (db.entries.session_id == session_record.id)
        grid = SQLFORM.grid(query,
            args=[session_record.id],
            csv=False,
            ui=ui,
            _class='table',
            searchable=False,
            user_signature=False
        )

        prev_vals = None
        vals_error = None
        is_home = True
        if 'edit' in request.args: # Get previous vals and errors
            prev_vals = grid.update_form.record.vals
            vals_error = grid.update_form.errors.vals
        if 'edit' in request.args or 'new' in request.args: # Replace fields with user's custom fields
            grid.element('#entries_vals__row.field', replace=lambda el: _entry_fields(session_record.labels, prev_vals, vals_error))
            grid.element('#entries_result_val__label').components = [session_record.result_label]
            is_home = False

        return dict(grid=grid, analytics=is_home and DIV('Placeholder'))

    query = (db.sessions.owner_id == auth.user_id)
    tl = db.sessions
    grid = SQLFORM.grid(query, 
        csv=False,
        ui=ui,
        searchable=False,
        editable=False,
        ondelete=_delete_entries,
        _class='table',
        details=False,
        fields = [tl.name, tl.description, tl.created_on],
        user_signature=False,
        links=[dict(header='', body=_view_button)]
    )
    return dict(grid=grid)
    

def no_swearing(form):
  pass
  # form.errors.name = 'Wow! Bad!'

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

# prefix = 'web2py_grid' and 'w2p' or 'w2p_%s' % formname
# prefix = 'w2p'
# spanel_id = '%s_query_fields' % prefix
# sfields_id = '%s_query_panel' % prefix
# skeywords_id = '%s_keywords' % prefix
# # hidden fields to presever keywords in url after the submit
# hidden_fields = [INPUT(_type='hidden', _value=v, _name=k) for k, v in request.get_vars.items() if k not in ['keywords', 'page']]
# search_widget = lambda sfield, url: FORM(
#     INPUT(_name='keywords',
#           _id=skeywords_id, _class='input',
#           _onfocus="jQuery('#%s').change();jQuery('#%s').slideDown();" % (spanel_id, sfields_id) if True else ''
#           ),
#     INPUT(_type='submit', _value=T('Search'), _class="button is-primary"),
#     INPUT(_type='submit', _value=T('Clear'), _class="button",
#           _onclick="jQuery('#%s').val('');" % skeywords_id),
#     *hidden_fields,
#     _method="GET", _action=url)

@auth.requires_login()
def index():
  # q = (db.sessions.owner_id == auth.user_id)
  # sessions = db(q).select()
  # return dict(sessions=db(q).select())
  # TODO: don't use this grid thing, it's limiting and annoying
  return dict(sessions=SQLFORM.grid(db.sessions, _class='table', 
      csv=False, ui=ui))

@auth.requires_login()
def new():
  form = SQLFORM(db.sessions)
  # if form.process(onvalidation=no_swearing).accepted:
  if form.accepts(request, session):
    session.flash = T('Session added.')
    redirect(URL('session','index'))
  elif form.errors:
    session.flash = T('Please correct the info')
  return dict(form=form)

@auth.requires_login()
def edit():
  form = SQLFORM(db.sessions)
  # if form.process(onvalidation=no_swearing).accepted:
  if form.accepts(request,session):
    session.flash = T('Session added.')
    redirect(URL('session','index'))
  elif form.errors:
    session.flash = T('Please correct the info')
  return dict(form=form)
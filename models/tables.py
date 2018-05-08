# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

def _format_date(value, row):
  return value.strftime('%d/%m/%Y %H:%M')

db.define_table('sessions',
  Field('owner_id', db.auth_user, default=auth.user_id, readable=False, writable=False),
  Field('name', 'string', length=48, requires=IS_NOT_EMPTY()),
  Field('description', 'text'),
  Field('created_on', 'datetime', default=request.now, represent=_format_date, readable=True, writable=False),
  Field('updated_on', 'datetime', update=request.now, represent=_format_date, readable=False, writable=False),
  Field('labels', 'list:string', requires=IS_LIST_OF(IS_NOT_EMPTY(), minimum=2, maximum=16)),
  Field('result_label', 'string', requires=IS_NOT_EMPTY()),
  singular='Session',
  plural='Sessions'
)
db.sessions.id.readable = False

db.define_table('entries',
  Field('session_id', 'reference sessions', default=request.args(0), readable=False, writable=False),
  Field('created_on', 'datetime', default=request.now, represent=_format_date, readable=True, writable=False),
  Field('updated_on', 'datetime', update=request.now, represent=_format_date, readable=False, writable=False),
  Field('vals', 'list:string', requires=IS_LIST_OF(IS_DECIMAL_IN_RANGE(0.0, 1.0))),
  Field('result_val', 'string', requires=IS_DECIMAL_IN_RANGE(0.0, 1.0)),
  singular='Entry',
  plural='Entries'
)
db.entries.id.readable = False

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

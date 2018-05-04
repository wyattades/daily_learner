# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.


db.define_table('sessions',
  Field('owner_id', db.auth_user, default=auth.user_id, readable=False, writable=False),
  Field('name', 'string', length=48, requires=IS_NOT_EMPTY()),
  Field('description', 'text'),
  Field('created_on', 'datetime', default=request.now, writable=False),
  Field('updated_on', 'datetime', update=request.now, readable=False, writable=False),
  Field('labels', 'list:string', requires=IS_LIST_OF(IS_NOT_EMPTY(), minimum=2, maximum=16)),
  Field('result_label', 'string', requires=IS_NOT_EMPTY())
)

db.define_table('entries',
  Field('session_id', 'reference sessions', default=request.args(0), readable=False, writable=False),
  Field('created_on', 'datetime', default=request.now, readable=False, writable=False),
  Field('updated_on', 'datetime', update=request.now, readable=False, writable=False),
  Field('vals', 'list:string', requires=IS_LIST_OF(IS_DECIMAL_IN_RANGE(0.0, 1.0))),
  Field('result_val', 'string', requires=IS_DECIMAL_IN_RANGE(0.0, 1.0))
)

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.


db.define_table('sessions',
  Field('owner_id', db.auth_user, default=auth.user_id, readable=False, writable=False),
  Field('name', 'string', length=48, requires=IS_NOT_EMPTY()),
  Field('description', 'text'),
  Field('created_on', 'datetime', default=request.now, readable=False, writable=False),
  Field('updated_on', 'datetime', update=request.now, readable=False, writable=False),
  # format='%(name)s %(id)s',
)

db.define_table('entries',
  Field('session_id', 'reference sessions', readable=False, writable=False),
  Field('created_on', 'datetime', default=request.now, readable=False, writable=False),
  Field('updated_on', 'datetime', update=request.now, readable=False, writable=False)
)

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

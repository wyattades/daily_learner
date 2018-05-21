# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

def _format_date(value, row):
  if value is not None: return value.strftime('%d/%m/%Y %H:%M')
  return 'None'

LABEL_REQUIRES = [IS_MATCH('^\w+$', error_message='Label can only contain letters, numbers, and underscore'), IS_LENGTH(64, 1)]
db.define_table('sessions',
  Field('owner_id', db.auth_user, default=auth.user_id, readable=False, writable=False),
  Field('name', 'string', length=48, requires=IS_NOT_EMPTY()),
  Field('description', 'text'),
  Field('created_on', 'datetime', default=request.now, represent=_format_date, readable=True, writable=False),
  Field('updated_on', 'datetime', update=request.now, represent=_format_date, readable=False, writable=False),
  Field('labels', 'list:string', requires=IS_LIST_OF(LABEL_REQUIRES, minimum=2, maximum=16)),
  Field('result_label', 'string', requires=LABEL_REQUIRES),
  singular='Session',
  plural='Sessions',
  redefine=True, # I hope this is OK
)
db.sessions.id.readable = db.sessions.id.writable = False


def setattrs(obj, **kwargs):
  for k,v in kwargs.items():
      setattr(obj, k, v)

def config_session_table(table):
  setattrs(table.id, readable=False, writable=False)
  setattrs(table.created_on, default=request.now, represent=_format_date, readable=True, writable=False)
  setattrs(table.updated_on, update=request.now, represent=_format_date, readable=False, writable=False)
  for field in table:
    if field.name not in ['id','created_on','updated_on']:
      setattrs(field, requires=IS_FLOAT_IN_RANGE(0.0, 1.0))
  setattrs(table, singular='Entry', plural='Entries')

for table in db.tables():
  if table.startswith('session_'):
    config_session_table(db[table])

def get_session_table(id):
  key = 'session_{}'.format(id)
  if key not in db.tables():
    print('Failed to find table: {}'.format(key))
    raise HTTP(500)
  return db[key]

def create_session_table(id, labels, result_label):
  key = 'session_{}'.format(id)
  if key in db.tables():
    raise HTTP(500, 'Create session table: table {} already exists'.format(key))

  # Create table
  fields = [ Field(label, 'double') for label in labels ]
  fields.append(Field(result_label, 'double'))
  table = db.define_table(key,
    Field('created_on', 'datetime'),
    Field('updated_on', 'datetime'),
    *fields
  )
  config_session_table(table)

  if key not in db.tables():
    raise HTTP(500, 'Failed to create table: {}'.format(key))

  print('Created table: {}'.format(key))

  return table

def drop_session_table(id):
  key = 'session_{}'.format(id)
  if key in db.tables():
    db[key].drop()
    print('Dropped table: {}'.format(key))
  else:
    raise HTTP(500, 'Drop session table: table {} does not exist'.format(key))


# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

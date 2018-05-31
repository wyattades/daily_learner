from ml_models import MODELS

def _format_date(value, row):
  if value is not None: return value.strftime('%d/%m/%Y %H:%M')
  return 'None'

LABEL_REQUIRES = [IS_LENGTH(64, 1), IS_MATCH('^[a-zA-Z]\w*$',
  error_message='Label can only contain letters, numbers, and underscores, and must start with a letter')]
db.define_table('sessions',
  Field('owner_id', db.auth_user, default=auth.user_id, readable=False, writable=False),
  Field('name', 'string', length=48, requires=IS_NOT_EMPTY()),
  Field('description', 'text'),
  Field('created_on', 'datetime', default=request.now, represent=_format_date, readable=True, writable=False),
  Field('updated_on', 'datetime', update=request.now, represent=_format_date, readable=False, writable=False),
  Field('labels', 'list:string', requires=IS_LIST_OF(LABEL_REQUIRES, minimum=2, maximum=16)),
  Field('result_label', 'string', requires=LABEL_REQUIRES),
  Field('training', 'boolean', default=False, readable=False, writable=False),
  Field('model_type', 'string', length=48, requires=IS_IN_SET([ (model, model) for model in MODELS ]), default='LinearModel'),
  Field('model', 'blob', readable=False, writable=False),
  Field('stats', 'json', default='{}', readable=False, writable=False),
  singular='Session',
  plural='Sessions',
)
db.sessions.id.set_attributes(readable=False, writable=False)


def define_session_table(key, labels, result_label):
  fields = [
    Field(label, 'double', rname='"label_%d"' % index, requires=IS_FLOAT_IN_RANGE(0.0, 1.0))
    for index, label in enumerate(labels)
  ]
  fields.append(Field(result_label, 'double', rname='"result_label"', requires=IS_FLOAT_IN_RANGE(0.0, 1.0)))
  db.define_table(key,
    Field('created_on', 'datetime', default=request.now, represent=_format_date, readable=True, writable=False),
    Field('updated_on', 'datetime', update=request.now, represent=_format_date, readable=False, writable=False),
    *fields
  )
  table = db[key]
  table.id.set_attributes(readable=False, writable=False)
  table.singular = 'Entry'
  table.plural = 'Entries'

# We have to define all session databases on every request
for sess in db(db.sessions).select():
  define_session_table('session_{}'.format(sess.id), sess.labels, sess.result_label)

def get_session_table(id):
  key = 'session_{}'.format(id)
  if key not in db.tables():
    raise HTTP(500, 'Failed to find table: {}'.format(key))
  return db[key]

def create_session_table(session):
  key = 'session_{}'.format(session.id)
  if key in db.tables():
    raise HTTP(500, 'Create session table: table {} already exists'.format(key))

  try:
    define_session_table(key, session.labels, session.result_label)
  except:
    raise HTTP(500, 'Unknown error. Failed to create table: {}'.format(key))

  if key not in db.tables():
    raise HTTP(500, 'Failed to create table: {}'.format(key))

  print('Created table: {}'.format(key))

def drop_session_table(id):
  key = 'session_{}'.format(id)
  if key in db.tables():
    db[key].drop()
    print('Dropped table: {}'.format(key))
  else:
    raise HTTP(500, 'Drop session table: table {} does not exist'.format(key))

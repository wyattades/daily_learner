from ml_models import MODELS, rows_to_dataframe

def _get_session():
    session_id = request.args(0)
    session_record = db.sessions(session_id)
    if session_record is None or session_record.owner_id != auth.user_id:
        raise HTTP(403, 'session does not exist or you do not have access')
    return session_record

@auth.requires_login()
@auth.requires_signature()
def train_model():
    session_record = _get_session()
    session_entries = get_session_table(session_record.id)

    session_record.update_record(training=True)

    Model = MODELS[session_record.model_type]
    if Model is None: raise HTTP(500, 'Invalid model type')

    model = Model()
    model.upload_data(rows_to_dataframe(db(session_entries).select(), session_record.labels + [session_record.result_label]))

    # def save_model(model):
    #     record.update_record(model=model.save_model(), training=False, stats=model.get_stats())
    #     db.commit()
    stats = model.train()
    session_record.update_record(model=model.save_model(), training=False, stats=stats)

    return response.json(dict(stats=stats, training=False))


@auth.requires_login()
@auth.requires_signature()
def training_status():
    session_record = _get_session()
    return response.json(dict(training=session_record.training))


@auth.requires_login()
@auth.requires_signature()
def predict():
    session_record = _get_session()

    for label in session_record.labels:
        if label not in request.vars:
            raise HTTP(400, 'Must provide all session labels')

    prediction = None
    # prediction = ml.predict(session_record.model, request.vars)

    return response.json(dict(prediction=prediction))
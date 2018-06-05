
def _get_session():
    session_id = request.args(0)
    session_record = db.sessions(session_id)
    if session_record is None or session_record.owner_id != auth.user_id:
        raise HTTP(403, 'session does not exist or you do not have access')
    return session_record

def _create_model(MODELS, model_type):

    Model = MODELS[model_type]
    if Model is None: raise HTTP(500, 'Invalid model type')

    return Model()

@auth.requires_login()
@auth.requires_signature()
def train_model():
    from ml_models import ToSmallDataSetException, rows_to_dataframe, MODELS

    session_record = _get_session()
    stats = None
    print(session_record.training)
    if not session_record.training:
        session_entries = get_session_table(session_record.id)

        session_record.update_record(training=True)

        model = _create_model(MODELS, session_record.model_type)

        try:
            model.upload_data(rows_to_dataframe(db(session_entries).select(), session_record.labels + [session_record.result_label]))
        except ToSmallDataSetException:
            raise HTTP(400, 'DataSet too small')

        # def save_model(model):
        #     record.update_record(model=model.save_model(), training=False, stats=model.get_stats())
        #     db.commit()
        stats = model.train()
        session_record.update_record(model=model.save_model(), training=False, stats=stats, last_trained=request.now)

    return response.json(dict())


@auth.requires_login()
@auth.requires_signature()
def training_status():
    session_record = _get_session()
    session_table = get_session_table(session_record.id)

    status = 200
    if session_record.training: status = 102
    elif db(session_table).count() < 5: status = 406

    return response.json(dict(status=status, stats=session_record.stats, last_trained=session_record.last_trained))


@auth.requires_login()
@auth.requires_signature()
def predict():
    from ml_models import IncorrectPredictSizeException, rows_to_dataframe, MODELS

    session_record = _get_session()
    model = _create_model(MODELS, session_record.model_type)

    data_in = []
    for label in session_record.labels:
        val = request.vars[label]
        if val is None or val == '':
            raise HTTP(400, 'Must provide all session labels')
        data_in.append(float(val))

    if session_record.model is None:
        raise HTTP(400, 'Model is None for prediction')

    try:
        model.load_model(session_record.model)
    except Exception as e:
        print('asdadasd a da d sad as', e)
        session_record.update_record(model=None)

    if session_record.model_type == 'ScikitModel':
        session_entries = get_session_table(session_record.id)
        model.upload_data(rows_to_dataframe(db(session_entries).select(), session_record.labels + [session_record.result_label]))
        model.train()

    try:
        prediction = model.predict(data_in)
        return response.json(dict(prediction=prediction))
    except IncorrectPredictSizeException:
        raise HTTP(400, 'Incorrect Predict Size')

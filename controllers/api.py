from ml_models import MODELS, rows_to_dataframe, ToSmallDataSetException, IncorrectPredictSizeException 

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
    stats = None
    if not session_record.training:
        session_entries = get_session_table(session_record.id)

        session_record.update_record(training=True)

        Model = MODELS[session_record.model_type]
        if Model is None: raise HTTP(500, 'Invalid model type')

        model = Model()
        try:
            model.upload_data(rows_to_dataframe(db(session_entries).select(), session_record.labels + [session_record.result_label]))
        except ToSmallDataSetException:
            raise HTTP(400, 'DataSet too small')

        # def save_model(model):
        #     record.update_record(model=model.save_model(), training=False, stats=model.get_stats())
        #     db.commit()
        stats = model.train()
        session_record.update_record(model=model.save_model(), training=False, stats=stats, last_trained=request.now)

    return True


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
    session_record = _get_session()

    print(request.vars)

    for label in session_record.labels:
        if label not in request.vars:
            raise HTTP(400, 'Must provide all session labels')

    prediction = None
    # prediction = ml.predict(session_record.model, request.vars)
    # IncorrectPredictSizeException

    return response.json(dict(prediction=prediction))
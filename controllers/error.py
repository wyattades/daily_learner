

codes = {
    '0': 'An unknown error occurred!',
    '403': 'Sorry, you don\'t have access!',
    '404': 'Sorry, the thing you want isn\'t here!',
    '500': 'Sorry, something went wrong on our end!',
    '503': 'We\'re doing maintence here! Come back soon'
}

def index():
    status = request.vars.code
    message = request.vars.message
    if (status == None or status not in codes):
        status = '0'
    if (message == None):
        message = codes.get(status)
    return dict(message=message, status=request.vars.code, ticket=request.vars.ticket)

codes = {
    '403': 'Sorry, you don\'t have access!',
    '404': 'Sorry, the thing you want isn\'t here!',
    '500': 'Sorry, something went wrong on our end!',
    '503': 'We\'re doing maintence here! Come back soon'
}

def index():
    status = request.vars.code
    msg = codes.get(status)

    if (msg == None): msg = 'An unknown error occurred!'
    if (status == None): status = '0'

    return dict(message=msg, status=status, ticket=request.vars.ticket)

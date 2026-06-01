from vercel_wsgi import handle_request
from gov_schemes.wsgi import application


def handler(request, context):
    return handle_request(application, request, context)

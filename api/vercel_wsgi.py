import io
import sys
import base64
from urllib.parse import urlsplit, unquote


def _get_request_body(request):
    # try common attributes used by different runtimes
    if hasattr(request, 'body'):
        return request.body or b''
    if hasattr(request, 'get_data'):
        return request.get_data() or b''
    if hasattr(request, 'data'):
        return request.data or b''
    return b''


def _get_path_and_query(request):
    # try path, url, rawPath, pathname
    path = None
    query = ''
    if hasattr(request, 'path'):
        path = request.path
    elif hasattr(request, 'rawPath'):
        path = request.rawPath
    elif hasattr(request, 'url'):
        url = request.url
        parsed = urlsplit(url)
        path = parsed.path
        query = parsed.query
    elif hasattr(request, 'pathname'):
        path = request.pathname
    if path is None:
        path = '/'
    # try querystring attrs
    if hasattr(request, 'query') and isinstance(request.query, dict):
        from urllib.parse import urlencode
        query = urlencode(request.query, doseq=True)
    elif hasattr(request, 'query_string'):
        qs = request.query_string
        if isinstance(qs, bytes):
            try:
                query = qs.decode('utf-8')
            except Exception:
                query = ''
        else:
            query = qs or ''
    return unquote(path), query


def handle_request(application, request, context=None):
    """Adapt Vercel Python request to a WSGI environ, call the WSGI app,
    and return a Vercel-compatible response dict.
    """
    body = _get_request_body(request)
    path, query_string = _get_path_and_query(request)

    # Build basic WSGI environ
    environ = {}
    environ['REQUEST_METHOD'] = getattr(request, 'method', 'GET')
    environ['SCRIPT_NAME'] = ''
    environ['PATH_INFO'] = path
    environ['QUERY_STRING'] = query_string or ''
    host = ''
    if hasattr(request, 'headers'):
        # some runtimes expose a dict-like headers
        headers = request.headers
    else:
        headers = {}
    # Host
    host = headers.get('host') or headers.get('Host') or ''
    if host:
        parts = host.split(':')
        environ['SERVER_NAME'] = parts[0]
        environ['SERVER_PORT'] = parts[1] if len(parts) > 1 else '80'
    else:
        environ['SERVER_NAME'] = 'localhost'
        environ['SERVER_PORT'] = '80'

    environ['SERVER_PROTOCOL'] = headers.get('x-forwarded-proto', 'HTTP/1.1')
    environ['wsgi.version'] = (1, 0)
    environ['wsgi.url_scheme'] = 'https' if headers.get('x-forwarded-proto', '').lower() == 'https' else 'http'
    environ['wsgi.input'] = io.BytesIO(body)
    environ['wsgi.errors'] = sys.stderr
    environ['wsgi.multithread'] = False
    environ['wsgi.multiprocess'] = False
    environ['wsgi.run_once'] = False

    # Content headers
    content_type = headers.get('content-type') or headers.get('Content-Type')
    if content_type:
        environ['CONTENT_TYPE'] = content_type
    content_length = headers.get('content-length') or headers.get('Content-Length')
    if content_length:
        environ['CONTENT_LENGTH'] = content_length

    # HTTP_ headers
    for key, value in headers.items():
        if not value:
            continue
        k = key.upper().replace('-', '_')
        if k in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            continue
        environ[f'HTTP_{k}'] = value

    # start_response collector
    response_status = {}
    response_headers = {}

    def start_response(status, response_headers_list, exc_info=None):
        response_status['status'] = status
        response_headers['headers'] = response_headers_list

    # Call the WSGI application
    result = application(environ, start_response)

    try:
        body_chunks = b''.join([chunk if isinstance(chunk, (bytes, bytearray)) else chunk.encode('utf-8') for chunk in result])
    finally:
        if hasattr(result, 'close'):
            try:
                result.close()
            except Exception:
                pass

    status = response_status.get('status', '500 Internal Server Error')
    status_code = int(status.split(' ', 1)[0])
    headers_list = response_headers.get('headers', [])
    headers_out = {k: v for k, v in headers_list}

    # Try to decode body as utf-8; if fails, base64-encode and mark encoded
    try:
        body_text = body_chunks.decode('utf-8')
        is_base64 = False
        body_field = body_text
    except Exception:
        body_field = base64.b64encode(body_chunks).decode('ascii')
        is_base64 = True

    return {
        'statusCode': status_code,
        'headers': headers_out,
        'body': body_field,
        'isBase64Encoded': is_base64,
    }

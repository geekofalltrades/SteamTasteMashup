def application(environ, start_response):
    line_tmpl = "Key: {} Value: {}\n"
    body_length = 0
    response = []
    for key, val in environ.items():
        line = line_tmpl.format(key, val)
        response.append(line)
        body_length += len(line)
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain'),
                        ('Content-Length', str(body_length))]
    start_response(status, response_headers)
    return response


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()

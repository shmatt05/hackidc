import webapp2
import json
import logging

__author__ = 'david'


class BaseFrameworkException(Exception):
    def __init__(self, *args, **kwargs):
        super(BaseFrameworkException, self).__init__(*args, **kwargs)
        self._code = None

    def code(self):
        return self._code


class BusinessException(BaseFrameworkException):
    def __init__(self, code, message):
        BaseFrameworkException.__init__(self, message)
        self._code = code


class Handler(webapp2.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(Handler, self).__init__(*args, **kwargs)

    @property
    def data_service(self):
        from shared.services import get_data_service

        return get_data_service()

    def get_request_fields(self, default_fields):
        fields = self.request.get('fields')
        if not fields:
            return default_fields
        else:
            return [field.strip() for field in fields.split(',')]

    def build_response(self, code, message, **response):
        meta = {'code': code, 'message': message}
        reply = {'meta': meta, 'response': response}

        self.response.headers['Content-Type'] = 'application/json'
        self.response.set_status(code, message)
        self.response.md5_etag()
        self.response.out.write(json.dumps(reply))

    def failed_response(self, code, message):
        self.build_response(code, message)

    def successful_response(self, **response):
        self.build_response(200, 'successful', **response)

    def digest_exception(self, exception):
        if isinstance(exception, BaseFrameworkException):
            logging.error(exception.message)

            exception_code = exception.code()
            exception_message = exception.message
        else:
            logging.exception(exception)

            exception_code = 500
            exception_message = exception.message

        exception_code = int(exception_code)
        if isinstance(exception_message, unicode):
            exception_message = exception_message.encode('utf8')

        self.response.set_status(exception_code, exception_message)
        self.failed_response(exception_code, exception_message)

    @staticmethod
    def check_request_parameter(value, name):
        if value is None:
            raise BusinessException(431, 'Missing request parameter "%s"' % name)

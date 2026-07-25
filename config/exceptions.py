from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        if isinstance(response.data, dict):
            if 'detail' in response.data:
                response.data = {'error': response.data['detail']}
            else:
                errors = {}
                for field, messages in response.data.items():
                    if isinstance(messages, list):
                        errors[field] = [str(m) for m in messages]
                    else:
                        errors[field] = str(messages)
                response.data = {'errors': errors}
    return response

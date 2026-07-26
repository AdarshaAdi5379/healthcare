from rest_framework import status
from rest_framework.response import Response


def format_errors(errors):
    if isinstance(errors, dict):
        if 'non_field_errors' in errors:
            return {'error': errors['non_field_errors'][0]}
        return {
            'errors': {
                k: [str(e) for e in v] if isinstance(v, list) else str(v)
                for k, v in errors.items()
            }
        }
    return {'error': str(errors)}


def success_response(message, data=None, http_status=status.HTTP_200_OK):
    body = {'message': message}
    if data is not None:
        body['data'] = data
    return Response(body, status=http_status)


def created_response(message, data=None):
    return success_response(message, data, status.HTTP_201_CREATED)


def deleted_response():
    return Response(status=status.HTTP_204_NO_CONTENT)


def error_response(message, http_status=status.HTTP_400_BAD_REQUEST):
    return Response({'error': message}, status=http_status)


class ResponseMixin:
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return created_response(
            f'{self.serializer_class.Meta.model._meta.verbose_name.title()} created successfully',
            serializer.data
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return success_response(
            f'{self.serializer_class.Meta.model._meta.verbose_name.title()} updated successfully',
            serializer.data
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return deleted_response()

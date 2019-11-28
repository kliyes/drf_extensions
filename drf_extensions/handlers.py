from logging import getLogger

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext_lazy as _
from django.http import Http404

from rest_framework import status, exceptions
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import exception_handler as _exception_handler

from .codes import ERROR_CODES


ERROR_CODES.update(getattr(settings, "ERROR_CODES", {}))
logger = getLogger("error_file")


def flat(d):
    """
    flat nested:
        {'enrollments': [{'id_card_num': ['invalid']}]}
    to:
        {'enrollments.id_card_num': ['invalid']}
    :param d:
    :return:
    """
    if not type(d) == str:
        for key, values in d.items():
            for index, value in enumerate(values):
                if value and type(value) == dict:
                    for inner_key, inner_value in value.items():
                        return {f"{key}[{index}].{inner_key}": inner_value}
    return d


def exception_handler(exc, context):
    """
    Custom exception handler, better error messages

    :param exc:
    :param context:
    :return:
    """
    if isinstance(exc, Http404):
        exc = exceptions.NotFound()
    elif isinstance(exc, PermissionDenied):
        exc = exceptions.PermissionDenied()

    response = _exception_handler(exc, context)

    error_field = None
    if response is None:  # should be 500 server error
        logger.exception(exc)
        if not settings.DEBUG:
            return Response(
                {
                    "field": error_field,
                    "code": ERROR_CODES.get("internal_server_error"),
                    "message": _("Internal Server Error"),
                    "data": None
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    else:
        codes = flat(exc.get_codes())
        response_data = flat(response.data)
        error_message = response_data.pop("detail", None)
        if error_message is None:
            error_message = _("Validation Error")
            error_code = "invalid"
        else:
            error_code = codes
        for field, errors_list in response_data.items():
            error_message = f"{errors_list[0]}"
            error_code = codes.get(field)[0]
            if not field == api_settings.NON_FIELD_ERRORS_KEY:
                error_field = field
            break
        data = {
            "field": error_field,
            "code": ERROR_CODES.get(error_code, ERROR_CODES.get("common")),
            "message": error_message,
            "data": None
        }
        response.data = data
        return response

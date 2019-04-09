from rest_framework import status


class SerializerRequestMixin(object):

    @property
    def request(self):
        return self.context.get("request")


class UpdateResponseDataMixin(object):

    def finalize_response(self, request, response, *args, **kwargs):
        response_data = response.data or {}
        if status.is_success(response.status_code) and "code" not in response_data:
            response.status_code = status.HTTP_200_OK
            response.data = {
                "field": None,
                "code": 0,
                "message": "success",
                "data": response_data
            }
        return super(UpdateResponseDataMixin, self).finalize_response(
            request, response, *args, **kwargs
        )

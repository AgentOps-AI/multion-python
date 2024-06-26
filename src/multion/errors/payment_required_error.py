# This file was auto-generated by Fern from our API Definition.

from ..core.api_error import ApiError
from ..types.payment_required_response import PaymentRequiredResponse


class PaymentRequiredError(ApiError):
    def __init__(self, body: PaymentRequiredResponse):
        super().__init__(status_code=402, body=body)

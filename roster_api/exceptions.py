from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status

def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns standardized error responses.
    """
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        # Standardize error format
        # Laravel often returns: {"message": "...", "errors": {...}} for validation
        # or {"status": "error", "message": "..."} for others.
        
        custom_response_data = {
            "status": "error",
            "message": "An error occurred",
        }
        
        # If it's a validation error (400)
        if response.status_code == 400:
            custom_response_data["message"] = "Validation Error"
            custom_response_data["errors"] = response.data
        elif isinstance(response.data, dict) and "detail" in response.data:
             custom_response_data["message"] = response.data["detail"]
        elif isinstance(response.data, list):
             custom_response_data["message"] = response.data[0]
        else:
             custom_response_data["message"] = str(response.data)

        # Update the response data
        response.data = custom_response_data
        
    return response

from rest_framework.response import Response
import secrets
import string

def ApiResponse(data=None, message="Success", status="success", status_code=200, **kwargs):
    """
    Standardized API Response helper.
    
    Args:
        data: The main data payload. If it's a dict, it can be merged or nested depending on needs.
              Here we allow flexibility: if data is passed, it's typically nested in the response,
              BUT for legacy compatibility with the 'index' endpoints which return { 'skills': [...] },
              we might pass that dict as **kwargs or handle it.
              
              However, the pattern seen in views is:
              return Response({
                  'status': 'success',
                  'message': 'Success', 
                  'skills': serializer.data
              })
              
              So we'll allow kwargs to be merged into the response body.
    """
    response_data = {
        "status": status,
        "message": message,
    }
    
    if data is not None:
        response_data['data'] = data
        
    if kwargs:
        response_data.update(kwargs)
        
    return Response(response_data, status=status_code)

def generate_password(length=12):
    """
    Generate a cryptographically secure random password.
    """
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(length))
        if (any(c.islower() for c in password)
                and any(c.isupper() for c in password)
                and any(c.isdigit() for c in password)
                and any(c in string.punctuation for c in password)):
            return password

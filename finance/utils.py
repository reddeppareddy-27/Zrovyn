from rest_framework.views import exception_handler
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler to provide consistent error responses.
    
    Args:
        exc: The exception raised
        context: The context in which the exception occurred
        
    Returns:
        Response object with error details
    """
    response = exception_handler(exc, context)

    if response is None:
        # Log unexpected exceptions
        logger.exception(f"Unexpected error: {exc}")
        return response

    # Log error for debugging
    logger.warning(f"API Error: {exc.__class__.__name__} - {str(exc)}")

    # Customize error response format
    if response.status_code == status.HTTP_400_BAD_REQUEST:
        response.data = {
            'success': False,
            'message': 'Invalid input provided.',
            'errors': response.data,
            'status_code': response.status_code,
        }
    elif response.status_code == status.HTTP_401_UNAUTHORIZED:
        response.data = {
            'success': False,
            'message': 'Authentication required.',
            'status_code': response.status_code,
        }
    elif response.status_code == status.HTTP_403_FORBIDDEN:
        response.data = {
            'success': False,
            'message': 'You do not have permission to perform this action.',
            'status_code': response.status_code,
        }
    elif response.status_code == status.HTTP_404_NOT_FOUND:
        response.data = {
            'success': False,
            'message': 'The requested resource was not found.',
            'status_code': response.status_code,
        }
    elif response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        response.data = {
            'success': False,
            'message': 'An internal server error occurred.',
            'status_code': response.status_code,
        }

    return response

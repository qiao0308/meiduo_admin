from rest_framework_jwt.utils import jwt_response_payload_handler
def user_response_payload_handler(token, user=None, request=None):
    return{
        'token':token,
        'id':user.id,
        'username':user.username
    }


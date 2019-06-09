from rest_framework_jwt.utils import jwt_response_payload_handler

from rest_framework_jwt.utils import jwt_payload_handler



def user_response_payload_handler(token, user=None, request=None):
    return{
        'token':token,
        'id':user.id,
        'username':user.username
    }
def user_payload_handler(user):
    payload=jwt_payload_handler(user)
    payload['mobile']=user.mobile

    if 'email' in payload:
        del payload['email']


    return payload

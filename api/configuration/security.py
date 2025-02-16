from keycloak import KeycloakOpenID, KeycloakAdmin
from keycloak.exceptions import KeycloakAuthenticationError
from fastapi import Security, HTTPException, status, Depends
from fastapi.security import APIKeyHeader, HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated


from api.configuration.settings import envs


keycloak_openid = KeycloakOpenID(
    server_url=envs.SERVER_URL,
    client_id=envs.CLIENT_ID,
    realm_name=envs.REALM_NAME,
    client_secret_key=envs.CLIENT_SECRET_KEY,
)

keycloak_admin = KeycloakAdmin(
    server_url=envs.SERVER_URL,
    username="admin@gmail.com",
    password="dev1234",
    realm_name=envs.REALM_NAME,
    client_id=envs.CLIENT_ID,
    client_secret_key=envs.CLIENT_SECRET_KEY,
)

oauth2_scheme = HTTPBearer()
api_key_scheme = APIKeyHeader(name="token")

forbidden_exception = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="You're not allowed to access this resource, contact your administrator",
    headers={"WWW-Authenticate": "Bearer"},
)

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid token",
    headers={"WWW-Authenticate": "Bearer"},
)


async def get_api_key(api_key: str = Security(api_key_scheme)):
    if api_key == envs.API_KEY:
        return api_key
    else:
        raise forbidden_exception


# to-do: add a function that allows change the registration_completed of the user


async def finish_registration(
    token: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    try:
        userinfo = keycloak_openid.userinfo(token.credentials)
    except KeycloakAuthenticationError:
        raise credentials_exception

    changes = {
        "email": userinfo["email"],
        "firstName": userinfo["given_name"],
        "lastName": userinfo["family_name"],
        "attributes": {"registration_completed": True},
    }

    keycloak_admin.update_user(user_id=userinfo["sub"], payload=changes)

    return userinfo


async def get_current_user(
    token: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    try:
        userinfo = keycloak_openid.userinfo(token.credentials)     
    except KeycloakAuthenticationError:
        raise credentials_exception

    userinfo["roles"] = []
    if "luckypay" in userinfo["resource_access"].keys(): 
        userinfo["roles"] = userinfo["resource_access"]["luckypay"]["roles"]
    if not userinfo["registration_completed"]:
        raise HTTPException(403, "You need to finish your registration before!")
    return userinfo

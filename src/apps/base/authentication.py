from rest_framework import authentication, exceptions

from integracoes.firebase.utils import (
    buscar_ou_criar_usuario_do_firebase,
    verificar_token_firebase,
)


class FirebaseAuthentication(authentication.BaseAuthentication):
    www_authenticate_realm = "api"

    def authenticate(self, request):
        token = self.get_token_from_request(request)
        if token is None:
            return None

        try:
            decoded = verificar_token_firebase(token)
        except ValueError as err:
            raise exceptions.AuthenticationFailed(
                "O seu acesso expirou, faça o login novamente para poder prosseguir."
            ) from err

        user, created = buscar_ou_criar_usuario_do_firebase(decoded)
        return (user, token)

    def authenticate_header(self, request):
        return f'Bearer realm="{self.www_authenticate_realm}"'

    def get_token_from_request(self, request):
        auth = request.META.get("HTTP_AUTHORIZATION", "")
        if auth.startswith("Bearer "):
            return auth.split(" ", 1)[1].strip()
        return None

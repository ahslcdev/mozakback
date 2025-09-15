from firebase_admin import auth as firebase_auth
from firebase_admin import exceptions as firebase_exceptions

from apps.usuarios.models import Usuario


def verificar_token_firebase(id_token: str):
    try:
        decoded = firebase_auth.verify_id_token(id_token)
        return decoded
    except firebase_exceptions.FirebaseError as e:
        raise ValueError(f"Firebase token inválido: {e}") from e


def buscar_ou_criar_usuario_do_firebase(decoded_token: str):
    uid, email, nome = (
        decoded_token.get("uid"),
        decoded_token.get("email"),
        decoded_token.get("name") or decoded_token.get("displayName"),
    )

    username = f"fb_{uid}"

    user = None
    if email:
        try:
            user = Usuario.objects.get(email__iexact=email)
        except Usuario.DoesNotExist:
            user = None

    if not user:
        user, created = Usuario.objects.get_or_create(
            username=username,
            defaults={
                "email": email or "",
                "username": nome or username,
                "is_active": True,
            },
        )
    else:
        created, changed = False, False

        if email and user.email != email:
            user.email = email
            changed = True
        if nome and getattr(user, "nm_cliente", None) != nome:
            user.nm_cliente = nome
            changed = True
        if changed:
            user.save(update_fields=["email", "nm_cliente"])

    return user, created

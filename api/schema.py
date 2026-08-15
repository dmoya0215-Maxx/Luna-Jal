from drf_spectacular.utils import extend_schema, extend_schema_view

from .views import PeopleViewSet, UserViewSet


person_schema = extend_schema_view(
    list=extend_schema(
        summary="Listar personas",
        description="Obtiene todas las personas registradas en el sistema."
    ),
    retrieve=extend_schema(
        summary="Consultar persona",
        description="Obtiene la información de una persona específica."
    ),
    create=extend_schema(
        summary="Crear persona",
        description="Registra una nueva persona."
    ),
    update=extend_schema(
        summary="Actualizar persona",
        description="Actualiza completamente la información de una persona."
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente persona",
        description="Actualiza parcialmente la información de una persona."
    ),
    destroy=extend_schema(
        summary="Eliminar persona",
        description="Elimina una persona del sistema."
    ),
)


user_schema = extend_schema_view(
    list=extend_schema(
        summary="Listar usuarios",
        description="Obtiene todos los usuarios registrados."
    ),
    retrieve=extend_schema(
        summary="Consultar usuario",
        description="Obtiene la información de un usuario específico."
    ),
    create=extend_schema(
        summary="Crear usuario",
        description="Registra un nuevo usuario."
    ),
    update=extend_schema(
        summary="Actualizar usuario",
        description="Actualiza completamente un usuario."
    ),
    partial_update=extend_schema(
        summary="Actualizar parcialmente usuario",
        description="Actualiza parcialmente un usuario."
    ),
    destroy=extend_schema(
        summary="Eliminar usuario",
        description="Elimina un usuario."
    ),
)
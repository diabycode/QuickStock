from django.contrib.auth.models import Permission
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_str


def log_user_action(user, obj, action_flag, change_message=''):
    LogEntry.objects.log_action(
        user_id=user.pk,
        content_type_id=ContentType.objects.get_for_model(obj).pk,
        object_id=obj.pk,
        object_repr=force_str(obj),
        action_flag=action_flag,
        change_message=change_message
    )


def get_perm_verbose_name(perm: Permission):
    verbose_name = None
    verbose = {
        'add': 'Ajouter',
        'change': 'Modifier',
        'delete': 'Supprimer',
        'view': 'Voir'
    }
    perm_type = None
    if perm.codename.startswith('add_'):
        perm_type = 'add'
    elif perm.codename.startswith('change_'):
        perm_type = 'change'
    elif perm.codename.startswith('delete_'):
        perm_type = 'delete'
    elif perm.codename.startswith('view_'):
        perm_type = 'view'

    if perm_type:
        model_name: str= perm.content_type.model_class()._meta.verbose_name.capitalize()
        verbose_name = f"{verbose[perm_type]} - {model_name}"
    return verbose_name if verbose_name != None else perm.name


def get_all_permissions(edit_default: bool=False, excludes: list=[]):
    content_types = ContentType.objects.all().exclude(model__in=excludes)
    models = [c.model_class() for c in content_types]
    permissions = Permission.objects.none()

    for model in models:
        perms = get_model_permissions(model, edit_default=edit_default)
        permissions = (permissions | perms)
    permissions.distinct()

    return permissions


def get_model_permissions(model_class, edit_default=False):
    content_type = ContentType.objects.get_for_model(model_class)
    # get permissions
    permissions = Permission.objects.filter(content_type=content_type)

    # set with for loop verbose_name
    for perm in permissions:
        verbose_name = perm.name
        if edit_default:
            verbose_name = get_perm_verbose_name(perm)
        setattr(perm, "verbose_name", verbose_name)
    return permissions



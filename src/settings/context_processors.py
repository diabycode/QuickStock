
from settings.models import EditableSettings

def app_settings(request):
    return {
        "app_settings": EditableSettings.load(),
    }



from settings.models import EditableSettings

def settings_context(request):
    return {
        "company_name": EditableSettings.load().company_name
    }


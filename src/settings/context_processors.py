
from settings.models import EditableSettings

def company_name(request):
    return {
        "company_name": EditableSettings.load().company_name
    }


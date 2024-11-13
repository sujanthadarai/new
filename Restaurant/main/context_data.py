from datetime import datetime

def current_date(request):
    return {'date':datetime.now()}
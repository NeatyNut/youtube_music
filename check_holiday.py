from datetime import datetime

class isholiday:
    today = datetime.now().date()
    weekend = today.weekday()
    holiday = True if weekend >= 5 else False
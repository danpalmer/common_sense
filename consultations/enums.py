from django_enumfield import Enumeration, Item


class ConsultationStateEnum(Enumeration):
    OPEN = Item(10, 'open')
    CLOSED = Item(20, 'closed')
    OUTCOME = Item(30, 'outcome')

    DISPLAY_TYPE_TO_ENUM_TYPE = {
        'Open consultation': OPEN,
        'Closed consultation': CLOSED,
        'Consultation outcome': OUTCOME,
    }

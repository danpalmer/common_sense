from django_enumfield import Enum, Item


ConsultationStateEnum = Enum('ConsultationStateEnum',
    Item(10, 'open', 'Open consultation'),
    Item(20, 'closed', 'Closed consultation'),
    Item(30, 'outcome', 'Consultation outcome'),
)
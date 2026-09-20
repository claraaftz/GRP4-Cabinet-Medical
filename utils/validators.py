#Exception levée si patient n'existe pas
class PatientNotFoundError(Exception):
    pass

#Exception levée si consultation n'existe pas
class ConsultationNotFoundError(Exception):
    pass

#Exception levée si numéro de sécurité sociale invalide
class InvalidSecurityNumberError(Exception):
    pass

#Exception levée si statut de consultation invalide
class InvalidConsultationStatusError(Exception):
    pass


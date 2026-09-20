from functools import wraps
from datetime import datetime

from utils.validators import PatientNotFoundError


def log_action(description):


    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            date_heure = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open("data/log.txt", "a", encoding="utf-8") as fichier:
                fichier.write(
                    f"[{date_heure}] Action effectuée : {description}\n"
                )

            return result

        return wrapper

    return decorator


def validate_patient(func):

    @wraps(func)
    def wrapper(self, patient, *args, **kwargs):

        if patient is None:
            raise PatientNotFoundError(
                "Le patient n'existe pas."
            )

        if not hasattr(patient, "numero_securite_sociale"):
            raise PatientNotFoundError(
                "Le patient fourni est invalide."
            )

        return func(self, patient, *args, **kwargs)

    return wrapper

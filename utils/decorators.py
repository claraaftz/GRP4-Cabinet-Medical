from functools import wraps
from datetime import datetime
from utils.validators import PatientNotFoundError

#Decorateur : enregistre action dans log (date + heure)
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


#Decorateur : vérifie si patient existe
def validate_patient(func):

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        n_secu = kwargs.get("n_securite_sociale") or kwargs.get("numero_securite_sociale")
        if not n_secu and args:
            n_secu = args[0]
            
        patients_dict = getattr(self, "patients", {})
        if n_secu not in patients_dict:
            raise PatientNotFoundError(f"Aucun patient trouvé avec le N° de Sécurité Sociale : {n_secu}")
        return func(self, *args, **kwargs)
    
    return wrapper
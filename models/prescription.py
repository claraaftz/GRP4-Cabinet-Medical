from abc import ABC, abstractmethod


__all__ = [
    "PrescriptionMedicamenteuse",
    "PrescriptionExamen",
    "PrescriptionKinesitherapie"
]

#Classe abstraite pour les prescriptions
class Prescription(ABC) :
    def __init__(self, traitement: str, posologie: str, duree_traitement: str ) -> None:
        self._traitement = traitement
        self._posologie = posologie
        self._duree_traitement = duree_traitement

    #Méthode abstraite : afficher les informations de la prescription
    @abstractmethod
    def afficher_details(self) :
        pass

    #Aide IA : Comment pas bloquer JSON tout en gardant l'architecture des consignes
    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @staticmethod
    def from_dict(data: dict):
        p_type = data.get("type")
        if p_type == "Medicamenteuse":
            return PrescriptionMedicamenteuse(
                medicament=data["medicament"],
                posologie=data["posologie"],
                duree_traitement=data["duree_traitement"],
                dosage=data["dosage"],
                frequence=data["frequence"]
            )
        elif p_type == "Examen":
            return PrescriptionExamen(
                type_examen=data["type_examen"],
                laboratoire_recommande=data["laboratoire_recommande"],
                posologie=data["posologie"],
                duree_traitement=data["duree_traitement"]
            )
        elif p_type == "Kinesitherapie":
            return PrescriptionKinesitherapie(
                zone_traite=data["zone_traite"],
                nb_seance=data["nb_seance"],
                posologie=data["posologie"],
                duree_traitement=data["duree_traitement"]
            )
        raise ValueError("Type de prescription inconnu")



class PrescriptionMedicamenteuse(Prescription) :
    def __init__(self, medicament: str, posologie: str, duree_traitement: str, dosage: str, frequence: str) -> None:
        super().__init__(medicament, posologie, duree_traitement)
        self._medicament = medicament
        self._dosage = dosage
        self._frequence = frequence

    def afficher_details(self) -> str:
        return (
            "Prescription medicamenteuse :\n"
            f"- Medicament : {self._medicament}\n"
            f"- Dosage : {self._dosage}\n"
            f"- Fréquence : {self._frequence}\n"
            f"- Posologie : {self._posologie}\n"
            f"- Durée du traitement : {self._duree_traitement}\n"
            )

    def to_dict(self) -> dict:
        return {
            "type": "Medicamenteuse",
            "medicament": self._medicament,
            "posologie": self._posologie,
            "duree_traitement": self._duree_traitement,
            "dosage": self._dosage,
            "frequence": self._frequence
        }


    
class PrescriptionExamen(Prescription):
    def __init__(self, type_examen: str, laboratoire_recommande: str, *, posologie: str ="Aucune", duree_traitement: str ="Aucune", ) -> None:
        super().__init__(type_examen, posologie, duree_traitement)
        self._type_examen = type_examen
        self._laboratoire_recommande = laboratoire_recommande

    def afficher_details(self) -> str:
        return (
            "Prescription d'examen :\n"
            f"- Type d'examen : {self._type_examen}\n"
            f"- laboratoire recommandé : {self._laboratoire_recommande}\n"
            f"- Posologie : {self._posologie}\n"
            f"- Durée du traitement : {self._duree_traitement}\n"
        )

    def to_dict(self) -> dict:
        return {
            "type": "Examen",
            "type_examen": self._type_examen,
            "laboratoire_recommande": self._laboratoire_recommande,
            "posologie": self._posologie,
            "duree_traitement": self._duree_traitement
        }

    

class PrescriptionKinesitherapie(Prescription) :
    def __init__(self, zone_traite: str, nb_seance: int, posologie: str = "À définir", duree_traitement: str = "À définir") -> None:
        super().__init__("Kinesitherapie", posologie, duree_traitement)
        self._zone_traite = zone_traite
        self._nb_seance = nb_seance
  
    def afficher_details(self) -> str:
        return (
            "Prescription Kinesitherapie \n"
            f"- Zone à traiter : {self._zone_traite} \n"
            f"- Nombre de seance : {self._nb_seance} \n"
            f"- Posologie : {self._posologie}\n"
            f"- Durée du traitement : {self._duree_traitement}\n"
        )

    def to_dict(self) -> dict:
        return {
            "type": "Kinesitherapie",
            "zone_traite": self._zone_traite,
            "nb_seance": self._nb_seance,
            "posologie": self._posologie,
            "duree_traitement": self._duree_traitement
        }
    


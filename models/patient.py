from datetime import date
from utils.validators import InvalidSecurityNumberError


class Patient:
    def __init__(self, n_securite_sociale: str, nom: str, prenom: str, date_naissance: date, adresse: str, telephone: str):
        self.n_securite_sociale = n_securite_sociale 
        self._nom = nom
        self._prenom = prenom
        self._date_naissance = date_naissance
        self._adresse = adresse
        self._telephone = telephone
        self.liste_consultations = []

    #getters et setters
    @property
    def n_securite_sociale(self) -> str:
        return self._n_securite_sociale
    @n_securite_sociale.setter
    def n_securite_sociale(self, numero: str):
        if not self.verification_n_securite_sociale(numero):
            raise InvalidSecurityNumberError("Numéro invalide ! Il doit contenir 15 chiffres.")
        self._n_securite_sociale = numero

    @property
    def telephone(self) -> str:
        return self._telephone
    @telephone.setter
    def telephone(self, telephone: str):
        self._telephone = telephone

    @property
    def nom(self) -> str:
        return self._nom
    @nom.setter
    def nom(self, nom: str):
        self._nom = nom

    @property
    def prenom(self) -> str:
        return self._prenom
    @prenom.setter
    def prenom(self, prenom: str):
        self._prenom = prenom

    @property
    def adresse(self) -> str:
        return self._adresse
    @adresse.setter
    def adresse(self, adresse: str):
        self._adresse = adresse

    @property
    def date_naissance(self) -> date:
        return self._date_naissance
    @date_naissance.setter
    def date_naissance(self, date_naissance: date):
        self._date_naissance = date_naissance



    #contraintes méthodes métier cours
    #Méthode static : verifie chaine = 15 chiffres
    @staticmethod
    def verification_n_securite_sociale(numero: str) -> bool:
        return isinstance(numero, str) and len(numero) == 15 and numero.isdigit()

    #Méthode : calculer l'age du patient avec data de naissance
    @property
    def age(self) -> int:
        aujourdhui = date.today()
        age = aujourdhui.year - self.date_naissance.year
        if (aujourdhui.month, aujourdhui.day) < (self.date_naissance.month, self.date_naissance.day):
            age -= 1
        return age

    #Méthode : convertir le patient en dictionnaire
    def to_dict(self) -> dict:
        return {
            "n_securite_sociale": self.n_securite_sociale,
            "nom": self.nom,
            "prenom": self.prenom,
            "date_naissance": self.date_naissance.isoformat(),
            "adresse": self.adresse,
            "telephone": self.telephone,
        }

    #Méthode : Change representation dans console
    def __repr__(self) -> str:
        return f"Patient(n_securite_sociale={self.n_securite_sociale}, nom={self.nom}, prenom={self.prenom}, age={self.age})"
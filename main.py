from abc import ABC, abstractmethod
import mysql.connector
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mediatheque_db"
    )
    print("Connexion réussie à la base de données")
except mysql.connector.Error as err:
    print(f"Erreur de connexion : {err}")

curseur = conn.cursor()

class Document(ABC):

    def __init__(self, titre):
        self.titre = titre
        self.__disponible = True  

    @property
    def disponible(self):
        return self.__disponible

    def changeEtat (self, etat):
        self.__disponible = etat

    @abstractmethod
    def emprunter(self):
        pass

    @abstractmethod
    def retourner(self):
        pass
class Livre(Document):

    def __init__(self, titre, auteur):
        super().__init__(titre)
        self.auteur = auteur

    def emprunter(self):
        if not self.disponible:
            raise Exception(" Ce livre est déjà emprunté.")
        self.changeEtat(False)
        print("Livre emprunté.")

    def retourner(self):
        if self.disponible:
            raise Exception(" Ce livre est déjà disponible.")
        self.changeEtat(True)
        print(" Livre retourné.")

    def __str__(self):
        return f"Livre | {self.titre} |  de {self.auteur} | Disponible : {self.disponible}"

class Magazine(Document):

    def __init__(self, titre, theme):
        super().__init__(titre)
        self.theme = theme

    def emprunter(self):
        if not self.disponible:
            raise Exception("Ce magazine est déjà emprunté.")
        self.changeEtat(False)
        print(" Magazine emprunté.")

    def retourner(self):
        if self.disponible:
            raise Exception(" Ce magazine est déjà disponible.")
        
        self.changeEtat(True)
        print(" Magazine retourné.")

    def __str__(self):
        return f"Magazine | {self.titre} | N°{self.theme} | Disponible : {self.disponible}"

class Bibliothecaire:
    """Gestionnaire du catalogue."""

    def __init__(self):
        self.catalogue = []
        
    def ajouter_document(self, document):
        self.catalogue.append(document)

    # def rechercher_par_titre(self, titre):
    #     for doc in self.catalogue:
    #         if doc.titre == titre:
    #             return doc
    #     return None

    def afficher_catalogue(self):
        if not self.catalogue:
            print(" Catalogue vide.")
            return

        for doc in self.catalogue:
            print(doc)
    
    def ajouter_livre(self,livre):
        sql = "insert into Document (titre,auteur)values(%s,%s)"
        curseur.execute(sql,(livre.titre,livre.auteur))
        conn.commit()
        print("ajouter avec succes")
          
    def ajouter_Magazine(self,magazine):
        sql = "insert into Document (titre,theme)values(%s,%s)"
        curseur.execute(sql,(magazine.titre,magazine.theme))
        conn.commit()
        print("ajouter avec succes")
        
    def rechercher_document(self,titre):
        sql="select id,statut from Document where titre = %s"
        curseur.execute(sql,(titre,))
        return curseur.fetchone()
            
    def emprunter(self,id_document):
        sql = "insert into Emprunt (id_document)values(%s)"
        curseur.execute(sql,(id_document,))
        conn.commit()
       
    def modifier_statut(self,id_document,statut):
        sql="update Document set statut=%s where id = %s"
        curseur.execute(sql,(statut,id_document))
        conn.commit()
    
    def statut(self,id_document):
        sql = "select statut from Document where id = %s"
        curseur.execute(sql,(id_document,))
        document = curseur.fetchone()
        return document[0]
    
    def chercher_emprunt(self, id_document):
        sql = "select e.id from Emprunt e join Document d on e.id_document = d.id where d.id = %s "
        curseur.execute(sql,(id_document,))
        emprunt = curseur.fetchone()
        return emprunt
        
    def changer_statut_emprunt(self,id_emprunt):

        sql="update Emprunt set statut='retourner' where id = %s"
        curseur.execute(sql,(id_emprunt,))
        conn.commit() 
    
    
           

class Menu:
   

    def __init__(self):
        self.biblio = Bibliothecaire()


    def afficher(self):
        print("\n---------- MENU -----------")
        print("1. Ajouter un Livre")
        print("2. Ajouter un Magazine")
        print("3. Emprunter un document")
        print("4. Retourner un document")
        print("5. Afficher le catalogue")
        print("6. Quitter")

    def lancer(self):
        while True:
            self.afficher()
            choix = input("Choix : ")

            match choix:

                case "1":
                    titre = input("Titre : ")
                    auteur = input("Auteur : ")
                    self.biblio.ajouter_document(Livre(titre, auteur))
                    self.biblio.ajouter_livre(Livre(titre, auteur))

                case "2":
                    titre = input("Titre : ")
                    theme = input("Theme : ")
                    self.biblio.ajouter_document(Magazine(titre, theme))
                    self.biblio.ajouter_Magazine(Magazine(titre, theme))

                case "3":
                    titre = input("Titre du document : ")
                    t=self.biblio.rechercher_document(titre)
                    if t:
  
                        if self.biblio.statut(t[0]) == "disponible":
                            self.biblio.emprunter(t[0])
                            print("emprunt effectuer avec succes")
                        
                            self.biblio.modifier_statut(t[0],"emprunter") 
                        else:
                            print("document déja emprunter")   
                    else:
                        print("document non trouvé")
                                              

                case "4":
                    titre = input("Titre du document : ")
                    doc = self.biblio.rechercher_document(titre)
                    if doc:
                        
                        if doc[1]=="emprunter":
                           emprunt = self.biblio.chercher_emprunt(doc[0])
                           
                           if emprunt:
                               self.biblio.changer_statut_emprunt(emprunt[0])
                               self.biblio.modifier_statut(doc[0],"disponible")
                               print ("empreunt retourner avec succés")
                           else:
                               print("emprunt non trouvé")  
                        else:
                            print("document deja retourner")  
                    else:
                        print("Document introuvable.")

                case "5":
                    self.biblio.afficher_catalogue()

                case "6":
                    print("Au revoir ")
                    break

                case _:
                    print("Choix invalide.")


if __name__ == "__main__":
    menu = Menu()
    menu.lancer()
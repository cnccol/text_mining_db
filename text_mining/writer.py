from .database import db

class Writer:

    def save(self, document, collection_name):
        try:
            print(document)
            data = document.dict()
            print(data)
            data["id"] = str(data["id"])
            db.collection(collection_name).document(str(document.id)).set(data)
            return True
        except:
            return False

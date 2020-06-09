import process_text_mining as pm
import update_database as udb
import update_database_with_pickles as udbp

WHERE = 'cnc5'



GROUPS = ['HV','HV','HV','HV','Certificaciones','Contratos',
        'Licitaciones','Licitaciones','Licitaciones','Licitaciones',
        'Licitaciones','Licitaciones','Licitaciones','Licitaciones',
        'Licitaciones','Licitaciones','Oponentes']

def process_all():

    print("INIT update database")
    for i in range(len(FOLDERS)):
        folder = FOLDERS[i]
        group = GROUPS[i]
        udb.update_database(folder, group)

    print("END update database")

    print("INIT update database with pickles")
    for x in set(GROUPS):
        print(x)
        udbp.update_database(x+'.pickle')

    print("END update database with pickles")

    print("INIT READING")
    for x in set(GROUPS)
        print(x)
        pm.process_all_docs(x)

    print("END READING")

import process_text_mining as pm
import update_database as udb
import update_database_with_pickles as udbp

WHERE = 'cnc5'

FOLDERS = ['/run/user/1000/gvfs/smb-share:server=10.20.135.21,share=archivos/CNC_LICITACIONES/CNC_LICITACIONES/Hojas_de_Vida',
        '/run/user/1000/gvfs/smb-share:server=10.20.135.21,share=archivos/CNC_LICITACIONES/CNC_LICITACIONES/Licitaciones/HOJAS DE VIDA',
        '/run/user/1000/gvfs/smb-share:server=10.20.135.21,share=archivos/CNC_LICITACIONES/CNC_LICITACIONES/Licitaciones/HOJAS DE VIDA CONSULTORES PARA LICITACIONES',
        '/run/user/1000/gvfs/smb-share:server=10.20.135.21,share=archivos/CNC_LICITACIONES/CNC_LICITACIONES/Licitaciones/HV ABOGADOS',
        '/run/user/1000/gvfs/smb-share:server=10.20.135.21,share=archivos/CNC_LICITACIONES/CNC_LICITACIONES/Certificaciones',
        '/run/user/1000/gvfs/smb-share:server=10.20.135.21,share=archivos/CNC_LICITACIONES/CNC_LICITACIONES/Contratos',
        '/run/user/1000/gvfs/smb-share:server=10.20.135.21,share=archivos/CNC_LICITACIONES/Licitaciones/2010',
        '/run/user/1000/gvfs/smb-share:server=10.20.135.21,share=archivos/CNC_LICITACIONES/Licitaciones/2011',
        '/run/user/1000/gvfs/smb-share:server=10.20.135.21,share=archivos/CNC_LICITACIONES/Licitaciones/2012',
        '/run/user/1000/gvfs/smb-share:server=10.20.135.21,share=archivos/CNC_LICITACIONES/Licitaciones/2013',
        '/run/user/1000/gvfs/smb-share:server=10.20.135.21,share=archivos/CNC_LICITACIONES/Licitaciones/2014',
        '/run/user/1000/gvfs/smb-share:server=10.20.135.21,share=archivos/CNC_LICITACIONES/Licitaciones/2015',
        '/run/user/1000/gvfs/smb-share:server=10.20.135.21,share=archivos/CNC_LICITACIONES/Licitaciones/2016',
        '/run/user/1000/gvfs/smb-share:server=10.20.135.21,share=archivos/CNC_LICITACIONES/Licitaciones/2017',
        '/run/user/1000/gvfs/smb-share:server=10.20.135.21,share=archivos/CNC_LICITACIONES/CNC_LICITACIONES/Licitaciones/2018',
        '/run/user/1000/gvfs/smb-share:server=10.20.135.21,share=archivos/CNC_LICITACIONES/CNC_LICITACIONES/Licitaciones/2019',
        '/run/user/1000/gvfs/smb-share:server=10.20.135.21,share=archivos/CNC_LICITACIONES/CNC_LICITACIONES/Licitaciones/Nueva carpeta']

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

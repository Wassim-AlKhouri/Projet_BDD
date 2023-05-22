
''' 
Lors du parsing de diagnostique 

NISS_path = {} // Avant boucle for

NISS_path[NISS] = pathology

return NISS_path
'''



'''
Lors du parsing de patient ou dossier patient 

Double_dic = {} // Avant boucle for

list_best_med_spe(NISS_path[NISS], inami_medecin, Double_dic)

return Double_Dic

'''


def list_best_med_spe(pathologie, inami_medecin, double_dic):
    if pathologie not in double_dic:
        double_dic[pathologie] = {}
    if inami_medecin not in double_dic[pathologie]:
        double_dic[pathologie][inami_medecin] = 0
    double_dic[pathologie][inami_medecin] += 1

def sort_med_for_pathologie(pathologie, double_dic):
    if pathologie in double_dic:
        medecins = double_dic[pathologie]
        sorted_medecins = sorted(medecins.items(), key=lambda x: x[1], reverse=True)
        for inami_medecin, nbre_patient in sorted_medecins:
            print("Inami médecin:", inami_medecin)
            print("Nombre d'apparitions:", nbre_patient)
    else:
        print("La spécialité spécifiée n'existe pas.")

'''
sorted_info = sorted(info.items(), key=lambda x: count.get(x[1].split(",")[0], float('inf')))

'''
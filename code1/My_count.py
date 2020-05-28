def count(a_list):
    dict = {}
    for key in a_list:
        dict[key] = dict.get(key,0) + 1 
        #s'il y a pas de key dans le dictionnaire,il retourne 0 par defaut
    return dict

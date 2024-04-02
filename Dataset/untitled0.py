# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 00:40:58 2024

@author: unsik6
"""

import os
path = os.getcwd()

image_path = path + "\\images"
label_path = path + "\\labels"

insect20names = ["Asiablatta_kyotensis", "Asilidae", "Bibio_tenebrosus", "Blaptica_dubia",
                 "Blattella_germanica", "Bradysia_agrestis", "Cryptocercus_kyebangensis",
                 "Dermatobia_hominis", "Drosophila_melanogaster", "Drosophilidae",
                 "Gasterophilus", "Glossina", "Gromphadorhina_portentosa", 
                 "Lasioderma_serricorne", "Lucilia_caesar", "Lycoriella_mali",
                 "Musca_domestica", "Oestridae", "Penthetria_japonica", "Periplaneta_americana"]
ass = ["Asilidae"]

print(os.path.exists(image_path))
print(os.path.exists(label_path))
i = 1

for name in insect20names:
    local_image_path = image_path + "\\" + name
    local_label_path = label_path + "\\" + name
    out = name + "_" + str(i) + ": " + str(os.path.exists(local_image_path)) + "/" + str(os.path.exists(local_label_path))
    print(out)
    image_list = os.listdir(local_image_path)
    label_list = os.listdir(local_label_path)
    
    """
    for cur_image_name in image_list:
        cur_check_image = cur_image_name[:-4]
        
        isExist = 0
        for cur_label_name in label_list:
            cur_check_label = cur_label_name[:-4]
            
            if cur_check_image == cur_check_label:
                isExist = 1
                break
        if isExist == 0:
            print("No label for " + cur_check_image)
            os.remove(local_image_path + "\\" + cur_image_name)
            print("Delete " + cur_check_image)
    
    for cur_label in label_list:
        cur_check_label = cur_label[:-4]
        
        isExist = 0
        for cur_image in image_list:
            cur_check_image = cur_image[:-4]
            if cur_check_image == cur_check_label:
                isExist = 1
        if isExist == 0:
            print(cur_check_label)
            os.remove(local_label_path + "\\" + cur_label)
    """
    print(len(image_list) == len(label_list))
    print(len(image_list))
            
    i += 1
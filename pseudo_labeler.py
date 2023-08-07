import os
import argparse
from tqdm import tqdm
import shutil

def parsing():
    parser = argparse.ArgumentParser()
    parser.add_argument('--images-path', type=str, help='image folders or file')
    parser.add_argument('--labeler', type=str, help='labeler file path; please input yolo parent dir')
    parser.add_argument('--labels', nargs='+', type=str, help='class names or txt file')
    parser.add_argument('--keywords', nargs='+', type=str, help='keywords combined with class name; "class name + keyword" will be searched.')
    parser.add_argument('--index', type=int, default = 0, help='class index, start index if multiple class')
    parser.add_argument('--conf', type=float, default = 0.25, help='pseudo labeling cofidence treshold')
    parser.add_argument('--crawl', action='store_true', help='crwaling')
    parser.add_argument('--num', type=int, default=1000 ,help='the maximum number of collected image of each label')
    pars = parser.parse_args()
    print(vars(pars))
    
    # If you don't allow crawling, then you have to input image pathes
    if not pars.crawl:
        if pars.images_path == None  or not os.path.exists(change_path(pars.images_path)):
            print('Error: There is no image source.')
            exit(1)
        if len(pars.labels) != 1:
            print('Error: Only one label is allowed without crawling.')
            exit(1)
    if pars.labels == None:
        print('Error: There is no label.')
        exit(1)
    if pars.labeler == None or not os.path.exists(change_path(pars.labeler)):
        print('Error: There is no labeler')
        exit(1)
    return pars

# check keywords from arguements
def name_parsing(names):
    name_list = []
    if len(names) == 1 and names[0][-4:] == '.txt': # labels file
        if os.path.exists(names[0]):
            label_file = open(names, 'r')
            while True:
                line = label_file.readline()                
                if not line: break
                name_list.append(line)
            label_file.close()
        else:
            print('Error: No labels file directories.')
            exit(0)
    elif len(names) < 1:
        print('Error: No label')
        exit(0)
    else:
        name_list = names
    print('Name list is successfully parsed : ', end = '')
    print(name_list)
    return name_list

# Check path with parsing
# Change all '/' to '\\'
def change_path(path : str):
    path = path.replace('/', '\\')
    print(path)
    return path

# Call yolov5
def pseudo_labeling(images_path, labeler_path, conf, label, index):
    print('Start psuedo-labeling: ' + label)
    detect_path = labeler_path + '/detect.py'
    weight_path = labeler_path + '/runs/train/pseudo_labeler/weights/best.pt'
    cmd = 'python ' + detect_path + ' --weights ' + weight_path + ' --conf '
    cmd = cmd + str(conf) + ' --name pseudo_labeling --save-tx --source '
    cmd = cmd + str(images_path)
    os.system(cmd)
    
    # Move result folder
    res_folder = labeler_path + '/runs/detect/pseudo_labeling'
    res_folder = change_path(res_folder)
    shutil.move(res_folder, os.getcwd())
    os.rename('pseudo_labeling', label + ' pseudo')
    labels_folder = label + ' pseudo' + '\\labels'
    labels = os.listdir(labels_folder)
    
    # Change labels
    for label_file in tqdm(labels):
        # Read the label text file written by yolo.detect
        new_labels = []
        file = open(labels_folder + '\\' + label_file, 'r')
        while True:
            line = file.readline()
            line_seg = list(line.split())
            # Skip the last empty line
            if len(line_seg) < 2:
                break
            # Change class index to our index
            line_seg[0] = str(index)
            new_labels.append(line_seg[:-1])
        file.close()
        # Rewrite the label text file
        file = open(labels_folder + '\\' + label_file, 'w')
        for i in range(len(new_labels)):
            for j in range(len(new_labels[i])):
                file.write(new_labels[i][j])
                if j < len(new_labels[i]) - 1: file.write(' ')
            if i < len(new_labels) - 1: file.write('\n')
        file.close()  
    

def main(pars):
    name_list = name_parsing(pars.labels)
    
    # If crawl true, crawl all input keywords
    if pars.crawl == True:
        # create cmd line
        cmd = 'python img_crawler_embedded.py --labels'
        for names in name_list:
            cmd += ' ' + names
        cmd += ' --num ' + str(pars.num)
        if pars.keywords != None:
            cmd += ' --keywords'
            for word in pars.keywords:
                cmd += ' ' + word
        os.system(cmd) # call crawler
    
    # Pseudo Labeling using pre-trained yolov5 model
    label_index = pars.index
    if not pars.crawl:
        pseudo_labeling(pars.images_path, pars.labeler, pars.conf, pars.labels[0], label_index)
    else:
        for name in name_list:
            images_path = 'images\\' + name
            pseudo_labeling(images_path, pars.labeler, pars.conf, name, label_index)
            label_index += 1
    return 0

if __name__ == '__main__':
    pars = parsing()
    main(pars)
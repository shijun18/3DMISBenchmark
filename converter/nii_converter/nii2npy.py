import sys
sys.path.append('..')
import os
import glob
from tqdm import tqdm
import time
import shutil
import json
import numpy as np

from nii_converter.nii_reader import Nii_Reader
from converter.utils import save_as_hdf5


# Different samples are saved in different folder
def nii_to_hdf5(input_path, save_path, annotation_list, target_format, image_postfix, label_postfix, resample=True):
    if resample:
        save_path = save_path + '-resample'

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    else:
        shutil.rmtree(save_path)
        os.makedirs(save_path)

    path_list =os.listdir(input_path)
    start = time.time()
    for ID in tqdm(path_list):
        data_path = os.path.join(input_path, ID)
        image_path = glob.glob(os.path.join(data_path, image_postfix))[0]
        label_path = glob.glob(os.path.join(data_path, label_postfix))[0]
        
        try:
            reader = Nii_Reader(image_path, target_format, label_path, annotation_list, trunc_flag=False, normalize_flag=False)
        except:
            print("Error data: %s" % ID)
            continue
        else:
            if resample:
                images = reader.get_resample_images().astype(np.int16)
                labels = reader.get_resample_labels().astype(np.uint8)
            else:
                images = reader.get_raw_images().astype(np.int16)
                labels = reader.get_raw_labels().astype(np.uint8)

            hdf5_path = os.path.join(save_path, ID + '.hdf5')

            save_as_hdf5(images, hdf5_path, 'image')
            save_as_hdf5(labels, hdf5_path, 'label')

    print("run time: %.3f" % (time.time() - start))



# All samples are saved in the same folder
def nii_to_hdf5_v2(input_path, save_path, annotation_list, target_format, image_postfix, label_postfix, resample=True):
    if resample:
        save_path = save_path + '-resample'

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    else:
        shutil.rmtree(save_path)
        os.makedirs(save_path)

    path_list = os.listdir(input_path)
    # the <<id_list>> needs to be customized
    if 'Covid-Seg' in input_path:
        id_list = set([case.split('_')[0].split('-')[-1] for case in path_list])
    elif 'LiTS' in input_path:
        id_list = set([case.split('-')[-1].split('.')[0] for case in path_list]) #LITS
    print(len(id_list))
    start = time.time()
    for ID in tqdm(id_list):
        print('=====%s is in processing!====='%ID)
        if 'Covid-Seg' in input_path:
            image_path = glob.glob(os.path.join(input_path, '*' + ID + image_postfix))[0]
            label_path = glob.glob(os.path.join(input_path, '*' + ID + label_postfix))[0]
        elif 'LiTS' in input_path:
            image_path = os.path.join(input_path,image_postfix.replace('*',ID))
            label_path = os.path.join(input_path,label_postfix.replace('*',ID))
        try:
            reader = Nii_Reader(image_path, target_format, label_path, annotation_list, trunc_flag=False, normalize_flag=False)
        except:
            print("Error data: %s" % ID)
            continue
        else:
            if resample:
                images = reader.get_resample_images().astype(np.int16)
                labels = reader.get_resample_labels().astype(np.uint8)
            else:
                images = reader.get_raw_images().astype(np.int16)
                labels = reader.get_raw_labels().astype(np.uint8)

            hdf5_path = os.path.join(save_path, ID + '.hdf5')

            save_as_hdf5(images, hdf5_path, 'image')
            save_as_hdf5(labels, hdf5_path, 'label')

    print("run time: %.3f" % (time.time() - start))


if __name__ == "__main__":
    # HaN
    json_file = './static_files/Structseg_HaN.json'
    # THOR
    # json_file = './static_files/Structseg_THOR.json'

    # HaN_GTV
    # json_file = './static_files/HaN_GTV.json'
    # THOR_GTV
    # json_file = './static_files/THOR_GTV.json'

    # segthor
    # json_file = './static_files/SegTHOR.json'
    # covid-seg
    # json_file = './static_files/Covid-Seg.json'
    # json_file = './static_files/LITS.json'
    with open(json_file, 'r') as fp:
        info = json.load(fp)
    # nii_to_hdf5_v2(info['nii_path'], info['npy_path'], info['annotation_list'], info['target_format'],image_postfix=info['image_postfix'],label_postfix=info['label_postfix'],resample=False)
    nii_to_hdf5(info['nii_path'], info['npy_path'], info['annotation_list'], info['target_format'],image_postfix=info['image_postfix'],label_postfix=info['label_postfix'],resample=False)
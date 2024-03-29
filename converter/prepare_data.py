import sys
sys.path.append('..')
import os
import numpy as np
from tqdm import tqdm
import time
import shutil
import h5py
from skimage.transform import resize
import json

from converter.utils import hdf5_reader


def store_images_labels(save_path, patient_id, images, labels, mode):

    if mode == '2d':
        for i in range(images.shape[0]):
            img = images[i]
            lab = labels[i]
            hdf5_file = h5py.File(os.path.join(save_path, '%s_%d.hdf5' % (patient_id, i)), 'w')
            hdf5_file.create_dataset('image', data=img.astype(np.int16))
            hdf5_file.create_dataset('label', data=lab.astype(np.uint8))
            hdf5_file.close()

    elif mode == '3d':
        hdf5_file = h5py.File(os.path.join(save_path, patient_id + '.hdf5'),'w')
        hdf5_file.create_dataset('image', data=images.astype(np.int16))
        hdf5_file.create_dataset('label', data=labels.astype(np.uint8))
        hdf5_file.close()


def prepare_data(input_path, save_path, data_shape, crop=0, mode='2d', for_training=True, retain=10):

    if not os.path.exists(save_path):
        os.makedirs(save_path)
    else:
        shutil.rmtree(save_path)
        os.makedirs(save_path)

    path_list = os.listdir(input_path)
    start = time.time()
    # keep 10~20 samples as final test set
    if for_training:
        if retain != 0:
            path_list = path_list[:-retain]
    else:
        path_list = path_list[-retain:]
    print(path_list)
    for item in tqdm(path_list):
        ID, _ = os.path.splitext(item)
        # print(ID)
        data_path = os.path.join(input_path, item)
        images = hdf5_reader(data_path, "image")
        labels = hdf5_reader(data_path, 'label')
        # print(images.shape)
        if crop != 0:
            images = images[:,crop:-crop,crop:-crop]
            labels = labels[:,crop:-crop,crop:-crop]
        
        class_list = list(np.unique(labels).astype(np.uint8))
        target_shape = data_shape
        if mode == '2d':
            target_shape = (images.shape[0], ) + data_shape

        if images.shape != target_shape:
            images = resize(images, target_shape, mode='constant')
            tmp_labels = np.zeros(target_shape, dtype=np.float32)
            for z in class_list:
                if z != 0:
                    roi = resize((labels == z).astype(np.float32),
                                target_shape,
                                mode='constant')
                    tmp_labels[roi >= 0.5] = z
            labels = tmp_labels

        store_images_labels(save_path, ID, images, labels, mode)
    print("run time: %.3f" % (time.time() - start))

if __name__ == "__main__":
    # keep 10 samples as final test set
    # cervical_oar
    # json_file = './dcm_converter/static_files/Cervical_Oar.json'
    # nasopharynx
    # json_file = './dcm_converter/static_files/Nasopharynx_Oar.json'
    # structseg_han
    # json_file = './nii_converter/static_files/Structseg_HaN.json'
    # structseg_thor
    # json_file = './nii_converter/static_files/Structseg_THOR.json'
    # han_gtv
    # json_file = './nii_converter/static_files/HaN_GTV.json'
    # thor_gtv
    # json_file = './nii_converter/static_files/THOR_GTV.json'
    # segthor
    json_file = '/staff/zzq/code/3DMISBenchmark/dataset/SegTHOR/SegTHOR.json'
    # covid-seg
    # json_file = './nii_converter/static_files/Covid-Seg.json'
    # lung
    # json_file = './dcm_converter/static_files/Lung_Oar.json'
    # lung tumor
    # json_file = './dcm_converter/static_files/Lung_Tumor.json'
    # egfr
    # json_file = './dcm_converter/static_files/EGFR.json'
    # LIDC
    # json_file = './dcm_converter/static_files/LIDC.json'
    # LITS
    # json_file = '/staff/zzq/code/3DMISBenchmark/dataset/LiTS/LITS.json'
    # Nasopharynx_Tumor
    # json_file = './dcm_converter/static_files/Nasopharynx_Tumor.json'
    # Cervical_Tumor
    # json_file = './dcm_converter/static_files/Cervical_Tumor.json'
    # Stomach_Oar
    # json_file = './dcm_converter/static_files/Stomach_Oar.json'
    # Liver_Oar
    # json_file = './dcm_converter/static_files/Liver_Oar.json'
    with open(json_file, 'r') as fp:
        info = json.load(fp)
        input_path = info['npy_path']
        setting_2d = info['2d_data']
        setting_3d = info['3d_data']
    # prepare_data(input_path, setting_2d['save_path'], tuple(setting_2d['shape']), setting_2d['crop'],mode='2d',retain=25)
    # prepare_data(input_path, setting_2d['test_path'], tuple(setting_2d['shape']), setting_2d['crop'],mode='2d',for_training=False,retain=25)
    prepare_data(input_path, setting_3d['save_path'], tuple(setting_3d['shape']), setting_3d['crop'],mode='3d',retain=0)
    # prepare_data(input_path, setting_3d['test_path'], tuple(setting_3d['shape']), setting_3d['crop'],mode='3d',for_training=False,retain=10)
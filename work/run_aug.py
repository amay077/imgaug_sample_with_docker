import imgaug as ia
from imgaug import augmenters as iaa
from matplotlib import pyplot as plt
import imageio
import glob
import os.path

def remove_glob(pathname):
    for p in glob.glob(pathname, recursive=False):
        if os.path.isfile(p):
            os.remove(p)

def main(dir_in, dir_out):

    # 出力先ディレクトリをクリーン
    remove_glob(dir_out + '/*')

    for filepath in glob.glob(dir_in +'/*'):
        print('in: ' + filepath)
        img = imageio.imread(filepath)

        # ノイズ
        noise(filepath, dir_out, img, [0.3, 0.4, 0.5])

        # 欠落
        cutout(filepath, dir_out, img, [0.005, 0.001, 0.02])

        # 移動
        trans(filepath, dir_out, img, [0.1, 0.2, 0.3])

        # 回転
        rotate(filepath, dir_out, img, [45, 80, 160])

        # 傾ける(疑似)
        shear(filepath, dir_out, img, [30, 50, 340])

# 加工後画像をファイルに保存する
def writeFile(filepath, dir_out, prefix, i, aug_img):
    filename = os.path.basename(filepath) # /data_in/img.jpg -> img.jpg
    root, ext = os.path.splitext(filename) # img.jpg -> (img, jpg)
    outpath = dir_out + '/' + root + '_' + prefix + '_' + str(i) + ext
    imageio.imwrite(outpath, aug_img)
    print('out: ' + outpath)

# ノイズを入れる
def noise(filepath, dir_out, img, params):
    i = 0
    for d in params:
        i = i + 1
        # 画像に変換を適用する
        augDropout = iaa.Dropout(p=d)
        aug_img = augDropout.augment_image(img)
        writeFile(filepath, dir_out, 'noise', i, aug_img)

# 部分欠落させる
def cutout(filepath, dir_out, img, params):
    i = 0
    for d in params:
        i = i + 1
        # 画像に変換を適用する
        aug = iaa.CoarseDropout((0.03, 0.15), size_percent=(d, d))
        aug_img = aug.augment_image(img)
        writeFile(filepath, dir_out, 'cutout', i, aug_img)

# 移動させる
def trans(filepath, dir_out, img, params):
    i = 0
    for d in params:
        i = i + 1
        # 画像に変換を適用する
        aug = iaa.Affine(translate_percent={"x": (-d, d), "y": (-d, d)}, mode='constant')
        aug_img = aug.augment_image(img)
        writeFile(filepath, dir_out, 'trans', i, aug_img)

# 回転させる
def rotate(filepath, dir_out, img, params):
    i = 0
    for d in params:
        i = i + 1
        # 画像に変換を適用する
        aug = iaa.Affine(rotate=d, mode='constant')
        aug_img = aug.augment_image(img)
        writeFile(filepath, dir_out, 'rotate', i, aug_img)

# 傾ける(疑似)
def shear(filepath, dir_out, img, params):
    i = 0
    for d in params:
        i = i + 1
        # 画像に変換を適用する
        aug = iaa.Affine(shear=d)
        aug_img = aug.augment_image(img)
        writeFile(filepath, dir_out, 'shear', i, aug_img)

dir = os.path.dirname(__file__) # 実行ファイルの場所
main(dir + '/images_in', dir + '/images_out')
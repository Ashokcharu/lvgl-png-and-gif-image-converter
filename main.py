import os
import subprocess
import natsort
from core.png_gif_c_raw import *
from PIL import Image
from numpy import *
import glob
import shutil


def convert_gif(subdir, add_outfd, files_png):
    frames = []
    for file in files_png:
        img = os.path.join(subdir, file)
        new_frame = Image.open(img)
        frames.append(new_frame)
    frames[0].save('{}.gif'.format(add_outfd), format='GIF',
                   append_images=frames[1:],
                   save_all=True,
                   duration=30,
                   loop=0)


def pngs_to_gifs(folders):
    for (subdir, dirs, files) in os.walk("images", topdown=False):
        files_png = natsort.natsorted(files, reverse=False)
        sub_splt = subdir.split(os.sep)
        add_outfd = folders[0] + sub_splt[len(sub_splt) - 1]
        print(sub_splt)
        if len(sub_splt) == 2:
            convert_gif(subdir, add_outfd, files_png)
        else:
            for fp in files_png:
                shutil.copy(folders[2] + fp, folders[0] + fp)


def optimize_gif_file():
    gfile = []
    gif_files = glob.glob(folders[0] + "*.gif")
    if len(gif_files) == 0:
        print("PNG to GIF conversion failed., Give an input PNG in the images folder and follow the folder structure properly!!!")
    else:
        print("Total", len(gif_files), "gifs and cheader")
        for gf in gif_files:
            subprocess.run('convert {} -fuzz 0.1% -layers Optimize {}'.format(gf, gf), shell=True)
            gs = gf.split(os.sep)
            ln = len(gs)
            print(gs[ln - 1], "Converted successfully")
            gfile.append(gf)
    return gfile


def gif_to_cBinary(folders):
    cf = ["raw", "true_color_alpha"]
    dith = 0
    for subdir, dirs, files in os.walk(folders[0]):
        for procesed_file in files:

            check_extension = procesed_file.split(".")

            if check_extension[1] == "gif":
                c_headers_folders = folders[0] + check_extension[0]
                fn = folders[0] + procesed_file
                conv = Converter(fn, check_extension[0], c_headers_folders, dith, cf[0], folders)
                conv.convert(conv.CF_RAW)
                conv.download_c(conv.out_name)

            elif check_extension[1] == "png":

                alpha = 1
                fn = folders[0] + procesed_file
                c_headers_folders = folders[1] + check_extension[0]

                conv = Converter(fn, check_extension[0], c_headers_folders, dith, cf[1], folders)

                conv.convert(conv.CF_TRUE_COLOR_332, alpha)

                c_332 = conv.format_to_c_array()
                conv.convert(conv.CF_TRUE_COLOR_565, alpha)
                c_565 = conv.format_to_c_array()
                conv.convert(conv.CF_TRUE_COLOR_565_SWAP, alpha)
                c_565_swap = conv.format_to_c_array()
                conv.convert(conv.CF_TRUE_COLOR_888, alpha)
                c_888 = conv.format_to_c_array()
                c_res = str(str(str(c_332) + str(c_565)) + str(c_565_swap)) + str(c_888)

                if cf[1] == "true_color_alpha":
                    conv.download_c(conv.out_name, conv.CF_TRUE_COLOR_ALPHA, c_res)


if __name__ == "__main__":

    folders = ['gif_png/', 'Cheaders/', "images/"]
    if not (os.path.exists(folders[0]) and os.path.exists(folders[1])):
        for fld in folders:
            os.makedirs(os.path.join(fld), exist_ok=True)
    pngs_to_gifs(folders)
    optimize_gif_file()
    gif_to_cBinary(folders)
    print("All Done...!")

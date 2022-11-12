import os
from PIL import Image


def jpgToBmp():
    cur_dst_dir =  os.getcwd()
    jpgTOBmp_cnt = 0
    try :
        os.mkdir(cur_dst_dir + "/BMP")
    except Exception as re:
        print("BMP 已经存在")

    for fileName in os.listdir(cur_dst_dir):
        if os.path.splitext(fileName)[1] == '.jpg':
            name = os.path.splitext(fileName)[0]
            newFileName = name + ".bmp"

            img = Image.open(cur_dst_dir + "/" + fileName)
            img.save(cur_dst_dir+"/BMP/"+newFileName)
            jpgTOBmp_cnt += 1
            print(f"{fileName} 转换为{newFileName}")

    print("总共jpg to bmp 个数为：",jpgTOBmp_cnt)




if __name__ == '__main__':
    cur_dst_dir = r'.\video_tzx\img'
    jpgTOBmp_cnt = 0


    for fileName in os.listdir(cur_dst_dir):
        if os.path.splitext(fileName)[1] == '.jpg':
            name = os.path.splitext(fileName)[0]
            newFileName = name + ".bmp"

            img = Image.open(cur_dst_dir + "/" + fileName)
            img.save( "./BMP/" + newFileName)
            jpgTOBmp_cnt += 1
            print(f"{fileName} 转换为{newFileName}")

    print("总共jpg to bmp 个数为：", jpgTOBmp_cnt)

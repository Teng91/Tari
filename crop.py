# Import Image class from PIL module
import os
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None  # 取消最大像素限制


input_path = "./input" # 自行修改輸入的圖片路徑
dirs = os.listdir(input_path)
count_crop = 0
for file in range(1, len(dirs)+1):
    filename = r"C:/_R11631006/yolov4/input/img" + str(file) + ".jpg" # 自行修改讀取圖片的路徑
    img = Image.open(filename)
    size = img.size
    weight = int(size[0] // 4)
    height = int(size[1] // 8)
    Obj_path = 'C:/_R11631006/yolov4/input_crop' # 自行修改輸出的圖片路徑
    os.makedirs(Obj_path, exist_ok=True)
    for j in range(8):
        for i in range(4):
            box = (weight * i, height * j, weight * (i + 1), height * (j + 1))
            region = img.crop(box)
            count_crop += 1
            region.save(Obj_path + '/{}.jpg'.format(count_crop)) # 儲存裁切後的圖片到輸出路徑

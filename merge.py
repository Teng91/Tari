#=====================合併單張影像=====================#
# from PIL import Image
#
# # 建立一個8x4的大影像
# image_width = 3546
# image_height = 2577
# big_image = Image.new('RGB', (4 * image_width, 8 * image_height))
#
# # 設定每行每列的影像數量
# rows = 4
# cols = 8
#
# # 迭代編號1-32的影像並加入到大影像中
# for i in range(1, 33):
#     # 讀取影像
#     image_path = f"./recover/{i}.jpg"  # 替換為實際影像的路徑
#     img = Image.open(image_path)
#
#     # 計算影像在大影像中的位置
#     row = (i - 1) // rows
#     col = (i - 1) % rows
#     x = col * img.width
#     y = row * img.height
#
#     # 將影像貼到大影像中
#     big_image.paste(img, (x, y))
#
# # 儲存合併後的大影像
# big_image.save("./big_image/merged_image.jpg")
#=====================合併單張影像=====================#

import cv2
from PIL import Image

# 建立一個8x4的大影像
image_width = 3546 # 自行修改影像寬度
image_height = 2577 # 自行修改影像高度

# 設定每行每列的影像數量
rows = 4
cols = 8

# 設定每組影像的數量
images_per_group = 32

# 迭代每組影像集合，共45組
for group_index in range(1, 1441, images_per_group):
    # 建立一個4x8的大影像
    big_image = Image.new('RGB', (rows * image_width, cols * image_height))

    # 迭代當前組內的每張小影像
    for i in range(group_index, group_index + images_per_group):
        if i > 1440:
            break

        # 讀取影像
        image_path = f"./recover/{i}.jpg"  # 替換為實際影像的路徑
        img = Image.open(image_path)

        # 計算影像在大影像中的位置
        row = (i - group_index) // rows
        col = (i - group_index) % rows
        x = col * img.width
        y = row * img.height

        # 將影像貼到大影像中
        big_image.paste(img, (x, y))


    # 儲存合併後的大影像
    big_image.save(f"./big_image/merged_image_{group_index // images_per_group + 1}.jpg")

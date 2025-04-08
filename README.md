# 外銷核可蘭園之有害生物鑑定作業
由臺灣大學生物機電工程研究所與農業部農業試驗所合作之計畫，其中兩個子計畫:
1. 自動化高解析度薊馬類害蟲辨識系統，搭配使用者介面
2. 自動化高解析度核可蘭園內害蟲辨識系統

```
Tari/
├── crop.py                     # 圖片裁切程式                    
├── merge.py                    # 圖片合併程式                    
├── img1.jpg                    # 原始影像範例                           
├── merged_img1.jpg             # 合併影像範例                            
├── README.md                   # 專案說明文件                            
├── user interface/             # 使用者介面相關程式碼                          
│   ├── readme.md               # 使用者介面說明文件                           
│   ├── one-stage/              # 單階段處理的子目錄                            
│   │   ├── readme.md           # 單階段處理說明文件                           
│   │   ├── Tari.py             # 使用者介面主程式                           
│   │   ├── ui.png              # 使用者介面範例圖片               
├── yolov7/                     # YOLOv7 模型相關程式碼               
│   ├── custom_data.yaml        # 自訂數據集配置             
│   ├── detect.py               # YOLOv7 檢測程式                
│   ├── hyp.scratch.custom.yaml # 超參數配置            
│   ├── metrics.py              # 評估指標程式                
│   ├── plots.py                # 繪圖工具程式              
│   ├── readme.md               # YOLOv7 說明文件             
│   ├── test.py                 # 測試程式              
│   ├── train.py                # 訓練程式                 
│   ├── yolov7-custom.yaml      # 自訂 YOLOv7 模型配置     
```
## Target species of Thrips
- *Thrips palmi* Karny 南黃薊馬
- *Frankliniella intonsa* Trybom 臺灣花薊馬
- *Scirtothrips dorsalis* Hood 小黃薊馬

## YOLOv7 object detector 
由中研院王建堯在2022年7月發表YOLOv7論文，並推出原始碼如下:
https://github.com/WongKinYiu/yolov7

**詳細的程式碼修改請至我的hackmd**

https://hackmd.io/@bhIA534oS4WfxIHxC2EFfA/r1WMd493j/%2FtWpevlu7SrGZvEZuN8VWxw

原始掃描影像:
![image](https://github.com/Teng91/Tari/blob/main/img1.jpg)
切割並經過YOLOv7訓練後的合併影像:
![image](https://github.com/Teng91/Tari/blob/main/merged_img1.jpg)

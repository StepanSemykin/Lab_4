import pandas as pd
import os 
import cv2
import numpy as np
from statistics import mean
import matplotlib.pyplot as plt
import random

def data_frame(data_frame: pd.DataFrame, directory_obj: str, name: str):
    data = os.listdir(directory_obj)
    
    if data_frame.empty:
        count = 0
    else: 
        data_list = data_frame["Class"].tolist()
        data_list = list(set(data_list))
        count = len(data_list) 
            
    for i in data:
        path = f"{directory_obj}\{i}"
        data_frame2 = pd.DataFrame({"Class": name, "path": [path], "tag": count})
        data_frame = pd.concat([data_frame, data_frame2], ignore_index = True)
    
    print(data_frame)
    return data_frame
    
def dimension(data_frame: pd.DataFrame):
    width_list = []
    height_list = []
    channels_list = []
    
    for i in data_frame.path: 
        img = cv2.imread(i)
        width_list.append(img.shape[0])
        height_list.append(img.shape[1])
        channels_list.append(img.shape[2])
    
    data_frame["width"] = pd.Series(width_list)
    data_frame["height"] = pd.Series(height_list)
    data_frame["channels"] = pd.Series(channels_list)
    
    print(data_frame)
    return data_frame
        
def stat(data_frame: pd.DataFrame):
    print(data_frame.describe())    
    if data_frame.tag.mean() == 0.5:
        print("Набор является сбалансированным\n")
    else: 
        print("Набор не является сбалансированным\n")   
 
def filter_tag(data_frame: pd.DataFrame, class_tag: int):
    data_frame2 = pd.DataFrame()
    data_frame2 = data_frame[data_frame.tag == class_tag]
    print(data_frame2)    
    return data_frame2

def filter_dimensions(data_frame: pd.DataFrame, class_tag: int, max_height: int, max_width: int): 
    data_frame2 = pd.DataFrame()
    data_frame2 = data_frame[(data_frame.tag == class_tag) & (data_frame.width <= max_width) & (data_frame.height <= max_height)]
    print(data_frame2)
    return data_frame2

def pixel(data_frame: pd.DataFrame, class_tag: int):
    data_frame2 = pd.DataFrame()
    data_frame2 = data_frame[data_frame.tag == class_tag]
    
    sum_list = []
    sum = 0
    
    for i in data_frame2.path:
        img = cv2.imread(i)
        sum += np.sum(img == [255, 255, 255])
        sum_list.append(sum)
    
    print(sum_list)
    print(len(sum_list))
    
    data_frame2["min"] = pd.Series(min(sum_list))
    data_frame2["max"] = pd.Series(max(sum_list))
    data_frame2["average"] = pd.Series(mean(sum_list)) 
    print(data_frame2)
    return data_frame2

def hist(data_frame: pd.DataFrame, class_tag: int):
    data_frame = data_frame[data_frame.tag == class_tag]
    
    path_list = []
    
    for i in data_frame.path:
        path_list.append(i)
    
    random.shuffle(path_list)
    
    img = cv2.imread(path_list[0])
    print(path_list[0])
    hist_b = cv2.calcHist([img], [0], None, [256], [0, 256])
    hist_g = cv2.calcHist([img],[1],None,[256],[0,256])
    hist_r = cv2.calcHist([img],[2],None,[256],[0,256])
    return hist_b, hist_g, hist_r

def output_hist(hist_b: np.ndarray, hist_g: np.ndarray, hist_r: np.ndarray):
    fig = plt.figure(figsize=(30, 8))
    
    fig.add_subplot(1, 3, 1)
    plt.plot(hist_b, color = "b")
    plt.title("Гистограмма изображения для СИНЕГО канала")
    plt.ylabel("Количество пикселей")
    plt.xlabel("Значение пикселя")
    
    fig.add_subplot(1, 3, 2)
    plt.plot(hist_g, color = "g")
    plt.title("Гистограмма изображения для ЗЕЛЕНОГО канала")
    plt.ylabel("Количество пикселей")
    plt.xlabel("Значение пикселя")
    
    fig.add_subplot(1, 3, 3)
    plt.plot(hist_r, color = "r")
    plt.title("Гистограмма изображения для КРАСНОГО канала")
    plt.ylabel("Количество пикселей")
    plt.xlabel("Значение пикселя")
    
    plt.show()
          
def main():
    """Separates code blocks."""
    df = pd.DataFrame()
    
    df = data_frame(df, "D:\Lab Python\Lab_1\dataset\ rose", "rose")
    df = data_frame(df, "D:\Lab Python\Lab_1\dataset\ tulip", "tulip")
    
    df = dimension(df)

    # stat(df)
    
    # df2 = pd.DataFrame()
    # df2 = filter_tag(df, 5)
    
    # df3 = pd.DataFrame()
    # df3 = filter_dimensions(df, 0, 300, 460)
    
    # df4 = pd.DataFrame() 
    # df4 = pixel(df, 0)
    
    b, g, r = hist(df, 0)
    print(type(b))
    output_hist(b, g, r)
    
    
 
if __name__ == "__main__":
	main()  
 
 # D:\Lab Python\Lab_1\dataset\ rose
 # D:\Lab Python\Lab_1\dataset\ tulip
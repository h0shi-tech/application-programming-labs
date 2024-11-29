import os
import pandas as pd
import cv2
import matplotlib.pyplot as plt


def create_dataframe(base_path, annotation_file):

    annotations = pd.read_csv(annotation_file)
    
    
    file_data = []
    for _, row in annotations.iterrows():
        rel_path = row['relative_path']  
        abs_path = os.path.abspath(os.path.join(base_path, rel_path))
        file_data.append([abs_path, rel_path])
    
    df = pd.DataFrame(file_data, columns=["Absolute Path", "Relative Path"])
    return df

def add_image_info(df):
    heights, widths, depths = [], [], []
    for path in df["Absolute Path"]:
        image = cv2.imread(path)
        if image is not None:
            height, width, depth = image.shape
        else:
            height, width, depth = None, None, None
        heights.append(height)
        widths.append(width)
        depths.append(depth)
    df["Height"] = heights
    df["Width"] = widths
    df["Depth"] = depths
    return df

def get_statistics(df):
    stats = df[["Height", "Width", "Depth"]].describe()
    print("Статистическая информация о размерах изображений:")
    print(stats)


def filter_by_dimensions(df, max_width, max_height):
    filtered_df = df[(df["Height"] <= max_height) & (df["Width"] <= max_width)]
    return filtered_df

def add_image_area(df):
    df["Area"] = df["Height"] * df["Width"]
    return df

def sort_by_area(df):
    df = df.sort_values(by="Area", ascending=True)
    return df


def plot_area_histogram(df):
    plt.figure(figsize=(10, 6))
    plt.hist(df["Area"].dropna(), bins=20, color="blue", alpha=0.7)
    plt.title("Распределение площадей изображений")
    plt.xlabel("Площадь изображения (пиксели)")
    plt.ylabel("Частота")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":

    base_path = "С:/images"  
    annotation_file = "annotation_file.csv"  

  
    df = create_dataframe(base_path, annotation_file)

    
    df = add_image_info(df)

  
    get_statistics(df)

    max_width, max_height = 500, 500  
    filtered_df = filter_by_dimensions(df, max_width, max_height)
    print("Отфильтрованный DataFrame:")
    print(filtered_df)

    
    df = add_image_area(df)

    
    df = sort_by_area(df)

    plot_area_histogram(df)

    df.to_csv("output_dataframe.csv", index=False)
    print("DataFrame сохранен в файл 'output_dataframe.csv'")

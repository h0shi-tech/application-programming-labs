import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse
import os

def main(input_path, output_path, crop_width, crop_height):
    # 1. Чтение изображения
    image = cv2.imread(input_path)
    
    if image is None:
        print("Ошибка: невозможно загрузить изображение. Проверьте путь к файлу.")
        return

    # Вывод размера изображения
    height, width, channels = image.shape
    print(f"Размер изображения: {width}x{height} пикселей, Каналы: {channels}")

    # 2. Построение гистограммы
    plt.figure()
    colors = ('b', 'g', 'r')
    for i, color in enumerate(colors):
        hist = cv2.calcHist([image], [i], None, [256], [0, 256])
        plt.plot(hist, color=color)
        plt.xlim([0, 256])

    plt.title('Гистограмма изображения')
    plt.xlabel('Значение пикселей')
    plt.ylabel('Частота')
    plt.legend(['Blue', 'Green', 'Red'])
    plt.show()

    # 3. Обрезка изображения
    cropped_image = image[:crop_height, :crop_width]

    # Проверка, не превышают ли размеры обрезки исходные размеры
    if crop_width > width or crop_height > height:
        print("Предупреждение: заданные размеры обрезки превышают размеры исходного изображения. "
              "Изображение будет обрезано до максимального доступного размера.")

    # 4. Отображение исходного и обрезанного изображения
    plt.figure(figsize=(10, 5))
    
    # Исходное изображение
    plt.subplot(1, 2, 1)
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title("Исходное изображение")
    
    # Обрезанное изображение
    plt.subplot(1, 2, 2)
    plt.imshow(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
    plt.title("Обрезанное изображение")

    plt.show()

    # 5. Сохранение результата
    cv2.imwrite(output_path, cropped_image)
    print(f"Обрезанное изображение сохранено по пути: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Обрезка изображения и построение гистограммы.")
    parser.add_argument("input_path", type=str, help="Путь к входному изображению")
    parser.add_argument("output_path", type=str, help="Путь для сохранения обрезанного изображения")
    parser.add_argument("crop_width", type=int, help="Ширина обрезанного изображения")
    parser.add_argument("crop_height", type=int, help="Высота обрезанного изображения")
    
    args = parser.parse_args()
    main(args.input_path, args.output_path, args.crop_width, args.crop_height)

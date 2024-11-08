# Импорт необходимых модулей и классов
import os  # Для работы с файловой системой 
import csv  
import sys  # Для доступа к аргументам командной строки
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler 

# Класс для краулинга изображений по ключевому слову и источнику (По умолчанию гугл, но я юзал бинг ( ͡❛ ͜ʖ ͡❛))
class CatImageCrawler:
    def __init__(self, keyword, save_folder, annotation_file, num_images, source='google'):
        
        self.keyword = keyword  
        self.save_folder = save_folder  
        self.annotation_file = annotation_file  
        self.num_images = num_images  
        self.source = source  

    # Метод для выполнения краулинга изображений
    def crawl_images(self):
        # Создание папки для сохранения изображений, если её нет
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)

        # тут настройки краулеров либо для гугла либо для бинга
        if self.source == 'google':
            crawler = GoogleImageCrawler(storage={'root_dir': self.save_folder})  
        elif self.source == 'bing':
            crawler = BingImageCrawler(storage={'root_dir': self.save_folder})  
        else:
            raise ValueError("Invalid source. Choose 'google' or 'bing'.")  # Ошибка для неверного источника

        # Настройка и запуск краулинга изображений
        crawler.crawl(
            keyword=self.keyword,  
            max_num=self.num_images,  
            min_size=(200, 200),  
            filters={'type': 'photo'},  
            file_idx_offset='auto'  
        )

        # Запись аннотаций изображений в CSV
        self._write_annotation()

    # Метод для записи аннотаций изображений в CSV файл
    def _write_annotation(self):
        
        with open(self.annotation_file, mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['absolute_path', 'relative_path']  
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()  # Запись заголовка

            # Запись путей изображений в CSV
            for filename in os.listdir(self.save_folder):
                if filename.endswith(('.png', '.jpg', '.jpeg')):  # Проверка типа файла
                    absolute_path = os.path.abspath(os.path.join(self.save_folder, filename))  # Абсолютный путь
                    relative_path = os.path.join(self.save_folder, filename)  # Относительный путь
                    writer.writerow({'absolute_path': absolute_path, 'relative_path': relative_path})  # Запись строки в CSV

# Класс для создания итератора по изображениям, загруженным в указанную папку или CSV файл
class ImageIterator:
    def __init__(self, annotation_file=None, folder_path=None):
        self.images = []  # Список путей к изображениям
        if annotation_file:
            self._load_from_csv(annotation_file)  # Загрузка путей из CSV файла
        elif folder_path:
            self._load_from_folder(folder_path)  # Загрузка путей из папки
        self.index = 0  # Начальный индекс итерации

    # Загрузка путей изображений из CSV файла
    def _load_from_csv(self, annotation_file):
        with open(annotation_file, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            self.images = [row['absolute_path'] for row in reader]  # Чтение путей из CSV

    # Загрузка путей изображений из папки
    def _load_from_folder(self, folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith(('.png', '.jpg', '.jpeg')):  # Проверка типа файла
                self.images.append(os.path.join(folder_path, filename))  # Добавление пути в список

    # Инициализация итератора
    def __iter__(self):
        return self

    # Метод для перебора изображений по одному
    def __next__(self):
        if self.index < len(self.images):  # Проверка, не вышли ли за пределы списка
            image_path = self.images[self.index]  # Получение текущего пути к изображению
            self.index += 1  # Переход к следующему изображению
            return image_path  # Возврат текущего изображения
        else:
            raise StopIteration  # Завершение итерации, если все изображения пройдены

# Точка входа при запуске скрипта из командной строки
if __name__ == "__main__":
    # Проверка количества аргументов командной строки
    if len(sys.argv) not in (5, 6):
        print("Usage: python script.py <keyword> <save_folder> <annotation_file> <num_images> [source]")
        sys.exit(1)

    # Присвоение переменным значений из аргументов командной строки
    keyword = sys.argv[1]  
    save_folder = sys.argv[2]  
    annotation_file = sys.argv[3]  
    num_images = int(sys.argv[4])  
    source = sys.argv[5] if len(sys.argv) == 6 else 'google'  

    # Создание и запуск экземпляра краулера
    crawler = CatImageCrawler(keyword, save_folder, annotation_file, num_images, source)
    crawler.crawl_images()

    # Использование итератора для просмотра скачанных изображений
    print("Iterating over loaded images:")
    image_iterator = ImageIterator(annotation_file=annotation_file)
    for image_path in image_iterator:
        print(image_path)  # Вывод пути к каждому изображению

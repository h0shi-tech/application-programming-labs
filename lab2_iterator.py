from pathlib import Path

class DatasetIterator:
    def __init__(self, dataset_path):
        self.image_paths = list(Path(dataset_path).glob("*.jpg"))  # Ищем все JPG-изображения
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.image_paths):
            raise StopIteration
        image_path = self.image_paths[self.index]
        self.index += 1
        return image_path

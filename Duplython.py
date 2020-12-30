import time
import os
import shutil
from hashlib import sha256

class Duplython:
    def __init__(self):
        self.home_dir = os.getcwd(); self.File_hashes = []
        self.Cleaned_dirs = []; self.Total_bytes_saved = 0
        self.block_size = 65536; self.count_cleaned = 0

    def welcome(self)->None:
        print('+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+')
        print('-')
        print('+ Скрипт для поиска и удаления дубликатов!')
        print('-')
        print('+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+\n')
        time.sleep(1)
        apply = input("После нажатия Enter, будет запущен процесс поиска файлов рядом со скриптом,\nа также поиск файлов в папках рядом со скриптом, а затем их удаление.\n\nТы согласен на данную операцию?")
        print('\nВ процессе поиска...')

    def generate_hash(self, Filename:str)->str:
        Filehash = sha256()
        try:
            with open(Filename, 'rb') as File:
                fileblock = File.read(self.block_size)
                while len(fileblock)>0:
                    Filehash.update(fileblock)
                    fileblock = File.read(self.block_size)
                Filehash = Filehash.hexdigest()
            return Filehash
        except:
            return False

    def clean(self)->None:
        all_dirs = [path[0] for path in os.walk('.')]
        for path in all_dirs:
            os.chdir(path)
            All_Files =[file for file in os.listdir() if os.path.isfile(file)]
            for file in All_Files:
                filehash = self.generate_hash(file)
                if not filehash in self.File_hashes:
                    if filehash:
                        self.File_hashes.append(filehash)
                        #print(file)
                else:
                    byte_saved = os.path.getsize(file); self.count_cleaned+=1
                    self.Total_bytes_saved+=byte_saved
                    os.remove(file); filename = file.split('/')[-1]
                    print(filename, '- УДАЛЁН!')
            os.chdir(self.home_dir)

    def cleaning_summary(self)->None:
        mb_saved = self.Total_bytes_saved/1048576
        mb_saved = round(mb_saved, 2)
        print('\n\n')
        print('+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+')
        print('Удалено файлов: ', self.count_cleaned)
        print('Сохранено места на диске: ', mb_saved, 'МБ')
        print('+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+')
        print('\n\n')
        apply = input("Работа завершена.")

    def main(self)->None:
        self.welcome();self.clean();self.cleaning_summary()

if __name__ == '__main__':
    App = Duplython()
    App.main()

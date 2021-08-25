import cv2 as cv
import numpy as np
import os

#список со всеми расширениями картинок
exts = ['jpg', 'png', 'bmp', 'ai', 'psd', 'ico', 'jpeg', 'ps', 'svg', 'tif', 'tiff']


def blur(img, power):
    #читаем файл
    img = cv.imread('input\\' + img)

    #находим лицо, используя стандартный шаблон
    has = cv.CascadeClassifier(cv.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = has.detectMultiScale(img, 1.3, 5)

    for (x, y, w, h) in faces:
        #получаем координаты лица с добавлением большей области покрытия 
        face = img[y - 20: y + h + 50, x - 20: x + w + 50]

        #блюрим лицо
        face = cv.blur(face,(power,power))

        #заменяем лицо на картинке заблюриным аналогом 
        img[y - 20: y + h + 50, x - 20: x + w + 50] = face

    #получаем файлы из папки 'output'
    files = os.listdir(path + "\\output")

    #проверяем на наличие повторения файлов и изменяем название в случае повторения
    number = 0

    for i in files:

        name = i.split('.')[0]

        try:
            number = int(name) + 1
        except:
            continue
    
    #записываем файл
    cv.imwrite(f'output\\{str(number)}.png', img)

#проверяем наличие папок и в случае их отсутствия создаем их
def make(path):
    try:
        os.mkdir(path + '\\output')

    except:
        pass

    try:
        os.mkdir(path + '\\input')
        #если папка не существует то возвращаем 'False'
        return False

    except:
        #если папка существует то возвращаем 'True'
        return True


def main(path, power):
    #стандартное значение для проверки
    done = False

    #проверяем является ли переменная 'power' числом и если не является то выставляем стандартное значение
    try:
        power = int(power)

    except:
        power = 7

    #в opencv значение не должно быть меньше еденицы , так что этот участок кода нормализует значение
    if power < 1:
        power = 1
    
    #почему то при установки значения 10 вылетает ошибка , так что это тоже нормализация
    elif power == 10:
        power = 11

    #получаем файлы папки 'input'
    files = os.listdir(path + "\\input")

    #получаем расширения файлов
    for i in files:

        ext = i.split('.')[-1]


        #если расширение есть в списке то запускаем функцию блюр и ставим done в значение 'True' для прохождения проверки
        if ext in exts:
            blur(i, power)
            done = True

    #выдаем ошибку при провале проверки 
    if not done:
        raise NameError("You didn't put a photo in 'input' folder")


if __name__ == '__main__':
    #получаем путь до скрипта
    path = os.path.abspath(os.getcwd())

    #выбираем значение блюра
    print("ВАЖНО!!! Названия файлов должны быть исключительно на английском!\n\n")
    power = input("Choose how powerfull will be the blur (standart number is 7): ")

    #проверяем на наличие папок и если есть таковые , то запускаем main иначе создаем папки и выдаем ошибку 
    if make(path):
        main(path, power)

    #выдаем ошибку при провале проверки 
    else:
        raise NameError("You didn't had necessary folders")
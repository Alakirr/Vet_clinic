from fastapi import FastAPI
from enum import Enum
from pydantic import BaseModel

app = FastAPI(title='Ветеринарная клиника',
              description='Данное приложение предоставляет несколько возможностей'
                          'по работе с данными ветеринарной клиники. '
                          'Вы можете хранить, добавлять и выводить данные.')

class DogType(str, Enum):
    terrier = 'terrier'
    bulldog = 'bulldog'
    dalmatian = 'dalmatian'

class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType

class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}


post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root():
    return 'Welcome to our Vet clinic!'


@app.post('/', summary='Show information about table post_db')
def get_post():
    '''
    Функция не имеет аргументов,
    на выходе выдает информацию по таблице post_db
    :return:
    '''
    return post_db


@app.get('/get_dog/', summary='Show information about dogs by their type')
def get_dog(kind:DogType='--') -> dict:
    '''
    Функция на вход принимает значение в формате string,
    которое пользователь может выбрать из выпадающего списка,
    сформированного на базе класса Dogtype.
    Функция выводит словарь c информацией по собакам,
    которая соответствует условию или выводит всех собак
    при выборе аргумента kind с дефолтным значением
    :param kind: Dogtype
    :return: result (dict)
    '''

    if kind == '--':
        return dogs_db

    result = {}
    for key, value in dogs_db.items():
        if kind == dogs_db[key].kind:
            result[key] = value

    return result


@app.post('/create_dog', summary='Create a new dog')
def create_dog(new_dog:Dog):
    '''
    Функция на вход принимает словарь,
    где хранятся данные по новой собаке,
    которые затем сохраняются в таблице dogs_db.
    Функция возвращает информацию по новой собаке
    :param new_dog: Dog
    :return:dogs_db[new_dog.pk]
    '''
    dogs_db[new_dog.pk] = new_dog
    return dogs_db[new_dog.pk]


@app.get('/get_dog_by_pk/{pk}', summary='Show information about dog by pk')
def get_dog_by_pk(pk: int):
    '''
    Функция на вход принимает pk (id собаки)
    и выводит информацию по данной собаке
    в формате словаря
    :param pk: int
    :return: dogs_db[pk]
    '''
    return dogs_db[pk]


@app.patch('/update_dog{pk}', summary='Update information about dog')
def update_dog(pk: int, dog:Dog):
    '''
    Функция на вход принимает pk (id собаки),
    по которой нужно будет вносить изменения, а также
    словарь с данными, которые необходимо поменять.
    На выходе функция возвращает словарь
    с измененными данными по одной собаке
    :param pk: int
    :param dog: Dog
    :return: dogs_db[pk]
    '''
    dogs_db[pk] = dog
    return dogs_db[pk]

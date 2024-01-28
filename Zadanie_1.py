
import os
import datetime
from functools import wraps

path = 'main.log'

def write_data(data1,path):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(data1)
def call_func(arg,kwa,func_name,time_start,result,time_run):
    if len(arg) == 0 and len(kwa) == 0:
        data = f'Функция {func_name} вызвана: {time_start} с пустыми аргументами, и возвращает: {result}. Время выполнения: {time_run} \n'
    elif len(arg) == 0:
        data = f'Функция {func_name} вызвана: {time_start} c аргументами: {kwa}, и возвращает: {result}. Время выполнения: {time_run} \n'
    elif len(kwa) == 0:
        data = f'Функция {func_name} вызвана: {time_start} c аргументами: {arg}, и возвращает: {result}. Время выполнения: {time_run} \n'
    else:
        data = f'Функция {func_name} вызвана: {time_start} c аргументами: {arg}{kwa}, и возвращает: {result}. Время выполнения: {time_run} \n'
    return data

def logger(old_function):
    time_start = datetime.datetime.now()

    def new_function1(*args, **kwargs):

        result = old_function(*args, **kwargs)
        time_end  = datetime.datetime.now()
        time_run = time_end - time_start
        data = call_func(args,kwargs,old_function.__name__,time_start,result,time_run)
        print(result)
        write_data(data, path)
        return result

    return new_function1





def test_1():

    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'



#Задание 2
def logger2(path):


    def __logger(old_function):
        time_start = datetime.datetime.now()
        @wraps(old_function)
        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            data = call_func(args, kwargs, old_function.__name__, time_start, result)
            write_data(data, path)
            return result
        return new_function

    return __logger


def test_2():
    paths2 = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths2:
        if os.path.exists(path):
            os.remove(path)

        @logger2(path)
        def hello_world():
            return 'Hello World'

        @logger2(path)
        def summator(a, b=0):
            return a + b

        @logger2(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths2:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()
    test_2()
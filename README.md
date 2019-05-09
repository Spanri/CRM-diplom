# СЭД МТУСИ

> Vue.js/Django проект

## Построение

### Фронтенд, Vue.js

Не забудьте установить npm!

``` bash
# перейти в папку с фронтендом
cd frontend

# установить зависимости
npm install

# запустить с горячей перезагрузкой localhost:8080
npm run dev

# построить для продакшена с минификацией
npm run build

# построить для продакшена и посмотреть bundle analyzer report
npm run build --report
```

### Бекенд, Django

Не забудьте установить python!

``` bash
# установить зависимости
pip3 install -r requirements.txt

# Миграция таблиц
python manage.py migrate

# В командной строке указать password smtp сервера (вместо
# password подставить пароль, он есть у разработчика приложения).
# Вроде бы это не перманентно делается, я не поняла, но иначе не
# работает
set edms-mtuci-password=password

# Завести суперюзера (email любой, он не проверяется)
python manage.py createsuperuser

# запустить
python manage.py runserver

# зайти в администратора (данные суперюзера)
http://localhost:8000/api/admin/login/?next=/api/admin/
```

## Другие штуки

[Документация](http://edms-mtuci.herokuapp.ru/docs "edms-mtuci.herokuapp.ru/docs") 
ссылка пока что не работает, но пусть будет, использовать [эту ссылку](http://localhost:8000/docs/), когда сервер запущен

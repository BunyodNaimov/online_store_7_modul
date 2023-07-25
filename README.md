# Онлайн магазин

## Добро пожаловать в проект [Minbar-uz-clone](https://bunyodadmin.pythonanywhere.com/swagger/) этот проект является копией сайта [minbar.uz](https://www.minbar.uz/)
# Обзор проекта

Онлайн магазин - это веб-приложение для онлайн-торговли, написанное на Python с использованием Django. Это приложение позволяет пользователям просматривать список товаров, добавлять их в корзину, оформлять заказы и получать уведомления о состоянии заказа.

# Установка

Чтобы запустить этот проект на своем локальном компьютере, выполните следующие шаги:

Установите Django, выполнив следующую команду:
```stylus
pip install django
```

Клонируйте репозиторий проекта:
```stylus
git clone https://github.com/BunyodNaimov/online_store_new.git
```

Перейдите в директорию проекта:
```stylus
cd online_store_new
```
Создайте виртуальное окружение:
```stylus
python -m venv env
```

Активируйте виртуальное окружение:
```stylus
source env/bin/activate
```
Установите необходимые пакеты:
```stylus
pip install -r requirements.txt
```

Запустите сервер:
```stylus
python manage.py runserver
```

Перейдите на веб-сайт по адресу ```stylus http://127.0.0.1:8000/``` в вашем браузере.

# Структура проекта

Проект имеет следующую структуру директорий:

```stylus
online_store_new/
├── cart/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── context_processors.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── categories/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── orders/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── products/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── users/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── backends.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── env
├── LICENSE
├── manage.py
├── README.md
└── requirements.txt
```
В проекте есть несколько приложений, таких как cart, categories, orders, products, и users. Каждое приложение имеет свой собственный файл models.py для моделей, файл views.py для представлений и файл urls.py для маршрутов. В config находятся файлы, связанные с настройками проекта, такие как settings.py, urls.py и т.д.

# Как использовать

## Приложение имеет следующие функции:

Просмотр товаров: на главной странице отображаются все доступные товары в виде карточек, которые содержат изображение, название, описание и цену.
Добавление товаров в корзину: пользователи могут добавлять товары в корзину со страницы товара или со страницы категории.
Оформление заказа: пользователи могут оформлять заказы, выбрав нужные товары из корзины и заполнив форму заказа.
Получение уведомлений о состоянии заказа: пользователи получают уведомления на электронную почту о состоянии своих заказов.

## Cart
![image](https://github.com/BunyodNaimov/online_store_new/assets/122611882/661a2ee4-2482-4624-88f2-9af352df4a1c)

```GET /cart/``` - Эта точка API может использоваться для получения корзины покупок пользователя.

```POST /cart/add-to-cart/{product_id}``` - Эта точка API может использоваться для добавления товара в корзину покупок пользователя.

```POST /cart/remove-from-cart/{product_id}``` - Эта точка API может использоваться для удаления товара из корзины покупок пользователя.

## Categories
![image](https://github.com/BunyodNaimov/online_store_new/assets/122611882/64da5f06-a87b-44b0-a1e8-fe0aecb80a1d)

```GET /categories/``` - Эта точка API может использоваться для получения списка всех категорий.

```POST /categories/``` - Эта точка API может использоваться для создания новой категории.

```GET /categories/{id}/``` - Эта точка API может использоваться для получения информации о конкретной категории.

```PUT /categories/{id}/``` - Эта точка API может использоваться для обновления информации о конкретной категории.

```DELETE /categories/{id}/``` - Эта точка API может использоваться для удаления конкретной категории.

## Orders
![image](https://github.com/BunyodNaimov/online_store_new/assets/122611882/47f7eb37-92ff-484e-91d0-642e036cee44)

```GET /orders/``` - Эта точка API может использоваться для получения списка всех заказов.

```POST /orders/``` - Эта точка API может использоваться для создания нового заказа.

## Products
![image](https://github.com/BunyodNaimov/online_store_new/assets/122611882/f8c163f3-cb3b-4176-a36b-2d1e2a684cc7)

```GET /products/``` - Точка API для получения списка всех продуктов.

```POST /products/``` - Точка API для создания нового продукта.

```GET /products/{id}/``` - Точка API для получения информации о конкретном продукте.

```PUT /products/{id}/``` - Точка API для обновления информации о конкретном продукте.

```DELETE /products/{id}/``` - Точка API для удаления конкретного продукта.

## Users
![image](https://github.com/BunyodNaimov/online_store_new/assets/122611882/c91662a0-7c13-44c5-a93b-b9ab16bd1086)

```POST /users/login/``` - Эта точка API может использоваться для входа в систему пользователя.

```POST /users/phone/check-verification-code/``` - Эта точка API может использоваться для проверки кода подтверждения телефона.

```POST /users/phone/phone-login/``` - Эта точка API может использоваться для входа в систему пользователя с использованием номера телефона.

```POST /users/phone/phone-register/``` - Эта точка API может использоваться для регистрации нового пользователя с использованием номера телефона.

```POST /users/phone/send-verification-code/``` - Эта точка API может использоваться для отправки кода подтверждения телефона.

```POST /users/register/``` - Эта точка API может использоваться для регистрации нового пользователя.

# api_for_User_AbstractUser

    git clone https://github.com/Foxfix/api_for_User_AbstractUser.git
    cd api_for_User_AbstractUser/
    pip install -r requirements.txt
    python manage.py runserver
    python manage.py migrate
    python manage.py createsuperuser
    
    http://127.0.0.1:8000/api/register/    регистрация клиента
    http://127.0.0.1:8000/api/login/       вход 
    http://127.0.0.1:8000/api/id/          личные данные клиента по id (доступны только владельцу
    http://127.0.0.1:8000/api/             список клиентов. Доступен только админу.           
    
Поля first_name,last_name, email, passport_number  обязательны при регистрации.
Когда пользователь создает учетную запись, он или она должны подтвердить личность.
Я использовала [JWT](http://getblimp.github.io/django-rest-framework-jwt) token
Токен генерится для каждого раза при входе. Без него доступ к информации закрыт.
    
Тестим помощью cURL.

    curl -X GET http://127.0.0.1:8000/api/  
    {"detail":"Authentication credentials were not provided."}
    
    Cписок клиентов доступен только админу

    Логинимся http://127.0.0.1:8000/api/login/  под админом, получаем токен
  ![api](http://ipic.su/img/img7/fs/joxi_screenshot_1492730176307.1492731933.png)
    
    Проверяем в терминале
    
    curl -H "Authorization: JWT <token>" http://127.0.0.1:8000/api/
    
    Получаем весь список клиентов. При этом, если запросим детали клиента по id
    
    curl -H "Authorization: JWT <token>" http://127.0.0.1:8000/api/1/ 
    {"detail":"You do not have permission to perform this action."}
    
    получим ограничение. К личной информации доступ есть только у владельца.
    Логинимся под клиетом (владельцем профиля) http://127.0.0.1:8000/api/login/
    Получаем токен.
    
    curl -H "Authorization: JWT <token>" http://127.0.0.1:8000/api/id_клиента/
    Получаем личную информацию по профилю клиента.
    {"first_name":"Norma","last_name":"Backer","email":"our@i.ua","balance":"0.0000","username":"norma","passport_number":"CK123478","accaunt":true}
    
    При этом запрос curl -H "Authorization: JWT <token>" http://127.0.0.1:8000/api/id_иного_клиента/
    Выдаст {"detail":"You do not have permission to perform this action."}
    т.к. доступ к личной информации других клиентов ограничен.
 
Сразу при регистрации пользователь создается не активным и ожидает одобрения админа.
В админ панели добавлены настройки для ограничения доступа к superuser и отдельным полям,
опция для подтверждения профиля.

 ![api](https://wmpics.pics/di-0V5T.png)
 
 
 Пользователь может изменять свои данные.
 
 ![api](http://ipic.su/img/img7/fs/joxi_screenshot_1492731538260.1492732173.png)
 
 Аккаунт стоит в положении True, пользователь может изменить на false, 
 тем самым поставив администратора в известность о закрытии профиля. Профиль может быть удален.
 
 ![api](https://wmpics.pics/di-YOUD.png) 
 
    Доп проверки для себя:
    http://127.0.0.1:8000/login/
    http://127.0.0.1:8000/logout/
    http://127.0.0.1:8000/register/
 
 В  [этом](https://github.com/Foxfix/api_client) приложении дополнительные поля для user были добавлены 
 иным способом, с использованием связи один-к-одному с пользовательской моделью. 

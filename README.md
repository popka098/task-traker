# task-traker
Попытка сделать работу над ошибками с хакатона

# Установка
Убедитесь что у вас установлены актуальные версии
- [Node.js](https://nodejs.org/en/)
- [Python3.12](https://www.python.org/)

После чего выполните следующие действия в коммандной строке:
```
git clone https://github.com/popka098/task-traker.git
cd task-traker
make install
```
Благодаря данным действиям проект будет готов к работе

# Запуск (разработка)
Перед запуском не забудьте подключиться к venv:
```
source fastapi-backend/.venv/bin/activate
```
Что бы запустить проект достаточно выполнить следующую комманду:
```
make dev
```
Вы сможете увидеть проект на следующих адрессах:
- vue - [http://localhost:5173/](http://localhost:5173/)
- fastapi - [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

Что бы отдельно друг от друга запусть vue и fastapi:\
Для fastapi
```
cd fastapi-backend
python main.py
```
Для vue
```
cd vue-frontend
npm run dev
```
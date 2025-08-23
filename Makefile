BACKEND_DIR=fastapi-backend
FRONTEND_DIR=vue-frontend

# Запуск одновременно fastapi и vue
dev:
	cd ${BACKEND_DIR} && python main.py & \
	cd ${FRONTEND_DIR} && npm run dev

# Остановка всех uvicorn и vite процессов
stop:
	killall -9 uvicorn || true
	killall -9 node || true

# Установка пакетов
install:
	# Создание виртуального окружения для FastAPI
	cd ${BACKEND_DIR} && [ -d .venv ] || python -m venv .venv
	# Установка python-пакетов
	cd ${BACKEND_DIR} && .venv/bin/pip install --upgrade pip && .venv/bin/pip install -r requirements.txt
	# Установка npm-пакетов
	cd ${FRONTEND_DIR} && npm install

# Создание миграции
migrate:
	cd ${BACKEND_DIR} && alembic revision --autogenerate -m "$(msg)"

# Применение миграции
upgrade:
	cd ${BACKEND_DIR} && alembic upgrade head

# Создание миграции + применение миграции
autoup:
	cd ${BACKEND_DIR} && alembic revision --autogenerate -m "$(msg)" && alembic upgrade head

# Запуск одновременно fastapi и vue
dev:
	cd fastapi-backend && python main.py & \
	cd vue-frontend && npm run dev

# Остановка всех uvicorn и vite процессов
stop:
	killall -9 uvicorn || true
	killall -9 node || true

# Установка пакетов
install:
	# Создание виртуального окружения для FastAPI
	cd fastapi-backend && [ -d .venv ] || python -m venv .venv
	# Установка python-пакетов
	cd fastapi-backend && .venv/bin/pip install --upgrade pip && .venv/bin/pip install -r requirements.txt
	# Установка npm-пакетов
	cd vue-frontend && npm install

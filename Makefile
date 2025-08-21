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
	# Установка python-пакетов для FastAPI
	cd fastapi-backend && python -m pip install -r requirements.txt
	# Установка npm-пакетов для Vue
	cd vue-frontend && npm install

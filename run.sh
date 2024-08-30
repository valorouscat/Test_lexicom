#!/bin/bash

# Получение пути к директории скрипта
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Переход в директорию скрипта
cd $SCRIPT_DIR

# Проверка наличия docker-compose.yml
if [ ! -f "docker-compose.yml" ]; then
  echo "Error: docker-compose.yml not found in $SCRIPT_DIR"
  exit 1
fi

# Функция для остановки docker-compose
function stop_docker_compose {
  echo "Stopping Docker Compose..."
  docker-compose down
  if [ $? -eq 0 ]; then
    echo "Docker Compose stopped successfully"
  else
    echo "Failed to stop Docker Compose"
  fi
  exit 0
}

# Перехват сигналов завершения процесса
trap stop_docker_compose SIGINT SIGTERM

# Запуск docker-compose
docker-compose up -d

# Проверка статуса запуска
if [ $? -eq 0 ]; then
  echo "Docker Compose started successfully"
else
  echo "Failed to start Docker Compose"
  exit 1
fi

# Бесконечный цикл, чтобы скрипт не завершался
while true; do
  sleep 1
done
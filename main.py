from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
import os

# Настройки сервера
HOST = "localhost"
PORT = 8080


class MyServer(BaseHTTPRequestHandler):
    """
    Класс для обработки входящих запросов.
    """

    def do_GET(self):
        """
        Обработка GET-запросов. Возвращает HTML-страницу контактов.
        """
        # Формируем путь к файлу (относительно main.py)
        file_path = os.path.join("templates", "contacts.html")

        # Проверяем, существует ли файл
        if os.path.exists(file_path):
            self.send_response(200)
            # ВАЖНО: возвращаем text/html, как требуют критерии
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            # ЧТЕНИЕ ФАЙЛА С ПОМОЩЬЮ КОНТЕКСТНОГО МЕНЕДЖЕРА (with open)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                self.wfile.write(content.encode("utf-8"))
        else:
            # Если файл не найден, возвращаем 404
            self.send_response(404)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write("404: Файл не найден".encode("utf-8"))

    def do_POST(self):
        """
        Обработка POST-запросов (отправка формы).
        """
        # Получаем длину тела запроса
        content_length = int(self.headers.get('Content-Length', 0))

        # Читаем тело запроса
        post_data = self.rfile.read(content_length).decode("utf-8")

        # Парсим данные (urlencoded -> словарь)
        parsed_data = parse_qs(post_data)

        # Выводим данные в консоль (критерий оценки)
        print("\n" + "=" * 50)
        print("📥 ПОЛУЧЕН POST-ЗАПРОС:")
        for key, value in parsed_data.items():
            print(f"   {key}: {value[0]}")
        print("=" * 50 + "\n")

        # После отправки формы возвращаем ту же страницу (или можно вернуть страницу "Спасибо")
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

        # Для простоты возвращаем страницу контактов снова
        file_path = os.path.join("templates", "contacts.html")
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            self.wfile.write(content.encode("utf-8"))


if __name__ == "__main__":
    # Инициализация сервера
    webServer = HTTPServer((HOST, PORT), MyServer)
    print(f"🚀 Сервер запущен: http://{HOST}:{PORT}")
    print("Нажмите Ctrl+C, чтобы остановить сервер.")

    try:
        # Запуск бесконечного цикла прослушивания
        webServer.serve_forever()
    except KeyboardInterrupt:
        # Корректная остановка
        pass

    webServer.server_close()
    print("\n🛑 Сервер остановлен.")

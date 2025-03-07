import http.server
import socketserver

# Порт, на котором будет работать сервер
PORT = 8000
hostName = "localhost" # Имя хоста

# Класс обработчика запросов
class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Читаем содержимое HTML-файла
        try:
            with open("web_site/contacts_page.html", "r", encoding="utf-8") as f:
                html_content = f.read()
        except FileNotFoundError:
            self.send_response(404)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>404 Not Found</h1></body></html>")
            return

        # Отправляем ответ с HTML-контентом
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        try:  # Добавляем try...except для BrokenPipeError
            self.wfile.write(html_content.encode("utf-8"))
        except BrokenPipeError:
            print("BrokenPipeError: Соединение с клиентом разорвано.") # Логируем ошибку (опционально)
            pass # Просто пропускаем ошибку

# Создаем обработчик TCP-соединений
Handler = MyHandler

if __name__ == "__main__":
    # Создаем TCP-сервер
    with socketserver.TCPServer((hostName, PORT), Handler) as httpd:
        print(f"Сервер запущен на http://{hostName}:{PORT}")  # Более понятное сообщение
        # Обрабатываем запросы до остановки сервера
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nСервер остановлен.")
            pass
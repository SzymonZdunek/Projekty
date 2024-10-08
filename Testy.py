pip uninstall pynput
pip install pynput

from pynput import keyboard

def on_press(key):
    try:
        print(f'Key pressed: {key.char}')  # Wyświetla klawisz wciśnięty przez użytkownika
    except AttributeError:
        print(f'Special key pressed: {key}')  # Wyświetla klawisz specjalny (np. enter, esc)

def on_release(key):
    if key == keyboard.Key.esc:  # Zatrzymuje nasłuchiwanie po naciśnięciu ESC
        return False

# Nasłuchiwanie klawiatury
with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

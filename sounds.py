from pygame import mixer


def fire():
    mixer.init()
    mixer.music.load("egg_fall/sounds/fire.mp3")
    mixer.music.play()


def catch():
    mixer.init()
    mixer.music.load("egg_fall/sounds/catch.mp3")
    mixer.music.play()


def miss():
    mixer.init()
    mixer.music.load("egg_fall/sounds/miss.mp3")
    mixer.music.play()


def main_theme():
    mixer.init()
    mixer.music.load("egg_fall/sounds/main_theme.mp3")
    mixer.music.play()


def survive_theme():
    mixer.init()
    mixer.music.load("egg_fall/sounds/survive_theme.mp3")
    mixer.music.play()


def time_theme():
    mixer.init()
    mixer.music.load("egg_fall/sounds/time_theme.mp3")
    mixer.music.play()
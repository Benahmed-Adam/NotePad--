import pygame as pg
import sys
import os
import json
from ui import TextZone, Button, CheckBox

def get_luminance(color: pg.Color) -> float:
    r, g, b = color[:3]
    return 0.299 * r + 0.587 * g + 0.114 * b


class Menu:
    def __init__(self, main):
        self.main = main

    def _handle_resize(self, event):
        self.main.resize(event.w, event.h, None)

    def _draw_message(self, message: str, y_offset: int = 140, color=(255, 255, 0)):
        if message:
            font = pg.font.SysFont("arial", 24)
            txt = font.render(message, True, color)
            x = self.main.screen_size[0] // 2 - 200
            y = self.main.screen_size[1] // 2 + y_offset
            self.main.window.blit(txt, (x, y))

    def save_interface(self):
        screen_w, screen_h = self.main.screen_size
        text_zone = TextZone("Filename...", (400, 50), 30, (screen_w // 2 - 200, screen_h // 2 - 100), 30, [str], "Nom : ")
        text_zone.text = self.main.filename
        save_button = Button("Save", (200, 50), 30, (screen_w // 2, screen_h // 2))
        cancel_button = Button("No.", (200, 50), 30, (screen_w // 2, screen_h // 2 + 70))

        running = True
        message = ""

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.main.running = False
                    sys.exit()
                elif event.type == pg.VIDEORESIZE:
                    self._handle_resize(event)
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    running = False

                text_zone.event(event)
                save_button.event(event)
                cancel_button.event(event)

            if save_button.is_clicked:
                filename = text_zone.get()

                try:
                    with open(filename, "w", encoding="utf-8") as f:
                        f.write(self.main.text_engine.text)
                    message = f"Sauvegardé dans '{filename}'"
                except Exception as e:
                    message = f"Erreur : {e}"
                save_button.is_clicked = False

            if cancel_button.is_clicked:
                running = False

            self.main.window.fill((30, 30, 30))
            text_zone.draw(self.main.window)
            save_button.draw(self.main.window)
            cancel_button.draw(self.main.window)
            self._draw_message(message)
            pg.display.flip()
            self.main.clock.tick(60)

    def load_interface(self):
        screen_w, screen_h = self.main.screen_size
        text_zone = TextZone("Nom du fichier...", (400, 50), 30, (screen_w // 2 - 200, screen_h // 2 - 100), 30, [str], "Nom : ")
        load_button = Button("Charger", (200, 50), 30, (screen_w // 2, screen_h // 2))
        cancel_button = Button("Annuler", (200, 50), 30, (screen_w // 2, screen_h // 2 + 70))

        running = True
        message = ""

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.main.running = False
                    sys.exit()
                elif event.type == pg.VIDEORESIZE:
                    self._handle_resize(event)
                elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    running = False

                text_zone.event(event)
                load_button.event(event)
                cancel_button.event(event)

            if load_button.is_clicked:
                filename = text_zone.get()

                try:
                    with open(filename, "r", encoding="utf-8") as f:
                        self.main.text_engine.text = f.read()
                    message = f"Fichier '{filename}' chargé !"
                    self.main.filename = filename
                except Exception as e:
                    message = f"Erreur : {e}"
                load_button.is_clicked = False

            if cancel_button.is_clicked:
                running = False

            self.main.window.fill((30, 30, 30))
            text_zone.draw(self.main.window)
            load_button.draw(self.main.window)
            cancel_button.draw(self.main.window)
            self._draw_message(message)
            pg.display.flip()
            self.main.clock.tick(60)

    def settings(self):

        elements: list[CheckBox] = []
        spacing = 50
        size = (30, 30)
        start_x, start_y = 200, 100
        column_width = 350
        screen_w, screen_h = self.main.screen_size
        max_height = screen_h - 300
        x, y = start_x, start_y

        options = [
            ("Play music ? :", self.main.play_music),
            ("Popups ? :", self.main.ads),
            ("Can shake ? :", self.main.text_engine.can_shake)
        ]

        options += [
            (f"{effect} ? :", self.main.text_engine.has_effect(effect))
            for effect in self.main.text_engine.effects.available_effects
        ]

        for label, value in options:
            elements.append(CheckBox((x, y), size, label, value))
            y += spacing
            if y > max_height:
                y = start_y
                x += column_width

        right_x = x + column_width
        font_zone = TextZone("Example : couriernew", (500, 50), 30, (right_x, y), 30, [str], "Font : ")
        font_zone.text = self.main.text_engine.font_name
        y += spacing + 50

        background_zone = TextZone("Example : background.jpg", (500, 50), 30, (right_x, y), 30, [str], "Background image : ")
        background_zone.text = self.main.settings["background"]
        y += spacing + 50

        valider_button = Button("Save", (200, 50), 30, (screen_w // 2, screen_h - screen_h // 8))
        leave_button = Button("Leave", (200, 50), 30, (screen_w // 2, screen_h - screen_h // 20))

        error_message = ""

        while self.main.running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.main.running = False
                    sys.exit()
                elif event.type == pg.VIDEORESIZE:
                    self._handle_resize(event)

                for checkbox in elements:
                    checkbox.update(event)
                font_zone.event(event)
                background_zone.event(event)
                valider_button.event(event)
                leave_button.event(event)

            if valider_button.is_clicked:
                error_message = ""
                valid = True

                font_name = font_zone.get().lower()
                background_file = background_zone.get()
                font_exists = font_name in pg.font.get_fonts()

                if not font_exists:
                    error_message += f"Police invalide : '{font_name}'.\n"
                    valid = False

                if background_file:
                    full_path = os.path.join(self.main.media_folder, background_file)
                    if not os.path.isfile(full_path):
                        error_message += f"Image introuvable : '{full_path}'.\n"
                        valid = False
                    elif not background_file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                        error_message += f"Format non pris en charge : '{background_file}'.\n"
                        valid = False

                if valid:
                    self.main.play_music = elements[0].value
                    self.main.ads = elements[1].value
                    self.main.text_engine.can_shake = elements[2].value

                    for i, effect in enumerate(self.main.text_engine.effects.available_effects):
                        checkbox_value = elements[3 + i].value
                        if checkbox_value:
                            self.main.text_engine.add_effect(effect)
                        else:
                            self.main.text_engine.remove_effect(effect)

                    self.main.text_engine.font = pg.font.SysFont(font_name, self.main.text_engine.font_size)
                    self.main.text_engine.font.set_bold(True)
                    self.main.text_engine.font_name = font_name

                    if background_file:
                        self.main.text_engine.background = background_file
                        image_path = os.path.join(self.main.media_folder, background_file)
                        self.main.text_engine.background_image = pg.transform.smoothscale(pg.image.load(image_path), self.main.screen_size)
                        avg_color = pg.transform.average_color(self.main.text_engine.background_image)
                        lum = get_luminance(avg_color)
                        color = (0, 0, 0) if lum > 128 else (255, 255, 255)
                    else:
                        self.main.text_engine.background_image = None
                        self.main.text_engine.background = None
                        color = (255, 255, 255)

                    self.main.text_engine.text_color = color
                    self.main.text_engine.cursor.color = color

                    self.main.settings.update({
                        "play_music": self.main.play_music,
                        "ads": self.main.ads,
                        "can_shake": self.main.text_engine.can_shake,
                        "effects": self.main.text_engine.active_effects,
                        "font": font_name,
                        "background": background_file
                    })

                    with open("settings.json", "w", encoding="utf-8") as f:
                        json.dump(self.main.settings, f, indent=4, ensure_ascii=False)

                valider_button.is_clicked = False

            if leave_button.is_clicked:
                return

            self.main.window.fill((30, 30, 30))
            for checkbox in elements:
                checkbox.draw(self.main.window)

            font_zone.draw(self.main.window)
            background_zone.draw(self.main.window)
            valider_button.draw(self.main.window)
            leave_button.draw(self.main.window)

            if error_message:
                font = pg.font.SysFont("arial", 20)
                for i, line in enumerate(error_message.splitlines()):
                    if line:
                        txt = font.render(line, True, (255, 50, 50))
                        self.main.window.blit(txt, (50, self.main.screen_size[1] - 100 + i * 25))

            pg.display.flip()
            self.main.clock.tick(60)

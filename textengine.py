import pygame as pg
import string
import pyperclip
import random
from effects import Effects

class Cursor:
    def __init__(self, text_engine: 'TextEngine'):
        self.x = 0
        self.y = 0
        self.text_engine = text_engine
        self.visible = True
        self.blink_timer = 0
        self.color = (255, 255, 255)

    def update(self, event: pg.event.Event):
        lines = self.text_engine.get_lines()

        if event.type != pg.KEYDOWN:
            return

        if event.key == pg.K_UP and self.y > 0:
            self.y -= 1
        elif event.key == pg.K_DOWN and self.y < len(lines) - 1:
            self.y += 1
        elif event.key == pg.K_LEFT:
            if self.x > 0:
                self.x -= 1
            elif self.y > 0:
                self.y -= 1
                self.x = len(lines[self.y])
        elif event.key == pg.K_RIGHT:
            if self.x < len(lines[self.y]):
                self.x += 1
            elif self.y < len(lines) - 1:
                self.y += 1
                self.x = 0

        self.x = min(self.x, len(lines[self.y]))

    def insert_char(self, char: str):
        lines = self.text_engine.get_lines()
        line = lines[self.y]
        lines[self.y] = line[:self.x] + char + line[self.x:]
        self.text_engine.set_text('\n'.join(lines))
        self.x += 1

    def backspace(self):
        lines = self.text_engine.get_lines()
        if self.x > 0:
            line = lines[self.y]
            lines[self.y] = line[:self.x - 1] + line[self.x:]
            self.x -= 1
        elif self.y > 0:
            previous_len = len(lines[self.y - 1])
            lines[self.y - 1] += lines[self.y]
            del lines[self.y]
            self.y -= 1
            self.x = previous_len
        self.text_engine.set_text('\n'.join(lines))

    def return_key(self):
        lines = self.text_engine.get_lines()
        before, after = lines[self.y][:self.x], lines[self.y][self.x:]
        lines[self.y] = before
        lines.insert(self.y + 1, after)
        self.text_engine.set_text('\n'.join(lines))
        self.y += 1
        self.x = 0

    def draw(self, surface: pg.Surface, font: pg.font.Font, font_size: int):
        lines = self.text_engine.get_lines()
        if self.y >= len(lines):
            return

        self.blink_timer = (self.blink_timer + 1) % 20
        self.visible = self.blink_timer < 10

        if not self.visible:
            return

        cursor_x = self.text_engine.view[0]
        line = lines[self.y]

        for i in range(self.x):
            char_surface = font.render(line[i], True, (255, 255, 255))
            cursor_x += char_surface.get_width()

        cursor_y = self.text_engine.view[1] + self.y * font_size

        pg.draw.rect(surface, self.color, (cursor_x, cursor_y, 2, font_size))



class TextEngine:
    def __init__(self, main, font_name: str):
        self.main = main
        self.font_name = font_name
        self.font_size = 36
        self.font = pg.font.SysFont(font_name, self.font_size)
        self.font.set_bold(True)

        self.screen = pg.Surface(self.main.screen_size)
        self.text = ""
        self.view = [10.0, 10.0]
        self.cursor = Cursor(self)
        self.text_color = (255, 255, 255)

        self.effects = Effects(self.screen.get_size(), 60)
        self.active_effects = []
        self.can_shake = False
        self.shake_timer = 0

        self.background = None
        self.background_image = None

        self.dragging = False
        self.drag_start_pos = None
        self.original_view = self.view.copy()

        self.explosion_sound = pg.mixer.Sound(self.main.media_folder + "explosion.wav")
        self.explosion_sound.set_volume(0.5)

    def add_effect(self, effect: str):
        if effect not in self.effects.available_effects:
            raise ValueError(f"L'effet '{effect}' n'existe pas.")
        if effect not in self.active_effects:
            self.active_effects.append(effect)
        return self

    def remove_effect(self, effect: str):
        if effect in self.active_effects:
            self.active_effects.remove(effect)
        return self

    def reset_view(self):
        self.view = [10.0, 10.0]
        self.cursor.x = 0
        self.cursor.y = 0

    def has_effect(self, effect: str) -> bool:
        return effect in self.active_effects

    def handle_inputs(self, event: pg.event.Event):
        if event.type == pg.KEYDOWN:
            keys = pg.key.get_pressed()

            if self.can_shake:
                self.add_effect("shake")
                self.explosion_sound.play()

            if event.key == pg.K_c and (keys[pg.K_LCTRL] or keys[pg.K_RCTRL]):
                pyperclip.copy(self.text)
            elif event.key == pg.K_v and (keys[pg.K_LCTRL] or keys[pg.K_RCTRL]):
                for char in pyperclip.paste():
                    self.cursor.return_key() if char == "\n" else self.cursor.insert_char(char)
            elif event.key == pg.K_BACKSPACE:
                self.cursor.backspace()
            elif event.key == pg.K_RETURN:
                self.cursor.return_key()
            elif event.key == pg.K_TAB:
                for _ in range(5):
                    self.cursor.insert_char(' ')
            elif event.unicode in (string.printable + "éèàçµ$£¤%€") and event.unicode != "":
                self.cursor.insert_char(event.unicode)

            self.shake_timer = 0
        elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            self.dragging = True
            self.drag_start_pos = event.pos
            self.original_view = self.view.copy()

        elif event.type == pg.MOUSEMOTION and self.dragging:
            dx, dy = event.pos[0] - self.drag_start_pos[0], event.pos[1] - self.drag_start_pos[1]
            self.view[0] = self.original_view[0] + dx
            self.view[1] = self.original_view[1] + dy

        elif event.type == pg.MOUSEWHEEL:
            if (self.font_size > 16 or event.y > 0) and (self.font_size < 500 or event.y < 0):
                self.font_size = max(16, self.font_size + event.y * 10)
                self.font = pg.font.SysFont(self.font_name, self.font_size)
                self.font.set_bold(True)

        elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False

    def get_view(self):
        return self.view

    def get_lines(self):
        return self.text.split('\n')

    def set_text(self, new_text: str):
        self.text = new_text

    def update(self, event: pg.event.Event):
        self.handle_inputs(event)
        self.cursor.update(event)

    def render(self):
        self.screen.fill((30, 30, 30))
        if self.background:
            self.screen.blit(self.background_image, (0, 0))

        screen_width, screen_height = self.screen.get_size()
        view_x, view_y = self.view

        lines = self.get_lines()
        font_height = self.font_size

        start_line = max(0, int(-view_y // font_height))
        end_line = min(len(lines), int((screen_height - view_y) // font_height) + 1)

        y_offset = view_y + start_line * font_height
        for y in range(start_line, end_line):
            line = lines[y]
            x_offset = view_x
            for char in line:
                char_surface = self.font.render(char, True, self.text_color)
                char_width = char_surface.get_width()

                if x_offset + char_width < 0:
                    x_offset += char_width
                    continue
                if x_offset > screen_width:
                    break

                if self.has_effect("rotate"):
                    char_surface = self.effects.rotate(char_surface)

                self.screen.blit(char_surface, (x_offset, y_offset))
                x_offset += char_width

            y_offset += font_height

        self.cursor.draw(self.screen, self.font, self.font_size)


    def draw(self, window: pg.Surface):
        self.render()
        if self.has_effect("particles"):
            self.effects.update_particles(self.screen)

        final = self.screen.copy()
        offset_x, offset_y = 0, 0
        self.effects.cc  = (self.effects.cc + 0.5) % 200_000
        self.effects.rotation = (self.effects.rotation + 1) % 360
        for effect in self.active_effects[:]:
            if effect == "shake":
                duration, amplitude = 60, 15
                if self.shake_timer < duration:
                    amp = int(amplitude * (1 - self.shake_timer / duration))
                    offset_x += random.randint(-amp, amp)
                    offset_y += random.randint(-amp, amp)
                    self.shake_timer += 1
                else:
                    self.remove_effect("shake")
                    self.shake_timer = 0
            elif effect == "scanlines":
                final = self.effects.scanlines(final)
            elif effect == "chromatic":
                final = self.effects.chromatic_aberration(final)
            elif effect == "gradient":
                final = self.effects.animated_gradient_overlay(final)
            elif effect == "glitch":
                final = self.effects.glitch(final)
            elif effect == "noise":
                final = self.effects.noise_overlay(final)
            elif effect == "wave":
                final = self.effects.wave_distortion(final)
            elif effect == "blur":
                final = self.effects.blur(final)

        window.blit(final, (offset_x, offset_y))

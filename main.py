import os
import sys
import threading
import time
import random
import json
import pygame as pg
from pyvidplayer2 import Video
from textengine import TextEngine
from menu import Menu
from popup import Popup

def get_luminance(color: pg.Color) -> float:
    r, g, b = color[:3]
    return 0.299 * r + 0.587 * g + 0.114 * b

class Main:
    def __init__(self, screen_size: tuple[int, int]):
        self.screen_size = [screen_size[0] + 20, screen_size[1] + 20]
        self.window = pg.display.set_mode(self.screen_size, pg.RESIZABLE)
        self.clock = pg.time.Clock()
        pg.display.set_caption("NotePad--")

        with open("settings.json", "r", encoding="utf-8") as f:
            self.settings: dict = json.load(f)

        self.music_playing = False
        self.ads = self.settings.get("ads", False)
        self.play_music = self.settings.get("play_music", False)
        self.media_folder = self.settings.get("media_folder", "")

        font_name = self.settings.get("font", "")
        if font_name not in pg.font.get_fonts():
            print(f"La police '{font_name}' n'existe pas.\nPolices disponibles : {pg.font.get_fonts()}")
            sys.exit(-1)

        self.text_engine = TextEngine(self, font_name)
        self.text_engine.can_shake = self.settings.get("can_shake", False)

        for effect in self.settings.get("effects", []):
            self.text_engine.add_effect(effect)

        self.running = True
        self.text_engine.background = self.settings.get("background", "")
        if self.text_engine.background:
            bg_path = os.path.join(self.media_folder, self.text_engine.background)
            self.text_engine.background_image = pg.image.load(bg_path)
            luminance = get_luminance(pg.transform.average_color(self.text_engine.background_image))
            color = (0, 0, 0) if luminance > 128 else (255, 255, 255)
            self.text_engine.text_color = color
            self.text_engine.cursor.color = color

        videos_path = os.path.join(self.media_folder, "videos")
        self.videos = [f for f in os.listdir(videos_path) if f.endswith(".mp4")]
        self.popups: list[Popup] = []
        threading.Thread(target=self._popups_thread, daemon=True).start()

        self.filename = "Sans titre"

        self.menus = Menu(self)
        self.resize(*self.screen_size, None)

    def _popups_thread(self):
        while self.running:
            time.sleep(0.1)
            if self.ads and len(self.popups) < 10 and random.randint(0, 300) == 69:
                max_x = max(0, self.screen_size[0] - 300)
                max_y = max(0, self.screen_size[1] - 300)
                pos = (random.randint(0, max_x), random.randint(0, max_y))
                video_path = os.path.join(self.media_folder, "videos", random.choice(self.videos))
                self.popups.append(Popup(pos, (200, 200), self.screen_size, video_path))
            elif not self.ads:
                self.popups.clear()

    def update(self, event: pg.event.Event):
        self.text_engine.update(event)
        for popup in self.popups[:]:
            popup.close_button.event(event, popup.pos)
            if popup.close_button.is_clicked:
                self.popups.remove(popup)

    def toggle_music(self):
        if self.play_music and not self.music_playing:
            music_dir = os.path.join(self.media_folder, "music")
            musics = [f for f in os.listdir(music_dir) if os.path.isfile(os.path.join(music_dir, f))]
            if musics:
                chosen = random.choice(musics)
                pg.mixer.music.load(os.path.join(music_dir, chosen))
                pg.mixer.music.play(-1, fade_ms=20000)
                pg.mixer.music.set_volume(1.0)
                self.music_playing = True
        elif not self.play_music and self.music_playing:
            pg.mixer.music.stop()
            self.music_playing = False

    def draw(self):
        self.text_engine.draw(self.window)
        max_x = self.screen_size[0]
        max_y = self.screen_size[1]

        for popup in self.popups:
            x = min(max(popup.pos[0], 0), max_x - popup.size[0] - 100)
            y = min(max(popup.pos[1], 0), max_y - popup.size[1] - 100)
            popup.pos = (x, y)
            self.window.blit(popup.draw(), popup.pos)

    def intro(self):
        vid = Video(os.path.join(self.media_folder, "intro.mp4"))
        vid.resize(self.screen_size)
        vid.set_volume(1.0)
        while vid.active:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    vid.stop()
                    sys.exit()
                if event.type == pg.VIDEORESIZE:
                    self.resize(event.w, event.h, vid)
            if vid.draw(self.window, (0, 0), force_draw=False):
                pg.display.update()

    def resize(self, width: int, height: int, video: Video):
        self.screen_size = [width, height]
        self.window = pg.display.set_mode(self.screen_size, pg.RESIZABLE)
        self.text_engine.screen = pg.Surface(self.screen_size)
        self.text_engine.effects.canvas_size = self.screen_size
        if video:
            video.resize(self.screen_size)
        if self.text_engine.background:
            self.text_engine.background_image = pg.transform.smoothscale(self.text_engine.background_image, self.screen_size)

    def run(self):
        try:
            self.intro()
            self.toggle_music()
            while self.running:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        self.running = False
                        sys.exit()
                    if event.type == pg.VIDEORESIZE:
                        self.resize(event.w, event.h, None)
                    if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                        self.menus.settings()
                    self.update(event)

                keys = pg.key.get_pressed()
                ctrl = keys[pg.K_LCTRL] or keys[pg.K_RCTRL]

                if ctrl and keys[pg.K_r]:
                    self.text_engine.reset_view()
                if ctrl and keys[pg.K_s]:
                    self.menus.save_interface()
                if ctrl and keys[pg.K_o]:
                    self.menus.load_interface()

                self.toggle_music()
                self.draw()
                pg.display.flip()
                self.clock.tick(60)
                pg.display.set_caption("NotePad-- | " + self.filename + f" | FPS : {round(self.clock.get_fps(), 2)}")

        except KeyboardInterrupt:
            self.running = False

if __name__ == "__main__":
    pg.init()
    pg.key.set_repeat(300, 30)
    main = Main((1200, 800))
    main.run()
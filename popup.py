import pygame as pg
import imageio.v3 as iio
from ui import Button

class Popup:
    _video_cache: dict[str, list[pg.Surface]] = {}

    def __init__(self, pos: tuple[int, int], size: tuple[int, int], screen_size: tuple[int], video_path: str):
        self.pos = pos
        self.size = size
        self.screen_size = screen_size
        self.close_button = Button("X", (50, 50), 50, (self.size[0] + 50, 50))

        self.frames = self._load_video_frames(video_path, self.size)
        self.frame_counter = 0

    @classmethod
    def _load_video_frames(cls, path: str, target_size: tuple[int, int]) -> list[pg.Surface]:
        if path in cls._video_cache:
            return cls._video_cache[path]

        frames = []
        for frame in iio.imiter(path):
            height, width = frame.shape[:2]
            frame = frame.astype('uint8')

            mode = 'RGB' if frame.shape[2] == 3 else 'RGBA'
            surface = pg.image.frombuffer(frame.tobytes(), (width, height), mode).convert_alpha()
            surface = pg.transform.scale(surface, target_size).convert()
            frames.append(surface)

        cls._video_cache[path] = frames
        return frames

    def draw(self) -> pg.Surface:
        current_frame = self.frames[self.frame_counter]
        self.frame_counter = (self.frame_counter + 1) % len(self.frames)

        margin = 50
        canvas_size = (self.size[0] + 2 * margin, self.size[1] + 2 * margin)
        canvas = pg.Surface(canvas_size, pg.SRCALPHA)
        canvas.fill((0, 0, 0, 0))

        canvas.blit(current_frame, (margin, margin))
        self.close_button.draw(canvas, self.pos)

        return canvas

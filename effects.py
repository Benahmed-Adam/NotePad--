import pygame as pg
import math
import numpy as np
import random
import threading

class Effects:
    def __init__(self, canvas_size, fps):
        self.canvas_size = canvas_size
        self.frame_count = fps
        self.frames = []
        self.current_frame = 0
        self.frame_delay = 0
        self.frame_delay_counter = 0
        self.rotation = 0
        self.spawn_interval = 50
        self.last_spawn_time = 0
        self.particles = []
        self.available_effects = ["blur", "rotate", "gradient", "particles", "shake", "glitch", "scanlines", "wave", "noise", "chromatic"]
        self.cc = 0

        threading.Thread(target=self._generate_gradient_frames).start()

    def _create_particle(self) -> dict:
        return {
            "position": [
                random.uniform(20, self.canvas_size[0] - 20),
                random.uniform(20, self.canvas_size[1] - 20)
            ],
            "velocity": [
                random.uniform(-1.0, 1.0),
                random.uniform(-1.0, -0.5)
            ],
            "size": random.randint(4, 15),
            "lifespan": random.uniform(1.0, 3.0)
        }

    def _draw_particle(self, particle: dict, canvas: pg.Surface) -> None:
        x, y = particle["position"]
        radius = int(particle["size"])

        pg.draw.circle(canvas, (255, 255, 255), (int(x), int(y)), radius)

        glow_radius = radius * 2
        glow_surf = pg.Surface((glow_radius * 2, glow_radius * 2), pg.SRCALPHA)
        pg.draw.circle(glow_surf, (20, 20, 60, 100), (glow_radius, glow_radius), glow_radius)
        canvas.blit(glow_surf, (x - glow_radius, y - glow_radius), special_flags=pg.BLEND_RGB_ADD)

    def update_particles(self, canvas: pg.Surface) -> None:
        current_time = pg.time.get_ticks()

        if current_time - self.last_spawn_time >= self.spawn_interval:
            self.particles.append(self._create_particle())
            self.last_spawn_time = current_time

        for particle in self.particles[:]:
            pos, vel = particle["position"], particle["velocity"]
            pos[0] += vel[0]
            pos[1] += vel[1]
            particle["size"] -= 0.1
            vel[1] += 0.01
            particle["lifespan"] -= 1 / (self.frame_count * 2)

            if particle["size"] > 0:
                self._draw_particle(particle, canvas)

            if particle["size"] <= 0 or particle["lifespan"] <= 0:
                self.particles.remove(particle)

    def _generate_gradient_frames(self) -> None:
        width, height = self.canvas_size
        x = np.linspace(0, 1, width)
        y = np.linspace(0, 1, height)
        xx, yy = np.meshgrid(x, y)
        ratio = (xx + yy) / 2

        brightness, amplitude = 80, 80

        for i in range(self.frame_count):
            phase = math.radians((i / self.frame_count) * 360)
            r = (brightness + amplitude * np.sin(2 * math.pi * ratio + phase)).astype(np.uint8)
            g = (brightness + amplitude * np.sin(2 * math.pi * ratio + phase + 2)).astype(np.uint8)
            b = (brightness + amplitude * np.sin(2 * math.pi * ratio + phase + 4)).astype(np.uint8)
            a = np.full_like(r, 60, dtype=np.uint8)

            frame = np.dstack((r, g, b, a))
            surface = pg.image.frombuffer(frame.flatten(), (width, height), "RGBA").convert_alpha()
            self.frames.append(surface)

    def animated_gradient_overlay(self, canvas: pg.Surface) -> pg.Surface:
        result = canvas.copy()
        if len(self.frames) == self.frame_count:
            gradient = self.frames[self.current_frame]
            result.blit(pg.transform.scale(gradient, canvas.get_size()), (0, 0), special_flags=pg.BLEND_RGBA_ADD)

            self.frame_delay_counter += 1
            if self.frame_delay_counter >= self.frame_delay:
                self.current_frame = (self.current_frame + 1) % self.frame_count
                self.frame_delay_counter = 0
        return result

    def rotate(self, canvas: pg.Surface) -> pg.Surface:
        return pg.transform.rotate(canvas.copy(), self.rotation)

    def blur(self, canvas: pg.Surface, passes: int = 2, offset: int = 3) -> pg.Surface:
        result = canvas.copy()
        for i in range(1, passes + 1):
            shifted = pg.transform.scale(canvas, self.canvas_size)
            shifted.set_alpha(30)
            result.blit(shifted, (offset * i, offset * i))
            result.blit(shifted, (-offset * i, -offset * i))
        return result

    def glitch(self, canvas: pg.Surface) -> pg.Surface:
        result = canvas.copy()
        arr = pg.surfarray.pixels3d(result)
        height = arr.shape[1]

        for _ in range(5):
            y = random.randint(0, height - 10)
            h = random.randint(1, 5)
            offset = random.randint(-20, 20)
            arr[:, y:y + h] = np.roll(arr[:, y:y + h], offset, axis=0)

        del arr
        return result

    def scanlines(self, canvas: pg.Surface) -> pg.Surface:
        result = canvas.copy()
        for y in range(0, result.get_height(), 2):
            pg.draw.line(result, (0, 0, 0, 40), (0, y), (result.get_width(), y))
        return result

    def wave_distortion(self, canvas: pg.Surface, amplitude=5, frequency=0.05) -> pg.Surface:
        result = pg.Surface(canvas.get_size())
        width, height = canvas.get_size()

        for y in range(height):
            offset = int(amplitude * math.sin(frequency * y + self.cc * 0.2))
            row = canvas.subsurface((0, y, width, 1))
            result.blit(row, (offset, y))

        return result

    def noise_overlay(self, canvas: pg.Surface, intensity=100, update_every=1) -> pg.Surface:
        if not hasattr(self, "_noise_frame_count"):
            self._noise_frame_count = 0
            self._cached_noise = None

        if self._noise_frame_count % update_every == 0 or self._cached_noise is None:
            noise = np.random.randint(0, intensity, (128, 128, 3), dtype=np.uint8)
            self._cached_noise = pg.surfarray.make_surface(noise.transpose([1, 0, 2]))
            self._cached_noise.set_alpha(20)
        self._noise_frame_count += 1

        result = canvas.copy()
        scaled_noise = pg.transform.smoothscale(self._cached_noise, canvas.get_size())
        result.blit(scaled_noise, (0, 0), special_flags=pg.BLEND_RGB_ADD)
        return result

    def chromatic_aberration(self, canvas: pg.Surface, shift=5) -> pg.Surface:
        result = canvas.copy()
        arr = pg.surfarray.pixels3d(result)
        r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]

        shifted_r = np.roll(r, shift, axis=1)
        shifted_b = np.roll(b, -shift, axis=1)

        arr[:,:,0] = shifted_r
        arr[:,:,2] = shifted_b

        del arr
        return result




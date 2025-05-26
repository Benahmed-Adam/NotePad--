import pygame as pg

class Button:
    def __init__(self, text: str, size: tuple[int, int], font_size: int, pos: tuple[int, int]) -> None:
        self.is_clicked = False
        self.size = size
        self.pos = pos
        self.font = pg.font.Font(None, font_size)
        self.text_surf = self.font.render(text, True, (0, 0, 0))

        self.rect = pg.Rect(
            pos[0] - size[0] // 2,
            pos[1] - size[1] // 2,
            size[0],
            size[1]
        )

        self.surface_idle = pg.Surface(size, pg.SRCALPHA)
        self.surface_hover = pg.Surface(size, pg.SRCALPHA)

        pg.draw.rect(self.surface_idle, (170, 170, 170), self.surface_idle.get_rect(), border_radius=50)
        pg.draw.rect(self.surface_hover, (100, 100, 100), self.surface_hover.get_rect(), border_radius=50)

    def draw(self, canvas: pg.Surface, offset: tuple[int, int] = (0, 0)) -> None:
        mouse_pos = pg.mouse.get_pos()
        local_mouse = (mouse_pos[0] - offset[0], mouse_pos[1] - offset[1])

        if self.rect.collidepoint(local_mouse):
            canvas.blit(self.surface_hover, self.rect.topleft)
        else:
            canvas.blit(self.surface_idle, self.rect.topleft)

        text_rect = self.text_surf.get_rect(center=self.pos)
        canvas.blit(self.text_surf, text_rect)

    def event(self, event: pg.event.Event, offset: tuple[int, int] = (0, 0)) -> None:
        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_pos = pg.mouse.get_pos()
            local_mouse = (mouse_pos[0] - offset[0], mouse_pos[1] - offset[1])
            self.is_clicked = self.rect.collidepoint(local_mouse)


class CheckBox:
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], label: str, value: bool) -> None:
        self.value = value
        self.pos = pos
        self.size = size
        self.font = pg.font.Font(None, 30)
        self.label_surf = self.font.render(label, True, (255, 255, 255))

        self.rect = pg.Rect(pos, size)
        self.surface_on = self._create_selected_surface()
        self.surface_off = self._create_unselected_surface()

    def _create_selected_surface(self) -> pg.Surface:
        surf = pg.Surface(self.size)
        surf.fill((0, 0, 0))
        pg.draw.rect(surf, (255, 255, 255), surf.get_rect(), width=2)
        pg.draw.line(surf, (255, 255, 255), (5, 5), (self.size[0] - 5, self.size[1] - 5), 2)
        pg.draw.line(surf, (255, 255, 255), (5, self.size[1] - 5), (self.size[0] - 5, 5), 2)
        return surf

    def _create_unselected_surface(self) -> pg.Surface:
        surf = pg.Surface(self.size)
        surf.fill((0, 0, 0))
        pg.draw.rect(surf, (255, 255, 255), surf.get_rect(), width=2)
        return surf

    def draw(self, canvas: pg.Surface) -> None:
        label_pos = (self.pos[0] - self.label_surf.get_width() - 10, self.pos[1])
        canvas.blit(self.label_surf, label_pos)
        canvas.blit(self.surface_on if self.value else self.surface_off, self.pos)

    def update(self, event: pg.event.Event) -> None:
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.value = not self.value


class TextZone:
    def __init__(
        self,
        default_text: str,
        size: tuple[int, int],
        font_size: int,
        pos: tuple[int, int],
        max_length: int,
        accept_type: list[type],
        label: str
    ) -> None:
        self.accept_type = accept_type
        self.font = pg.font.Font(None, font_size)
        self.size = size
        self.pos = pos
        self.default_text = default_text
        self.text = ""
        self.max_length = max_length
        self.is_writing = False
        self.label_surf = self.font.render(label, True, (255, 255, 255))

    def get(self) -> str:
        return self.text

    def reset(self) -> None:
        self.text = ""

    def draw(self, canvas: pg.Surface) -> None:
        label_pos = (
            self.pos[0] - self.size[0] // 2 - self.label_surf.get_width() - 10,
            self.pos[1] - self.label_surf.get_height() // 2
        )
        canvas.blit(self.label_surf, label_pos)

        rect = pg.Rect(
            self.pos[0] - self.size[0] // 2,
            self.pos[1] - self.size[1] // 2,
            self.size[0],
            self.size[1]
        )

        border_color = (0, 255, 0) if self.is_writing else (175, 175, 175)
        pg.draw.rect(canvas, border_color, rect, 2)

        display_text = self.text if self.text else self.default_text
        text_surface = self.font.render(display_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.pos)
        canvas.blit(text_surface, text_rect)

    def event(self, event: pg.event.Event) -> None:
        rect = pg.Rect(
            self.pos[0] - self.size[0] // 2,
            self.pos[1] - self.size[1] // 2,
            self.size[0],
            self.size[1]
        )

        if event.type == pg.MOUSEBUTTONDOWN:
            self.is_writing = rect.collidepoint(pg.mouse.get_pos())

        elif event.type == pg.KEYDOWN and self.is_writing:
            if event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < self.max_length:
                char = event.unicode
                if (int if char.isdigit() else str) in self.accept_type:
                    self.text += char

import os
import pygame
from PIL import Image

LOGICAL_W, LOGICAL_H = 128, 128
UPSCALE_TO_240 = True
FULLSCREEN = True

def _init_sdl_video():
    os.environ.setdefault("SDL_VIDEODRIVER", "kmsdrm")
    try:
        pygame.display.init()
        return
    except Exception:
        pygame.display.quit()
    os.environ["SDL_VIDEODRIVER"] = "fbcon"
    os.environ.setdefault("SDL_FBDEV", "/dev/fb0")
    pygame.display.init()

class LCD:
    def __init__(self):
        self.width = LOGICAL_W
        self.height = LOGICAL_H
        self._screen = None
        self._surf = None
        self._scale = 1

    def LCD_Init(self, scan_dir=None):
        pygame.init()
        _init_sdl_video()
        flags = pygame.FULLSCREEN if FULLSCREEN else 0
        if UPSCALE_TO_240:
            target_w, target_h = 240, 240
        else:
            display_info = pygame.display.Info()
            target_w, target_h = display_info.current_w, display_info.current_h
        self._screen = pygame.display.set_mode((target_w, target_h), flags)
        self._surf = pygame.Surface((self.width, self.height))
        self._scale = target_w // self.width if UPSCALE_TO_240 else max(
            1, min(target_w // self.width, target_h // self.height)
        )
        pygame.mouse.set_visible(False)
        self.LCD_Clear()

    def LCD_Clear(self):
        self._screen.fill((0, 0, 0))
        pygame.display.flip()

    def LCD_ShowImage(self, pil_image, x=0, y=0):
        if pil_image.mode != "RGB":
            pil_image = pil_image.convert("RGB")
        raw = pil_image.tobytes()
        surf = pygame.image.fromstring(raw, (self.width, self.height), "RGB")
        if self._scale != 1:
            surf = pygame.transform.scale(
                surf, (self.width * self._scale, self.height * self._scale)
            )
        rect = surf.get_rect(center=self._screen.get_rect().center)
        self._screen.blit(surf, rect)
        pygame.display.flip()

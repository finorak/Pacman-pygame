# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    test.py                                           :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: nyramana <nyramana@student.42antananariv  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/08/19 10:49:01 by nyramana         #+#    #+#              #
#    Updated: 2026/09/03 11:49:19 by nyramana        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #

import math

from ..core import XMain
from .base import Screen


class MainMenue(Screen):
    def __init__(self, xmain: XMain) -> None:
        super().__init__(xmain)
        self.assets.update(
            self.load_assets(
                {
                    "back": "assets/logo/Back.png",
                    "logo": "assets/logo/Logo.png",
                    "start": "assets/button/start.png",
                    "instructions": "assets/button/instruction.png",
                    "highscore": "assets/button/highscore.png",
                    "exit": "assets/button/exit.png",
                }
            )
        )
        self.set_position(
            self.assets,
            {
                "back": (1000, 100),
                "start": (
                    self.get_center(self.assets["start"].sprite.width),
                    350,
                ),
                "instructions": (
                    self.get_center(self.assets["instructions"].sprite.width),
                    400,
                ),
                "highscore": (
                    self.get_center(self.assets["highscore"].sprite.width),
                    450,
                ),
                "exit": (
                    self.get_center(self.assets["exit"].sprite.width),
                    500,
                ),
            },
        )

    def get_input(self, key: int, _) -> None | str:
        if key == 65293:
            return "game"
        elif key == 113:
            self.xmain.mlx.mlx_loop_exit(self.xmain.mlx_ptr)
        elif key == 104:
            return "highscore"
        elif key == 105:
            return "instructions"
        else:
            print(key)

    def update(self, dt: float) -> None:
        self.time += dt
        self.assets["logo"].pos_y = 50 + math.sin(self.time * 2) * 10
        self.assets["logo"].pos_x = (
            self.get_center(self.assets["logo"].sprite.width)
            - 10
            + math.cos(10 + self.time * 2) * 10
        )
        self.assets["back"].pos_x -= dt * 30

    def render(self) -> None:
        self.xmain.mlx.mlx_clear_window(
            self.xmain.mlx_ptr,
            self.xmain.mlx_window,
        )
        self._render_background()
        self._render_instruction()

    def _render_instruction(self) -> None:
        for name, image in self.assets.items():
            if name == "back":
                continue
            self.xmain.mlx.mlx_put_image_to_window(
                self.xmain.mlx_ptr,
                self.xmain.mlx_window,
                image.sprite.img,
                int(image.pos_x),
                int(image.pos_y),
            )

    def _render_background(self) -> None:
        image_width = self.assets["back"].sprite.width

        x = self.assets["back"].pos_x

        while x < self.xmain.screen_w:
            self.xmain.mlx.mlx_put_image_to_window(
                self.xmain.mlx_ptr,
                self.xmain.mlx_window,
                self.assets["back"].sprite.img,
                int(x),
                int(self.assets["back"].pos_y),
            )
            x += image_width

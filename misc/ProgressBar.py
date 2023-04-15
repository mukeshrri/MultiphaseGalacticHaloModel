# -*- coding: utf-8 -*-
"""
Created on Thu May 12 08:28:23 2022

@author: alankar
"""

import colorama


class ProgressBar(object):
    def __init__(self: "ProgressBar", color: str = colorama.Fore.YELLOW) -> None:
        self.percent = 0.0
        self.bar = "█" * int(self.percent) + "-" * (100 - int(self.percent))
        self.color = color
        print(self.color + f"\r|{self.bar}| {self.percent:.2f}%", end="\r", flush=True)

    def progress(self: "ProgressBar", progress: int, total: int) -> None:
        self.percent = 100.0 * (progress / total)
        self.bar = "█" * int(self.percent) + "-" * (100 - int(self.percent))
        print(self.color + f"\r|{self.bar}| {self.percent:.2f}%", end="\r", flush=True)
        if progress == total:
            print(
                colorama.Fore.GREEN + f"\r|{self.bar}| {self.percent:.2f}%",
                end="\r",
                flush=True,
            )

    def end(self: "ProgressBar") -> None:
        print(colorama.Fore.RESET, flush=True)

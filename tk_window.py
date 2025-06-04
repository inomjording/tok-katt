import time
import tkinter as tk
import numpy as np
from enum import Enum, auto


class Direction(Enum):
    LEFT = auto()
    RIGHT = auto()


window = tk.Tk()
window.overrideredirect(True)
window.attributes("-topmost", True)
window.wm_attributes('-transparentcolor', 'white')
label = tk.Label(window, bd=0, bg='white')
label.pack()


class WindowPet:
    def __init__(self, pet):
        self.pet = pet
        self.coordinates = np.array([0, window.winfo_screenheight() - 96])
        self.update_position()
        self.timestamp = time.time()
        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        # Bind mouse events for drag and drop
        label.bind("<Button-1>", self.on_drag_start)
        label.bind("<B1-Motion>", self.on_drag_motion)
        label.bind("<ButtonRelease-1>", self.on_drag_end)

        window.after(0, self.update)
        window.mainloop()

    def update(self):
        if not self.dragging:
            self.move()
        self.pet.queue_behavior()

        window.after(100, self.update)

    def move(self):
        self.coordinates = self.pet.move(self.coordinates)
        self.update_position()

    def on_drag_start(self, event):
        self.dragging = True
        # Calculate the offset between mouse position and window position
        self.drag_offset_x = event.x_root - self.coordinates[0]
        self.drag_offset_y = event.y_root - self.coordinates[1]

    def on_drag_motion(self, event):
        if self.dragging:
            # Update coordinates based on mouse position and offset
            self.coordinates[0] = event.x_root - self.drag_offset_x
            self.coordinates[1] = event.y_root - self.drag_offset_y
            self.update_position()

    def on_drag_end(self, event):
        self.dragging = False

    def update_position(self):
        window.geometry("64x64+{x}+{y}".format(x=str(self.coordinates[0]), y=str(self.coordinates[1])))
        label.configure(image=self.pet.next_frame())
        label.pack()


class Animation:
    def __init__(self, image_left, image_right, frames):
        self.frames = frames
        self.left = self.image_info(image_left)
        self.right = self.image_info(image_right)
        self.frame_index = 0

    def image_info(self, image_path):
        return [tk.PhotoImage(file=image_path, format="gif -index %i" % i) for i in range(self.frames)]

    def next_frame(self, direction):
        self.frame_index = (self.frame_index + 1) % self.frames
        return self.left[self.frame_index] if direction == Direction.LEFT else self.right[self.frame_index]

    def finished_animation_loop(self):
        return self.frame_index == self.frames - 1


class ShortAnimation(Animation):
    def __init__(self, image_left, image_right, frames, multiplier, lengthen=None):
        self.multiplier = multiplier
        self.lengthen = lengthen
        super().__init__(image_left, image_right, frames)
        self.frames = len(self.left)

    def image_info(self, image_path):
        frames = [tk.PhotoImage(file=image_path, format="gif -index %i" % i) for i in range(self.frames)]
        return self.multiply_frames(frames) if self.lengthen is None else self.multiply_frame(frames, self.lengthen)

    def multiply_frame(self, frames, frame_indices):
        frame_list = []
        for i in range(len(frames)):
            if i in frame_indices:
                frame_list += self.multiplier * [frames[i]]
            else:
                frame_list.append(frames[i])
        return frame_list

    def multiply_frames(self, frames):
        frame_list = []
        for i in range(len(frames)):
            frame_list += self.multiplier * [frames[i]]
        return frame_list


cat_animations = {
    "walk": Animation("images/cat-walk.gif", "images/cat-walk-right.gif", 13),
    "idle": Animation("images/cat.gif", "images/cat-right.gif", 11),
    "idle_blink": Animation("images/cat-blink.gif", "images/cat-blink-right.gif", 11),
    "sit": Animation("images/cat-sit.gif", "images/cat-sit-right.gif", 5),
    "sitting": ShortAnimation("images/cat-sitting.gif", "images/cat-sitting-right.gif", 7, 4, [0, 3]),
    "sitting_blink": Animation("images/cat-sitting-blink.gif", "images/cat-sitting-blink-right.gif", 7),
    "lie": Animation("images/cat-lie.gif", "images/cat-lie-right.gif", 5),
    "lying": ShortAnimation("images/cat-lying.gif", "images/cat-lying-right.gif", 4, 5, [0, 2]),
    "lying_blink": Animation("images/cat-lying-blink.gif", "images/cat-lying-blink-right.gif", 4),
    "sleepy": Animation("images/cat-sleepy.gif", "images/cat-sleepy-right.gif", 3),
    "sleeping": ShortAnimation("images/cat-sleeping.gif", "images/cat-sleeping-right.gif", 2, 5),
    "sit_up": Animation("images/cat-stand.gif", "images/cat-stand-right.gif", 5),
    "stand_up": Animation("images/cat-stand-up.gif", "images/cat-stand-up-right.gif", 5),
}

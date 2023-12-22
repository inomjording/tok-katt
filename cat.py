import random
from tk_window import *


class Behavior:
    def __init__(self,
                 name,
                 animation,
                 next_behavior,
                 velocity=np.array([0, 0]),
                 change_direction=False):
        self.name = name
        self.animation = animation
        self.velocity = velocity
        self.next_behavior = next_behavior
        self.change_direction = change_direction
        self.animation_index = 0

    def set_animation_index(self):
        self.animation_index = (self.animation_index + 1) % len(self.animation)

    def get_animation(self):
        return self.animation[self.animation_index]


class Pet:
    def __init__(self):
        self.behaviors = None
        self.current_behavior = None
        self.direction = Direction.RIGHT
        self.behavior_queue = []

    def move(self, coordinates):
        if coordinates[0] == 0:
            self.direction = Direction.RIGHT
        elif coordinates[0] == window.winfo_screenwidth():
            self.direction = Direction.LEFT
        return np.add(coordinates, np.multiply(self.current_behavior.velocity,
                                               np.array([-1, 1]) if self.direction == Direction.LEFT else
                                               np.array([1, 1])))

    def next_behavior(self):
        behavior_count = len(self.current_behavior.next_behavior)
        if behavior_count == 1:
            return self.behaviors.get(self.current_behavior.next_behavior[0])
        else:
            name = self.current_behavior.next_behavior[random.randint(0, behavior_count - 1)]
            return self.behaviors.get(name)

    def transition_behavior(self, next_behavior): return None

    @staticmethod
    def should_change(multiplier): return random.randint(0, multiplier) == 0

    def queue_behavior(self):
        if not self.current_behavior.get_animation().finished_animation_loop():
            return
        if len(self.behavior_queue) > 0:
            self.set_current_behavior()
        if self.current_behavior.change_direction & self.should_change(5):
            self.direction = Direction.LEFT if self.direction == Direction.RIGHT else Direction.RIGHT
        if self.should_change(2):
            next_behavior = self.next_behavior()
            transition_behavior = self.transition_behavior(next_behavior)
            if transition_behavior is not None:
                self.behavior_queue.append(transition_behavior)
            self.behavior_queue.append(next_behavior)

    def set_current_behavior(self):
        self.current_behavior = self.behavior_queue.pop(0)

    def next_frame(self):
        animation = self.current_behavior.get_animation()
        if animation.finished_animation_loop():
            self.current_behavior.set_animation_index()
        return animation.next_frame(self.direction)


class Cat(Pet):
    cat_behaviors = {
        "walking": Behavior("walking", [cat_animations.get("walk")], ["idle"], np.array([3, 0]), True),
        "sitting": Behavior("sitting", [cat_animations.get("sitting"), cat_animations.get("sitting"),
                                        cat_animations.get("sitting_blink")],["lying", "idle"]),
        "lying": Behavior("lying", [cat_animations.get("lying"), cat_animations.get("lying"),
                                    cat_animations.get("lying_blink")],["sleeping", "sitting"]),
        "sleeping": Behavior("sleeping", [cat_animations.get("sleeping")], ["lying"]),
        "idle": Behavior("idle", [cat_animations.get("idle"), cat_animations.get("idle_blink")], ["walking", "sitting"],
                         change_direction=True),
    }

    def __init__(self):
        super().__init__()
        self.behaviors = self.cat_behaviors
        self.current_behavior = self.cat_behaviors.get("walking")

    def transition_behavior(self, next_behavior):
        name_current = self.current_behavior.name
        name_next = next_behavior.name
        match (name_current, name_next):
            case ("idle", "sitting"):
                return Behavior("sit", [cat_animations.get("sit")], [next_behavior.name])
            case ("sitting", "lying"):
                return Behavior("lie", [cat_animations.get("lie")], [next_behavior.name])
            case ("sitting", "idle"):
                return Behavior("stand_up", [cat_animations.get("stand_up")], [next_behavior.name])
            case ("lying", "sitting"):
                return Behavior("sit_up", [cat_animations.get("sit_up")], [next_behavior.name])
            case _:
                return None

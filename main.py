from cat import *

if __name__ == "__main__":
    try:
        my_cat = Cat()
        my_pet_window = WindowPet(my_cat)
    finally:
        exit(130)

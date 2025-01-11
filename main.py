import badger2040
import badger_os
display = badger2040.Badger2040()

##### TODOs #####
# - Add bounces checking for HP and spell slots
# - Adjust font sizing/spacing if name/class is too big
# - Cleanup var naming from previous example file

# Global Constants
WIDTH = badger2040.WIDTH #296
HEIGHT = badger2040.HEIGHT #128

COMPANY_HEIGHT = 30
LEFT_PADDING = 20
COMPANY_TEXT_SIZE = 0.6

IMAGE_SIZE = 64

CHAR_PATH = "/charsheet.txt"

DEFAULT_CHAR = """Mixty
Paladin
2
16
2"""
      
def show_dnd(hp, mp, fast):
    HEIGHT = 3
    TEXT_SIZE = 3

    if fast:
        display.set_update_speed(badger2040.UPDATE_TURBO)

    clear_display()
    
    display.set_font("bitmap8") # The 8 denotes the height of the text
    display.text(f"{NAME} - {CLASS_NAME} {LEVEL}", LEFT_PADDING, HEIGHT, scale=TEXT_SIZE)
    display.line(LEFT_PADDING - 2, (HEIGHT + 8*TEXT_SIZE)+4, 255, (HEIGHT + 8*TEXT_SIZE)+4, 2)
    
    display.text(f"Hit Points: {hp}", LEFT_PADDING, (HEIGHT + 8*TEXT_SIZE)*2 - 10, scale=TEXT_SIZE)
    display.text(f"Spell Slots: {mp}", LEFT_PADDING, (HEIGHT + 8*TEXT_SIZE)*3 - 10, scale=TEXT_SIZE)
    
    display.set_font("bitmap6") # The 8 denotes the height of the text
    display.text(f"Use Slot", 0, (HEIGHT + 2 + 8*TEXT_SIZE)*4)
    display.text(f"Long Rest", 100, (HEIGHT + 2 + 8*TEXT_SIZE)*4)
    display.text(f"Refresh", 220, (HEIGHT + 2 + 8*TEXT_SIZE)*4)

    display.update()
    
    if fast:
        display.set_update_speed(badger2040.UPDATE_NORMAL)
        
def clear_display():
    display.set_pen(15)
    display.clear()
    display.set_pen(0)

# Main Area
# Open the character sheet file
try:
    file = open(CHAR_PATH, "r")
except OSError:
    with open(CHAR_PATH, "w") as f:
        f.write(DEFAULT_TEXT)
        f.flush()
    file = open(CHAR_PATH, "r")

# Strip newlines
sheet = file.read().splitlines()

NAME = sheet[0]
CLASS_NAME = sheet[1]
LEVEL = sheet[2]
MAX_HP = sheet[3]
MAX_SLOTS = sheet[4]

state = {
    "current_hp": MAX_HP,
    "current_slots": MAX_SLOTS,
}

# Will override existing values if anything was previously saved
badger_os.state_load("dnd", state)
    
while True:
    # Sometimes a button press or hold will keep the system
    # powered *through* HALT, so latch the power back on.
    display.keepalive()
    
    fast_update = True
    
    if display.pressed(badger2040.BUTTON_UP):
        state["current_hp"] += 1

    if display.pressed(badger2040.BUTTON_DOWN):
        state["current_hp"] -= 1
        
    if display.pressed(badger2040.BUTTON_A):
        state["current_slots"] -= 1
        fast_update = False
    
    if display.pressed(badger2040.BUTTON_B):
        # Long Rest Reset
        state["current_hp"] = MAX_HP
        state["current_slots"] = MAX_SLOTS
        fast_update = False
    
    if display.pressed(badger2040.BUTTON_C):
        # Force slow display update
        fast_update = False
    
    show_dnd(state["current_hp"], state["current_slots"], fast_update)
    
    badger_os.state_save("dnd", state)
    
    # Halt the Badger to save power, it will wake up if any of the front buttons are pressed
    display.halt()

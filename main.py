import arcade
import math
import os, os.path
import random
from PIL import Image
from typing import List

# Game window parameters
WIDTH = 1000
HEIGHT = 800

# Card parameters
card_width = WIDTH // 20
card_height = HEIGHT // 9

# Shuffle button coordinates
shuffle_button_x = math.floor(WIDTH / (800/550))
shuffle_button_y = HEIGHT // 12
shuffle_text_x = shuffle_button_x + 40
shuffle_text_y = shuffle_button_y + 15

in_game = False
start_game = False
pick_up_card = False
using_card = None
card_stacked = False
card_slotted = False


# Main deal slot coordinates and card storage lists
deal_slot_x = WIDTH // 14
deal_slot_y = HEIGHT - 90
deal_slot_cards = []
dealt_cards = []

# Stacking slot coordinates and card storage lists
other_slots_x = [math.floor(WIDTH/(800/num)) for num in range(570, 721, 50)]
other_slots_y = HEIGHT - 80
all_slots = [[], [], [], []]

# Stack for each of the seven card columns at the start of game
columns = [[] for _ in range(7)]

# Coordinates of card columns 
columns_x = [math.floor(WIDTH / (800/x)) for x in range(171, 514, 57)]
columns_y = math.floor(HEIGHT / 1.5)

card_names = ['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king']
shuffled_cards = []

# This section loads required images by asking for a path to the images directory from the user
# sample path: c:/Users/iliarom.BASE.000/Desktop/GitHub/Solitaire/images
path = input("Please enter path to your images directory (sample path: c:/Users/iliarom.BASE.000/Desktop/GitHub/Solitaire/images): ")
img_paths = [f"images/{card}" for card in os.listdir(path)]
card_imgs = {texture: arcade.load_texture(texture) for texture in img_paths}


class PlayingCard:
    """Creates and organizes the playing cards
    """
    full_deck = []
    hearts = {}
    diamonds = {}
    spades = {}
    clubs = {}

    def __init__(self, value: int, suite: str, x: int, y: int):
        self.image = None
        self.value = value
        self.suite = suite
        self.x = x
        self.y = y
        self.old_x = x
        self.old_y = y
        self.flipped = True
        self.bottom_cards = []
        self.top_cards = []
        PlayingCard.full_deck.append(self)

    def __str__(self) -> str:
        return f"{self.value}, {self.suite}"
    
    @classmethod
    def make_cards(cls):
        """Creates playing cards
        """
        global card_names

        i = 0
        while i < 13:
            cls.hearts[card_names[i]] = PlayingCard(i+1, 'hearts', (i+1) * 57, 400)           
            i += 1

        j = 0
        while j < 13:
            cls.diamonds[card_names[j]] = PlayingCard(j+1, 'diamonds', (j+1) * 57, 325)            
            j += 1

        k = 0
        while k < 13:
            cls.spades[card_names[k]] = PlayingCard(k+1, 'spades', (k+1) * 57, 250)          
            k += 1

        l = 0
        while l < 13:
            cls.clubs[card_names[l]] = PlayingCard(l+1, 'clubs', (l+1) * 57, 175)            
            l += 1

        # Attaching images to each card object
        for card in cls.full_deck:
            card.image = card_imgs[f"images/{card.suite}{card.value}.jpg"]


    @classmethod
    def shuffle_cards(cls):
        """ Rearanges the order of the cards in full_deck and stores the new list in the shuffled_cards variable
        """
        global shuffled_cards

        shuffled_cards = random.sample(cls.full_deck, len(cls.full_deck))


class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        arcade.set_background_color(arcade.color.WHEAT)

        # If you have sprite lists, you should create them here,
        # and set them to None

    def setup(self):
        PlayingCard.make_cards()

    def on_draw(self):
        arcade.start_render()
        global start_game, in_game
        global card_height, card_height, card_names
        global deal_slot_x, deal_slot_y, other_slots_x, other_slots_y, all_slots
        global columns, columns_x, columns_y
        global shuffled_cards, deal_slot_cards, dealt_cards
        global shuffle_button_x, shuffle_button_y, shuffle_text_x, shuffle_text_y

        # draw hearts playing cards
        for card in PlayingCard.hearts.values():
            arcade.draw_rectangle_filled(card.x, card.y, card_width, card_height, arcade.color.RED)
            arcade.draw_texture_rectangle(card.x, card.y, card_width, card_height, card.image)

        i = 0
        while i < 13:
            if list(PlayingCard.hearts.values())[i].flipped:
                arcade.draw_text(card_names[i], list(PlayingCard.hearts.values())[i].x-card_width//4, list(PlayingCard.hearts.values())[i].y, color=arcade.color.WHITE)
                arcade.draw_text("hearts", list(PlayingCard.hearts.values())[i].x-card_width//3, list(PlayingCard.hearts.values())[i].y-10, arcade.color.WHITE, font_size=8)
            i += 1

        # draw diamonds playing cards
        for card in PlayingCard.diamonds.values():
            arcade.draw_rectangle_filled(card.x, card.y, card_width, card_height, arcade.color.RED)
            arcade.draw_texture_rectangle(card.x, card.y, card_width, card_height, card.image)

        i = 0
        while i < 13:
            if list(PlayingCard.diamonds.values())[i].flipped:
                arcade.draw_text(card_names[i], list(PlayingCard.diamonds.values())[i].x-card_width//4, list(PlayingCard.diamonds.values())[i].y, color=arcade.color.WHITE)
                arcade.draw_text("diamonds", list(PlayingCard.diamonds.values())[i].x-card_width//2, list(PlayingCard.diamonds.values())[i].y-10, color=arcade.color.WHITE, font_size=8)
            i += 1

        # draw spades playing cards
        for card in PlayingCard.spades.values():
            arcade.draw_rectangle_filled(card.x, card.y, card_width, card_height, arcade.color.BLACK)
            arcade.draw_texture_rectangle(card.x, card.y, card_width, card_height, card.image)

        i = 0
        while i < 13:
            if list(PlayingCard.spades.values())[i].flipped:
                arcade.draw_text(card_names[i], list(PlayingCard.spades.values())[i].x-card_width//4, list(PlayingCard.spades.values())[i].y, color=arcade.color.WHITE)
                arcade.draw_text("spades", list(PlayingCard.spades.values())[i].x-card_width//3, list(PlayingCard.spades.values())[i].y-10, arcade.color.WHITE, font_size=8)
            i += 1

        # draw clubs playing cards
        for card in PlayingCard.clubs.values():
            arcade.draw_rectangle_filled(card.x, card.y, card_width, card_height, arcade.color.BLACK)
            arcade.draw_texture_rectangle(card.x, card.y, card_width, card_height, card.image)

        i = 0
        while i < 13:
            if list(PlayingCard.clubs.values())[i].flipped:
                arcade.draw_text(card_names[i], list(PlayingCard.clubs.values())[i].x-card_width//4, list(PlayingCard.clubs.values())[i].y, color=arcade.color.WHITE)
                arcade.draw_text("clubs", list(PlayingCard.clubs.values())[i].x-card_width//3, list(PlayingCard.clubs.values())[i].y-10, arcade.color.WHITE, font_size=8)
            i += 1

        # redraw card         
        for card in shuffled_cards:
            redraw(card)
        for card in dealt_cards:
            redraw(card)
        for i in range(4):
            for card in all_slots[i]:
                redraw(card)
        for i in range(7):
            for card in columns[i]:
                redraw(card)

        # draw slots for cards
        arcade.draw_rectangle_outline(deal_slot_x, deal_slot_y, card_width, card_height, arcade.color.BLUE)
        for i in range(4):
            arcade.draw_rectangle_outline(other_slots_x[i], other_slots_y, card_width, card_height, arcade.color.BLUE)

        #column slots
        if in_game:
            for i in range(7):
                if columns[i] == [] and pick_up_card and using_card.value == 13:
                    arcade.draw_rectangle_outline(columns_x[i], columns_y, card_width, card_height, arcade.color.BLUE)

        # draw shuffle button used to shuffle and put the cards into playing formation
        arcade.draw_xywh_rectangle_filled(shuffle_button_x, shuffle_button_y, 150, 50, arcade.color.GUPPIE_GREEN)
        arcade.draw_text('Shuffle', shuffle_text_x, shuffle_text_y, arcade.color.BLACK, 20)

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        """
        global HEIGHT, WIDTH
        global shuffled_cards, deal_slot_cards, dealt_cards, all_slots, columns
        global start_game, in_game
        global deal_slot_x, deal_slot_y, columns_x, columns_y, card_width, card_height
        global using_card


        if start_game:
            # empties slot lists
            for i in range(4):
                all_slots[i] = []
            # empties column lists
            for i in range(7):
                columns[i] = []
            # empties deal slot list and dealt cards list
            deal_slot_cards = []
            dealt_cards = []

            # places the first 28 cards in playing position
            i = 0
            while i < 28:
                for row_num in range(7):
                    for row_len in range(7 - row_num):

                        card = shuffled_cards[i] 
                        start_x = math.floor(WIDTH / (800/171)) + row_num * math.floor(WIDTH / (800/57))    

                        card.x = start_x + math.floor(WIDTH / (800/57)) * (row_len)
                        card.y = columns_y - card_height // 2 * (row_num)
                        
                        if row_len == 0:
                            card.flipped = True
                        else:
                            card.flipped = False
                        
                        columns[row_num+row_len].append(card)
                        card.bottom_cards = []
                        card.top_cards = []

                        i += 1

            # places the remaining cards into the deal slot
            for card in shuffled_cards[28:]:
                deal_slot_cards.append(card)
                card.flipped = True
                card.bottom_cards = []
                card.top_cards = []

            start_game = False

        # card positioning
        for card in deal_slot_cards:
            card.x = deal_slot_x
            card.y = deal_slot_y

        for card in PlayingCard.full_deck:
            # card stacking
            if card.bottom_cards != []:
                bottom_card = card.bottom_cards[0]
                bottom_card.x = card.x
                bottom_card.y = card.y - card_height // 2
            
            if in_game:
                # in game card flip mechanics
                for i in range(7):
                    if columns[i] != [] and card == columns[i][-1]:
                        card.flipped = True
                for c in dealt_cards:
                    if dealt_cards != [] and c == dealt_cards[-1]:
                        c.flipped = True
                    else:
                        c.flipped = False
                for c in deal_slot_cards:
                    if deal_slot_cards != [] and c == deal_slot_cards[-1]:
                        c.flipped = True
                    else:
                        c.flipped = False
                

    '''
    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.
        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass
    '''

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        global pick_up_card, using_card
        
        if pick_up_card:
            using_card.x = x
            using_card.y = y
             

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        global pick_up_card, using_card, card_stacked, card_slotted
        global deal_slot_x, deal_slot_y, deal_slot_cards, dealt_cards, other_slots_x, other_slots_y, all_slots
        global card_height, card_width
        global start_game, in_game
        global shuffle_button_x, shuffle_button_y

        w = card_width // 2
        h = card_height // 2

        # deal slot mechanics         
        if x in range(deal_slot_x-w, deal_slot_x+w) and y in range(deal_slot_y-h, deal_slot_y+h):

            if deal_slot_cards == []:
                # resets deal slot if its empty
                deal_slot_cards = dealt_cards[-1::-1]
                dealt_cards = []
            else:
                # deals card
                card = deal_slot_cards[-1]
                card.y = deal_slot_y - card_height
                deal_slot_cards.remove(card)
                dealt_cards.append(card)
            print(f"in_slot: {len(deal_slot_cards)}, out: {len(dealt_cards)}")


        # Picking up and clicking on individual cards
        for card in PlayingCard.full_deck:
            if x in range(card.x-w, card.x+w) and y in range(card.y-h, card.y+h) and card.flipped:
                card.old_x = card.x
                card.old_y = card.y
                using_card = card
                pick_up_card = True          
                card_stacked = False
                card_slotted = False
                # card stacking mechanic
                for top_card in PlayingCard.full_deck:
                    if using_card in top_card.bottom_cards:
                        top_card.bottom_cards.remove(using_card)

        # shuffle button
        if x in range(shuffle_button_x, shuffle_button_x+151) and y in range(shuffle_button_y,shuffle_button_y+51):
            PlayingCard.shuffle_cards()
            in_game = True
            start_game = True


    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        global pick_up_card, using_card, card_stacked, card_slotted
        global other_slots_x, other_slots_y, all_slots, dealt_cards
        global card_width, card_height
        global columns, columns_x, columns_y

        w = card_width // 2
        h = card_height // 2

        if pick_up_card and using_card != None:

            # slots mechanics
            for i in range(4):
                if x in range(other_slots_x[i]-w, other_slots_x[i]+w) and y in range(other_slots_y-h, other_slots_y+h) and slot_card(using_card, all_slots[i]):
                    card_slotted = True
                    card_stacked = False
                    all_slots[i].append(using_card)
                    using_card.x = other_slots_x[i]
                    using_card.y = other_slots_y
                    using_card.top_cards = []

                    # removing card from other slot lists
                    for j in range(4):
                        if using_card in all_slots[j] and j != i:
                            all_slots[j].remove(using_card)

                    # removing card from column lists
                    for col in range(7):
                        if using_card in columns[col]:
                            columns[col].remove(using_card)

                    # removing card from dealt_cards
                    if using_card in dealt_cards:
                        dealt_cards.remove(using_card)

            # column slot mechanics
            if in_game and using_card.value == 13:
                for i in range(7):
                    if x in range(columns_x[i]-w, columns_x[i]+w) and y in range(columns_y-h, columns_y+h) and columns[i] == []:
                        columns[i].append(using_card)
                        using_card.x = columns_x[i]
                        using_card.y = columns_y
                        card_slotted = True
                        card_stacked = False

                        # removing card from dealt_cards
                        if using_card in dealt_cards:
                            dealt_cards.remove(using_card)

                        for j in range(7):
                            if j != i and using_card in columns[j]:
                                columns[j].remove(using_card) # removing from old column
                                for card in using_card.bottom_cards:
                                    columns[i].append(card) # appending to new column
                                    columns[j].remove(card) # removing from old column

            # card stacking mechanics
            for card in PlayingCard.full_deck:
                if card_collision(card) and card.bottom_cards == [] and cards_stack(card) and card not in deal_slot_cards and card not in dealt_cards:                    
                    card.bottom_cards.append(using_card)
                    card_stacked = True
                    card_slotted = False

                    # removing card from dealt_cards
                    if using_card in dealt_cards:
                        dealt_cards.remove(using_card)

                    # removing cards from slot lists
                    for i in range(4):
                        if using_card in all_slots[i]:
                            all_slots[i].remove(using_card)

                    # removing cards from column lists
                    for i in range(7):
                        if using_card in columns[i]:
                            columns[i].remove(using_card)
                            for c in using_card.bottom_cards:
                                columns[i].remove(c)

                    # appending cards to top_cards list
                    if card not in using_card.top_cards:
                        using_card.top_cards.append(card)

                    # appending cards to bottom_cards list
                    for top_card in PlayingCard.full_deck:
                        if card in top_card.bottom_cards:
                            top_card.bottom_cards.append(using_card)
                            if top_card not in using_card.top_cards:
                                using_card.top_cards.append(top_card)

                    # appending cards to column lists
                    for i in range(7):
                        if card in columns[i]:
                            columns[i].append(using_card)
                            for c in using_card.bottom_cards:
                                columns[i].append(c)

            # Snap back mechanics
            if not card_stacked and not card_slotted:
                using_card.x = using_card.old_x
                using_card.y = using_card.old_y
                if using_card.top_cards != []:
                    c = using_card.top_cards[0] # the first top card
                    c.bottom_cards.insert(0, using_card)
                for card in using_card.top_cards[1:]:
                    card.bottom_cards.append(using_card)
            
            pick_up_card = False

def card_collision(card: PlayingCard) -> bool:
    """
    Checks if using_card and another playing card have collided
    """
    global using_card
    global card_width, card_height
    global deal_slot_x, deal_slot_y, other_slots_x, other_slots_y

    w = card_width
    h = card_height
     
    card_x = (card.x - w // 2, card.x + w // 2)
    card_y = (card.y - h // 2, card.y + h // 2)
    using_x = (using_card.x - w, using_card.x + w)
    using_y = (using_card.y - h, using_card.y + h)

    collision_a = False
    collision_b = False

    if using_card != card and card not in using_card.bottom_cards:
        # cards in placement slots
        for i in range(4):
            if using_card.x in range(other_slots_x[i], other_slots_x[i]+w) and using_card.y in range(other_slots_y, other_slots_y+h):
                return False

        # cards in deal slot
        if using_card.x in range(deal_slot_x-w//2, deal_slot_x+w//2) and using_card.y in range(deal_slot_y-h//2, deal_slot_y+h//2):
            return False

        # normal card collision
        elif using_card.x in range(card_x[0], card_x[1]) and using_card.y in range(card_y[0], card_y[1]):
            collision_a = True
        elif card.x in range(using_x[0], using_x[1]) and card.y in range(using_y[0], using_y[1]):
            collision_b = True

    if collision_a or collision_b:
        return True

    return False


def cards_stack(card: PlayingCard) -> bool:
    """Checks if cards are able to stack based on their values
    """
    global using_card

    if using_card != None:
        red = 'hearts,diamonds'
        black = 'spades,clubs'
        if using_card.value + 1 == card.value:
            if using_card.suite in red and card.suite in black:
                return True
            elif using_card.suite in black and card.suite in red:
                return True

    return False


def slot_card(card: PlayingCard, slot: List[PlayingCard]) -> bool:
    """Checks if given card can be placed into given slot
    """
    if card.bottom_cards == []:
        if card.value == 1 and slot == []:
            return True
        elif slot != [] and card.value - 1 == slot[-1].value and card.suite == slot[-1].suite:
            return True
        else:
            return False
    else:
        return False

def redraw(card: PlayingCard) -> None:
    """Redraws cards in specified order so that the stack of cards is seen properly by the user
    """
    global card_width, card_height
    global card_imgs

    if card.suite == 'hearts' or card.suite == 'diamonds':
        arcade.draw_rectangle_filled(card.x, card.y, card_width, card_height, arcade.color.RED)
        arcade.draw_texture_rectangle(card.x, card.y, card_width, card_height, card.image)                       
    else:
        arcade.draw_rectangle_filled(card.x, card.y, card_width, card_height, arcade.color.BLACK)
        arcade.draw_texture_rectangle(card.x, card.y, card_width, card_height, card.image)
    
    if card.flipped:
        arcade.draw_text(card_names[card.value-1], card.x-card_width//4, card.y, color=arcade.color.WHITE)
        arcade.draw_text(card.suite, card.x-card_width//3, card.y-10, arcade.color.WHITE, font_size=8)
    else:
        arcade.draw_texture_rectangle(card.x, card.y, card_width, card_height, card_imgs["images/blue_back.jpg"])

def main():
    game = MyGame(WIDTH, HEIGHT, "Solitaire")
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()

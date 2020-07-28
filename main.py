import arcade
import random
from typing import List

WIDTH = 800
HEIGHT = 600

start_game = False
pick_up_card = False
using_card = None
card_placed = False

card_width = 40
card_height = 70

deal_slot_x = 57
deal_slot_y = 510

# x coordinates:  x1,  x2,  x3,  x4  
other_slots_x = [550, 600, 650, 700]
other_slots_y = 475

card_names = ['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king']
shuffled_cards = []
deal_slot_cards = []

#     slot:  1   2   3   4
all_slots = [[], [], [], []]

class PlayingCard:
    """Creates and organizes the playing cards
    """
    full_deck = []
    hearts = {}
    diamonds = {}
    spades = {}
    clubs = {}

    def __init__(self, value: int, suite: str, x: int, y: int):
        self.value = value
        self.suite = suite
        self.x = x
        self.y = y
        self.old_x = x
        self.old_y = y
        self.flipped = True
        self.bottom_cards = []
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
        # Create your sprites and sprite lists here
        pass

    def on_draw(self):
        arcade.start_render()
        global start_game
        global card_height, card_height, card_names, shuffled_cards
        global deal_slot_x, deal_slot_y, other_slots_x, other_slots_y

        # draw hearts playing cards
        for card in PlayingCard.hearts.values():
            arcade.draw_rectangle_filled(card.x, card.y, card_width, card_height, arcade.color.RED)

        i = 0
        while i < 13:
            if list(PlayingCard.hearts.values())[i].flipped:
                arcade.draw_text(card_names[i], list(PlayingCard.hearts.values())[i].x-card_width//4, list(PlayingCard.hearts.values())[i].y, color=arcade.color.WHITE)
                arcade.draw_text("hearts", list(PlayingCard.hearts.values())[i].x-card_width//3, list(PlayingCard.hearts.values())[i].y-10, arcade.color.WHITE, font_size=8)
            i += 1

        # draw diamonds playing cards
        for card in PlayingCard.diamonds.values():
            arcade.draw_rectangle_filled(card.x, card.y, card_width, card_height, arcade.color.RED)

        i = 0
        while i < 13:
            if list(PlayingCard.diamonds.values())[i].flipped:
                arcade.draw_text(card_names[i], list(PlayingCard.diamonds.values())[i].x-card_width//4, list(PlayingCard.diamonds.values())[i].y, color=arcade.color.WHITE)
                arcade.draw_text("diamonds", list(PlayingCard.diamonds.values())[i].x-card_width//2, list(PlayingCard.diamonds.values())[i].y-10, color=arcade.color.WHITE, font_size=8)
            i += 1

        # draw spades playing cards
        for card in PlayingCard.spades.values():
            arcade.draw_rectangle_filled(card.x, card.y, card_width, card_height, arcade.color.BLACK)

        i = 0
        while i < 13:
            if list(PlayingCard.spades.values())[i].flipped:
                arcade.draw_text(card_names[i], list(PlayingCard.spades.values())[i].x-card_width//4, list(PlayingCard.spades.values())[i].y, color=arcade.color.WHITE)
                arcade.draw_text("spades", list(PlayingCard.spades.values())[i].x-card_width//3, list(PlayingCard.spades.values())[i].y-10, arcade.color.WHITE, font_size=8)
            i += 1

        # draw clubs playing cards
        for card in PlayingCard.clubs.values():
            arcade.draw_rectangle_filled(card.x, card.y, card_width, card_height, arcade.color.BLACK)

        i = 0
        while i < 13:
            if list(PlayingCard.clubs.values())[i].flipped:
                arcade.draw_text(card_names[i], list(PlayingCard.clubs.values())[i].x-card_width//4, list(PlayingCard.clubs.values())[i].y, color=arcade.color.WHITE)
                arcade.draw_text("clubs", list(PlayingCard.clubs.values())[i].x-card_width//3, list(PlayingCard.clubs.values())[i].y-10, arcade.color.WHITE, font_size=8)
            i += 1

        # redraw card
        
        for card in shuffled_cards:
                if card.suite == 'hearts' or card.suite == 'diamonds':
                    arcade.draw_rectangle_filled(card.x, card.y, card_width, card_height, arcade.color.RED)                       
                else:
                    arcade.draw_rectangle_filled(card.x, card.y, card_width, card_height, arcade.color.BLACK)
                if card.flipped:
                    arcade.draw_text(card_names[card.value-1], card.x-card_width//4, card.y, color=arcade.color.WHITE)
                    arcade.draw_text(card.suite, card.x-card_width//3, card.y-10, arcade.color.WHITE, font_size=8)
                   
        # draw slots for cards
        arcade.draw_rectangle_outline(deal_slot_x, deal_slot_y, card_width, card_height, arcade.color.BLUE)
        for i in range(4):
            arcade.draw_xywh_rectangle_outline(other_slots_x[i], other_slots_y, card_width, card_height, arcade.color.BLUE)

        # draw shuffle button used to shuffle and put the cards into playing formation
        arcade.draw_xywh_rectangle_filled(550, 50, 150, 50, arcade.color.GUPPIE_GREEN)
        arcade.draw_text('Shuffle', 590, 65, arcade.color.BLACK, 20)


    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        """
        global shuffled_cards, deal_slot_cards, all_slots
        global start_game
        global deal_slot_x, deal_slot_y, card_width, card_height
        global using_card

        # after shuffle button is pressed
        if start_game:
            # places the first 28 cards in playing position
            i = 0
            while i < 28:
                for row_num in range(7):
                    for row_len in range(7 - row_num):

                        card = shuffled_cards[i] 
                        start_x = 171 + row_num*57    

                        card.x = start_x + 57 * (row_len)
                        card.y = 400 - card_height // 2 * (row_num) 
                        
                        if row_len == 0:
                            card.flipped = True
                        else:
                            card.flipped = False

                        card.bottom_cards = []

                        i += 1

            # places the remaining cards into the deal slot
            for card in shuffled_cards[28:]:
                deal_slot_cards.append(card)
                card.flipped = True
                card.x = deal_slot_x
                card.y = deal_slot_y
                card.bottom_cards = []

            # empties slot lists
            for i in range(4):
                all_slots[i] = []
            
            start_game = False

        # card stacking
        for top_card in PlayingCard.full_deck:
            if top_card.bottom_cards != []:
                card = top_card.bottom_cards[0]
                card.x = top_card.x
                card.y = top_card.y - card_height // 2

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
        global pick_up_card, using_card
        global deal_slot_x, deal_slot_y, deal_slot_cards, other_slots_x, other_slots_y, all_slots
        global card_height, card_width
        global start_game

        w = card_width // 2
        h = card_height // 2

        # deal slot mechanics         
        if x in range(deal_slot_x-w, deal_slot_x+w) and y in range(deal_slot_y-h, deal_slot_y+h):
            card = deal_slot_cards[-1]            
            card.x = deal_slot_x
            card.y = deal_slot_y - card_height
            deal_slot_cards.remove(card)

        # Picking up and clicking on individual cards
        for card in PlayingCard.full_deck:
            if x in range(card.x-w, card.x+w) and y in range(card.y-h, card.y+h):
                card.old_x = card.x
                card.old_y = card.y
                pick_up_card = True
                using_card = card
                card.flipped = True
                # card stacking mechanic
                for top_card in PlayingCard.full_deck:
                    if card in top_card.bottom_cards:
                        top_card.bottom_cards.remove(card)
                # removing cards from slot lists
                for i in range(4):
                    if using_card in all_slots[i]:
                        print('card removed')
                        print(len(all_slots[i]))
                        all_slots[i].remove(using_card)

        # shuffle button
        if x in range(550, 701) and y in range(50, 101):
            PlayingCard.shuffle_cards()
            start_game = True


    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        global pick_up_card, using_card
        global other_slots_x, other_slots_y
        global card_width, card_height
        global card_placed

        w = card_width
        h = card_height

        if pick_up_card and using_card != None:
            if not card_placed:
                using_card.x = using_card.old_x
                using_card.y = using_card.old_y
            # slots mechanics
            for i in range(4):
                if x in range(other_slots_x[i], other_slots_x[i]+w) and y in range(other_slots_y, other_slots_y+h) and slot_card(using_card, all_slots[i]):
                    print('card placed')
                    all_slots[i].append(using_card)
                    using_card.x = other_slots_x[i] + card_width // 2
                    using_card.y = other_slots_y + card_height // 2

            # card stacking mechanics
            for card in PlayingCard.full_deck:
                if card_collision(card) and card.bottom_cards == [] and cards_stack(card):                    
                        card.bottom_cards.append(using_card)
                        for top_card in PlayingCard.full_deck:
                            if card in top_card.bottom_cards:
                                top_card.bottom_cards.append(using_card)
            
            pick_up_card = False

def card_collision(card: PlayingCard) -> bool:
    """
    Checks if using card and another playing card have collided
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
        # cards in placements slots
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
    """Checks if card can be placed in the slot
    """
    if card.value == 1 and slot == []:
        return True
    elif slot != [] and card.value - 1 == slot[-1].value and card.suite == slot[-1].suite:
        return True
    
    return False

def main():
    PlayingCard.make_cards()
    game = MyGame(WIDTH, HEIGHT, "Solitaire")
    game.setup()
    arcade.run()



if __name__ == "__main__":
    main()


import arcade
import random

WIDTH = 800
HEIGHT = 600

start_game = False
pick_up_card = False
using_card = None

card_width = 40
card_height = 70

deal_slot_x = 57
deal_slot_y = 510

card_names = ['ace', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'jack', 'queen', 'king']
shuffled_cards = []


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
        self.flipped = True
        self.redraw = False
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
        global card_height, card_height, card_names
        global deal_slot_x, deal_slot_y 

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
        for card in PlayingCard.full_deck:
            if card.redraw:
                if card.suite == 'hearts' or card.suite == 'diamonds':
                    arcade.draw_rectangle_filled(card.x, card.y, card_width, card_height, arcade.color.RED)
                    
                else:
                    arcade.draw_rectangle_filled(card.x, card.y, card_width, card_height, arcade.color.BLACK)

                if card.flipped:
                    arcade.draw_text(card_names[card.value-1], card.x-card_width//4, card.y, color=arcade.color.WHITE)
                    arcade.draw_text(card.suite, card.x-card_width//3, card.y-10, arcade.color.WHITE, font_size=8)
            
                
        # draw slots for cards
        arcade.draw_rectangle_outline(deal_slot_x, deal_slot_y, card_width, card_height, arcade.color.BLUE)

        for num in range(4):
            arcade.draw_xywh_rectangle_outline(550 + num*50, 475, card_width, card_height, arcade.color.BLUE)

        # draw shuffle button used to shuffle and put the cards into playing formation
        arcade.draw_xywh_rectangle_filled(550, 50, 150, 50, arcade.color.GUPPIE_GREEN)
        arcade.draw_text('Shuffle', 590, 65, arcade.color.BLACK, 20)


    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        global shuffled_cards, deal_slot_x, deal_slot_y, card_width, card_height
        global start_game

        # playing formation
        if start_game:
            i = 0
            while i < 28:                            # places the first 28 cards in playing position
                for row_num in range(7):
                    for row_len in range(7 - row_num):

                        card = shuffled_cards[i] 
                        end_x = 456    

                        card.x = end_x - 57 * (row_len)
                        card.y = 400 - card_height // 2 * (row_num) 
                        
                        if row_len == 6 - row_num:
                            card.flipped = True
                        else:
                            card.flipped = False
                                                
                        i += 1

            for card in shuffled_cards[28:]:        # places the remaining cards into the deal slot
                card.flipped = False
                card.x = deal_slot_x
                card.y = deal_slot_y

            start_game = False


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
        global deal_slot_x, deal_slot_y
        global card_height, card_height
        global start_game

        # Picking up and clicking on individual cards
        for card in PlayingCard.full_deck:
            if x in range(card.x-card_width//2, card.x+card_width//2) and y in range(card.y-card_height//2, card.y+card_height//2):
                pick_up_card = True
                using_card = card
                # card.flipped = not card.flipped
        
        # Useless deal slot function
        ''' 
        if x in range(deal_slot_x-card_width//2, deal_slot_x+card_width//2) and y in range(deal_slot_y-card_height//2, deal_slot_y+card_height//2):
            for card in PlayingCard.full_deck:
                card.x = deal_slot_x
                card.y = deal_slot_y
        '''

        # shuffle button
        if x in range(550, 701) and y in range(50, 101):
            PlayingCard.shuffle_cards()
            start_game = True


    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        global pick_up_card, using_card

        pick_up_card = False
        using_card = None


def main():
    PlayingCard.make_cards()
    game = MyGame(WIDTH, HEIGHT, "Solataire")
    game.setup()
    arcade.run()
    

if __name__ == "__main__":
    main()


import pygame as pg
from time import sleep
from sys import exit
from random import randint, shuffle
pg.init()

class Algorithm:


    def __init__(self, items, bg_colour = (0, 0, 0), block_colour = (0, 255, 0), speed = 20, phrase = "Bubble Sort Visualised", text_colour = (255, 255, 255), spacing = 1):
        self.index = self.p_index = self.count = self.comparisons = self.current_num_iter = self.is_sorted = 0
        self.items = items
        self.speed = speed
        self.spacing = spacing

        self.screen = self.clock = None

        self.blocks = []

        self.bg_colour = bg_colour
        self.text_colour = text_colour
        self.block_colour = block_colour

        self.phrase = self.make_phrase(phrase)
        self.solved_phrase = phrase

    def create_blocks(self):
        #creates each block object with Rect and adds to block list
        for i, v in enumerate(self.items):
            rect = pg.Rect(0, 0, (self.x-(len(items)*self.spacing))//len(items), v)
            block = Blocks(v, rect, self.block_colour)
            self.blocks.append(block)

    def make_phrase(self, phrase):
        # makes phrase in format to be shuffled with a counter so that it can be sorted later
        self.p_index = 0
        phrase = [[i, char] for i, char in enumerate(phrase)]
        shuffle(phrase)
        return phrase

    def sort_phrase(self):
        # sorts one value then returns to display it
        phrase = self.phrase
        if self.p_index == len(phrase)-1:self.p_index = 0
        if phrase[self.p_index][0] > phrase[self.p_index+1][0]:
            phrase[self.p_index], phrase[self.p_index+1] = phrase[self.p_index+1], phrase[self.p_index] # swapping values
        self.p_index +=1

    def bubble(self):
        # sorts one item at a time, also checks to see if list is sorted
        items = self.items
        j = self.index
        if self.is_sorted == len(items) or j == len(items)-1:
            for block in self.blocks:
                block.colour = (255, 0, 0)
            return
        self.current_num_iter += 1
        self.blocks[j].colour = (255, 0, 0)
        for block in self.blocks:
            if block != self.blocks[j]: block.colour = self.block_colour# makes other blocks green
        if items[j] > items[j+1]:# sorts
            self.is_sorted = 0
            self.comparisons += 1
            items[j], items[j+1] = items[j+1], items[j]

        self.items = items
        self.index +=1
        self.is_sorted +=1
        self.count +=1

        # check other value to be sorted and -2 because you don't check last element
        if j == (len(self.items)-2):
            self.index = 0
            self.is_sorted += 1

    def display_blocks(self):
        # displays all the blocks in the blocks list
        for i, v in enumerate(self.items):
            self.blocks[i].x = i * self.x//len(items)
            self.blocks[i].height = v
        for block in self.blocks:
            rect = block.rect()
            rect.bottom = self.y
            pg.draw.rect(self.screen, block.colour, rect)

    def load_display(self, x=800, y=500, speed=60):
        # loads the screen with variables
        self.x, self.y = x, y
        self.text_template = pg.font.Font(None, self.x//40)
        self.title_template  = pg.font.Font(None, self.x//10)
        self.screen = pg.display.set_mode((x, y))
        self.clock = pg.time.Clock()
        self.create_blocks()
        self.upd_display(speed)

    def upd_display(self, spd):
        # updates the screen
        speed = spd
        main = True
        angle, v = 0, 0.2
        while True:
            # main menu
            if main:
                self.screen.fill((0, 0, 0))
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        exit()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if event.button == 1: main = False
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_r:
                            pg.quit()
                            exit()

                # displays updated phrase
                phrase = self.title_template.render("".join(char[1] for char in self.phrase), False, self.text_colour) # updates phrase
                click = self.text_template.render("Click to Begin", False, (255, 255, 255))
                by = self.text_template.render("By Lucas Reinholc-Gomez", False, (255, 255, 255))
                by = pg.transform.rotate(by, angle)
                self.screen.blit(phrase, phrase.get_rect(center = (self.x//2, self.y//3)))
                self.screen.blit(click, click.get_rect(center = (self.x//2, 14*(self.y//24))))
                self.screen.blit(by, by.get_rect(center = (self.x//2, 3*(self.y//4))))
                self.sort_phrase()

                angle += v
                if angle > 10 or angle < -10:
                    v *= -1

                self.clock.tick(100)

            # Bubble sorting view
            else:
                self.screen.fill(self.bg_colour)
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        pg.quit()
                        exit()
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_d:
                            speed = speed*(10**100)
                            if speed > 10**1000:
                                speed = 10**20
                        if event.key == pg.K_a:
                            speed = speed // 100
                            if speed < 1: speed = 1
                        if event.key == pg.K_r:
                            pg.quit()
                            exit()
                    if event.type == pg.KEYUP:
                        if event.key in (pg.K_d, pg.K_a):
                            speed = spd

                self.bubble()
                self.display_blocks()

                # shows data on the sorting
                a = self.text_template.render(f"{len(self.items)} items", False, (255,255,255))
                b = self.text_template.render(f"{self.current_num_iter} iterations", False, (255,255,255))
                c = self.text_template.render(f"{self.comparisons} comparisons", False, (255,255,255))
                self.screen.blit(a, a.get_rect(center = (90,  20)))
                self.screen.blit(b, b.get_rect(center = (320,  20)))
                self.screen.blit(c, c.get_rect(center = (600,  20)))

                self.clock.tick(speed)
            pg.display.update()

# class for blocks
class Blocks:
    def __init__(self, value, rect, colour):
        self.value = value
        self.x, self.y, self.width, self.height = rect
        self.colour = colour
    def rect(self):
        return pg.Rect(self.x, self.y, self.width, self.height)

if __name__ == "__main__":
    items = [randint(1, 1000) for _ in range(50)]
    #items = [i for i in range(0, 500, 20)]
    shuffle(items)
    sort = Algorithm(items, block_colour = (0, 255, 0))
    sort.load_display(y = 1090, speed = 5, x = 1920) # if you increase fps it also increases the speed of the sorting

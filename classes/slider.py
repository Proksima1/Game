import pygame
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

pygame.init()
win = pygame.display.set_mode((1000, 600))

slider = Slider(win, 100, 100, 800, 40, min=0, max=100, step=1)
output = TextBox(win, 475, 200, 50, 50, fontSize=24)

run = True
while run:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()
    win.fill((255, 255, 255))
    slider.listen(events)
    slider.draw()
    output.setText(slider.getValue())
    output.draw()
    pygame.display.update()

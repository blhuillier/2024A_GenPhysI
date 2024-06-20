'''

    The Solar System Simulation project for General Physics I, Sejong University. 
    The project was done by combining effort of Zwe Htet Aung, NGO THANH DAT and HASSAN AFRIDI.

'''

import pygame
from planets import *
import asyncio

pygame.init()
size = (800, 600)
WIDTH, HEIGHT = size[0], size[1]
WINDOW = pygame.display.set_mode(size)
UNIVERSE_IMG = pygame.image.load('./assets/background.jpg')
UNIVERSE_IMG = pygame.transform.scale(UNIVERSE_IMG, (WIDTH, HEIGHT))
COLOR_WHITE = (255, 255, 255)
COLOR_SUN = (252, 150, 1)
COLOR_MERCURY = (173, 168, 165)
COLOR_VENUS = (227, 158, 28)
COLOR_EARTH = (107, 147, 214)
COLOR_MARS = (193, 68, 14)
COLOR_JUPITER = (216, 202, 157)
COLOR_SATURN = (191, 189, 175)
COLOR_URANUS = (209, 231, 231)
COLOR_NEPTUNE = (63, 84, 186)
COLOR_MOON = (200, 200, 200)

IMG_SUN = pygame.image.load('./assets/sun.png').convert_alpha()
IMG_MOON = pygame.image.load('./assets/moon.png').convert_alpha()
IMG_EARTH = pygame.image.load('./assets/earth.png').convert_alpha()
IMG_JUPITER = pygame.image.load('./assets/jupiter.png').convert_alpha()
IMG_MARS = pygame.image.load('./assets/mars.png').convert_alpha()
IMG_MERCURY = pygame.image.load('./assets/mercury.png').convert_alpha()
IMG_NEPTUNE = pygame.image.load('./assets/neptune.png').convert_alpha()
IMG_SATURN = pygame.image.load('./assets/saturn.png').convert_alpha()
IMG_VENUS = pygame.image.load('./assets/venus.png').convert_alpha()
IMG_URANUS = pygame.image.load('./assets/uranus.png').convert_alpha()


FONT_1 = pygame.font.SysFont("Trebuchet MS", 16)
FONT_2 = pygame.font.SysFont("Trebuchet MS", 12)
pygame.display.set_caption("Solar System Simulation")
elapsed_time = 0

# planets
sun = Planet(0, 0, 30 * Planet.SCALE * 10 ** 9, IMG_SUN, COLOR_SUN, 1.98892 * 10 ** 30)
sun.sun = True

mercury = Planet(-0.387 * Planet.AU, 0, 5 * Planet.SCALE * 10 ** 9, IMG_MERCURY, COLOR_MERCURY, 3.30 * 10 ** 23)
mercury.y_vel = 47.4 * 1000

venus = Planet(-0.723 * Planet.AU, 0, 9 * Planet.SCALE * 10 ** 9, IMG_VENUS, COLOR_VENUS, 4.8685 * 10 ** 24)
venus.y_vel = 35.02 * 1000

earth = Planet(-1 * Planet.AU, 0, 10 * Planet.SCALE * 10 ** 9, IMG_EARTH, COLOR_EARTH, 5.9722 * 10 ** 24)
earth.y_vel = 29.783 * 1000

mars = Planet(-1.524 * Planet.AU, 0, 5 * Planet.SCALE * 10 ** 9, IMG_MARS, COLOR_MARS, 6.39 * 10 ** 23)
mars.y_vel = 24.077 * 1000

jupiter = Planet(-5.204 * Planet.AU, 0, 20 * Planet.SCALE * 10 ** 9, IMG_JUPITER, COLOR_JUPITER, 1.898 * 10 ** 27)
jupiter.y_vel = 13.06 * 1000

saturn = Planet(-9.573 * Planet.AU, 0, 18 * Planet.SCALE * 10 ** 9, IMG_SATURN, COLOR_SATURN, 5.683 * 10 ** 26)
saturn.y_vel = 9.68 * 1000

uranus = Planet(-19.165 * Planet.AU, 0, 14 * Planet.SCALE * 10 ** 9, IMG_URANUS, COLOR_URANUS, 8.681 * 10 ** 25)
uranus.y_vel = 6.80 * 1000

neptune = Planet(-30.178 * Planet.AU, 0, 12 * Planet.SCALE * 10 ** 9, IMG_NEPTUNE, COLOR_NEPTUNE, 1.024 * 10 ** 26)
neptune.y_vel = 5.43 * 1000

moon = Moon(earth, 0.1 * Planet.AU, 5 * Planet.SCALE * 10 ** 9, IMG_MOON, COLOR_MOON)       # changed moon's distance for visual purpose


async def simulation():
    run = True
    pause = False
    show_distance = False
    clock = pygame.time.Clock()
    move_x = 0
    move_y = 0
    draw_line = True

    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus, neptune]
    mercury_energies = []
    venus_energies = []
    earth_energies = []
    mars_energies = []
    time_axis = []

    while run:
        WINDOW.blit(UNIVERSE_IMG, (0,0))
        global elapsed_time


        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and
                                             (event.key == pygame.K_x or event.key == pygame.K_ESCAPE)):
                run = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pause = not pause
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                show_distance = not show_distance
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                draw_line = not draw_line
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                Planet.SCALE *= 0.75
                for planet in planets:
                    planet.update_scale(0.75)
                moon.update_scale(0.75)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                Planet.SCALE *= 1.25
                for planet in planets:
                    planet.update_scale(1.25)
                moon.update_scale(1.25)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP and Planet.TIMESTEP < 24 * 3600 * 4:
                Planet.TIMESTEP *= 2
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN and Planet.TIMESTEP > 24 * 3600 / 2:
                Planet.TIMESTEP /= 2

        for planet in planets:
            if not pause:
                planet.update_position(planets)
                # Collect energy data
                if planet == mercury:
                    mercury_energies.append(planet.E_total)
                elif planet == venus:
                    venus_energies.append(planet.E_total)
                elif planet == earth:
                    earth_energies.append(planet.E_total)
                elif planet == mars:
                    mars_energies.append(planet.E_total)

            if show_distance:
                planet.draw(WINDOW, 1, move_x, move_y, draw_line)
            else:
                planet.draw(WINDOW, 0, move_x, move_y, draw_line)

        if not pause:
            moon.update_position()
            elapsed_time += Planet.TIMESTEP / (24 * 365.4 * 3600)
        moon.draw(WINDOW, move_x, move_y, draw_line)

        # Collect time data
        time_axis.append(elapsed_time)

        fps_text = FONT_1.render("FPS: " + str(int(clock.get_fps())), True, COLOR_WHITE)
        WINDOW.blit(fps_text, (15, 15))
        text_surface = FONT_1.render("Press X or ESC to exit", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 35))
        text_surface = FONT_1.render("Press D to turn on/off distance", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 55))
        text_surface = FONT_1.render("Press S to turn on/off drawing orbit lines", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 75))
        text_surface = FONT_1.render("Use arrow up and down to control the timestep", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 95))
        text_surface = FONT_1.render("Press Space to pause/unpause", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 115))
        text_surface = FONT_1.render("Use scroll-wheel to zoom", True, COLOR_WHITE)
        WINDOW.blit(text_surface, (15, 135))
        sun_surface = FONT_1.render("- Sun", True, COLOR_SUN)
        WINDOW.blit(sun_surface, (15, 185))
        mercury_surface = FONT_1.render("- Mercury", True, COLOR_MERCURY)
        WINDOW.blit(mercury_surface, (15, 205))
        venus_surface = FONT_1.render("- Venus", True, COLOR_VENUS)
        WINDOW.blit(venus_surface, (15, 225))
        earth_surface = FONT_1.render("- Earth", True, COLOR_EARTH)
        WINDOW.blit(earth_surface, (15, 245))
        mars_surface = FONT_1.render("- Mars", True, COLOR_MARS)
        WINDOW.blit(mars_surface, (15, 265))
        jupiter_surface = FONT_1.render("- Jupiter", True, COLOR_JUPITER)
        WINDOW.blit(jupiter_surface, (15, 285))
        saturn_surface = FONT_1.render("- Saturn", True, COLOR_SATURN)
        WINDOW.blit(saturn_surface, (15, 305))
        uranus_surface = FONT_1.render("- Uranus", True, COLOR_URANUS)
        WINDOW.blit(uranus_surface, (15, 325))
        neptune_surface = FONT_1.render("- Neptune", True, COLOR_NEPTUNE)
        WINDOW.blit(neptune_surface, (15, 345))

        time_text = FONT_1.render(f"Timestep: {Planet.TIMESTEP / (24 * 3600)} days", True, COLOR_WHITE)
        WINDOW.blit(time_text, (WIDTH - 150 , 15))
        time_text = FONT_1.render(f"Elapsed Time: {elapsed_time:.2f} years", True, COLOR_WHITE)
        WINDOW.blit(time_text, (WIDTH - 195 , 35))

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()

    

async def main():
    await simulation()

asyncio.run(main())

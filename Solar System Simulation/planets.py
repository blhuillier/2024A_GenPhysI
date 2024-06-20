import pygame
import math

pygame.init()
FONT_2 = pygame.font.SysFont("Trebuchet MS", 12)
COLOR_WHITE = (255, 255, 255)
WIDTH, HEIGHT = 800, 600

class Planet:
    AU = 149.6e6 * 1000  # Astronomical unit
    G = 6.67428e-11  # Gravitational constant
    TIMESTEP = 12 * 3600  # Seconds in 12 hours
    SCALE = 130 / AU

    def __init__(self, x, y, radius, image, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.image = image
        self.color = color
        self.mass = mass
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0
        self.x_vel = 0
        self.y_vel = 0
        self.vel = 0
        self.E_K = 0
        self.E_P = 0

    def draw(self, window, show, move_x, move_y, draw_line):
        size = (2 * self.radius, 2 * self.radius)
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x + move_x, y + move_y))
            if draw_line:
                pygame.draw.lines(window, self.color, False, updated_points, 1)

        self.image = pygame.transform.scale(self.image, size)  # render images
        draw_rect = self.image.get_rect(center = (x, y))

        window.blit(self.image, draw_rect)

        if not self.sun:
            distance_text = FONT_2.render(f"{round(self.distance_to_sun * 1.057 * 10 ** -16, 8)} light years", True, COLOR_WHITE)
            if show:
                window.blit(distance_text, (int(x) - distance_text.get_width() / 2 + move_x,
                                            int(y) - distance_text.get_height() / 2 - 20 + move_y))

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)             # Pythagorean's Theorem
        if other.sun:
            self.distance_to_sun = distance
        force = self.G * self.mass * other.mass / distance ** 2             # Newton's Law
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force                   
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        self.x_vel += total_fx / self.mass * self.TIMESTEP                  # F = ma -> a = F / m
        self.y_vel += total_fy / self.mass * self.TIMESTEP
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))
        self.calculate_energy()

    def update_scale(self, scale):
        self.radius *= scale

    def calculate_energy(self):
        sun_mass = 1.98892 * 10 ** 30
        self.vel = math.sqrt(self.x_vel ** 2 + self.y_vel ** 2)
        self.E_K = 0.5 * self.mass * self.vel ** 2

        if self.distance_to_sun == 0:
            self.E_P = 0  # Set gravitational potential energy to 0 if distance is 0
        else:
            self.E_P = - self.G * self.mass * sun_mass / self.distance_to_sun

        self.E_total = self.E_K + self.E_P


class Moon:
    def __init__(self, planet, distance, radius, image, color):
        self.planet = planet
        self.distance = distance  # distance from the planet in meters
        self.radius = radius
        self.color = color
        self.image = image
        self.angle = 0
        self.x = self.planet.x + self.distance
        self.y = self.planet.y
        self.orbit = []

    def draw(self, window, move_x, move_y, draw_line):
        size = (2 * self.radius, 2 * self.radius)
        x = self.x * Planet.SCALE + WIDTH / 2
        y = self.y * Planet.SCALE + HEIGHT / 2
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                px, py = point
                px = px * Planet.SCALE + WIDTH / 2
                py = py * Planet.SCALE + HEIGHT / 2
                updated_points.append((px + move_x, py + move_y))
            if draw_line:
                pygame.draw.lines(window, self.color, False, updated_points, 1)

        self.image = pygame.transform.scale(self.image, size)  # render images
        draw_rect = self.image.get_rect(center = (x, y))
        window.blit(self.image, draw_rect)

    def update_position(self):
        self.angle += 2 * math.pi / (27.3 * 24 * 3600 / Planet.TIMESTEP)  # Moon's orbit period is 27.3 days
        self.x = self.planet.x + self.distance * math.cos(self.angle)
        self.y = self.planet.y + self.distance * math.sin(self.angle)
        self.orbit.append((self.x, self.y))

    def update_scale(self, scale):
        self.radius *= scale




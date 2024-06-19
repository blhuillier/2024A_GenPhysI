import numpy as np
import pygame

# Initialize Pygame
pygame.init()

WIDTH, HEIGHT = 800, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravitation Pull Simulation")

# Define colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
LIGHT_BLUE = (173, 216, 230)
DARK_BLUE = (0, 0, 139)
BLACK = (0, 0, 0)

FONT = pygame.font.SysFont("comicsans", 16)
INPUT_FONT = pygame.font.SysFont("comicsans", 32)

comet_radius = 10
comets = []
cosmic_objects = []

AU = 149.6e6 * 1000  # One Astronomical Unit in meters
INITIAL_SCALE = 250 / AU  # Initial scale for visualization (1 AU = 250 pixels)
G = 6.67430e-11  # gravitational constant, m^3 kg^-1 s^-2
TIMESTEP = 86400 / 2  # one day in seconds
SCALE = INITIAL_SCALE


class CelestialObject:
    def __init__(self, x, y, radius, color, mass, velocity=None, fixed=False):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.fixed = fixed
        self.orbit = []
        self.vel = np.array(velocity if velocity else [0, 0], dtype="float64")

    def update_position(self, objects):
        if not self.fixed:
            total_fx = total_fy = 0
            for obj in objects:
                if obj == self:
                    continue
                fx, fy = self.calculate_gravitational_force(obj)
                total_fx += fx
                total_fy += fy
            self.vel[0] += total_fx / self.mass * TIMESTEP
            self.vel[1] += total_fy / self.mass * TIMESTEP
            self.x += self.vel[0] * TIMESTEP
            self.y += self.vel[1] * TIMESTEP
            if len(self.orbit) >= 10000:
                self.orbit.pop(0)
            self.orbit.append((self.x, self.y))

    def calculate_gravitational_force(self, other):
        distance_x = other.x - self.x
        distance_y = other.y - self.y
        distance = np.sqrt(distance_x**2 + distance_y**2)
        if distance == 0:
            return 0, 0  # Avoid division by zero
        force = G * self.mass * other.mass / distance**2
        theta = np.arctan2(distance_y, distance_x)
        force_x = np.cos(theta) * force
        force_y = np.sin(theta) * force
        return force_x, force_y

    def draw(self, win, scale):
        x = self.x * scale + WIDTH / 2
        y = self.y * scale + HEIGHT / 2
        pygame.draw.circle(win, self.color, (int(x), int(y)), self.radius)

    def draw_path(self, win, color, scale):
        if len(self.orbit) > 1:
            for i in range(len(self.orbit) - 1):
                start_pos = (
                    self.orbit[i][0] * scale + WIDTH / 2,
                    self.orbit[i][1] * scale + HEIGHT / 2,
                )
                end_pos = (
                    self.orbit[i + 1][0] * scale + WIDTH / 2,
                    self.orbit[i + 1][1] * scale + HEIGHT / 2,
                )
                if i % 2 == 0:  # Draw every second segment
                    pygame.draw.line(win, color, start_pos, end_pos, 2)


def check_collision(comet, objects):
    for obj in objects:
        if obj == comet:
            continue
        distance = np.sqrt((comet.x - obj.x) ** 2 + (comet.y - obj.y) ** 2)
        if distance <= (comet.radius + obj.radius) * SCALE:
            return True
    return False


def draw_text_input_box(prompt, input_text, pos):
    pygame.draw.rect(WIN, WHITE, pos)
    pygame.draw.rect(WIN, BLACK, pos, 2)
    prompt_surface = INPUT_FONT.render(prompt, True, WHITE)
    input_surface = INPUT_FONT.render(input_text, True, BLACK)
    WIN.blit(prompt_surface, (pos[0] + 10, pos[1] - 40))
    WIN.blit(input_surface, (pos[0] + 10, pos[1] + 10))


def add_comet_form():
    input_boxes = [
        {"prompt": "Distance from Sun (AU):", "input_text": "", "value": None},
        {"prompt": "Velocity (m/s):", "input_text": "", "value": None},
        {"prompt": "Position angle (degrees):", "input_text": "", "value": None},
        {"prompt": "Direction (degrees):", "input_text": "", "value": None},
    ]

    active_box = 0
    input_rect = pygame.Rect(WIDTH / 2 - 200, HEIGHT / 2 - 100, 400, 50)

    adding_comet = True
    while adding_comet:
        WIN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if active_box < len(input_boxes) - 1:
                        active_box += 1
                    else:
                        try:
                            distance_au = float(input_boxes[0]["input_text"])
                            velocity = float(input_boxes[1]["input_text"])
                            angle_deg = float(input_boxes[2]["input_text"])
                            direction = float(input_boxes[3]["input_text"])
                            adding_comet = False
                            add_comet(distance_au, velocity, angle_deg, direction)
                        except ValueError:
                            pass
                elif event.key == pygame.K_BACKSPACE:
                    input_boxes[active_box]["input_text"] = input_boxes[active_box][
                        "input_text"
                    ][:-1]
                else:
                    input_boxes[active_box]["input_text"] += event.unicode

        for i, box in enumerate(input_boxes):
            draw_text_input_box(
                box["prompt"], box["input_text"], input_rect.move(0, i * 60)
            )

        pygame.display.update()


def add_comet(distance_au, velocity, angle_deg, direction):
    angle_rad = np.radians(angle_deg - 90)
    direction_rad = np.radians(direction - 180)
    distance = distance_au * AU
    x = distance * np.cos(angle_rad)
    y = distance * np.sin(angle_rad)
    vx = -velocity * np.sin(direction_rad)
    vy = velocity * np.cos(direction_rad)

    comet = CelestialObject(
        x, y, comet_radius, LIGHT_BLUE, 1e4, [vx, vy]
    )  # Arbitrary mass for comet
    comets.append(comet)


def increase_scale():
    global SCALE
    SCALE *= 1.1


def decrease_scale():
    global SCALE
    SCALE /= 1.1


def main():
    run = True
    clock = pygame.time.Clock()
    mercury = CelestialObject(
        0.387 * AU, 0, 3, DARK_GREY, 3.30 * 10**23, [0, 47.87 * 1000]
    )
    venus = CelestialObject(0.723 * AU, 0, 5, WHITE, 4.8685 * 10**24, [0, 35.02 * 1000])
    earth = CelestialObject(-1 * AU, 0, 6, BLUE, 5.9724 * 10**24, [0, 29.78 * 1000])
    mars = CelestialObject(-1.524 * AU, 0, 4, RED, 6.417 * 10**23, [0, 24.077 * 1000])
    jupiter = CelestialObject(
        5.2 * AU, 0, 11, ORANGE, 1.898 * 10**27, [0, 13.07 * 1000]
    )
    saturn = CelestialObject(9.58 * AU, 0, 9, YELLOW, 5.683 * 10**26, [0, 9.69 * 1000])
    uranus = CelestialObject(
        19.22 * AU, 0, 8, LIGHT_BLUE, 8.681 * 10**25, [0, 6.81 * 1000]
    )
    neptune = CelestialObject(
        30.05 * AU, 0, 8, DARK_BLUE, 1.024 * 10**26, [0, 5.43 * 1000]
    )
    sun = CelestialObject(0, 0, 20, YELLOW, 1.98892 * 10**30, [0, 0], fixed=True)

    global cosmic_objects
    cosmic_objects = [
        mercury,
        venus,
        earth,
        mars,
        jupiter,
        saturn,
        uranus,
        neptune,
        sun,
    ]

    while run:
        clock.tick(60)  # Set the clock rate to 60 FPS
        WIN.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_k:
                    add_comet_form()
                elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                    increase_scale()
                elif event.key == pygame.K_MINUS or event.key == pygame.K_UNDERSCORE:
                    decrease_scale()

        for comet in comets[:]:
            comet.update_position(cosmic_objects + comets)
            comet.draw(WIN, SCALE)
            comet.draw_path(WIN, LIGHT_BLUE, SCALE)

        for celestial in cosmic_objects:
            celestial.update_position(cosmic_objects + comets)
            celestial.draw(WIN, SCALE)

        pygame.display.update()


main()
pygame.quit()

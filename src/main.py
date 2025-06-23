# Example file showing a basic pygame "game loop"
import pygame
import random
import os
from fox import FoxClass
from squirrel import SquirrelClass
from hunter import HunterClass
from projectile import Projectile
from explosion import Explosion
from muzzle_flash import MuzzleFlash
from environment import Environment
from witch import WitchClass

print("Imports done")

# pygame setup
pygame.init()
print("Pygame initialized")
pygame.mixer.init()
pygame.font.init()

XSIZE = 1280
YSIZE = 720
screen = pygame.display.set_mode((XSIZE, YSIZE))

BACKGROUND = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'bg.png'))
BACKGROUND = pygame.transform.scale(BACKGROUND, (XSIZE, YSIZE))

GRID_WIDTH = XSIZE // 50
GRID_HEIGHT = YSIZE // 50
GRID_SIZE = XSIZE // GRID_WIDTH
TOTAL_OBSTACLES = 20
MIN_BLOBS = 2
MAX_BLOBS = 4

ROCK_IMAGE_1 = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'rock1.png'))
ROCK_IMAGE_1 = pygame.transform.scale(ROCK_IMAGE_1, (GRID_SIZE, GRID_SIZE))

ROCK_IMAGE_2 = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'rock2.png'))
ROCK_IMAGE_2 = pygame.transform.scale(ROCK_IMAGE_2, (GRID_SIZE, GRID_SIZE))

ROCK_IMAGE_3 = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'rock3.png'))
ROCK_IMAGE_3 = pygame.transform.scale(ROCK_IMAGE_3, (GRID_SIZE, GRID_SIZE))

ROCK_IMAGE_4 = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'rock4.png'))
ROCK_IMAGE_4 = pygame.transform.scale(ROCK_IMAGE_4, (GRID_SIZE, GRID_SIZE))

ROCK_IMAGE_5 = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'rock5.png'))
ROCK_IMAGE_5 = pygame.transform.scale(ROCK_IMAGE_5, (GRID_SIZE, GRID_SIZE))

ROCK_IMAGE_LIST = [ROCK_IMAGE_1, ROCK_IMAGE_2, ROCK_IMAGE_3, ROCK_IMAGE_4, ROCK_IMAGE_5]

FOX_WIDTH = round(XSIZE/20)
FOX_HEIGHT = round(XSIZE/20)
FOX_IMAGE = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'fox.png'))
FOX_IMAGE = pygame.transform.flip(
    pygame.transform.scale(FOX_IMAGE, (FOX_WIDTH, FOX_HEIGHT)), 
    True, False)
FOX_IMAGE_RIGHT = FOX_IMAGE
FOX_IMAGE_LEFT = pygame.transform.flip(FOX_IMAGE, True, False)

STEP_LENGTH = round(XSIZE/175)
JUMP_LENGTH = STEP_LENGTH * 25
FOX_MAX_STAMINA = 100
FOX_MAX_HEALTH = 100
FOX_STAMINA_RECOVERY = 5
JUMP_STAMINA_REQUIREMENT = 25

BAR_WIDTH = 200
BAR_HEIGHT = 25
BAR_MARGIN = 20

SQUIRREL_WIDTH = round(XSIZE/25)
SQUIRREL_HEIGHT = round(XSIZE/25)
SQUIRREL_IMAGE = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'squirrel.png'))
SQUIRREL_IMAGE = pygame.transform.scale(SQUIRREL_IMAGE, (SQUIRREL_WIDTH, SQUIRREL_HEIGHT))

BULLET_SPEED = 8
BULLET_WIDTH = 10
BULLET_IMAGE = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'bullet.png'))
BULLET_IMAGE = pygame.transform.scale(BULLET_IMAGE, (BULLET_WIDTH, BULLET_WIDTH))

HUNTER_WIDTH = round(XSIZE/15)
HUNTER_HEIGHT = round(XSIZE/15)
HUNTER_STEP_LENGTH = 8
HUNTER_IMAGE = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'hunter.png'))
HUNTER_IMAGE = pygame.transform.scale(HUNTER_IMAGE, (HUNTER_WIDTH, HUNTER_HEIGHT))

WITCH_WIDTH = round(XSIZE/20)
WITCH_HEIGHT = round(XSIZE/20)
WITCH_STEP_LENGTH = 8
WITCH_AOE_RADIUS = 75
WITCH_ATTACK_DURATION = 600
WITCH_IMAGE = pygame.image.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'witch.png'))
WITCH_IMAGE = pygame.transform.scale(WITCH_IMAGE, (WITCH_WIDTH, WITCH_HEIGHT))


pygame.display.set_caption("My first game")
clock = pygame.time.Clock()

BLACK = (0,0,0)
WHITE = (255,255,255)
FPS = 60

SCORE_FONT = pygame.font.SysFont('comicsans', 40)

#WALK_SOUND1 = pygame.mixer.Sound(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'grass1.mp3'))
#WALK_SOUND2 = pygame.mixer.Sound(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'grass2.mp3'))
FOX_JUMPING_SOUND = pygame.mixer.Sound(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'fox_jumping.mp3'))
FOX_EATS_SOUND = pygame.mixer.Sound(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'fox_eating.mp3'))
FOX_HIT_SOUND = pygame.mixer.Sound(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'fox_hit.mp3'))
FOX_OUT_OF_STAMINA_SOUND = pygame.mixer.Sound(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'fox_breathing.mp3'))
HUNTER_SPAWNING_SOUND = pygame.mixer.Sound(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'hunter_spawning.mp3'))
HUNTER_SHOOTING_SOUND = pygame.mixer.Sound(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'hunter_shooting.mp3'))
DYING_SOUND = pygame.mixer.Sound(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'dying.mp3'))



def draw_window(player_score, hunters, squirrel_npc, fox_player, projectiles, explosions, muzzle_flashes, env, witches, aoe_list):

    screen.blit(BACKGROUND,(0,0))
    screen.blit(SQUIRREL_IMAGE, squirrel_npc.pos)
    for hunter in hunters:
        screen.blit(HUNTER_IMAGE, hunter.pos)

    for witch in witches:
        screen.blit(WITCH_IMAGE, witch.pos)
        witch.draw_teleport_trail(screen, pygame)

    score_text = SCORE_FONT.render("Score: " + str(player_score), 1, WHITE)
    screen.blit(score_text, (10,0))

    if(fox_player.latest_horizontal=="right"):
        screen.blit(FOX_IMAGE_RIGHT, fox_player.pos)
    elif(fox_player.latest_horizontal=="left"):
        screen.blit(FOX_IMAGE_LEFT, fox_player.pos)

    for projectile in projectiles:
        screen.blit(BULLET_IMAGE, projectile.pos)

    for aoe in aoe_list:
        aoe.draw(screen)

    for explosion in explosions:
        still_animating = explosion.draw(screen)
        if not still_animating:
            explosions.remove(explosion)

    for muzzle_flash in muzzle_flashes:
        still_animating = muzzle_flash.draw(screen)
        if not still_animating:
            muzzle_flashes.remove(muzzle_flash)

    env.draw(screen, ROCK_IMAGE_LIST)

    fox_player.draw_jump_trail(screen, pygame=pygame)

    draw_bars(fox_player)

    # flip() the display to put your work on screen
    pygame.display.flip()
    

def draw_status_bar(current_value, max_value, x, y, width, height, fill_color):
    # Clamp value ratio between 0.0 and 1.0
    ratio = max(0, min(current_value / max_value, 1))

    # Colors
    bar_bg_color = (50, 50, 50)         # Dark gray background
    bar_border_color = (255, 255, 255)  # White border

    # Background rectangle
    bg_rect = pygame.Rect(x, y, width, height)
    pygame.draw.rect(screen, bar_bg_color, bg_rect)

    # Filled portion
    fill_width = int(width * ratio)
    fill_rect = pygame.Rect(x, y, fill_width, height)
    pygame.draw.rect(screen, fill_color, fill_rect)

    # Border
    pygame.draw.rect(screen, bar_border_color, bg_rect, 2)

def draw_bars(fox_player):

    x = XSIZE - BAR_WIDTH - BAR_MARGIN
    stamina_y = BAR_MARGIN  # Stamina at the bottom-right corner
    health_y = stamina_y + BAR_HEIGHT + 5     # Health 5px above stamina

    draw_status_bar(
        current_value=fox_player.health,
        max_value=FOX_MAX_HEALTH,
        x=x,
        y=health_y,
        width=BAR_WIDTH,
        height=BAR_HEIGHT,
        fill_color=(220, 20, 60)  # Crimson red for health
    )

    draw_status_bar(
        current_value=fox_player.stamina,
        max_value=FOX_MAX_STAMINA,
        x=x,
        y=stamina_y,
        width=BAR_WIDTH,
        height=BAR_HEIGHT,
        fill_color=(50, 205, 50)  # Lime green for stamina
    )



def check_eat(fox_player, squirrel_npc):
    fox_rect = pygame.Rect(fox_player.pos[0], fox_player.pos[1], FOX_WIDTH, FOX_HEIGHT)
    squirrel_rect = pygame.Rect(squirrel_npc.pos[0], squirrel_npc.pos[1], SQUIRREL_WIDTH, SQUIRREL_HEIGHT)

    return fox_rect.colliderect(squirrel_rect)

def check_jumping_eat(fox_player, squirrel_npc):
    fox_x, fox_y = fox_player.pos
    squirrel_x, squirrel_y = squirrel_npc.pos

    jump_length = fox_player.jump_length
    steps = 10
    step_size = jump_length / steps

    dx, dy = fox_player.get_direction_vector()

    for _ in range(steps):
        fox_x += dx * step_size
        fox_y += dy * step_size

        fox_x = max(0, min(fox_player.x_max, fox_x))
        fox_y = max(0, min(fox_player.y_max, fox_y))

        fox_rect = pygame.Rect(fox_x, fox_y, FOX_WIDTH, FOX_HEIGHT)
        squirrel_rect = pygame.Rect(squirrel_x, squirrel_y, SQUIRREL_WIDTH, SQUIRREL_HEIGHT)

        if fox_rect.colliderect(squirrel_rect):
            return True

    return False


def check_bullet_collision(projectile, fox_player):
    proj_x, proj_y = projectile.pos
    proj_rect = pygame.Rect(proj_x, proj_y, BULLET_WIDTH, BULLET_WIDTH)
    fox_rect = pygame.Rect(fox_player.pos[0], fox_player.pos[1], FOX_WIDTH, FOX_HEIGHT)
    return proj_rect.colliderect(fox_rect)
    


def main():


    env = Environment(
        grid_width=GRID_WIDTH,
        grid_height=GRID_HEIGHT,
        grid_size=GRID_SIZE,
        total_obstacles=TOTAL_OBSTACLES,
        min_blobs=MIN_BLOBS,
        max_blobs=MAX_BLOBS
    )

    fox_player = FoxClass(
        position=(round(XSIZE / 2), round(YSIZE / 2)),
        direction="right",
        step_length=STEP_LENGTH,
        jump_length=JUMP_LENGTH,
        x_max=XSIZE - FOX_WIDTH,
        y_max=YSIZE - FOX_HEIGHT,
        latest_horizontal="right",
        stamina=FOX_MAX_STAMINA,
        health=FOX_MAX_HEALTH,
        jump_stamina=JUMP_STAMINA_REQUIREMENT,
        env=env,
        width=FOX_WIDTH,
        height=FOX_HEIGHT
    )

    squirrel_npc = SquirrelClass(
        x_max=XSIZE - SQUIRREL_WIDTH,
        y_max=YSIZE - SQUIRREL_HEIGHT,
        env=env,
        width=SQUIRREL_WIDTH,
        height=SQUIRREL_HEIGHT
    )

    # hunter_npc = HunterClass(
    #     x_max=XSIZE - HUNTER_WIDTH,
    #     y_max=YSIZE - HUNTER_HEIGHT,
    #     step_length=HUNTER_STEP_LENGTH,
    #     bullet_speed=BULLET_SPEED,
    #     width=HUNTER_WIDTH,
    #     height=HUNTER_HEIGHT,
    #     env=env
    #)

    witch_npc =  WitchClass(
        x_max=XSIZE - WITCH_WIDTH,
        y_max=YSIZE - WITCH_HEIGHT,
        step_length=WITCH_STEP_LENGTH,
        width=WITCH_WIDTH,
        height=WITCH_HEIGHT,
        env=env,
        aoe_radius=WITCH_AOE_RADIUS,
        duration=WITCH_ATTACK_DURATION
    )

    hunters = []
    witches = [witch_npc]
    projectiles = []
    explosions = []
    muzzle_flashes = []
    aoe_list = []

    print("Top of main")

    show_title_menu(screen, SCORE_FONT)

    running = True
    counter = 0
    player_score = 0


    while running:
        counter += 1
        has_eaten = False
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    jump_return = fox_player.jump(FOX_JUMPING_SOUND)
                    if jump_return=="SUCCESS":
                        has_eaten = check_jumping_eat(fox_player, squirrel_npc)
                    elif jump_return=="NO STAMINA":
                        FOX_OUT_OF_STAMINA_SOUND.play()
                    elif jump_return=="BLOCKED":
                        pass
        
        keys_pressed = pygame.key.get_pressed()
        fox_player.handle_movement(keys_pressed=keys_pressed, pygame=pygame)

        if(not has_eaten):
            has_eaten = check_eat(fox_player, squirrel_npc)

        if(has_eaten):
            FOX_EATS_SOUND.play()
            player_score += 1
            if(player_score % 10 == 0):
                if random.random() < 0.5:
                    new_hunter = hunter_npc = HunterClass(
                        x_max=XSIZE - HUNTER_WIDTH,
                        y_max=YSIZE - HUNTER_HEIGHT,
                        step_length=HUNTER_STEP_LENGTH,
                        bullet_speed=BULLET_SPEED,
                        width=HUNTER_WIDTH,
                        height=HUNTER_HEIGHT,
                        env=env
                    )
                    hunters.append(new_hunter)
                    HUNTER_SPAWNING_SOUND.play()
                else:
                    new_witch =  WitchClass(
                        x_max=XSIZE - WITCH_WIDTH,
                        y_max=YSIZE - WITCH_HEIGHT,
                        step_length=WITCH_STEP_LENGTH,
                        width=WITCH_WIDTH,
                        height=WITCH_HEIGHT,
                        env=env,
                        aoe_radius=WITCH_AOE_RADIUS,
                        duration=WITCH_ATTACK_DURATION
                    )
                    witches.append(new_witch)
            squirrel_npc.spawn()

        if(counter % 25 == 0):
            squirrel_npc.jitter_walk()
            fox_player.stamina_recovery(stamina_recovery=FOX_STAMINA_RECOVERY, max_stamina=FOX_MAX_STAMINA)

        if(counter % 10 == 0):
            for hunter in hunters:
                hunter.walk(fox_player.pos)
                shot = hunter.attack(fox_pos=fox_player.pos, projectile_list=projectiles)
                if(shot):
                    explosions.append(MuzzleFlash((hunter.pos[0] + (HUNTER_WIDTH // 2), hunter.pos[1] +  (HUNTER_HEIGHT // 2)), pygame))
                    HUNTER_SHOOTING_SOUND.play()
            
            for witch in witches:
                witch.walk(fox_player.pos)
                spell_cast = witch.attack(fox_pos=fox_player.pos, aoe_list=aoe_list)
                if(spell_cast):
                    pass # here play sound

        for projectile in list(projectiles):  # Copy to allow removal during iteration
            projectile.move()
            if not (0 <= projectile.pos[0] <= XSIZE and 0 <= projectile.pos[1] <= YSIZE):
                projectiles.remove(projectile)
            elif not env.is_walkable(projectile.pos, BULLET_WIDTH, BULLET_WIDTH):
                projectiles.remove(projectile)
            else:
                # Check collision with fox
                if(check_bullet_collision(projectile, fox_player)):
                    print("Fox hit!")
                    explosions.append(Explosion((fox_player.pos[0] + (FOX_WIDTH // 2), fox_player.pos[1] + (FOX_HEIGHT // 2)), pygame))
                    fox_player.hit()
                    FOX_HIT_SOUND.play()
                    projectiles.remove(projectile)

        # Update AoE spells
        for aoe in list(aoe_list):
            if aoe.is_fox_in_range(fox_player.pos):
                fox_player.hit_small()  # Or any effect you want

            if not aoe.update():
                aoe_list.remove(aoe)


        if(fox_player.health <= 0):
            running = False
            DYING_SOUND.play()
            break

        draw_window(player_score, hunters, squirrel_npc, fox_player, projectiles, explosions, muzzle_flashes, env, witches, aoe_list)

        clock.tick(FPS)  # limits FPS to 60
    
    draw_game_over(screen, final_score=player_score, font=SCORE_FONT)
    pygame.time.delay(3000)

    player_name = get_player_name(screen, SCORE_FONT, player_score, hunters, squirrel_npc, fox_player, projectiles, explosions, muzzle_flashes, env, witches, aoe_list)
    save_high_score(player_name, player_score)

    show_high_scores(screen, SCORE_FONT, "high_scores.txt", player_score, hunters, squirrel_npc, fox_player, projectiles, explosions, muzzle_flashes, env, witches, aoe_list)
    pygame.time.delay(5000)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                main()

    pygame.quit()


def show_title_menu(screen, font):
    screen.blit(BACKGROUND,(0,0))

    overlay = pygame.Surface((XSIZE, YSIZE))
    overlay.set_alpha(180)
    overlay.fill((50, 50, 50))
    screen.blit(overlay, (0, 0))

    game_over_font = pygame.font.SysFont('comicsans', 80)
    game_over_text = game_over_font.render("Leap of the Fox", True, (255, 255, 255))
    text_rect = game_over_text.get_rect(center=(XSIZE // 2, YSIZE // 2 - 50))
    screen.blit(game_over_text, text_rect)

    score_text = font.render(f"Press any key to start", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(XSIZE // 2, YSIZE // 2 + 20))
    screen.blit(score_text, score_rect)

    pygame.display.flip()

    waiting = True
    while (waiting):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False
        clock.tick(FPS)


def draw_game_over(screen, final_score, font):
    overlay = pygame.Surface((XSIZE, YSIZE))
    overlay.set_alpha(180)
    overlay.fill((50, 50, 50))
    screen.blit(overlay, (0, 0))

    game_over_font = pygame.font.SysFont('comicsans', 80)
    game_over_text = game_over_font.render("GAME OVER", True, (255, 255, 255))
    text_rect = game_over_text.get_rect(center=(XSIZE // 2, YSIZE // 2 - 50))
    screen.blit(game_over_text, text_rect)

    score_text = font.render(f"Final Score: {final_score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(XSIZE // 2, YSIZE // 2 + 20))
    screen.blit(score_text, score_rect)

    pygame.display.flip()

def get_player_name(screen, font, final_score, hunters, squirrel_npc, fox_player, projectiles, explosions, muzzle_flashes, env, witches, aoe_list):
    name = ""
    active = True
    input_box = pygame.Rect(XSIZE // 2 - 125, YSIZE // 2 + 80, 250, 75)
    clock = pygame.time.Clock()

    # Redraw the game window and overlay
    draw_window(final_score, hunters, squirrel_npc, fox_player, projectiles, explosions, muzzle_flashes, env, witches, aoe_list)
    overlay = pygame.Surface((XSIZE, YSIZE))
    overlay.set_alpha(180)
    overlay.fill((50, 50, 50))
    screen.blit(overlay, (0, 0))

    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "Anonymous"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    if len(name) < 12:
                        name += event.unicode

        # Draw prompt text
        prompt = font.render("Enter your name:", True, (255, 255, 255))
        screen.blit(prompt, (XSIZE // 2 - prompt.get_width() // 2, YSIZE // 2 + 20))

        # Draw solid grey background inside input box
        pygame.draw.rect(screen, (100, 100, 100), input_box)           # Solid grey box
        pygame.draw.rect(screen, (255, 255, 255), input_box, 2)        # White border

        # Render typed text
        text_surface = font.render(name, True, (255, 255, 255))
        screen.blit(text_surface, (input_box.x + 10, input_box.y + 20))

        # Update display
        pygame.display.flip()
        clock.tick(30)

    return name if name else "Anonymous"



def save_high_score(name, score, filename="high_scores.txt"):
    with open(filename, "a") as file:
        file.write(f"{name}: {score}\n")

def show_high_scores(screen, font, filename, final_score, hunters, squirrel_npc, fox_player, projectiles, explosions, muzzle_flashes, env, witches, aoe_list):
    if not os.path.exists(filename):
        return

    with open(filename, "r") as file:
        scores = [line.strip() for line in file.readlines() if line.strip()]

    scores = sorted(scores, key=lambda x: int(x.split(": ")[1]), reverse=True)
    top_scores = scores[:10]

    draw_window(final_score, hunters, squirrel_npc, fox_player, projectiles, explosions, muzzle_flashes, env, witches, aoe_list)
    overlay = pygame.Surface((XSIZE, YSIZE))
    overlay.set_alpha(180)
    overlay.fill((50, 50, 50))
    screen.blit(overlay, (0, 0))

    y_offset = 100
    header = font.render("High Scores", True, (255, 255, 0))
    screen.blit(header, (XSIZE // 2 - header.get_width() // 2, y_offset))

    for i, score_line in enumerate(top_scores):
        text = font.render(score_line, True, (255, 255, 255))
        screen.blit(text, (XSIZE // 2 - text.get_width() // 2, y_offset + 55 + i * 40))

    pygame.display.flip()



if __name__ == "__main__":
    main()

import pygame

pygame.init()
size = (888, 500)
Screen = pygame.display.set_mode(size)
pygame.display.set_caption("Hit The Zombie")
icon = pygame.image.load("./dino/icon.png")
pygame.display.set_icon(icon)
walk_rt = [pygame.image.load(f"./dino/Walk ({i}).png") for i in range(1, 11)]
walk_lt = [pygame.image.load(f"./dino/LWalk ({i}).png") for i in range(1, 11)]
bkg = pygame.image.load("./dino/bkg.jpg")
char_idle = [pygame.image.load("./dino/Idle.png"),
             pygame.image.load("./dino/L_Idle.png")]
fireball = [pygame.image.load("./dino/Bullet.png"),
            pygame.image.load("./dino/LBullet.png")]
menu_icon = pygame.image.load("./dino/Menu.png")
rules_page = pygame.image.load("./dino/Rules.jpg")
clock = pygame.time.Clock()


class Player:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 6
        self.isjumping = False
        self.jump_pos = 10
        self.left = False
        self.right = False
        self.walk_count = 0
        self.standing = True
        self.health = 5
        self.inCollidingRange = False

    def draw(self, screen):
        if self.walk_count + 1 >= 30:
            self.walk_count = 0

        if not self.standing:
            if self.left:
                screen.blit(walk_lt[self.walk_count // 3], (self.x, self.y))  # 1 pic for 3 frames
                self.walk_count += 1
            elif self.right:
                screen.blit(walk_rt[self.walk_count // 3], (self.x, self.y))
                self.walk_count += 1
        else:
            if self.left:
                screen.blit(char_idle[1], (self.x, self.y))
            else:
                screen.blit(char_idle[0], (self.x, self.y))
        self.hitbox = (self.x + 18, self.y + 3, 40, 65)  # HITBOX HERE FOR DINO
        pygame.draw.rect(screen, (255, 0, 0), (self.hitbox[0] - 10, self.hitbox[1] - 10, 60, 7))  # Red
        if self.health != 0:
            pygame.draw.rect(screen, (0, 200, 0),
                             (self.hitbox[0] - 10, self.hitbox[1] - 10, 60 - (12 * (5 - self.health)), 7))  # Green
        Pl_name = font_of_player_name.render(player_name[:7], True, (0, 0, 0))
        screen.blit(Pl_name, (self.hitbox[0] - 5, self.hitbox[1] - 35))

    def hit(self):
        if self.health > 0:
            self.health -= 1
        self.inCollidingRange = True


class Bullet:
    def __init__(self, x, y, facing):
        self.x = x
        self.y = y
        self.facing = facing
        self.velocity = 10 * facing

    def draw(self, screen):
        if self.facing == 1:
            screen.blit(fireball[0], (self.x, self.y))
        else:
            screen.blit(fireball[1], (self.x, self.y))


class Enemy:
    walk_rt = [pygame.image.load(f"./zombie/Walk ({i}).png") for i in range(1, 11)]
    walk_lt = [pygame.image.load(f"./zombie/LWalk ({i}).png") for i in range(1, 11)]

    def __init__(self, x, y, width, height, start, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.path = [start, end]
        self.facing = 1
        self.velocity = 5
        self.walk_count = 0

    def draw(self, screen):
        self.movement()
        if self.walk_count + 1 >= 30:
            self.walk_count = 0

        if self.velocity > 0:
            screen.blit(self.walk_rt[self.walk_count // 3], (self.x, self.y))
            self.walk_count += 1
        else:
            screen.blit(self.walk_lt[self.walk_count // 3], (self.x, self.y))
            self.walk_count += 1
        self.hitbox = (self.x + 15, self.y, 40, 75)  # HITBOX HERE FOR ZOM

    def movement(self):
        if not (self.path[0] < self.x + self.velocity < self.path[1]):  # If not in walk range
            self.facing *= -1
            self.velocity *= -1  # change dirtn & reset walk count
            self.walk_count = 0
        self.x += self.velocity

    def hit(self):
        self.velocity += 0.5 * self.facing


def fade():
    fade = pygame.Surface(size)
    fade.fill((0, 0, 0))
    for alpha in range(0, 256, 7):
        fade.set_alpha(alpha)
        Redraw_Screen()
        Screen.blit(fade, (0, 0))
        pygame.display.update()


def Redraw_Screen():
    Screen.blit(bkg, (0, 0))
    high_scr = font_of_high_score.render(f"High Score: {high_score} ", True, (0, 0, 0))
    your_scr = font_of_hits.render(f"Your Score: {your_score}", True, (0, 0, 0))
    Screen.blit(high_scr, (760, 0))
    Screen.blit(your_scr, (760, 20))
    dino.draw(Screen)
    zombie.draw(Screen)
    for bullet in bullets:
        bullet.draw(Screen)


# ||-----MAIN LOOP-----||#
main = True
menu = True
is_first_time = True
rules = False
font_of_start_game = pygame.font.SysFont("arial", 50, True)
font_of_rules = pygame.font.SysFont("arial", 50, True)
font_of_quit_game = pygame.font.SysFont("arial", 50, True)
font_of_game_starts_in = pygame.font.SysFont("arial", 40, True)
while menu:  # Main Menu
    start_game = font_of_start_game.render("START", True, (255, 255, 255))
    rules = font_of_rules.render("RULES", True, (255, 255, 255))
    quit_game = font_of_quit_game.render("QUIT", True, (255, 255, 255))
    Screen.fill((255, 255, 255))
    # Start button
    pygame.draw.rect(Screen, (0, 0, 0), (40, 425, 175, 60))
    pygame.draw.rect(Screen, (255, 0, 0), (40, 425, 175, 60), 2)
    Screen.blit(start_game, (60, 425))
    # Rules button
    pygame.draw.rect(Screen, (0, 0, 0), (350, 425, 175, 60))
    pygame.draw.rect(Screen, (255, 0, 0), (350, 425, 175, 60), 2)
    Screen.blit(rules, (370, 425))
    # Quit button
    pygame.draw.rect(Screen, (0, 0, 0), (660, 425, 175, 60))
    pygame.draw.rect(Screen, (255, 0, 0), (660, 425, 175, 60), 2)
    Screen.blit(quit_game, (700, 425))

    Screen.blit(menu_icon, (235, 0))

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            main, menu = False, False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if 40 <= pos[0] <= 215 and 425 <= pos[1] <= 485:  # Start
                menu = False

            if 350 <= pos[0] <= 525 and 425 <= pos[1] <= 485:  # Rules
                rules, menu = True, False
                i = 20
                while i > 0:
                    Screen.blit(rules_page, (0, 0))
                    game_starts_in = font_of_game_starts_in.render("Game Starts in " + str(i) + " seconds", True,
                                                                   (150, 0, 0))
                    Screen.blit(game_starts_in, (444, 444))
                    clock.tick(1)
                    i -= 1
                    pygame.display.update()

            if 660 <= pos[0] <= 835 and 425 <= pos[1] <= 485:  # Quit
                main, menu = False, False

    pygame.display.update()

while main:
    fps = 30
    run = True
    dino = Player(100, 325, 75, 75)
    zombie = Enemy(813, 320, 75, 75, 0, 813)
    bullets = []
    bullet_count = 0
    if not is_first_time:
        high_score = max(high_score, your_score)
        with open("data.txt", mode="w") as file:
            file.write(f"High Score : {high_score}")
    else:
        with open("data.txt") as file:
            high_score = int(file.read().split(":")[1])
    your_score = 0
    player_name = "Player"
    font_of_hits = pygame.font.SysFont("arial", 20, True)
    font_of_high_score = pygame.font.SysFont("arial", 20, True)
    font_of_player_name = pygame.font.SysFont("arial", 17, True, True)
    font_of_game_over = pygame.font.SysFont("arial", 100, True)
    font_of_try_again = pygame.font.SysFont("arial", 50, True)

    # Game screen starts here
    while run:
        clock.tick(fps)
        Redraw_Screen()

        if not dino.inCollidingRange:
            if dino.hitbox[1] < zombie.hitbox[1] + zombie.hitbox[3] and dino.hitbox[1] + dino.hitbox[3] > zombie.hitbox[1]:
                if dino.hitbox[0] + dino.hitbox[2] > zombie.hitbox[0] and dino.hitbox[0] < zombie.hitbox[0] + \
                        zombie.hitbox[2]:
                    dino.hit()
        if dino.inCollidingRange:
            i = False
            if dino.hitbox[1] < zombie.hitbox[1] + zombie.hitbox[3] and dino.hitbox[1] + dino.hitbox[3] > zombie.hitbox[1]:
                if dino.hitbox[0] + dino.hitbox[2] > zombie.hitbox[0] and dino.hitbox[0] < zombie.hitbox[0] + \
                        zombie.hitbox[2]:
                    i = True
            if not i:
                dino.inCollidingRange = False

        if bullet_count > 0:
            bullet_count += 0.5  # So we can shoot once per 10 frames (as bullet_count +=0.5)
        if bullet_count > 5:
            bullet_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run, main = False, False

        for bullet in bullets:  # width 25px height 20px
            if bullet.y < zombie.hitbox[1] + zombie.hitbox[3] and bullet.y + 20 > zombie.hitbox[1]:
                if bullet.x + 25 > zombie.hitbox[0] and bullet.x < zombie.hitbox[0] + zombie.hitbox[2]:
                    zombie.hit()
                    your_score += 1
                    if your_score >= high_score:
                        high_score = your_score
                    bullets.remove(bullet)

            if 0 < bullet.x < 888:
                bullet.x += bullet.velocity
            else:
                bullets.remove(bullet)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            run, main = False, False

        # This bullet_count makes to shoot 1 fire ball for 1 loop...
        if keys[pygame.K_SPACE] and bullet_count == 0:
            if dino.left:
                facing = -1
            else:
                facing = 1

            if len(bullets) < 3:
                if facing == 1:
                    bullets.append(Bullet(dino.x + 55, dino.y + 10, facing))
                else:
                    bullets.append(Bullet(dino.x - 10, dino.y + 10, facing))
            bullet_count = 0.5

        if keys[pygame.K_RIGHT]:
            if dino.x <= 888 - dino.width + 5:
                dino.x += dino.velocity
            dino.right = True
            dino.left = False
            dino.standing = False

        elif keys[pygame.K_LEFT]:
            if dino.x >= 0 - 5:
                dino.x -= dino.velocity
            dino.right = False
            dino.left = True
            dino.standing = False

        else:
            dino.standing = True
            dino.walk_count = 0

        # Should not go up or down while jumping...
        if not (dino.isjumping):
            if keys[pygame.K_UP]:
                dino.isjumping = True
                # This if-else makes the jump facing left also & removes blinking while jump
                if dino.right:
                    dino.left = False
                    pass
                elif dino.left:
                    dino.right = False
                    pass

                dino.walk_count = 0

        else:
            if dino.jump_pos >= -10:
                neg = 1
                if dino.jump_pos < 0:
                    neg = -1
                # Sq.Func to make a jump...You can also use cubic or linear func...
                dino.y -= (dino.jump_pos ** 2) // 2 * neg
                dino.jump_pos -= 2
            else:
                dino.jump_pos = 10
                dino.isjumping = False
        if dino.health == 0:
            fade()
            is_first_time = False
            break
        pygame.display.update()

    # Game Over screen starts here
    while run:
        game_over = font_of_game_over.render("GAME OVER!!!", True, (255, 255, 255))
        try_again = font_of_try_again.render(f"Try Again?  Your score is {your_score}", True, (255, 255, 255))
        Screen.blit(game_over, (150, 150))
        pygame.draw.rect(Screen, (255, 0, 0), (315, 250, 240, 60))
        pygame.draw.rect(Screen, (255, 255, 255), (315, 250, 240, 60), 2)
        Screen.blit(try_again, (330, 250))

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run, main = False, False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 315 <= pos[0] <= 555 and 250 <= pos[1] <= 310:
                    run = False  # gets out of game over loop

        pygame.display.update()

pygame.quit()

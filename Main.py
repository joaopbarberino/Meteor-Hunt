import pygame
import random
import Constants
import Classes.Bullet as bullet
import Classes.Player as player
import Classes.Meteors as meteor

pygame.init()

clock = pygame.time.Clock()
pygame.display.set_caption("Meteor Hunt")
click_do_mouse = pygame.mixer.Sound("./Sounds/laser5.ogg")
background_position = [0, -1200]
background_image = pygame.image.load("Images/Background/darkPurple.png").convert()
loop_game = 0
pygame.mouse.set_visible(False)
score = 0

player = player.Player()

# --- Sprite Lists

# List of every sprite
all_sprites_list = pygame.sprite.Group()

# List of each bullet
bullet_list = pygame.sprite.Group()

# List of each meteor
meteor_list = pygame.sprite.Group()
meteors_hit_list = pygame.sprite.Group()

all_sprites_list.add(player)

done = False

while not done:
    pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_do_mouse.play()
            # Fire a bullet if the user clicks the mouse button
            shot = bullet.Bullet()
            # Set the bullet to where the player is
            shot.rect.x = pos[0]+44
            shot.rect.y = pos[1]-60
            #Add the bullet to the lists
            all_sprites_list.add(shot)
            bullet_list.add(shot)

    if score == 10:
        Constants.ASTEROID_MOVE_SPEED = 5
        Constants.ASTEROID_SUMMON_TIME = 60
    elif score == 20:
        Constants.ASTEROID_MOVE_SPEED = 10
        Constants.ASTEROID_SUMMON_TIME = 30

    # Summon meteors
    if loop_game % Constants.ASTEROID_SUMMON_TIME == 0:
        asteroid = meteor.Meteor()
        asteroid.reposicionar(Constants.X)
        meteor_list.add(asteroid)
    loop_game += 1

    # --- Game Logic

    #Call update method on all the sprites
    all_sprites_list.update()
    meteor_list.update(Constants.X, Constants.Y, Constants.ASTEROID_MOVE_SPEED)
    bullet_list.update()
    # Calculate mechanics for each bullet
    for shot in bullet_list:
        #Remove the bullet if it flies up off the screen
        if shot.rect.y < -40:
            bullet_list.remove(shot)
            all_sprites_list.remove(shot)
        # See if the player block has collided with anything.
        meteors_hit_list = pygame.sprite.spritecollide(shot, meteor_list, True)

        # Check the list of collisions.
        for asteroid in meteors_hit_list:
            score = score + 1
            print(score)
            meteor_list.remove(asteroid)
            bullet_list.remove(shot)
            all_sprites_list.remove(shot)

    #Remove player if it's hit
    player_hit_list = pygame.sprite.spritecollide(player, meteor_list, True)

    if player_hit_list:
        all_sprites_list.remove(player)
    else:
        Constants.screen.blit(player.image, pos)

    Constants.screen.blit(background_image, background_position)

    # Roll the background
    if background_position[1] >= 0:
        background_position[1] = -1200
    else:
        background_position[1] += 2

    # Draw all the sprites
    all_sprites_list.draw(Constants.screen)
    meteor_list.draw(Constants.screen)
    bullet_list.draw(Constants.screen)

    pygame.display.update()

    clock.tick(60)

pygame.quit()

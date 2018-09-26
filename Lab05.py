# Walter Irvin
# Lab 05

import pygame
import time
import random
import math

pygame.init()
#BASE STUFF---------------------------------
myfont = pygame.font.SysFont("starwars.ttf", 26)
screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
atime = time.time()
stime = time.time()
white = (255,255,255)
black = (0,0,0)
music = pygame.mixer.music.load("Imperia.ogg")
launch = pygame.mixer.Sound("launch.wav")
pygame.mixer.Sound.set_volume(launch, 0.1)
pygame.mixer.music.play(-1,0)
done = False
flip = pygame.display.flip
# amount sets how many stars there will be, from 100 - 200 stars
rand = random.randint(100,200)
c = 0
i = 0
starlist = []
startgame = False
#NOW TO OTHER VARIABLES---------------------
dead = pygame.mixer.Sound("dead.wav")
ufospawn = pygame.mixer.Sound("spawn.wav")
launch = pygame.mixer.Sound("launch.wav")
explode = pygame.mixer.Sound("explode.wav")
exterminate = pygame.mixer.Sound("exterminate.wav")
beam = pygame.mixer.Sound("beam.wav")
power = pygame.mixer.Sound("power.wav")
laser = pygame.mixer.Sound("laserfire.wav")
# IMAGES ------------------------------------
ufo_fname = pygame.image.load("ufo.bmp").convert()
rocket = pygame.image.load("normalrocket.bmp").convert()
powerup = pygame.image.load("fusionrocket.bmp").convert()
rocket = pygame.transform.scale(rocket, (64,50))
powerup = pygame.transform.scale(powerup, (64,50))
ufobullet = pygame.image.load("ufobullet.bmp").convert()
ufobullet = pygame.transform.scale(ufobullet, (40,40))
grad_img = pygame.image.load("grad.png")
ufo_grad = pygame.image.load("ufo_grad.png")
#colorkeys
ufo_fname.set_colorkey(white)
rocket.set_colorkey(white)
powerup.set_colorkey(white)
ufobullet.set_colorkey(white)


pygame.mixer.Sound.set_volume(launch, 0.4)
pygame.mixer.Sound.set_volume(ufospawn, 0.4)
pygame.mixer.Sound.set_volume(explode, 1)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.Sound.set_volume(laser, 0.5)


for c in range(rand):
    stars_x = random.randint(0,800)
    stars_y = random.randint(0,600)
    stars_radius = random.randint(2,5)
    newstar = [stars_x, stars_y]
    starlist.append(newstar)
    c += 1
# Some star variables that help determine movement
starspeed = 100


#For the text scrolling
scrollspeed = 50
startscroll = 600
#variables for the launcher 0 = not moving, 1 = moving upwards
launcherspeed = 200
launcherdirection = 0
y1 = 600
launcherx = 0
# Ufo variables
ufo_spawntime = 5
ufo_y = random.randint(150,350)
ufo_x = random.randint(0,800)
ufo_count = 0
ufolist = []
ufos = []
ufo_speed = 100
ufo_counter = 0
# Rockets variables
rocketlist = []
newrocket = []
rocketspeed = 200
smokelist = []

# This is my attempt at integrating a highscore system.
file = open("highscore.txt", 'r', encoding='utf-8')

debug = False
debugtoggle = 0
explodelist = [] # each particle is [x,y,hspeed,vspeed,life,radius]
textlist = ['No one would have believed in the last years of the nineteenth century', 'that this world was being watched keenly and closely by intelligences',
            'greater than man\'s and yet as mortal as his own; that as men busied themselves','about their various concerns they were scrutinised and studied, perhaps',
            'almost as narrowly as a man with a microscope might scrutinise the transient','creatures that swarm and multiply in a drop of water. With infinite complacency',
            'men went to and fro over this globe about their little affairs, serene in','their assurance of their empire over matter. It is possible that the infusoria',
            'under the microscope do the same. No one gave a thought to the older worlds','of space as sources of human danger, or thought of them only to dismiss',
            'the idea of life upon them as impossible or improbable. It is curious to recall','some of the mental habits of those departed days. At most terrestrial men',
            'fancied there might be other men upon Mars, perhaps inferior to themselves','and ready to welcome a missionary enterprise. Yet across the gulf of space,',
            'minds that are to our minds as ours are to those of the beasts that perish,','intellects vast and cool and unsympathetic, regarded this earth with envious',
            'eyes, and slowly and surely drew their plans against us. And early in the','twentieth century came the great disillusionment.','The planet Mars, I scarcely need remind the reader, revolves about the sun at a',
'mean distance of 140,000,000 miles, and the light and heat it receives from','the sun is barely half of that received by this world. It must be, if the',
'nebular hypothesis has any truth, older than our world; and long before this','earth ceased to be molten, life upon its surface must have begun its course.',
'The fact that it is scarcely one seventh of the volume of the earth must have','accelerated its cooling to the temperature at which life could begin. It has',
'air and water and all that is necessary for the support of animated existence.','Yet so vain is man, and so blinded by his vanity, that no writer, up to',
'the very end of the nineteenth century, expressed any idea that intelligent life','might have developed there far, or indeed at all, beyond its earthly level.',
'Nor was it generally understood that since Mars is older than our earth,','with scarcely a quarter of the superficial area and remoter from the sun,',
"it necessarily follows that it is not only more distant from time's beginning",'but nearer its end.',]
amplitude = 125
offset = 125
phase_mult = 0.01
phase_offset = 5
w = 0
score = 0
ufo_kills = 0
rocket_count = 0
power_up = 1000
startscreentimer = time.time()

ufo_bulletlist = []
xtime = time.time()
togglerocket = rocket
hp = 3
ufo_smokelist = []
megarocketlist = []
supplydrop_amount = 0
supplytimer = time.time()
highscore = file.read()
ufo_timer = 2
powerhit = 0

while not done:
    etime = time.time()
    dt = clock.tick() / 1000
    event = pygame.event.poll()
    x, y = pygame.mouse.get_pos()
    ufo_timer -= dt


    if x > launcherx:
        launcherx += launcherspeed * dt
    elif x < launcherx:
        launcherx -= launcherspeed * dt



    startscroll -= scrollspeed * dt
    if event.type == pygame.QUIT:
        done = True
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            done = True
        if event.key == pygame.K_q:
            done = True
        if event.key == pygame.K_RETURN:
            startgame = True
        if event.key == pygame.K_d and debugtoggle == 0:
            debug = True
            debugtoggle = 1
        elif event.key == pygame.K_d and debugtoggle == 1:
            debugtoggle = 0
            debug = False

    if startgame == False:
        screen.fill(black)
        if startscroll + len(textlist) * 20 <= 0:
            startscroll = 600
        y = startscroll
        for t in range(len(textlist)):
            intense = amplitude * math.sin(phase_mult * y + phase_offset) + offset
            textcolor = (intense,intense,intense)
            temp_a = pygame.font.Font.render(myfont,str(textlist[t]), True, (textcolor), 40)
            screen.blit(temp_a, (100,y))
            y += 20

        entercolor = amplitude * math.sin(0.04 * y + phase_offset) + offset
        finalenter = (entercolor,0,0)
        box = amplitude * math.sin(0.04 * y + phase_offset + 10) + offset
        boxcolor = (box,box,box)
        pygame.draw.rect(screen,(boxcolor), (295,545,200,30),0)
        temp_08 = pygame.font.Font.render(myfont, "Press ENTER to start...", True, (finalenter), 40)
        screen.blit(temp_08, (300, 550))
        flip()

    if startgame == True:
        screen.fill(black)
        start_screen = pygame.font.Font.render(myfont, "GET PSYCHED!", True, (white), 100)
        life_count = pygame.font.Font.render(myfont, "The amount of lives you have left: " + str(hp), True, (white), 40)
        temp_score = pygame.font.Font.render(myfont,"Score: " + str(score), True, (white), 40)
        temp_debug = pygame.font.Font.render(myfont,"-DEBUG-", True, (white), 40)
        temp_debug2 = pygame.font.Font.render(myfont,"[D]ebug mode", True, (white), 40)
        temp_rocket = pygame.font.Font.render(myfont,"Rockets: " + str(rocket_count), True, (white), 40)
        temp_ufo = pygame.font.Font.render(myfont,"UFOs: " + str(ufo_count), True, (white), 40)
        temp_launcher = pygame.font.Font.render(myfont,"Launcher tracks mouse", True, (white), 40)
        temp_fire = pygame.font.Font.render(myfont,"[LClick] to fire", True, (white), 40)
        temp_quit = pygame.font.Font.render(myfont,"[Q]uit", True, (white), 40)
        temp_highscore = pygame.font.Font.render(myfont, "Highscore: " + str(highscore), True, (white), 40)
        end_score = pygame.font.Font.render(myfont, "Your score was: " + str(score), True, (white), 40)
        end_highscore = pygame.font.Font.render(myfont, "Highscore was: " + str(highscore), True, (white), 40)

        if score > int(highscore) and hp > 0:
            highscore = score


        if etime - startscreentimer <= 5:
            screen.blit(start_screen, (350,300))

        if hp == 0:
            screen.fill((255,0,0))
            gameover = pygame.font.Font.render(myfont, "Game Over!", True, (white), 100)
            screen.blit(gameover, (350,300))
            pygame.mixer.Sound.play(dead)
            if score >= int(highscore):
                file = open("highscore.txt", 'w', encoding='utf-8')
                highscore = file.write(str(score))

            screen.blit(end_score, (300, 320))
            screen.blit(end_highscore, (300,340))
            flip()
            time.sleep(5)
            done = True
            break



        if debug == False:
            screen.blit(temp_score, (0,0))
            screen.blit(temp_highscore, (0,20))
            screen.blit(life_count, (200, 20))
            screen.blit(temp_debug2, (100,0))
            screen.blit(temp_launcher, (250,0))
            screen.blit(temp_fire, (480, 0))
            screen.blit(temp_quit,(650,0))
        elif debug == True:
            screen.blit(temp_score, (0, 0))
            screen.blit(life_count, (0, 40))
            screen.blit(temp_debug2, (0, 20))
            screen.blit(temp_launcher, (150, 20))
            screen.blit(temp_fire, (380, 20))
            screen.blit(temp_quit, (550, 20))
            screen.blit(temp_debug, (100,0))
            screen.blit(temp_rocket, (250,0))
            screen.blit(temp_ufo, (480, 0))
            screen.blit(temp_highscore, (580, 0))

        if score == power_up:

            if supplydrop_amount < 1:
                mega_x = random.randint(20,780)
                mega_y = random.randint(0,50)
                speed = 100
                mega_drop = [mega_x, mega_y, speed]
                megarocketlist.append(mega_drop)
            supplydrop_amount = 2

        elif score >= power_up:
            togglerocket = rocket
            power_up += 1000
            supplydrop_amount = 0

        if w < 1:
            pygame.mixer.Sound.set_volume(exterminate, 0.5)
            pygame.mixer.Sound.play(exterminate)
            w = 2

        if event.type == pygame.MOUSEBUTTONDOWN and etime - atime >= 0.7:
            pygame.mixer.Sound.play(launch)
            atime = time.time()
            newrocket = [launcherx, 600]
            rocketlist.append(newrocket)
            rocket_count += 1


        if etime - stime >= ufo_spawntime and ufo_count < 5:
            ufo_x = random.randint(0, 800)
            ufo_y = random.randint(0, 350)

            pygame.mixer.Sound.play(ufospawn)
            stime = time.time()
            ufo_count += 1
            ufo_direction = random.choice([1,-1])
            ufos = [ufo_x, ufo_y, ufo_direction]
            ufolist.append(ufos)


        for i in range(len(starlist)):
            starlist[i][1] += starspeed * dt
            if starlist[i][1] < 0:
                starlist[i][1] = 600
            if starlist[i][1] > 600:
                starlist[i][1] = 0

        for stars in starlist:
            pygame.draw.circle(screen,(white),( int(stars[0]), int(stars[1])), 2)


        pygame.draw.polygon(screen, (255,0,0),((launcherx, 580),(launcherx - 20,600),(launcherx + 20, 600)))
        if debug == True:
            pygame.draw.circle(screen, (white), (int(launcherx), 600), 25, 1)
        for i in range(len(ufolist)):
                ufolist[i][0] += ufo_speed * dt * ufolist[i][2]

                part_x = int(ufolist[i][0])
                part_y = int(ufolist[i][1])
                if debug == True:
                    pygame.draw.circle(screen, (white), (int(ufolist[i][0] + 64), int(ufolist[i][1] + 59)), 70, 1)
                screen.blit(ufo_fname, (int(ufolist[i][0]), int(ufolist[i][1] )),)
                if ufolist[i][0] < 0:
                    ufolist[i][0] = 800
                if ufolist[i][0] > 800:
                    ufolist[i][0] = 0
        if ufo_timer <= 0:
            bullet_speed = 200
            for u in ufolist:
                new_bullet = [u[0] + 75, u[1] + 50]
                ufo_bulletlist.append(new_bullet)
                pygame.mixer.Sound.play(laser)
            ufo_timer = 2

        for u in ufolist:
            for r in rocketlist:
                if (((u[0]+ 64) - r[0]) ** 2 + ((u[1] + 59) - r[1]) ** 2) ** 0.5 <= 64 + 20:

                    if togglerocket == rocket:
                        ufolist.remove(u)
                        score += 100
                        ufo_count -= 1
                    rocketlist.remove(r)
                    for e in range(100):
                        hspeed = random.randint(-100,100)
                        vspeed = random.randint(-100,100)
                        life = 1
                        rad = random.randint(2,5)
                        if togglerocket == powerup:
                            powerhit += 1
                            for k in range(len(ufolist) -1, -1, -1):
                                score += 100
                                for e in range(100):
                                    hspeed = random.randint(-100, 100)
                                    vspeed = random.randint(-100, 100)
                                    life = 1
                                    rad = random.randint(2, 5)
                                    explosion_new = [ufolist[k][0], ufolist[k][1], hspeed, vspeed, life, rad]
                                    explodelist.append(explosion_new)
                                ufo_count  = 0
                            #k >= len(ufolist):
                            ufolist.clear()
                        elif togglerocket == rocket:
                            explosion_new = [u[0],u[1], hspeed, vspeed, life, rad]
                            explodelist.append(explosion_new)

                    rocket_count -= 1
                    pygame.mixer.Sound.play(explode)
                    break

        for v in megarocketlist:
            v[1] += v[2] * dt
            if debug == True:
                pygame.draw.circle(screen, (white), (int(v[0]) + 30, int(v[1]) + 25), 20, 1)
            screen.blit(powerup, (int(v[0]), int(v[1])), (0,0,128,128))
            if v[1] >= 600:
                megarocketlist.remove(v)
            if ((int(v[0]) - int(launcherx)) ** 2 + (int(v[1]) - 580) ** 2) ** (1/2) <= 40:
                megarocketlist.remove(v)
                togglerocket = powerup
                pygame.mixer.Sound.play(power)
                hp += 1



        for o in ufo_bulletlist:
            ulife = 1
            urad = random.randint(2, 5)
            usmoke_hspeed = random.randint(-20, 20)
            usmoke_vspeed = random.randint(10,20)
            ufo_trail = [o[0], o[1], usmoke_hspeed, usmoke_vspeed, ulife, urad]
            ufo_smokelist.append(ufo_trail)


            o[1] += bullet_speed * dt

            if ((int(o[0]) - launcherx) ** 2 + (int(o[1]) - 580) ** 2) ** (1/2) <= 60:
                ufo_bulletlist.remove(o)
                pygame.mixer.Sound.play(beam)
                hp -= 1
            if o[1] > 600:
                ufo_bulletlist.remove(o)

            screen.blit(ufobullet, (int(o[0]-20), int(o[1]) -20), (0,0,128,128))
            if debug == True:
                pygame.draw.circle(screen, (white), (int(o[0]), int(o[1])), 20, 1)

        for m in ufo_smokelist:
            iy = (ufo_grad.get_width() - 1) * m[4]
            color_z2 = ufo_grad.get_at((int(iy), 0))
            pygame.draw.circle(screen, color_z2, (int(m[0]), int(m[1])), int(m[5]))

        j =  len(ufo_smokelist) - 1
        while j >= 0:
            ufo_smokelist[j][0] += ufo_smokelist[j][2] * dt
            ufo_smokelist[j][1] += ufo_smokelist[j][3] * dt
            ufo_smokelist[j][4] -= dt

            if ufo_smokelist[j][4] <= 0:
                ufo_smokelist.remove(ufo_smokelist[j])

            j -= 1




        for e in explodelist:
            ix = (grad_img.get_width()-1) * e[4]
            # Bug - sometimes this code snippet will act up and state something about a pixel index out of range.
            color = grad_img.get_at((int(ix), 0))
            pygame.draw.circle(screen, color, (int(e[0]), int(e[1])), int(e[5]))

        i = len(explodelist) - 1
        while i >= 0:
            explodelist[i][0] += explodelist[i][2] * dt
            explodelist[i][1] += explodelist[i][3] * dt
            explodelist[i][4] -= dt

            if explodelist[i][4] <= 0:
                explodelist.remove(explodelist[i])
            i -= 1



        for i in range(len(rocketlist)-1, -1, -1):

            if togglerocket == powerup and powerhit >= 1:
                togglerocket = rocket
                powerhit = 0


            rocketlist[i][1] -= rocketspeed * dt
            life = 1
            rad = random.randint(2,5)
            smoke_hspeed = random.randint(-20,20)
            smoke_vspeed = random.randint(-10,10)
            new_smoke = [rocketlist[i][0], rocketlist[i][1], smoke_hspeed, smoke_vspeed, life, rad]
            smokelist.append(new_smoke)

            if debug == True:
                pygame.draw.circle(screen, (white),(int(rocketlist[i][0] + 5), int(rocketlist[i][1] + 25)), 20, 1)
            screen.blit(togglerocket,(int(rocketlist[i][0]- 25), int(rocketlist[i][1])) , (0,0,128,128))
            if int(rocketlist[i][1]) <= 0:
                rocketlist.remove(rocketlist[i])
                rocket_count -= 1
            i += 1

        for s in smokelist:
            iz = (grad_img.get_width()-1) * s[4]
            color_z1 = grad_img.get_at((int(iz), 0))
            pygame.draw.circle(screen, color_z1, (int(s[0] + 4), int(s[1] + 50)), int(s[5]))

        smokecount = len(smokelist) - 1

        while smokecount >= 0:
            smokelist[smokecount][0] += smokelist[smokecount][2] * dt
            smokelist[smokecount][1] += smokelist[smokecount][3] * dt
            smokelist[smokecount][4] -= dt

            if smokelist[smokecount][4] <= 0:
                smokelist.remove(smokelist[smokecount])
            smokecount -= 1

    flip()

pygame.quit()
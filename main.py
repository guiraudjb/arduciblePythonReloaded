#---------------------------------IMPORTS-------------------------------
import os
os.environ['GLOG_minloglevel'] = '2'  # supprime les logs verbeux de MediaPipe/TFLite
import pygame
from pygame import *
pygame.init()
from Scripts.init import * # load config.ini and some variables
from Scripts.Sprites import *# load sprites
import cv2
#---------------------Procedures et fonctions---------------------------

def init_cibles():
    global cible1
    global cible2
    global cible3
    cible1 = Cible()
    cible1.rect.x = LARGEUR_ECRAN * 3/20 - LARGEUR_ECRAN*0.25/2
    cible1.rect.y = HAUTEUR_ECRAN * 16/20 - HAUTEUR_ECRAN*0.44/2

    cible2 = Cible()
    cible2.rect.x = LARGEUR_ECRAN *10/20 - LARGEUR_ECRAN*0.25/2
    cible2.rect.y = HAUTEUR_ECRAN * 16/20 - HAUTEUR_ECRAN*0.44/2

    cible3 = Cible()
    cible3.rect.x = LARGEUR_ECRAN * 17/20 - LARGEUR_ECRAN*0.25/2
    cible3.rect.y = HAUTEUR_ECRAN * 16/20 - HAUTEUR_ECRAN*0.44/2
    

def next_gamestate():
    global time_left
    global gamestate
    global score
    global intro_length
    global game_length
    global ending_length
    global ingamebackground
    global webcam_compatibility
    if gamestate == 0:
        gamestate = 1
        if webcam_compatibility == True:
            ingamebackground.image = ingamebackground.images[1]
            ingamebackground.image = pygame.transform.scale(ingamebackground.image, (LARGEUR_ECRAN, HAUTEUR_ECRAN))

        else:
            ingamebackground.image = ingamebackground.images[0]
            ingamebackground.image = pygame.transform.scale(ingamebackground.image, (LARGEUR_ECRAN, HAUTEUR_ECRAN))

        time_left = game_length
        score = 0
    elif gamestate == 1:
        gamestate = 2
        ingamebackground.image = ingamebackground.images[2]
        ingamebackground.image = pygame.transform.scale(ingamebackground.image, (LARGEUR_ECRAN, HAUTEUR_ECRAN))

        time_left = ending_length
    elif gamestate == 2:
        gamestate = 0
        time_left = intro_length
        
def ciblealeatoire():
    global cibleencours
    global oldcibleencours
    while cibleencours == oldcibleencours:
        cibleencours = random.randint(1, 3)
    oldcibleencours = cibleencours
    if sound_effects == True:
        if cibleencours == 1:
            pygame.mixer.music.load('./assets/Sounds/VoicesAI/gauche.wav')
            pygame.mixer.music.play(1)

        if cibleencours == 2:
            pygame.mixer.music.load('./assets/Sounds/VoicesAI/centre.wav')
            pygame.mixer.music.play(1)

        if cibleencours == 3:
            pygame.mixer.music.load('./assets/Sounds/VoicesAI/droite.wav')
            pygame.mixer.music.play(1)

def showcam():
    ecran.blit(mycam.images, (LARGEUR_ECRAN/2-mycam.width/2,0))
 
def countdown():
    global old_timer
    global game_timer
    global time_left
    game_timer = pygame.time.get_ticks()
    if game_timer - old_timer >= 1000:
        time_left = time_left - 1
        old_timer = game_timer

def update_score():
    global score
    global time_left
    global channel2
    if sound_effects == True:
        channel2.play(sfx_hit)

    score = score + 1
    time_left = time_left + bonus_time

def draw_camring():
    global ecran
    global camring

    if mycam.zoneinterdite == True:
        draw_go_to_shooting_zone()
        camring.image = camring.images[0]
        ecran.blit(camring.image, camring.rect)
    else:
        camring.image = camring.images[1]
        ecran.blit(camring.image, camring.rect)
    
def draw_text(text,x,y,blink,center,fnt,col):

    if fnt == 1:
        font1=FontDel1.render
        font2=FontDel2.render
    if fnt == 2:
        font1=FontDel3.render
        font2=FontDel4.render
        
    if col == 1:
        color1=red
        color2=redlight
    if col == 2:
        color1=orange
        color2=orangelight
    if col == 3:
        color1=yellow
        color2=yellowlight
    if col == 4:
        color1=blue
        color2=bluelight
    if col == 5:
        color1=green
        color2=greenlight
    
    
    text_img = font1(str(text),True,color1)
    text_img2 = font2(str(text),True,color2)
    
    if blink and not affichage:
        return

    w1, h1 = text_img.get_rect().size
    w2, h2 = text_img2.get_rect().size
    if center:
        ecran.blit(text_img,  (x - w1/2, y - h1/2))
        ecran.blit(text_img2, (x - w2/2, y - h2/2))
    else:
        ecran.blit(text_img,  (x, y))
        ecran.blit(text_img2, (x, y))
    
def debug_lines():
    for i in range(1, 20):
        pygame.draw.line(ecran, red, (LARGEUR_ECRAN*i/20, 0), (LARGEUR_ECRAN*i/20, HAUTEUR_ECRAN), 1)
        pygame.draw.line(ecran, red, (0, HAUTEUR_ECRAN*i/20), (LARGEUR_ECRAN, HAUTEUR_ECRAN*i/20), 1)
    

def draw_go_to_shooting_zone():
    draw_text("Go to the shooting zone",LARGEUR_ECRAN*10/20,HAUTEUR_ECRAN*11/20,False,True,1,1)

def draw_intro_text():
    draw_text("HIGH SCORE",LARGEUR_ECRAN*10/20,HAUTEUR_ECRAN*1/20,False,True,1,4)
    draw_text(str(high_score),LARGEUR_ECRAN*10/20,HAUTEUR_ECRAN*3/20,False,True,1,4)
    draw_text("GAME START",LARGEUR_ECRAN*10/20,HAUTEUR_ECRAN*6/20,False,True,1,5)
    draw_text("IN",LARGEUR_ECRAN*10/20,HAUTEUR_ECRAN*8/20,False,True,1,5)
    draw_text(str(time_left),LARGEUR_ECRAN*10/20,HAUTEUR_ECRAN*10/20,False,True,1,5)
    draw_text("CREDIT  : ",LARGEUR_ECRAN*17/20,HAUTEUR_ECRAN*19/20,False,True,2,3)
    draw_text(str(credit_left),LARGEUR_ECRAN*19/20,HAUTEUR_ECRAN*19/20,False,True,2,3)

def draw_intro_insertCoin():
    draw_text("HIGH SCORE",LARGEUR_ECRAN*10/20,HAUTEUR_ECRAN*1/20,False,True,1,4)
    draw_text(str(high_score),LARGEUR_ECRAN*10/20,HAUTEUR_ECRAN*3/20,False,True,1,4)
    draw_text("CREDIT  : ",LARGEUR_ECRAN*17/20,HAUTEUR_ECRAN*19/20,False,True,2,3)
    draw_text(str(credit_left),LARGEUR_ECRAN*19/20,HAUTEUR_ECRAN*19/20,False,True,2,3)
def draw_ingame_text():
    if time_left <= 15:
        #red
        draw_text(str(time_left),LARGEUR_ECRAN*10/20,HAUTEUR_ECRAN*9/20,True,True,1,1)
    elif time_left <= 30:
        #orange
        draw_text(str(time_left),LARGEUR_ECRAN*10/20,HAUTEUR_ECRAN*9/20,False,True,1,2)
    elif time_left <= 45:
        #yellow
        draw_text(str(time_left),LARGEUR_ECRAN*10/20,HAUTEUR_ECRAN*9/20,False,True,1,3)
    else:
        #green
        draw_text(str(time_left),LARGEUR_ECRAN*10/20,HAUTEUR_ECRAN*9/20,False,True,1,5)
       
    
    draw_text("POINTS",LARGEUR_ECRAN*4/20,HAUTEUR_ECRAN*1/20,False,True,1,4)
    draw_text(str(score),LARGEUR_ECRAN*4/20,HAUTEUR_ECRAN*3/20,False,True,1,4)
    
    #affichage des credits
    draw_text("CREDIT  : ",LARGEUR_ECRAN*17/20,HAUTEUR_ECRAN*19/20,False,True,2,3)
    draw_text(str(credit_left),LARGEUR_ECRAN*19/20,HAUTEUR_ECRAN*19/20,False,True,2,3)
def draw_ending_text():
    draw_text("HIGH SCORE",LARGEUR_ECRAN*10/20,HAUTEUR_ECRAN*1/20,False,True,1,4)
    draw_text(str(high_score),LARGEUR_ECRAN*10/20,HAUTEUR_ECRAN*3/20,False,True,1,4)
    draw_text(str(time_left),LARGEUR_ECRAN*10/20,HAUTEUR_ECRAN*1/3,False,True,1,3)
    
    if score >= high_score:
        draw_text("YOUR SCORE",LARGEUR_ECRAN*10/20,HAUTEUR_ECRAN*11/20,True,True,1,5)
        draw_text(str(score),LARGEUR_ECRAN*10/20,HAUTEUR_ECRAN*13/20,True,True,1,5)
        draw_text("New record !!!",LARGEUR_ECRAN*10/20,HAUTEUR_ECRAN*9/20,True, True,2,5)
        print("high score")
    else:
        draw_text("YOUR SCORE",LARGEUR_ECRAN*10/20,HAUTEUR_ECRAN*11/20,False,True,1,3)
        draw_text(str(score),LARGEUR_ECRAN*10/20,HAUTEUR_ECRAN*13/20,False,True,1,3)
    
    #affichage des credits
    draw_text("CREDIT  : ",LARGEUR_ECRAN*17/20,HAUTEUR_ECRAN*19/20,False,True,2,3)
    draw_text(str(credit_left),LARGEUR_ECRAN*19/20,HAUTEUR_ECRAN*19/20,False,True,2,3)
def draw_cibles():
    global ecran
    global cible1
    global cible2
    global cible3
    global cibleencours
    if cibleencours == 1:
        cible1.image = cible1.images[1]
        cible2.image = cible1.images[0]
        cible3.image = cible1.images[0]
        
    elif cibleencours == 2:
            
        cible1.image = cible1.images[0]
        cible2.image = cible1.images[1]
        cible3.image = cible1.images[0]
        
    elif cibleencours == 3:
            
        cible1.image = cible1.images[0]
        cible2.image = cible1.images[0]
        cible3.image = cible1.images[1]
        
    ecran.blit(cible1.image, cible1.rect)
    ecran.blit(cible2.image, cible2.rect)
    ecran.blit(cible3.image, cible3.rect)
    
def animate_cible():
    global oldcibleencours
    if oldcibleencours == 1:
        cible1.image = cible1.images[2]
    if oldcibleencours == 2:
        cible2.image = cible2.images[2]
    if oldcibleencours == 3:
        cible3.image = cible3.images[2]
    for i in range(3):
        ecran.blit(cible1.image, cible1.rect)
        ecran.blit(cible2.image, cible2.rect)
        ecran.blit(cible3.image, cible3.rect)
        ingamedraw()
        clock.tick(9)
    

def ingamedraw():
    draw_ingame_text()
    if debug_line == True:
        debug_lines()
    if ShowFPS == True:
        fps = str(int(clock.get_fps()))
        FPS1 = FontDel1.render(fps, True, blue)
        FPS2 = FontDel2.render(fps, True, bluelight)
        ecran.blit(FPS1,(0,0))
        ecran.blit(FPS2,(0,0))
    pygame.display.flip()

#-------------------------DEBUT DU Programme ---------------------------
#initialise background table
print("loading sprites")
logo = ArducibleLogo()
introbackground = BackgroundFrame()
ingamebackground = Background()
ingamebackground.image = pygame.transform.scale(ingamebackground.image, (LARGEUR_ECRAN, HAUTEUR_ECRAN))
Animation1 =  AnimationFrame1()
Animation2 =  AnimationFrame2()
Animation3 =  AnimationFrame3()
Animation4 =  AnimationFrame4()
anim1 = Anim1()
anim1_flipped = Anim1Flipped()
camring = ColoredRing()
camring_width, camring_height = camring.image.get_rect().size
camring.rect.x = LARGEUR_ECRAN/2 - camring_width/2
sfx_hit = pygame.mixer.Sound('./assets/Sounds/Son3.wav')

#initialise webcam if actived in config.ini
if active_webcam:
    try:
        from Scripts.opencvcam import Cam
        print("activating webcam")
        mycam = Cam()
        mycam.update()
        
        
        if mycam.webcam_compatibility == True:
            webcam_compatibility = True
        else:
            webcam_compatibility = False
            
        if webcam_compatibility == True:
            
            ingamebackground.image = ingamebackground.images[1]
        else:
            webcam_zone_interdite = False
            ingamebackground.image = ingamebackground.images[0]
    except Exception as e:
        print(f"Webcam/MediaPipe error: {e}")
        webcam_compatibility = False
        webcam_zone_interdite = False
        ingamebackground.image = ingamebackground.images[0]
        
else:
    webcam_compatibility = False
    webcam_zone_interdite = False
    ingamebackground.image = ingamebackground.images[0]

pygame.display.set_caption("Arducible PÉTANQUE GAME") # set window title
icon = pygame.image.load("assets/icons/192x192.png")
pygame.display.set_icon(icon)
# Charge l'image de l'icone


if Fullscreen:
    ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN), pygame.SCALED | pygame.FULLSCREEN, vsync=1)
else:
    ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN), pygame.SCALED )


#initialise the screen
white = [255, 255, 255]
ecran.fill(white)
time_left = 7
if background_music == True:
    music = pygame.mixer.Sound('./assets/Sounds/intro.wav')
    channel1.play(music)

while time_left >= 0:

    ecran.fill(white)
    countdown()
    logo_width, logo_height = logo.image.get_rect().size
    logo.image = pygame.transform.scale(logo.image, (logo.img_width*LARGEUR_ECRAN/1920,logo.img_height*HAUTEUR_ECRAN/1080))
    ecran.blit(logo.image,(LARGEUR_ECRAN/2-logo_width/2,HAUTEUR_ECRAN/2-logo_height/2))
    #draw_text("ARDUCIBLE PETANQUE GAME",LARGEUR_ECRAN/2,HAUTEUR_ECRAN*1/4,True,True,1,5)
    pygame.display.flip()
time_left = intro_length
# run the background game music

if background_music == True:
    print("Turn on music")
    music = pygame.mixer.Sound('./assets/Sounds/Arducible vibe.mp3')
    
    channel1.play(music, loops = -1)
    
    


init_cibles()


#---------------------------main game loop------------------------------

while continuer:
    #global timer pour le blinking text
    current_time=pygame.time.get_ticks()
    if current_time - old_current_time > 500:
        old_current_time=current_time
        if affichage == True:
            affichage=False
        else:
            affichage=True
                    
    #-----------------------begining scene------------------------------
    if gamestate == 0:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continuer = False
                print("exit game")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    continuer = False
                    print("exit game")
           
            elif event.type == pygame.KEYUP:
                #press m key to mute/unmute only backgroud music
                if event.key == pygame.K_i:
                        credit_left = credit_left + 1
                if event.key == pygame.K_m:
                        if channel1.get_busy():
                            channel1.fadeout(FadeoutTime)
                        else:
                            channel1.play(music, loops = -1)
                #press s key to mute/unmute soud effects and music
                if event.key == pygame.K_s:
                    if sound_effects == True:
                        if channel1.get_busy():
                            channel1.fadeout(FadeoutTime)
                        sound_effects = False
                    else:
                        sound_effects = True
                        #if not channel1.get_busy():
                        channel1.play(music, loops = -1)
                    
                        
                        
        
        introbackground.update()

        ecran.blit(introbackground.image, introbackground.rect)
        


        
        if debug_line == True:
            debug_lines()
        
        if ShowFPS == True:
            fps = str(int(clock.get_fps()))
            FPS1 = FontDel1.render(fps, True, blue)
            FPS2 = FontDel2.render(fps, True, bluelight)
            ecran.blit(FPS1,(0,0))
            ecran.blit(FPS2,(0,0))

        if credit_left < 1:
            #print("insert Coin")
            draw_text("insert coin",LARGEUR_ECRAN/2,HAUTEUR_ECRAN*3/4, True,True,1,3)
            draw_intro_insertCoin()
            Animation1.update()
            ecran.blit(Animation1.image, (LARGEUR_ECRAN*4/20-Animation1.res_img_width/2, HAUTEUR_ECRAN*9/20-Animation1.res_img_height/2 ))
            Animation2.update()
            ecran.blit(Animation2.image, (LARGEUR_ECRAN*8/20-Animation2.res_img_width/2, HAUTEUR_ECRAN*9/20-Animation2.res_img_height/2 ))
            Animation3.update()
            ecran.blit(Animation3.image, (LARGEUR_ECRAN*12/20-Animation3.res_img_width/2, HAUTEUR_ECRAN*9/20-Animation3.res_img_height/2 ))
            Animation4.update()
            ecran.blit(Animation4.image, (LARGEUR_ECRAN*16/20-Animation4.res_img_width/2, HAUTEUR_ECRAN*9/20-Animation4.res_img_height/2 ))
           
        else:
            if not music_fadeout_started:
                channel1.fadeout(9000)
                music_fadeout_started = True
            countdown()
            draw_intro_text()
            if time_left <= 0:
                music_fadeout_started = False
                credit_left = credit_left-1
                if background_music == True:
                    music = pygame.mixer.Sound('./assets/Sounds/Boules Under the Sun.mp3')
                    channel1.play(music, loops = -1)

                next_gamestate()

        #    if webcam_compatibility == True:
        #        mycam.updateintro(mycam.cap, mycam.mp_drawing,mycam.mp_pose)
        #        showcam()
        #        pygame.display.flip()
        #        if mycam.results.pose_landmarks:
        #            if mycam.LeftHandUp == True and mycam.RightHandUp == True :
        #                player = mycam.images
        #                cartoonize_player()
        #                pygame.image.save(player, "image.jpg")
            #waiting = False
        #                print(mycam.LeftHandUp, mycam.RightHandUp)
                



        pygame.display.flip()

        
    #-----------------------Game scene----------------------------------
    if gamestate == 1:
        countdown()
        
        
        if webcam_compatibility == True:
            mycam.update()
            showcam()
            webcam_zone_interdite = mycam.zoneinterdite
            ecran.blit(ingamebackground.image, ingamebackground.rect)
            #ecran.blit(ingamebackground.image, ingamebackground.rect)
            #if DebugCam == True:
            #   showcam()
            
            draw_camring()
        else:
            ecran.blit(ingamebackground.image, ingamebackground.rect)


        for event in pygame.event.get():
            
            
            if event.type == pygame.QUIT:
                
                continuer = False
                print("exit game")
            
            elif event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_ESCAPE:
                    continuer = False
                    print("exit game")

            elif event.type == pygame.KEYUP:
                
                if webcam_zone_interdite == False:
                    
                    if event.key == pygame.K_i:
                        credit_left = credit_left + 1
                    if event.key == pygame.K_e:
                        
                        if cibleencours == 1:
                            animate_cible()
                            update_score()
                            ciblealeatoire()
                    if event.key == pygame.K_r:
                        
                        if cibleencours == 2:
                            animate_cible()
                            update_score()
                            ciblealeatoire() 
                    
                    if event.key == pygame.K_t:
                        
                        if cibleencours == 3:
                            animate_cible()
                            update_score()
                            ciblealeatoire()
                    
                    if event.key == pygame.K_m:
                        if channel1.get_busy():
                            channel1.fadeout(FadeoutTime)
                        else:
                            channel1.play(music, loops = -1)
                    
                    if event.key == pygame.K_s:
                        if sound_effects == True:
                            if channel1.get_busy():
                                channel1.fadeout(FadeoutTime)
                                sound_effects = False
                        else:
                            sound_effects = True
                            #if not channel1.get_busy():
                            channel1.play(music, loops = -1)



        draw_cibles()
        ingamedraw()
        
        if time_left <= 0:
            if background_music == True:
                music = pygame.mixer.Sound('./assets/Sounds/Arducible vibe.mp3')
                channel1.play(music, loops = -1)
    
            next_gamestate()

        #clock.tick(60)
    #-----------------------ending scene--------------------------------    
    if gamestate == 2:
        
        countdown()
        
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
            
                continuer = False
                print("exit game")
            
            elif event.type == pygame.KEYDOWN:
            
                if event.key == pygame.K_ESCAPE:
            
                    continuer = False
                    print("exit game")
            
                    
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_i:
                        credit_left = credit_left + 1
                if event.key == pygame.K_m:
                        if channel1.get_busy():
                            channel1.fadeout(FadeoutTime)
                        else:
                            channel1.play(music, loops = -1)
                            
                if event.key == pygame.K_s:
                    if sound_effects == True:
                        if channel1.get_busy():
                            channel1.fadeout(FadeoutTime)
                        sound_effects = False
                    else:
                        sound_effects = True
                        #if not channel1.get_busy():
                        channel1.play(music, loops = -1)
                
        
        if score >= high_score:
            high_score = score
            save_high_score(high_score)

        ecran.blit(ingamebackground.image, ingamebackground.rect)

        draw_ending_text()
        
        if debug_line == True:
            debug_lines()
        
        if ShowFPS == True:
            fps = str(int(clock.get_fps()))
            FPS1 = FontDel1.render(fps, True, blue)
            FPS2 = FontDel2.render(fps, True, bluelight)
            ecran.blit(FPS1,(200,0))
            ecran.blit(FPS2,(200,0))
            #ecran.blit(player, (0,0))
        
        pygame.display.flip()
        
        if time_left <= 0:
            next_gamestate()
            
    clock.tick(FPS) #set to 30 FPS
    
    

pygame.quit()

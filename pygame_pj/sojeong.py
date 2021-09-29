import pygame
import random
from time import sleep


WHITE = (255,255,255) # 흰색을 표현하는 값
RED = (255,0,0)       # 빨강색을 표현하는 값
pad_width=1080        # 게임판의 길이
pad_height = 650      # 게임판의 높이
background_width = 1080

sled_width = 144
sled_height = 105

barrier_width = 128
barrier_height = 128

snowball_width = 64
snowball_height = 64
ice_width = 64
ice_height = 68

life_height = 64

health = 3 # 초기 생명 3개로 정하기

# 총 시간
total_time = 31

# 시작 시간 >> tick을 받아옴
start_ticks = pygame.time.get_ticks()

# 승리했을 때 
def victory():
    global gamepad, health
    health = 3  # 다시 생명 3개로 설정
    pygame.mixer.music.stop()               # 게임 bgm -> 승리 bgm으로 전환
    pygame.mixer.music.load("victory.mp3")  
    pygame.mixer.music.set_volume(0.01)
    pygame.mixer.music.play(-1)
    dispMessage("Victory!")                 # Victory! 출력
    sleep(8.7)                              # 승리 bgm 8.7초 동안 틀기
    pygame.mixer.music.stop()
    initGame()                              # 다시 메뉴로 돌아가기

# 게임에서 졌을 때
def gameOver():
    global gamepad, health, total_time
    health = 3  # 다시 생명 3개로 설정
    pygame.mixer.music.stop()               # 게임 bgm -> 게임오버 bgm으로 전환
    pygame.mixer.music.load("gameover.mp3")
    pygame.mixer.music.set_volume(0.03)
    pygame.mixer.music.play(-1)
    dispMessage("GAME OVER")                # GAME OVER 출력
    sleep(6.2)                              # 승리 bgm 6.2초 동안 틀기
    pygame.mixer.music.stop()
    initGame()                              # 다시 메뉴로 돌아가기
    
# 게임 화면에 표시될 텍스트 모양과 영역 설정
def textObj(text,font): 
    textSurface = font.render(text,True, RED) 
    return textSurface, textSurface.get_rect()

# 게임 화면 정중앙에 text로 지정된 글자를 출력
def dispMessage(text): 
    global gamepad,total_time
    largeText = pygame.font.Font("freesansbold.ttf",115)  # 폰트, 크기 설정
    TextSurf, TextRect = textObj(text, largeText)         
    TextRect.center = ((pad_width/2),(pad_height/2))
    gamepad.blit(TextSurf, TextRect)    # 게임판 위에 글자 출력
    pygame.display.update()
    sleep(1)    # 1초동안 출력
    
# 장애물에 부딪혔을 때 
def crash(): 
    global gamepad, explosion_sound
    
    pygame.mixer.music.pause()   # 게임 bgm 잠시 멈춤
    boom=pygame.mixer.Sound.play(explosion_sound) # 부딪혔을 때 소리 설정
    boom.set_volume(0.01)    # 볼륨은 0.01
    dispMessage("Crashed!")  # Crashed! 출력
    runGame()                # 다시 게임으로 돌아가서 이어서 실행fr5oP 
  

# 삽입한 이미지 파일을 게임판 위에 그려주는 함수
def drawObject(obj, x, y):
    global gamepad
    gamepad.blit(obj, (x,y))

# 배경 이미지를 게임판 위에 그려주는 함수
def back(background, x,y): 
    global gamepad
    gamepad.blit(background,(x,y))

# 실제 게임이 구동되는 함수
def runGame(): 
    global gamepad, sled, clock, background1, background2, total_time, start_ticks, RED
    global barrier, snowball, ice,life, health, snowball_height, pad_height, life_height, time

    pygame.mixer.music.unpause()  # 중단했던 게임bgm 다시 플레이


    x=pad_height*0.2  # 썰매의 최초 위치
    y=pad_height*0.01 # 썰매의 최초 위치
    y_change = 0      # y의 좌표 변화

    background1_x=0 # 배경 이미지의 좌상단 모서리의 x좌표, 최초값은 0
    background2_x = background_width # 배경 이미지 복사본을 배경 이미지 원본 바로 다음에 위치시키도록 좌표 지정

    barrier_x = pad_width # 장애물의 x좌표는 게임판의 맨 오른쪽 끝
    barrier_y = random.randrange(0,pad_height) # y좌표는 게임판 높이 범위에서 무작위로 선택
    
    snowball_x = pad_width # 눈덩이의 x좌표는 게임판의 맨 오른쪽 끝
    snowball_y = random.randrange(0,pad_height)

    ice_x = pad_width # 눈덩이의 x좌표는 게임판의 맨 오른쪽 끝
    ice_y = random.randrange(0,pad_height)


    crashed = False
    while not crashed:
        for event in pygame.event.get():  # 키보드의 위 화살표와 아래 화살표 키를 누르면 비행기가 위 아래로 12픽셀씩 움직인다.
            if event.type == pygame.QUIT: # pygame의 X버튼을 누르면 while문 밖으로 빠져나가 게임 종료
                crashed = True

            if event.type == pygame.KEYDOWN: # 키가 눌렸을 때
                if event.key==pygame.K_UP:   # 위쪽 화살표 키 눌렀을 때
                    y_change=-12
                elif event.key==pygame.K_DOWN: # 아래쪽 화살표 키 눌렀을 때
                    y_change = 12
                    
            if event.type == pygame.KEYUP:   # 키가 눌렸을 때
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN: # 위쪽 화살표 키 눌렀을 때나 아래쪽 화살표 키 눌렀을 때
                    y_change = 0             # 움직이지 않는다

        gamepad.fill(WHITE)
        
        background1_x -=2 # 배경 이미지를 왼쪽으로 2픽셀 만큼 이동
        background2_x-=2  # 배경 이미지 복사본을 왼쪽으로 2픽셀 만큼 이동

        if background1_x == -background_width: # 배경 이미지가 게임판에서 사라지면 그 위치를 배경 이미지 복사본 오른쪽으로 다시 위치시킴
            background1_x = background_width   # 배경 이미지 복사본이 게임판에서 완전히 사라지면 배경 이미지 오른쪽으로 다시 위치시킴
            
        if background2_x == -background_width:
            background2_x = background_width
        back(background1, background1_x,0) # 배경 이미지를 게임판에 그리기 위해 좌상단 모서리의 x좌표를 y좌표로 전달, 최초값은 0,0
        back(background2, background2_x,0)
        drawObject(background1, background1_x, 0)
        drawObject(background1, background1_x, 0)

        # 폰트 정의  Font(None으로 하면 알아서 기본값으로 출력, 글씨 크기)
        game_font = pygame.font.Font(None, 40) 

        # 경과 시간 계산(milisecond라 1000으로 나눠 1초로 표시)
        # start_ticks 은 고정, pygame.time.get_ticks()는 점점 커지는 듯
        elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000

        #현재 남은 시간
        result_time = int(total_time - elapsed_time)

        # render(시간 표현글자, True, (색상 rgb 코드))
        timer = game_font.render("Time : {}".format(result_time), True, RED)

        # blit(화면에 타이머 출력, ( x, y 좌표))
        gamepad.blit(timer, (10, 10))

        y+=y_change # 키보드 입력에 따라 썰매의 y좌표를 변경
        if y<0:
            y=0
        elif y>pad_height-sled_height:
            y=pad_height-sled_height

        barrier_x-=7     # 장애물을 7픽셀씩 날아오게 함
        if barrier_x<=0: # 왼쪽 끝까지 날아가면 다시 오른쪽 끝에서 날아오게 함
            barrier_x=pad_width
            barrier_y=random.randrange(0,pad_height)
            if barrier_y<0:
                barrier_y=0
            elif barrier_y>pad_height-barrier_height:
                barrier_y=pad_height-barrier_height
            
        
        snowball_x-=12     # 장애물을 12픽셀씩 날아오게 함
        if snowball_x <=0: # 왼쪽 끝까지 날아가면 다시 오른쪽 끝에서 날아오게 함
            snowball_x = pad_width
            snowball_y=random.randrange(0,pad_height)
            if snowball_y<0:
                snowball_y=0
            elif snowball_y>pad_height-snowball_height:
                snowball_y=pad_height-snowball_height


        ice_x-=17      # 장애물을 17픽셀씩 날아오게 함
        if ice_x <=0:  # 왼쪽 끝까지 날아가면 다시 오른쪽 끝에서 날아오게 함
            ice_x = pad_width
            ice_y=random.randrange(0,pad_height)
            if ice_y<0:
                ice_y=0
            elif ice_y>pad_height-ice_height:
                ice_y=pad_height-ice_height

        if x+sled_width>barrier_x: # 썰매와 장애물이 부딪혔는지 확인
            if(y>barrier_y and y<barrier_y+barrier_height) or (y+sled_height>barrier_y and y+sled_height< barrier_y+barrier_height):
                health-=1  # 부딪히면 생명 1개 사라짐
                
                if health == 0: # 장애물과 부딪혔을 때 생명이 0이면 게임오버, 아니면 충돌 함수 호출
                    gameOver()
                crash()

        if x+sled_width>snowball_x: # 썰매와 장애물이 부딪혔는지 확인
                if (y>snowball_y and y<snowball_y+snowball_height) or (y+sled_height>snowball_y and y+sled_height< snowball_y+snowball_height):
                    health-=1  # 부딪히면 생명 1개 사라짐
                    
                    if health == 0: # 장애물과 부딪혔을 때 생명이 0이면 게임오버, 아니면 충돌 함수 호출
                        gameOver()
                    crash()
        
        if x+sled_width>ice_x: # 썰매와 장애물이 부딪혔는지 확인
            if(y>ice_y and y<ice_y+ice_height) or (y+sled_height>ice_y and y+sled_height< ice_y+ice_height):
                health-=1  # 부딪히면 생명 1개 사라짐
               
                if health == 0: # 장애물과 부딪혔을 때 생명이 0이면 게임오버, 아니면 충돌 함수 호출
                    gameOver()
                crash()

        # 시간 초과했을때 승리
        if health > 0 and result_time <= 0:
            victory()

        # 게임판에 이미지 파일들 출력
        drawObject(sled, x,y)
        drawObject(barrier, barrier_x, barrier_y)
        drawObject(snowball, snowball_x, snowball_y)
        drawObject(ice, ice_x, ice_y)
        
        for i in range(0,health):  # 남은 생명 게임판에 출력
            drawObject(life, i*60, pad_height-life_height)
            
        pygame.display.update() 
        clock.tick(60) # 60 프레임 설정
        
    pygame.quit() # pygame 종료
    quit()        # 스크립트 창 닫기

# 게임을 초기화하고 시작하는 함수
def initGame():   
    global gamepad, sled, clock,background1, background2, menu_background
    global barrier, snowball, ice, life, health, start_ticks
    global explosion_sound

    
    
    pygame.init() # PyGame 라이브러리 초기화
    gamepad = pygame.display.set_mode((pad_width, pad_height)) # 게임판 크기 설정
    pygame.display.set_caption("PyFlying")                     # 게임판 타이틀 설정
    sled = pygame.image.load("sled.png")                       # 게임 캐릭터 설정
    background1 = pygame.image.load("background.png")          # 게임 배경 설정
    background2 = background1.copy()                           # 게임 배경 복사
    barrier = pygame.image.load("barrier128.png")              # 게임 장애물1 설정
    snowball = pygame.image.load("snowball.png")               # 게임 장애물2 설정
    ice = pygame.image.load("ice.png")                         # 게임 장애물3 설정
    life = pygame.image.load("health.png")                     # 게임 생명 설정
    explosion_sound = pygame.mixer.Sound("explosion.wav")      # 부딪힐 때 나는 소리
    pygame.mixer.music.load("intro.mp3")                       # 게임 메뉴 노래 설정
    pygame.mixer.music.set_volume(0.03)                        # 볼륨 0.03 지정
    pygame.mixer.music.play(-1)                                # 메뉴 노래 플레이
    menu_background = pygame.image.load("menu.png")            # 메뉴 배경 설정

    gamepad.blit(menu_background,(0,0))     # 배경 이미지의 좌상단 모서리의 x좌표, 최초값은 0
    crashed = False
    while not crashed:
      for event in pygame.event.get():                # 이벤트가 발생 했을 시
            if event.type == pygame.MOUSEBUTTONDOWN:  # 마우스 버튼 이벤트가 발생 했을 때
                x,y = pygame.mouse.get_pos()          # 마우스가 눌린 위치를 받아옴
                if x >= 400 and x <= 700:             # 마우스를 누른 위치가 버튼이 그려진 x축 범위안에 들어 왔는지 판단
                        if y >= 350 and y <= 450:     # y축 범위 판단 후, 버튼 1이 눌렸을 경우(game start 버튼)
                            
                            start_ticks = pygame.time.get_ticks()  # 시작 시간 >> tick을 받아옴
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load("bgm.mp3")     # intro -> bgm으로 노래 변경
                            pygame.mixer.music.set_volume(0.03)    # 볼륨 0.03 설정
                            pygame.mixer.music.play(-1)
                            runGame()                 # 게임 구동 함수 호출, game start버튼이 눌렸음을 표시
                        if y >= 500 and y <= 600:     # y축 범위 판단 후, 버튼 2이 눌렸을 경우(game quit 버튼)
                            crashed = True            # 반복문 탈출을 위해 충돌여부를 참으로 만듬
                            pygame.quit()             # pygame을 종료시킴
                            quit()                    # 스크립트 종료
      pygame.display.update() 
      clock = pygame.time.Clock() # 게임의 초당 프레임 설정을 위한 클락 생성
    clock.tick(60)  # 60 프레임 설정
    
initGame() # 제일 처음에 initGame()을 호출하여 GUI 실행


import pygame
import random
import sys

# 초기화
pygame.init()

# 창 크기
window_size = (600, 600)

# 색상 정의
black = (0, 0, 0)
white = (255, 255, 255)

# 화면 생성
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Simple Game")

# 주인공 이미지 로드
player_image_original = pygame.image.load("ai_project/project/image/fish-removebg-preview.png")
player_size = player_image_original.get_size()
player_pos = [window_size[0] // 2 - player_size[0] // 2, 500]

# 아이템 이미지 로드
item1_image = pygame.image.load("ai_project/project/image/flang-removebg-preview.png")
item2_image = pygame.image.load("ai_project/project/image/hos.png")
item3_image = pygame.image.load("ai_project/project/image/plastic.png")
item_size = (50, 50)

# 하트 이미지 로드
heart_image = pygame.image.load("ai_project/project/image/heart-removebg-preview.png")
heart_size = (30, 30)

# 아이템 설정
items = []

# 점수 및 체력 설정
score = 0
health = 3

# 폰트 설정
font = pygame.font.Font(None, 36)

# 게임 루프
clock = pygame.time.Clock()
fall_speed = 3
item_spawn_timer = 0

# 초기 이미지는 왼쪽을 바라봄
facing_left = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= 5
        
        player_image_original = pygame.transform.flip(player_image_original, True, True)

    if keys[pygame.K_RIGHT] and player_pos[0] < window_size[0] - player_size[0]:
        player_pos[0] += 5
        
        player_image_original = pygame.transform.flip(player_image_original, False, False)
           

    

    # 아이템 생성
    item_spawn_timer += 1
    if item_spawn_timer == 30:
        item_spawn_timer = 0
        if random.uniform(0, 1) < 0.65:
            items.append([random.randint(0, window_size[0] - item_size[0]), 0, 10])  # 첫 번째 아이템
        elif random.uniform(0, 1) < 0.05:
            items.append([random.randint(0, window_size[0] - item_size[0]), 0, 20])  # 두 번째 아이템
        else:
            items.append([random.randint(0, window_size[0] - item_size[0]), 0, -1])  # 세 번째 아이템

    # 아이템 이동
    for item in items:
        item[1] += fall_speed

    # 충돌 체크
    for item in items:
        if (
            player_pos[0] < item[0] + item_size[0]
            and player_pos[0] + player_size[0] > item[0]
            and player_pos[1] < item[1] + item_size[1]
            and player_pos[1] + player_size[1] > item[1]
        ):
            if item[2] == 10:
                score += 10
            elif item[2] == 20:
                if health < 3:
                    health += 1
            elif item[2] == -1:
                health -= 1
                if health <= 0:
                    print("게임 종료 - 체력이 다 소진되었습니다.")
                    pygame.quit()
                    sys.exit()
            items.remove(item)

    # 화면 그리기
    screen.fill(black)
    screen.blit(player_image_original, (player_pos[0], player_pos[1]))

    for item in items:
        if item[2] == 10:
            screen.blit(item1_image, (item[0], item[1]))
        elif item[2] == 20:
            screen.blit(item2_image, (item[0], item[1]))
        elif item[2] == -1:
            screen.blit(item3_image, (item[0], item[1]))

    # 점수 및 체력 표시
    score_text = font.render("Score: " + str(score), True, white)
    screen.blit(score_text, (window_size[0] - 150, 20))

    for i in range(health):
        screen.blit(heart_image, (20 + i * 40, 20))

    pygame.display.update()
    clock.tick(60)


import pygame
import random
import sys

# 초기화
pygame.init()

# 창 크기
window_size = (800, 800)

# 색상 정의
black = (0, 0, 0)
white = (255, 255, 255)

# 화면 생성
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Simple Game")

# 시작화면 이미지 로드
start_screen_image = pygame.image.load("ai_project/project/image/intro.png")

# 주인공 이미지 로드
player_image_A = pygame.image.load("ai_project/project/image/fish-removebg-preview.png")
player_image_B = pygame.image.load("ai_project/project/image/fish_right.png")
player_images = [player_image_A, player_image_B]
current_player_image = player_images[0]
player_size = current_player_image.get_size()
player_pos = [window_size[0] // 2 - player_size[0] // 2, 700]

# 아이템 이미지 로드
item1_image = pygame.image.load("ai_project/project/image/flang-removebg-preview.png")
item2_image = pygame.image.load("ai_project/project/image/heart-removebg-preview.png")
item3_image = pygame.image.load("ai_project/project/image/plastic.png")
item_size = (50, 50)

# 하트 이미지 로드
heart_image = pygame.image.load("ai_project/project/image/hos-removebg-preview.png")
heart_size = (30, 30)

# 게임 종료 이미지 로드
game_over_image = pygame.image.load("ai_project/project/image/end.png")

# 아이템 설정
items = []

# 점수 및 체력 설정
score = 0
health = 3

# 폰트 설정
font = pygame.font.Font(None, 36)

# 게임 시작 여부를 나타내는 변수
game_started = False

# 게임 종료 여부를 나타내는 변수
game_over = False

# 게임 루프
clock = pygame.time.Clock()
fall_speed = 3
item_spawn_timer = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_started and not game_over:
            # 마우스 좌클릭 시 게임 시작
            game_started = True

    screen.fill(black)

    if not game_started:
        # 시작 화면에서 이미지를 띄움
        screen.blit(start_screen_image, (0, 0))
    elif game_over:
        # 게임 종료 화면에서 이미지를 띄움
        screen.blit(game_over_image, (0, 0))
    else:
        # 게임 시작 후의 로직
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_pos[0] > 0:
            player_pos[0] -= 5
        if keys[pygame.K_RIGHT] and player_pos[0] < window_size[0] - player_size[0]:
            player_pos[0] += 5

        # 아이템 이동
        for item in items:
            if not item[3]:  # 충돌하지 않았을 경우에만 이동
                item[1] += fall_speed

        # 충돌 체크
        for item in items:
            if not item[3]:  # 충돌하지 않았을 경우에만 체크
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
                            game_over = True  # 게임 종료 상태로 변경
                    item[3] = True  # 충돌 표시

        # 화면 그리기
        screen.blit(current_player_image, (player_pos[0], player_pos[1]))

        for item in items:
            if not item[3]:  # 충돌하지 않았을 경우에만 그림
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

        # 아이템 생성
        item_spawn_timer += 1
        if item_spawn_timer == 30:
            item_spawn_timer = 0
            if random.uniform(0, 1) < 0.65:
                items.append([random.randint(0, window_size[0] - item_size[0]), 0, 10, False])  # 네 번째 파라미터: 충돌 여부
            elif random.uniform(0, 1) < 0.05:
                items.append([random.randint(0, window_size[0] - item_size[0]), 0, 20, False])  # 다섯 번째 파라미터: 충돌 여부
            else:
                items.append([random.randint(0, window_size[0] - item_size[0]), 0, -1, False])  # 여섯 번째 파라미터: 충돌 여부

    # 나머지 코드
    pygame.display.update()
    clock.tick(60)
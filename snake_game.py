#cmd
#pip install pygame
import pygame
import random
import sys

# 초기화
pygame.init()

# 색 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 200, 0)

# 화면 크기 설정
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

CELL_SIZE = 20

DIRECTIONS = {
    'UP': (0, -1),
    'DOWN': (0, 1),
    'LEFT': (-1, 0),
    'RIGHT': (1, 0),
}
OPPOSITE_DIRECTION = {
    'UP': 'DOWN',
    'DOWN': 'UP',
    'LEFT': 'RIGHT',
    'RIGHT': 'LEFT',
}

# 화면 및 캡션
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("뱀 게임")
clock = pygame.time.Clock()

def load_font(size):
    korean_font = pygame.font.match_font('malgungothic') or pygame.font.match_font('malgun gothic')
    if korean_font:
        return pygame.font.Font(korean_font, size)
    return pygame.font.Font(None, size)

font = load_font(36)
small_font = load_font(24)


def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def get_next_position(position, direction):
    dx, dy = DIRECTIONS[direction]
    return [position[0] + dx * CELL_SIZE, position[1] + dy * CELL_SIZE]


def is_collision(position, body_positions):
    return (position[0] < 0 or position[0] >= SCREEN_WIDTH or
            position[1] < 0 or position[1] >= SCREEN_HEIGHT or
            position in body_positions)


def choose_ai_direction(ai_head, current_direction, apple_pos, ai_body, player_body):
    candidates = []
    for direction in DIRECTIONS:
        if direction == OPPOSITE_DIRECTION[current_direction]:
            continue
        next_head = get_next_position(ai_head, direction)
        if is_collision(next_head, ai_body[:-1] + player_body):
            continue
        distance = abs(next_head[0] - apple_pos[0]) + abs(next_head[1] - apple_pos[1])
        candidates.append((distance, direction))

    if candidates:
        candidates.sort(key=lambda item: item[0])
        return candidates[0][1]

    for direction in DIRECTIONS:
        next_head = get_next_position(ai_head, direction)
        if not is_collision(next_head, ai_body[:-1] + player_body):
            return direction

    return current_direction


def start_screen():
    screen.fill(BLACK)
    draw_text("뱀 게임", font, GREEN, screen, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 4)
    draw_text("방향키로 이동하세요", small_font, WHITE, screen, SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2)
    draw_text("아무 키를 누르면 시작합니다", small_font, WHITE, screen, SCREEN_WIDTH // 6, SCREEN_HEIGHT // 2 + 50)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return


def game_over_screen(player_score, ai_score):
    screen.fill(BLACK)
    draw_text("게임 종료", font, RED, screen, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3 - 40)
    draw_text(f"플레이어 점수: {player_score}", small_font, WHITE, screen, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3 + 10)
    draw_text(f"AI 점수: {ai_score}", small_font, WHITE, screen, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3 + 40)

    if player_score > ai_score:
        result_text = "플레이어 승리!"
    elif ai_score > player_score:
        result_text = "AI 승리!"
    else:
        result_text = "무승부!"

    draw_text(result_text, font, GREEN, screen, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3 + 90)
    draw_text("다시 시작하려면 R, 종료하려면 Q", small_font, WHITE, screen, SCREEN_WIDTH // 6, SCREEN_HEIGHT // 3 + 140)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


def main():
    player_snake = [[100, 220], [80, 220], [60, 220]]
    ai_snake = [[520, 260], [540, 260], [560, 260]]
    player_direction = 'RIGHT'
    player_change = player_direction
    ai_direction = 'LEFT'

    player_score = 0
    ai_score = 0
    player_alive = True
    ai_alive = True

    apple_pos = [random.randrange(1, SCREEN_WIDTH // CELL_SIZE) * CELL_SIZE,
                 random.randrange(1, SCREEN_HEIGHT // CELL_SIZE) * CELL_SIZE]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and player_alive:
                if event.key == pygame.K_UP and player_direction != 'DOWN':
                    player_change = 'UP'
                elif event.key == pygame.K_DOWN and player_direction != 'UP':
                    player_change = 'DOWN'
                elif event.key == pygame.K_LEFT and player_direction != 'RIGHT':
                    player_change = 'LEFT'
                elif event.key == pygame.K_RIGHT and player_direction != 'LEFT':
                    player_change = 'RIGHT'

        if player_alive:
            player_direction = player_change

        if ai_alive:
            ai_direction = choose_ai_direction(ai_snake[0], ai_direction, apple_pos, ai_snake, player_snake)

        player_next = get_next_position(player_snake[0], player_direction) if player_alive else None
        ai_next = get_next_position(ai_snake[0], ai_direction) if ai_alive else None

        player_collision = False
        ai_collision = False

        if player_alive:
            if (is_collision(player_next, player_snake[:-1]) or is_collision(player_next, ai_snake)):
                player_collision = True
        if ai_alive:
            if (is_collision(ai_next, ai_snake[:-1]) or is_collision(ai_next, player_snake)):
                ai_collision = True

        if player_alive and ai_alive and player_next == ai_next:
            player_collision = True
            ai_collision = True

        if player_collision:
            player_alive = False
        if ai_collision:
            ai_alive = False

        ate_by_player = player_alive and player_next == apple_pos
        ate_by_ai = ai_alive and ai_next == apple_pos

        if player_alive:
            player_snake.insert(0, player_next)
            if not ate_by_player:
                player_snake.pop()
            else:
                player_score += 1
        if ai_alive:
            ai_snake.insert(0, ai_next)
            if not ate_by_ai:
                ai_snake.pop()
            else:
                ai_score += 1

        if ate_by_player or ate_by_ai:
            apple_pos = [random.randrange(1, SCREEN_WIDTH // CELL_SIZE) * CELL_SIZE,
                         random.randrange(1, SCREEN_HEIGHT // CELL_SIZE) * CELL_SIZE]

        if not player_alive and not ai_alive:
            game_over_screen(player_score, ai_score)

        screen.fill(BLACK)
        pygame.draw.rect(screen, RED, pygame.Rect(apple_pos[0], apple_pos[1], CELL_SIZE, CELL_SIZE))

        for idx, pos in enumerate(player_snake):
            color = YELLOW if idx == 0 else GREEN
            pygame.draw.rect(screen, color, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))
        for idx, pos in enumerate(ai_snake):
            color = BLUE if idx == 0 else (0, 150, 200)
            pygame.draw.rect(screen, color, pygame.Rect(pos[0], pos[1], CELL_SIZE, CELL_SIZE))

        draw_text(f"플레이어: {player_score}", small_font, WHITE, screen, 10, 10)
        draw_text(f"AI: {ai_score}", small_font, WHITE, screen, 10, 35)

        pygame.display.update()
        clock.tick(10)

if __name__ == '__main__':
    start_screen()
    main()
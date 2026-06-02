import random
import tkinter as tk
from tkinter import messagebox

COLS = 10
ROWS = 20
CELL_SIZE = 28
PREVIEW_SIZE = 4
LEVEL_SPEED = lambda level: max(120, 700 - (level - 1) * 60)
POINTS = {1: 100, 2: 300, 3: 500, 4: 800}

SHAPES = [
    [],
    [[1, 1, 1, 1]],
    [[2, 2], [2, 2]],
    [[0, 3, 0], [3, 3, 3]],
    [[4, 4, 0], [0, 4, 4]],
    [[0, 5, 5], [5, 5, 0]],
    [[6, 6, 6], [0, 0, 6]],
    [[7, 7, 7], [7, 0, 0]],
]

COLORS = [
    None,
    '#4dd0e1',
    '#ffeb3b',
    '#9575cd',
    '#ff7043',
    '#66bb6a',
    '#f06292',
    '#90caf9',
]

class Tetris:
    def __init__(self, root):
        self.root = root
        self.root.title('Python Tetris')
        self.root.resizable(False, False)

        self.board = self.create_matrix(COLS, ROWS)
        self.current_piece = None
        self.next_piece = None
        self.score = 0
        self.level = 1
        self.lines = 0
        self.playing = False
        self.drop_interval = LEVEL_SPEED(self.level)
        self.drop_job = None

        self.create_widgets()
        self.bind_keys()
        self.new_game()

    def create_widgets(self):
        main_frame = tk.Frame(self.root, bg='#111')
        main_frame.pack(padx=12, pady=12)

        board_frame = tk.Frame(main_frame, bg='#1b1b1b', bd=2, relief='ridge')
        board_frame.grid(row=0, column=0, padx=(0, 12), pady=0)

        self.canvas = tk.Canvas(
            board_frame,
            width=COLS * CELL_SIZE,
            height=ROWS * CELL_SIZE,
            bg='#111',
            highlightthickness=0,
        )
        self.canvas.pack()

        side_frame = tk.Frame(main_frame, bg='#111')
        side_frame.grid(row=0, column=1, sticky='n')

        title = tk.Label(
            side_frame,
            text='테트리스',
            fg='#f6f6f6',
            bg='#111',
            font=('Segoe UI', 22, 'bold'),
        )
        title.pack(anchor='w', pady=(0, 12))

        desc = tk.Label(
            side_frame,
            text='Tkinter로 만든 간단한 테트리스입니다. ← → ↓ ↑, 스페이스로 하드 드롭 가능합니다.',
            fg='#ddd',
            bg='#111',
            font=('Segoe UI', 10),
            wraplength=260,
            justify='left',
        )
        desc.pack(anchor='w', pady=(0, 16))

        stats_frame = tk.Frame(side_frame, bg='#111')
        stats_frame.pack(fill='x', pady=(0, 16))

        self.score_label = self.create_stat_label(stats_frame, '점수', '0')
        self.level_label = self.create_stat_label(stats_frame, '레벨', '1')
        self.lines_label = self.create_stat_label(stats_frame, '라인', '0')

        preview_label = tk.Label(
            side_frame,
            text='다음 블록',
            fg='#f6f6f6',
            bg='#111',
            font=('Segoe UI', 12, 'bold'),
        )
        preview_label.pack(anchor='w', pady=(0, 8))

        self.preview_canvas = tk.Canvas(
            side_frame,
            width=PREVIEW_SIZE * CELL_SIZE,
            height=PREVIEW_SIZE * CELL_SIZE,
            bg='#111',
            highlightthickness=0,
        )
        self.preview_canvas.pack(pady=(0, 16))

        button_frame = tk.Frame(side_frame, bg='#111')
        button_frame.pack(fill='x')

        self.start_button = tk.Button(
            button_frame,
            text='게임 시작',
            command=self.start_game,
            bg='#64b5f6',
            fg='#111',
            font=('Segoe UI', 11, 'bold'),
            bd=0,
            relief='raised',
            padx=12,
            pady=10,
        )
        self.start_button.pack(fill='x', pady=(0, 8))

        self.restart_button = tk.Button(
            button_frame,
            text='재시작',
            command=self.new_game,
            bg='#ff8a65',
            fg='#111',
            font=('Segoe UI', 11, 'bold'),
            bd=0,
            relief='raised',
            padx=12,
            pady=10,
        )
        self.restart_button.pack(fill='x')

        controls = tk.Label(
            side_frame,
            text='조작: ← → ↓ ↑ 스페이스',
            fg='#bbb',
            bg='#111',
            font=('Segoe UI', 9),
            pady=14,
            justify='left',
        )
        controls.pack(anchor='w')

    def create_stat_label(self, parent, label, value):
        frame = tk.Frame(parent, bg='#111')
        frame.pack(fill='x', pady=2)
        tk.Label(frame, text=label, fg='#aaa', bg='#111', font=('Segoe UI', 10)).pack(side='left')
        var = tk.Label(frame, text=value, fg='#fff', bg='#111', font=('Segoe UI', 12, 'bold'))
        var.pack(side='right')
        return var

    def bind_keys(self):
        self.root.bind('<Left>', lambda event: self.move_piece(-1))
        self.root.bind('<Right>', lambda event: self.move_piece(1))
        self.root.bind('<Down>', lambda event: self.soft_drop())
        self.root.bind('<Up>', lambda event: self.rotate_piece())
        self.root.bind('<space>', lambda event: self.hard_drop())

    def create_matrix(self, width, height):
        return [[0 for _ in range(width)] for _ in range(height)]

    def new_game(self):
        if self.drop_job:
            self.root.after_cancel(self.drop_job)
            self.drop_job = None

        self.board = self.create_matrix(COLS, ROWS)
        self.score = 0
        self.level = 1
        self.lines = 0
        self.playing = False
        self.drop_interval = LEVEL_SPEED(self.level)
        self.current_piece = self.create_piece()
        self.next_piece = self.create_piece()
        self.update_stats()
        self.draw_board()
        self.draw_preview()

    def start_game(self):
        if not self.playing:
            self.playing = True
            self.schedule_drop()

    def create_piece(self):
        shape_id = random.randint(1, len(SHAPES) - 1)
        matrix = [row[:] for row in SHAPES[shape_id]]
        x = COLS // 2 - len(matrix[0]) // 2
        return {'matrix': matrix, 'pos': {'x': x, 'y': 0}, 'type': shape_id}

    def collide(self, matrix, pos):
        for y, row in enumerate(matrix):
            for x, value in enumerate(row):
                if value == 0:
                    continue
                px = pos['x'] + x
                py = pos['y'] + y
                if px < 0 or px >= COLS or py >= ROWS:
                    return True
                if py < 0:
                    continue
                if self.board[py][px] != 0:
                    return True
        return False

    def merge_piece(self):
        matrix = self.current_piece['matrix']
        pos = self.current_piece['pos']
        for y, row in enumerate(matrix):
            for x, value in enumerate(row):
                if value != 0:
                    self.board[pos['y'] + y][pos['x'] + x] = value

    def rotate(self, matrix, direction):
        rotated = [list(row) for row in zip(*matrix)]
        if direction > 0:
            rotated = [list(reversed(row)) for row in rotated]
        else:
            rotated.reverse()
        return rotated

    def rotate_piece(self):
        if not self.playing:
            return
        matrix = self.current_piece['matrix']
        rotated = self.rotate(matrix, 1)
        original_x = self.current_piece['pos']['x']
        original_matrix = self.current_piece['matrix']
        self.current_piece['matrix'] = rotated

        offsets = [0, -1, 1, -2, 2]
        for offset in offsets:
            self.current_piece['pos']['x'] = original_x + offset
            if not self.collide(self.current_piece['matrix'], self.current_piece['pos']):
                self.draw_board()
                return

        self.current_piece['matrix'] = original_matrix
        self.current_piece['pos']['x'] = original_x
        self.draw_board()

    def move_piece(self, dx):
        if not self.playing:
            return
        self.current_piece['pos']['x'] += dx
        if self.collide(self.current_piece['matrix'], self.current_piece['pos']):
            self.current_piece['pos']['x'] -= dx
        self.draw_board()

    def soft_drop(self):
        if not self.playing:
            return
        self.current_piece['pos']['y'] += 1
        if self.collide(self.current_piece['matrix'], self.current_piece['pos']):
            self.current_piece['pos']['y'] -= 1
            self.lock_piece()
        self.draw_board()

    def hard_drop(self):
        if not self.playing:
            return
        while not self.collide(self.current_piece['matrix'], {'x': self.current_piece['pos']['x'], 'y': self.current_piece['pos']['y'] + 1}):
            self.current_piece['pos']['y'] += 1
        self.lock_piece()
        self.draw_board()

    def lock_piece(self):
        self.merge_piece()
        removed = self.clear_lines()
        if removed > 0:
            self.score += POINTS.get(removed, 0)
            self.lines += removed
            self.level = self.lines // 10 + 1
            self.drop_interval = LEVEL_SPEED(self.level)
        self.update_stats()
        self.current_piece = self.next_piece
        self.next_piece = self.create_piece()
        self.draw_preview()
        if self.collide(self.current_piece['matrix'], self.current_piece['pos']):
            self.playing = False
            if self.drop_job:
                self.root.after_cancel(self.drop_job)
                self.drop_job = None
            messagebox.showinfo('게임 오버', f'게임 오버! 점수: {self.score}')

    def clear_lines(self):
        removed = 0
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        removed = ROWS - len(new_board)
        while len(new_board) < ROWS:
            new_board.insert(0, [0] * COLS)
        self.board = new_board
        return removed

    def schedule_drop(self):
        if not self.playing:
            return
        self.soft_drop()
        self.draw_board()
        self.drop_job = self.root.after(self.drop_interval, self.schedule_drop)

    def update_stats(self):
        self.score_label.config(text=str(self.score))
        self.level_label.config(text=str(self.level))
        self.lines_label.config(text=str(self.lines))

    def draw_board(self):
        self.canvas.delete('all')
        for y in range(ROWS):
            for x in range(COLS):
                value = self.board[y][x]
                color = COLORS[value] if value else '#111'
                self.draw_cell(self.canvas, x, y, color, value != 0)

        matrix = self.current_piece['matrix']
        pos = self.current_piece['pos']
        for y, row in enumerate(matrix):
            for x, value in enumerate(row):
                if value == 0:
                    continue
                px = pos['x'] + x
                py = pos['y'] + y
                if 0 <= px < COLS and 0 <= py < ROWS:
                    self.draw_cell(self.canvas, px, py, COLORS[value], True)

    def draw_preview(self):
        self.preview_canvas.delete('all')
        matrix = self.next_piece['matrix']
        offset_x = (PREVIEW_SIZE - len(matrix[0])) // 2
        offset_y = (PREVIEW_SIZE - len(matrix)) // 2
        for y in range(PREVIEW_SIZE):
            for x in range(PREVIEW_SIZE):
                self.draw_cell(self.preview_canvas, x, y, '#111', False)
        for y, row in enumerate(matrix):
            for x, value in enumerate(row):
                if value == 0:
                    continue
                self.draw_cell(self.preview_canvas, x + offset_x, y + offset_y, COLORS[value], True)

    def draw_cell(self, canvas, x, y, color, filled):
        x1 = x * CELL_SIZE
        y1 = y * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        if filled:
            canvas.create_rectangle(x1 + 1, y1 + 1, x2 - 1, y2 - 1, fill=color, outline='#222')
        else:
            canvas.create_rectangle(x1 + 1, y1 + 1, x2 - 1, y2 - 1, fill='#111', outline='#222')


if __name__ == '__main__':
    root = tk.Tk()
    app = Tetris(root)
    root.mainloop()

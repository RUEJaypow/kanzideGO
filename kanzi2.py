import pygame
import sys

# --- ゲーム設定 ---
SCREEN_WIDTH = 512  # Pygameは高解像度も扱えるため少し大きめに設定
SCREEN_HEIGHT = 448
GAME_TITLE = "Pygame ハイブリッドクイズ"
FONT_FILE = "misaki_gothic.ttf"
FONT_SIZE_M = 32  # フォントサイズを定義
FONT_SIZE_L = 40
FONT_SIZE_S = 24

# --- 色の定義 (R, G, B) ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 100, 100)
YELLOW = (255, 255, 100)
DARK_BLUE = (20, 20, 80)
GREEN_BG = (50, 150, 100)
PURPLE_HIGHLIGHT = (120, 100, 180)


# --- シーン管理用の定数 ---
SCENE_TITLE = 0
SCENE_QUIZ = 1
SCENE_INPUT = 2
SCENE_RESULT = 3

# --- クイズデータ ---
QUIZ_DATA = [
    {
        "type": "choice",
        "question": "日本で一番高い山は？",
        "choices": ["1. 槍ヶ岳", "2. 富士山", "3. 北岳"],
        "correct_choice_index": 1,
    },
    {
        "type": "fill_in",
        "question": ["for i in □(5):", "  print(i)", "# 0から4まで表示させたい", "# □に入る単語は？"],
        "answer": "range",
    },
    {
        "type": "choice",
        "question": "ことわざ「猫に○○」",
        "choices": ["1. かつおぶし", "2. またたび", "3. こばん"],
        "correct_choice_index": 2,
    },
]

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self.clock = pygame.time.Clock()

        # フォントオブジェクトの作成
        self.font_m = pygame.font.Font(FONT_FILE, FONT_SIZE_M)
        self.font_l = pygame.font.Font(FONT_FILE, FONT_SIZE_L)
        self.font_s = pygame.font.Font(FONT_FILE, FONT_SIZE_S)

        # 変数の初期化
        self.scene = SCENE_TITLE
        self.current_quiz_index = 0
        self.player_choice = -1
        self.player_answer = ""
        self.is_correct = False

    def run(self):
        """Pygameのメインループ"""
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()  # 画面全体を更新
            self.clock.tick(60)    # FPSを60に固定

    def handle_events(self):
        """イベント処理 (キー入力、マウス操作など)"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # --- マウス入力 ---
            if self.scene == SCENE_TITLE and event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # 左クリック
                    self.scene = SCENE_QUIZ

            # --- キーボード入力 ---
            if event.type == pygame.KEYDOWN:
                quiz = QUIZ_DATA[self.current_quiz_index]
                if self.scene == SCENE_QUIZ:
                    if quiz["type"] == "choice":
                        if event.key == pygame.K_1: self.check_choice_answer(0)
                        if event.key == pygame.K_2: self.check_choice_answer(1)
                        if event.key == pygame.K_3: self.check_choice_answer(2)
                    elif quiz["type"] == "fill_in":
                        if event.key == pygame.K_RETURN:
                            self.player_answer = ""
                            self.scene = SCENE_INPUT
                elif self.scene == SCENE_INPUT:
                    if event.key == pygame.K_RETURN:
                        self.check_fill_in_answer()
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_answer = self.player_answer[:-1]
                    else:
                        self.player_answer += event.unicode # 押された文字をそのまま追加
                elif self.scene == SCENE_RESULT:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        self.current_quiz_index = (self.current_quiz_index + 1) % len(QUIZ_DATA)
                        self.scene = SCENE_QUIZ


    def update(self):
        """ゲームの状態更新（今回はイベント処理に統合）"""
        pass

    def draw(self):
        """描画処理"""
        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        else:
            quiz = QUIZ_DATA[self.current_quiz_index]
            self.draw_quiz_base(quiz) # 共通の背景と問題文を描画

            if self.scene == SCENE_QUIZ:
                if quiz["type"] == "choice":
                    self.draw_choices(quiz)
                else: # fill_in
                    self.draw_text_centered("エンターキーで入力", self.font_s, WHITE, SCREEN_HEIGHT - 60)
            elif self.scene == SCENE_INPUT:
                self.draw_input_field()
            elif self.scene == SCENE_RESULT:
                if quiz["type"] == "choice":
                    self.draw_choices(quiz, highlight=True)
                else: # fill_in
                    self.draw_input_field(show_cursor=False)
                self.draw_result_message(quiz)

    # --- ヘルパー関数 (描画) ---
    def draw_text(self, text, font, color, x, y):
        """指定座標にテキストを描画"""
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, (x, y))
    
    def draw_text_centered(self, text, font, color, y):
        """指定Y座標の中央にテキストを描画"""
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH / 2, y))
        self.screen.blit(text_surface, text_rect)

    def draw_title_scene(self):
        self.screen.fill(DARK_BLUE)
        # ロゴ(ダミー)
        pygame.draw.rect(self.screen, (100,100,200), (SCREEN_WIDTH/2 - 100, 80, 200, 80))
        self.draw_text_centered("ロゴ", self.font_l, WHITE, 120)
        self.draw_text_centered("Click to Start", self.font_m, WHITE, 250)

    def draw_quiz_base(self, quiz):
        self.screen.fill(GREEN_BG)
        # 問題表示エリア
        pygame.draw.rect(self.screen, BLACK, (20, 20, SCREEN_WIDTH - 40, SCREEN_HEIGHT - 40))
        # 問題文の描画
        self.draw_text("もんだい", self.font_l, WHITE, 40, 40)
        pygame.draw.line(self.screen, WHITE, (40, 90), (180, 90), 2)
        
        q_text = quiz["question"]
        if isinstance(q_text, list): # 複数行の質問の場合
            for i, line in enumerate(q_text):
                self.draw_text(line, self.font_m, WHITE, 40, 110 + i * FONT_SIZE_M * 1.2)
        else: # 1行の質問
            self.draw_text(q_text, self.font_m, WHITE, 40, 110)

    def draw_choices(self, quiz, highlight=False):
        y_start = 250
        for i, choice in enumerate(quiz["choices"]):
            if highlight and self.player_choice == i:
                 # 選んだ選択肢をハイライト
                pygame.draw.rect(self.screen, PURPLE_HIGHLIGHT, (35, y_start + i * 45 - 5, SCREEN_WIDTH - 70, FONT_SIZE_M + 10))
            self.draw_text(choice, self.font_m, WHITE, 40, y_start + i * 45)

    def draw_input_field(self, show_cursor=True):
        self.draw_text("こたえ:", self.font_m, WHITE, 40, 280)
        cursor = "_" if (pygame.time.get_ticks() % 1000 < 500 and show_cursor) else ""
        self.draw_text(self.player_answer + cursor, self.font_m, WHITE, 180, 280)

    def draw_result_message(self, quiz):
        if self.is_correct:
            self.draw_text_centered("★ せいかい！ ★", self.font_l, YELLOW, 350)
        else:
            self.draw_text_centered("＞ ざんねん…", self.font_l, RED, 350)
            if quiz["type"] == "fill_in":
                answer_text = f'せいかいは「{quiz["answer"]}」'
                self.draw_text_centered(answer_text, self.font_s, WHITE, 390)
        self.draw_text_centered("エンターキーでつぎへ", self.font_s, WHITE, SCREEN_HEIGHT - 30)

    # --- ヘルパー関数 (ロジック) ---
    def check_choice_answer(self, selected_index):
        self.player_choice = selected_index
        quiz = QUIZ_DATA[self.current_quiz_index]
        self.is_correct = (self.player_choice == quiz["correct_choice_index"])
        self.scene = SCENE_RESULT
        
    def check_fill_in_answer(self):
        quiz = QUIZ_DATA[self.current_quiz_index]
        self.is_correct = (self.player_answer.lower() == quiz["answer"].lower())
        self.scene = SCENE_RESULT

if __name__ == '__main__':
    game = Game()
    game.run()
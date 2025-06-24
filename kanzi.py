import pyxel
import os
import sys

# PyxelUniversalFontの安全なインポート
try:
    import PyxelUniversalFont as puf
    PUF_AVAILABLE = True
except ImportError:
    print("警告: PyxelUniversalFontがインストールされていません")
    print("pip install pyxel-universal-font でインストールしてください")
    PUF_AVAILABLE = False

# --- ゲーム設定 ---
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
GAME_TITLE = "Pyxel Quiz Game"

# フォントファイルの候補リスト（より現実的な順序）
FONT_FILES = [
    # 相対パス（実際にありそうな場所）
    "NotoSansJP-Regular.ttf",
    "./NotoSansJP-Regular.ttf",
    "fonts/NotoSansJP-Regular.ttf",
    "./fonts/NotoSansJP-Regular.ttf",
    "assets/fonts/NotoSansJP-Regular.ttf", 
    "./assets/fonts/NotoSansJP-Regular.ttf",
    # システムフォント（Windows）
    "C:/Windows/Fonts/arial.ttf",
    "C:/Windows/Fonts/calibri.ttf",
]

# --- シーン管理用の定数 ---
SCENE_TITLE = 0
SCENE_QUIZ = 1
SCENE_INPUT = 2
SCENE_RESULT = 3

# --- クイズデータ ---
QUIZ_DATA = [
    {"question": "JAPAN'S HIGHEST MOUNTAIN?", "answer": "FUJI"},
    {"question": "PYTHON IS A TYPE OF ...?", "answer": "SNAKE"},
    {"question": "WHAT IS 10 + 5?", "answer": "15"},
    {"question": "WHAT COLOR IS THE SUN?", "answer": "YELLOW"},
    {"question": "HOW MANY DAYS IN A WEEK?", "answer": "7"},
    {"question": "CAPITAL OF FRANCE?", "answer": "PARIS"},
    {"question": "LARGEST OCEAN?", "answer": "PACIFIC"},
    {"question": "WHAT IS 2 * 6?", "answer": "12"},
]

class Game:
    def __init__(self):
        """ゲームの初期化"""
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title=GAME_TITLE, fps=60)

        # フォントの初期化
        self.writer = None
        self.use_custom_font = False
        self.font_size = 16  # フォントサイズを明示的に設定
        
        if PUF_AVAILABLE:
            self.init_font()
        else:
            print("PyxelUniversalFontが利用できません。内蔵フォントを使用します。")

        # 変数の初期化
        self.scene = SCENE_TITLE
        self.current_quiz_index = 0
        self.player_answer = ""
        self.result_message = ""
        self.is_correct = False
        self.blink_timer = 0
        self.score = 0
        self.total_questions = 0

        pyxel.run(self.update, self.draw)

    def init_font(self):
        """フォントの初期化（修正版）"""
        print("フォント初期化を開始...")
        
        for i, font_path in enumerate(FONT_FILES, 1):
            print(f"[{i}/{len(FONT_FILES)}] '{font_path}' を確認中...")
            
            # ファイル存在確認
            if not os.path.exists(font_path):
                print(f"  → ファイルが見つかりません")
                continue
                
            # ファイルサイズ確認
            try:
                file_size = os.path.getsize(font_path)
                print(f"  → ファイル発見 (サイズ: {file_size:,} bytes)")
                
                if file_size < 1000:  # 1KB未満は異常
                    print(f"  → ファイルサイズが小さすぎます")
                    continue
                    
            except Exception as e:
                print(f"  → ファイル情報取得エラー: {e}")
                continue
            
            # 読み取り権限確認
            if not os.access(font_path, os.R_OK):
                print(f"  → 読み取り権限がありません")
                continue
                
            # フォント読み込み試行（修正版）
            try:
                print(f"  → フォント読み込み中... (サイズ: {self.font_size})")
                
                # PyxelUniversalFontの正しい初期化方法
                # サイズパラメータを明示的に指定
                self.writer = puf.Writer(font_path, size=self.font_size)
                
                # 簡単な互換性テスト
                if self._test_font_compatibility():
                    self.use_custom_font = True
                    print(f"  ✓ フォント '{font_path}' を正常に読み込みました")
                    return
                else:
                    print(f"  → 互換性テスト失敗")
                    self.writer = None
                    continue
                    
            except Exception as e:
                print(f"  → 読み込み失敗: {e}")
                error_msg = str(e).lower()
                if "size" in error_msg:
                    print(f"     (フォントサイズの問題の可能性)")
                elif "format" in error_msg:
                    print(f"     (フォント形式が対応していない可能性)")
                elif "corrupted" in error_msg or "invalid" in error_msg:
                    print(f"     (フォントファイルが破損している可能性)")
                self.writer = None
                continue
        
        # すべてのフォントファイルが見つからない場合
        print("カスタムフォントが読み込めないため、内蔵フォントを使用します")
        self.use_custom_font = False

    def _test_font_compatibility(self):
        """フォントの互換性をテスト（修正版）"""
        try:
            # writerオブジェクトの基本的な属性をチェック
            if self.writer is None:
                return False
                
            # 必要なメソッドが存在するかチェック
            if not hasattr(self.writer, 'draw'):
                print("     drawメソッドが見つかりません")
                return False
            
            # 試験的な描画テスト（実際にはpyxelの画面外で実行）
            # ここではメソッドの存在のみをチェック
            return True
            
        except Exception as e:
            print(f"     互換性テストエラー: {e}")
            return False

    def draw_text(self, x, y, text, color=7):
        """テキスト描画の統一メソッド（修正版）"""
        if self.use_custom_font and self.writer:
            try:
                # PyxelUniversalFontでの描画
                # colorパラメータはPyxelUniversalFontでは使用されない可能性があるため
                # 基本的な描画のみ実行
                self.writer.draw(x, y, text)
                return True
            except Exception as e:
                # 初回エラー時のみログ出力
                if not hasattr(self, '_font_error_logged'):
                    print(f"カスタムフォント描画エラー: {e}")
                    print("内蔵フォントにフォールバック")
                    self._font_error_logged = True
                    self.use_custom_font = False
                
        # Pyxel内蔵フォントでの描画
        pyxel.text(x, y, text, color)

    def get_text_width(self, text):
        """テキスト幅を取得（修正版）"""
        if self.use_custom_font and self.writer:
            try:
                # PyxelUniversalFontでの幅取得を試行
                if hasattr(self.writer, 'get_text_width'):
                    return self.writer.get_text_width(text)
                elif hasattr(self.writer, 'width'):
                    return self.writer.width(text)
                else:
                    # カスタムフォントの概算（サイズベース）
                    return len(text) * (self.font_size * 0.6)
            except Exception:
                # エラー時は概算値を返す
                return len(text) * (self.font_size * 0.6)
        else:
            # Pyxel内蔵フォントの幅（1文字4ピクセル）
            return len(text) * 4

    def update(self):
        """ゲームの状態を更新"""
        self.blink_timer += 1
        
        if self.scene == SCENE_TITLE: 
            self.update_title_scene()
        elif self.scene == SCENE_QUIZ: 
            self.update_quiz_scene()
        elif self.scene == SCENE_INPUT: 
            self.update_input_scene()
        elif self.scene == SCENE_RESULT: 
            self.update_result_scene()

    def draw(self):
        """画面を描画"""
        pyxel.cls(1)

        if self.scene == SCENE_TITLE:
            self.draw_title_scene()
        elif self.scene == SCENE_QUIZ: 
            self.draw_quiz_base()
            self.draw_quiz_scene()
        elif self.scene == SCENE_INPUT: 
            self.draw_input_scene()
        elif self.scene == SCENE_RESULT: 
            self.draw_result_scene()

    # --- 更新処理 ---
    def update_title_scene(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) or pyxel.btnp(pyxel.KEY_SPACE):
            self.scene = SCENE_QUIZ
            self.score = 0
            self.total_questions = 0

    def update_quiz_scene(self):
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_KP_ENTER):
            self.scene = SCENE_INPUT
            self.player_answer = ""

    def update_input_scene(self):
        # アルファベット入力
        for i in range(26):
            key = pyxel.KEY_A + i
            if pyxel.btnp(key):
                self.player_answer += chr(ord('A') + i)
        
        # 数字入力
        for i in range(10):
            key = pyxel.KEY_0 + i
            if pyxel.btnp(key):
                self.player_answer += str(i)
        
        # スペース入力
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.player_answer += " "
        
        # バックスペース
        if pyxel.btnp(pyxel.KEY_BACKSPACE, hold=10, repeat=2):
            if self.player_answer:
                self.player_answer = self.player_answer[:-1]
        
        # エンター
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_KP_ENTER):
            self.check_answer()

    def update_result_scene(self):
        if (pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_KP_ENTER) or 
            pyxel.btnp(pyxel.KEY_SPACE)):
            self.current_quiz_index = (self.current_quiz_index + 1) % len(QUIZ_DATA)
            self.scene = SCENE_QUIZ

    # --- 描画処理 ---
    def draw_title_scene(self):
        """タイトル画面の描画"""
        # タイトル背景
        pyxel.rect(SCREEN_WIDTH // 2 - 100, 50, 200, 80, 8)
        pyxel.rectb(SCREEN_WIDTH // 2 - 100, 50, 200, 80, 7)
        
        # タイトルテキスト
        title_text = "QUIZ GAME"
        title_width = self.get_text_width(title_text)
        self.draw_text(SCREEN_WIDTH // 2 - title_width // 2, 70, title_text, 7)
        
        # スコア表示
        if self.total_questions > 0:
            score_text = f"LAST SCORE: {self.score}/{self.total_questions}"
            score_width = self.get_text_width(score_text)
            self.draw_text(SCREEN_WIDTH // 2 - score_width // 2, 100, score_text, 10)
        
        # 点滅するスタートメッセージ
        if self.blink_timer % 60 < 30:
            start_text = "CLICK OR PRESS SPACE"
            start_width = self.get_text_width(start_text)
            self.draw_text(SCREEN_WIDTH // 2 - start_width // 2, 160, start_text, 10)
            
            start_text2 = "TO START"
            start_width2 = self.get_text_width(start_text2)
            self.draw_text(SCREEN_WIDTH // 2 - start_width2 // 2, 180, start_text2, 10)

    def draw_quiz_base(self):
        """クイズ関連シーンの共通背景描画"""
        pyxel.rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, 3)
        pyxel.rect(20, 40, SCREEN_WIDTH - 40, SCREEN_HEIGHT - 80, 0)
        pyxel.rectb(20, 40, SCREEN_WIDTH - 40, SCREEN_HEIGHT - 80, 7)
        
        # 問題番号とスコア表示
        question_num = f"Q{self.current_quiz_index + 1}/{len(QUIZ_DATA)}"
        self.draw_text(30, 50, question_num, 10)
        
        score_text = f"SCORE: {self.score}/{self.total_questions}"
        score_width = self.get_text_width(score_text)
        self.draw_text(SCREEN_WIDTH - 30 - score_width, 50, score_text, 11)
        
        # 問題文表示（長い場合は改行）
        question = QUIZ_DATA[self.current_quiz_index]["question"]
        if len(question) > 30:  # 長い問題文の場合は分割
            words = question.split()
            mid = len(words) // 2
            line1 = " ".join(words[:mid])
            line2 = " ".join(words[mid:])
            self.draw_text(30, 80, line1, 7)
            self.draw_text(30, 100, line2, 7)
            answer_y = 130
        else:
            self.draw_text(30, 80, question, 7)
            answer_y = 110
        
        # 回答ラベル
        self.draw_text(30, answer_y, "YOUR ANSWER:", 7)
        return answer_y + 20

    def draw_quiz_scene(self):
        """クイズ画面の描画"""
        prompt_text = "PRESS ENTER TO ANSWER"
        prompt_width = self.get_text_width(prompt_text)
        self.draw_text(SCREEN_WIDTH // 2 - prompt_width // 2, 200, prompt_text, 11)

    def draw_input_scene(self):
        """テキスト入力画面の描画"""
        answer_y = self.draw_quiz_base()
        
        # 入力フィールドの背景
        pyxel.rect(30, answer_y, SCREEN_WIDTH - 60, 30, 6)
        pyxel.rectb(30, answer_y, SCREEN_WIDTH - 60, 30, 5)
        
        # 入力テキストとカーソル
        cursor = "_" if self.blink_timer % 40 < 20 else " "
        display_text = self.player_answer + cursor
        self.draw_text(35, answer_y + 8, display_text, 0)
        
        # 指示テキスト
        instruction = "TYPE AND PRESS ENTER"
        inst_width = self.get_text_width(instruction)
        self.draw_text(SCREEN_WIDTH // 2 - inst_width // 2, 200, instruction, 11)

    def draw_result_scene(self):
        """結果表示画面の描画"""
        answer_y = self.draw_quiz_base()
        
        # 入力された回答
        pyxel.rect(30, answer_y, SCREEN_WIDTH - 60, 30, 6)
        pyxel.rectb(30, answer_y, SCREEN_WIDTH - 60, 30, 5)
        self.draw_text(35, answer_y + 8, self.player_answer, 0)
        
        # 結果メッセージ
        result_color = 11 if self.is_correct else 8
        result_y = answer_y + 40
        self.draw_text(30, result_y, self.result_message, result_color)
        
        # 継続指示
        continue_text = "PRESS ENTER FOR NEXT"
        cont_width = self.get_text_width(continue_text)
        self.draw_text(SCREEN_WIDTH // 2 - cont_width // 2, 200, continue_text, 10)

    def check_answer(self):
        """回答をチェック"""
        if not self.player_answer.strip():
            return
            
        self.scene = SCENE_RESULT
        self.total_questions += 1
        correct_answer = QUIZ_DATA[self.current_quiz_index]["answer"]
        
        if self.player_answer.upper().strip() == correct_answer.upper():
            self.result_message = "CORRECT! EXCELLENT!"
            self.is_correct = True
            self.score += 1
        else:
            self.result_message = f"WRONG... ANSWER: {correct_answer}"
            self.is_correct = False

# ゲーム実行前のチェック
def main():
    """メイン関数"""
    print("=== Pyxel Quiz Game ===")
    print("システム情報:")
    print(f"  OS: {os.name}")
    print(f"  Python: {sys.version.split()[0]}")
    print(f"  作業ディレクトリ: {os.getcwd()}")
    print("")
    
    # PyxelUniversalFontの確認
    if PUF_AVAILABLE:
        print("PyxelUniversalFont: 利用可能")
    else:
        print("PyxelUniversalFont: 利用不可 (内蔵フォントを使用)")
    
    print("")
    print("フォント確認中...")
    
    # フォントファイルの存在確認
    found_fonts = []
    for font_path in FONT_FILES:
        if os.path.exists(font_path):
            try:
                size = os.path.getsize(font_path)
                found_fonts.append((font_path, size))
                print(f"✓ 発見: {font_path} ({size:,} bytes)")
            except:
                print(f"? 発見: {font_path} (サイズ不明)")
    
    if not found_fonts:
        print("⚠ カスタムフォントファイルが見つかりません")
        print("  → Pyxel内蔵フォントを使用します")
        print("")
        print("カスタムフォントを使用したい場合:")
        print("1. フォントダウンロード先:")
        print("   - Google Fonts: https://fonts.google.com/")
        print("   - NotoSansJP推奨: https://fonts.google.com/noto/specimen/Noto+Sans+JP")
        print("")
        print("2. 配置場所:")
        print("   - ゲームファイルと同じフォルダ")
        print("   - fonts/ サブフォルダ")
        print("")
    else:
        print(f"✓ {len(found_fonts)}個のフォントファイルを発見")
    
    print("")
    print("ゲーム開始...")
    print("操作方法:")
    print("  - スペースキー/クリック: 開始")
    print("  - Enter: 決定")
    print("  - アルファベット/数字: 入力")
    print("  - Backspace: 削除")
    print("")
    
    try:
        Game()
    except Exception as e:
        print(f"ゲーム実行エラー: {e}")
        print("Pyxelが正しくインストールされているか確認してください")

if __name__ == "__main__":
    main()
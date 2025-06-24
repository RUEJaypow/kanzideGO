import tkinter as tk
from tkinter import font as tkfont

# --- ゲーム設定 ---
GAME_TITLE = "Tkinter ハイブリッドクイズ"
FONT_FAMILY = "Yu Gothic UI"
FONT_SIZE_S = 12
FONT_SIZE_M = 16
FONT_SIZE_L = 24

# --- クイズデータ (変更なし) ---
QUIZ_DATA = [
    {
        "type": "choice",
        "question": "日本で一番高い山は？",
        "choices": ["1. 槍ヶ岳", "2. 富士山", "3. 北岳"],
        "correct_choice_index": 1,
    },
    {
        "type": "fill_in",
        "question": "Pythonでリストの要素数を取得する関数は len() ですが、文字列の長さを取得する場合も同じ関数を使います。この関数 len は何の略でしょう？",
        "answer": "length",
    },
    {
        "type": "choice",
        "question": "ことわざ「猫に○○」\n○○に入るのは？",
        "choices": ["1. かつおぶし", "2. またたび", "3. こばん"],
        "correct_choice_index": 2,
    },
]

class QuizApp(tk.Tk):
    """アプリケーション全体を管理するメインクラス"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title(GAME_TITLE)
        self.geometry("600x400") # ウィンドウサイズを少し拡大
        self.minsize(500, 350) # 最小サイズを指定

        # フォントオブジェクトを定義
        self.title_font = tkfont.Font(family=FONT_FAMILY, size=FONT_SIZE_L, weight="bold")
        self.question_font = tkfont.Font(family=FONT_FAMILY, size=FONT_SIZE_M)
        self.result_font = tkfont.Font(family=FONT_FAMILY, size=FONT_SIZE_L, weight="bold")
        self.default_font = tkfont.Font(family=FONT_FAMILY, size=FONT_SIZE_M)

        # クイズの状態を管理
        self.current_quiz_index = 0
        self.wrong_answer_count = 0 # 間違えた問題数を記録

        self._frame = None
        self.switch_frame("TitleFrame")

    def switch_frame(self, frame_class_name, **kwargs):
        """指定された名前のフレームに切り替える"""
        if self._frame:
            self._frame.destroy()
        
        FrameClass = globals()[frame_class_name]
        self._frame = FrameClass(master=self, controller=self, **kwargs)
        # gridを使用してウィンドウサイズ変更に追従させる
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self._frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

    def next_question(self):
        """次の問題に進むか、最終結果を表示する"""
        self.current_quiz_index += 1
        if self.current_quiz_index < len(QUIZ_DATA):
            self.switch_frame("QuizFrame")
        else:
            self.switch_frame("FinalResultFrame")
            
    def record_wrong_answer(self):
        """不正解の数をカウント"""
        self.wrong_answer_count += 1


class TitleFrame(tk.Frame):
    """タイトル画面"""
    def __init__(self, master, controller, **kwargs):
        super().__init__(master)
        self.controller = controller
        
        # --- UI改善: gridで中央配置 ---
        self.grid_rowconfigure((0, 3), weight=1) # 上下の余白行
        self.grid_columnconfigure(0, weight=1)   # 中央の列

        logo_label = tk.Label(self, text="ロゴ", font=controller.title_font, bg="lightblue", width=10, height=3)
        logo_label.grid(row=0, column=0, pady=(20,0))

        title_label = tk.Label(self, text="Tkinter クイズゲーム", font=controller.title_font)
        title_label.grid(row=1, column=0, pady=10)

        start_button = tk.Button(self, text="スタート", font=controller.default_font, width=15,
                                 command=lambda: controller.switch_frame("QuizFrame"))
        start_button.grid(row=2, column=0, pady=20)


class QuizFrame(tk.Frame):
    """クイズ画面"""
    def __init__(self, master, controller, **kwargs):
        super().__init__(master)
        self.controller = controller
        self.grid_columnconfigure(0, weight=1)

        quiz = QUIZ_DATA[controller.current_quiz_index]
        
        # --- UI改善: wraplengthでテキストを自動折り返し ---
        question_label = tk.Label(self, text=quiz["question"], font=controller.question_font, 
                                  wraplength=450, justify="left")
        question_label.grid(row=0, column=0, pady=20, sticky="w")

        if quiz["type"] == "choice":
            for i, choice in enumerate(quiz["choices"]):
                btn = tk.Button(self, text=choice, font=controller.default_font, 
                                command=lambda choice_idx=i: self.check_choice_answer(choice_idx))
                btn.grid(row=i+1, column=0, pady=5, sticky="ew") # sticky="ew"で横幅を合わせる
        else: # "fill_in"
            input_frame = tk.Frame(self)
            input_frame.grid(row=1, column=0, pady=20, sticky="ew")
            input_frame.grid_columnconfigure(1, weight=1)
            
            answer_label = tk.Label(input_frame, text="こたえ:", font=controller.default_font)
            answer_label.grid(row=0, column=0)
            
            self.entry = tk.Entry(input_frame, font=controller.default_font)
            self.entry.grid(row=0, column=1, padx=10, sticky="ew")
            self.entry.bind("<Return>", self.check_fill_in_answer)
            self.entry.focus_set() # 入力欄にフォーカスを合わせる

            submit_button = tk.Button(self, text="決定", font=controller.default_font,
                                      command=self.check_fill_in_answer)
            submit_button.grid(row=2, column=0, pady=10)

    def check_choice_answer(self, choice_index):
        quiz = QUIZ_DATA[self.controller.current_quiz_index]
        is_correct = (choice_index == quiz["correct_choice_index"])
        if not is_correct:
            self.controller.record_wrong_answer() # 不正解を記録
        
        result_info = {
            "is_correct": is_correct,
            "player_answer": quiz["choices"][choice_index],
            "correct_answer_text": f'せいかいは: {quiz["choices"][quiz["correct_choice_index"]]}'
        }
        self.controller.switch_frame("ResultFrame", result_info=result_info)
        
    def check_fill_in_answer(self, event=None):
        player_answer = self.entry.get()
        quiz = QUIZ_DATA[self.controller.current_quiz_index]
        is_correct = (player_answer.lower() == quiz["answer"].lower())
        if not is_correct:
            self.controller.record_wrong_answer() # 不正解を記録

        result_info = {
            "is_correct": is_correct,
            "player_answer": player_answer,
            "correct_answer_text": f'せいかいは: {quiz["answer"]}'
        }
        self.controller.switch_frame("ResultFrame", result_info=result_info)

class ResultFrame(tk.Frame):
    """各問題の結果表示画面"""
    def __init__(self, master, controller, result_info, **kwargs):
        super().__init__(master)
        self.controller = controller
        self.grid_rowconfigure((0, 4), weight=1)
        self.grid_columnconfigure(0, weight=1)

        result_msg, result_color = ("★ せいかい！ ★", "green") if result_info["is_correct"] else ("＞ ざんねん…", "red")
            
        result_label = tk.Label(self, text=result_msg, font=controller.result_font, fg=result_color)
        result_label.grid(row=0, column=0, pady=20)
        
        answer_label = tk.Label(self, text=f"あなたの回答: {result_info['player_answer']}", font=controller.default_font)
        answer_label.grid(row=1, column=0, pady=10)
        
        if not result_info["is_correct"]:
            correct_label = tk.Label(self, text=result_info["correct_answer_text"], font=controller.default_font)
            correct_label.grid(row=2, column=0, pady=10)

        next_button = tk.Button(self, text="次の問題へ", font=controller.default_font, width=15, command=controller.next_question)
        next_button.grid(row=3, column=0, pady=20)


class FinalResultFrame(tk.Frame):
    """全問終了後の最終結果画面"""
    def __init__(self, master, controller, **kwargs):
        super().__init__(master)
        self.controller = controller
        self.grid_rowconfigure((0, 3), weight=1)
        self.grid_columnconfigure(0, weight=1)

        total_questions = len(QUIZ_DATA)
        wrong_answers = controller.wrong_answer_count

        final_msg_label = tk.Label(self, text="クイズ終了！", font=controller.title_font)
        final_msg_label.grid(row=0, column=0, pady=20)

        score_text = f"全{total_questions}問中、不正解は {wrong_answers} 問でした。"
        score_label = tk.Label(self, text=score_text, font=controller.question_font)
        score_label.grid(row=1, column=0, pady=10)

        exit_button = tk.Button(self, text="終了する", font=controller.default_font, width=15, command=self.controller.destroy)
        exit_button.grid(row=2, column=0, pady=20)


if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()
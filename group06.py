import sys
import os
import pygame

# 実行ファイルのディレクトリにカレントディレクトリを変更（素材やスコアファイルの読み込みエラー防止）
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# --- 各自のモジュールをインポートする準備（後ほど合流） ---
# import player    # B君: プレイヤー（カゴ）担当
# import item      # C君: 落ちてくる物体（アイテム）担当
# import judge     # D君: 当たり判定＆スコア担当
# import ui        # E君: UI（文字表示）＆BGM担当
# import assets    # F君: グラフィック（素材・演出）担当
# import ranking   # G君: リザルト画面（スコア記録・ランキング）担当

# 定数定義（最初の1時間で全員で決める内容の例）
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 色の定義（RGB値）
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
RED = (255, 50, 50)
YELLOW = (255, 215, 0)

# ==========================================
# D君 (C0A25136) 担当箇所: 当たり判定＆スコア処理
# ==========================================
class ScoreManager:
    """
    プレイヤーと落ちてくるアイテムの当たり判定、およびスコアの加減算を管理するクラス
    """
    def __init__(self) -> None:
        pass  # 初期化処理（必要に応じて拡張可能）

    def check_collisions(self, player_rect: pygame.Rect, item_list: list) -> list:
        """
        プレイヤーの矩形とアイテムリストの当たり判定を行うメソッド
        
        Args:
            player_rect (pygame.Rect): プレイヤー（カゴ）の判定領域
            item_list (list): 画面内にあるアクティブなアイテムのリスト
            
        Returns:
            list: 衝突しなかった（画面に残る）アイテムの新しいリスト
        """
        remaining_items: list = []
        global current_score  # メインループのスコア変数を更新するためにグローバル宣言

        for item in item_list:
            # アイテムの判定（相手のコードが辞書型かオブジェクト型かによって調整可能）
            # ここでは一般的な辞書型（"rect"キーにpygame.Rectが入っている）と仮定
            item_rect = item["rect"] if isinstance(item, dict) else item.rect
            item_type = item["type"] if isinstance(item, dict) else item.type

            # colliderect で重なり（衝突）を判定
            if player_rect.colliderect(item_rect):
                # 衝突した場合：スコアの更新
                if item_type == "good":      # 良いアイテム（果物など）
                    current_score += 10
                elif item_type == "bad":     # 悪いアイテム（爆弾など）
                    current_score -= 20
                    if current_score < 0:    # スコアがマイナスにならないように安全処理
                        current_score = 0
                # 衝突したアイテムは remaining_items に追加しない（＝消滅させる）
            else:
                # 衝突しなかったアイテムは次のフレームも残す
                remaining_items.append(item)

        return remaining_items



def main():
    # Pygameの初期化
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("落ち物キャッチゲーム")
    clock = pygame.time.Clock()

    # ゲームの状態管理用変数
    # "TITLE": タイトル画面, "PLAY": ゲーム中, "GAMEOVER": ゲームオーバー（リザルト）画面
    game_state = "TITLE"

    # --- [D君・G君合流用変数] スコア管理の土台 ---
    current_score = 0  # 今回のスコア（D君がゲーム中に加算する）
    high_score = 0     # 最高スコア（G君がファイルから読み込む）
    score_manager = ScoreManager() #class のインスタンス化

    # ［G君の合流ポイント①: ゲーム起動時に最高スコアを読み込む］
    # 例: high_score = ranking.load_highscore()
    # 暫定処理（ファイルがなければ0、あれば数値を読み込む）
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as f:
            try:
                high_score = int(f.read())
            except ValueError:
                high_score = 0

    # フォントの用意（E君・G君のUI表示用フォントが決まるまでの暫定）
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 36)

    running = True
    while running:
        # FPS（フレームレート）の設定
        clock.tick(FPS)

        # ==========================================
        # 1. イベント処理（キー入力や閉じるボタンの監視）
        # ==========================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # キーボードが押されたときの処理
            if event.type == pygame.KEYDOWN:
                if game_state == "TITLE":
                    if event.key == pygame.K_SPACE:
                        # タイトル画面でスペースキーを押したらゲーム開始
                        current_score = 0  # スコアをリセット
                        game_state = "PLAY"

                elif game_state == "PLAY":
                    # ［B君の合流ポイント①］
                    # ゲーム中のキー入力（左右の移動など）は主にB君のモジュールに引き渡す
                    pass

                elif game_state == "GAMEOVER":
                    if event.key == pygame.K_SPACE:
                        # ゲームオーバー画面でスペースキーを押したらタイトルに戻る
                        game_state = "TITLE"

        # ==========================================
        # 2. データ更新処理（ゲームロジック）
        # ==========================================
        if game_state == "TITLE":
            pass

        elif game_state == "PLAY":
            # ［B君の合流ポイント②: プレイヤーの移動更新］
            # ［C君의 合流ポイント①: アイテムの落下更新］
            
            # ［D君の合流ポイント①: 当たり判定の計算とスコアの加減算］
            # ※ 'player_rect' と 'active_items' は他のメンバーの変数名に合わせて調整してください
            # active_items = score_manager.check_collisions(player_rect, active_items)
            
            # MVP確認用の暫定ルール（エンターキーを押したらゲーム終了・リザルトへ移動）
            # ※本番はD君の判定で「タイムアップ」や「ライフ0」になったら切り替える
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RETURN]:
                current_score = 150  # テスト用にスコアが入ったと仮定
                game_state = "GAMEOVER"
                
                # ［G君の合流ポイント②: ゲーム終了時にハイスコアを判定して保存］
                # 例: ranking.check_and_save_highscore(current_score)
                if current_score > high_score:
                    high_score = current_score
                    with open("highscore.txt", "w") as f:
                        f.write(str(high_score))

        elif game_state == "GAMEOVER":
            pass

        # ==========================================
        # 3. 描画処理（画面への表示）
        # ==========================================
        screen.fill(BLACK)  # 画面を黒でクリア

        if game_state == "TITLE":
            # タイトル画面の描画（E君・F君の素材が来るまでの暫定表示）
            title_text = font.render("FALLING CATCH GAME", True, BLUE)
            start_text = font.render("Press SPACE to Start", True, WHITE)
            screen.blit(title_text, (200, 200))
            screen.blit(start_text, (230, 350))

        elif game_state == "PLAY":
            # ［F君・B君の合流ポイント: プレイヤー（カゴ）の描画］
            # ［F君・C君の合流ポイント: アイテム（果物・爆弾）の描画］
            # ［E君の合流ポイント①: 画面上部への「現在のスコア」や「残り時間」の文字描画］

            # MVP確認用の暫定表示
            play_text = font.render("Playing... (Press Enter to Lose)", True, WHITE)
            screen.blit(play_text, (150, 250))

        elif game_state == "GAMEOVER":
            # ［G君の合流ポイント③: リザルト画面の描画（A君の画面を乗っ取る）］
            # G君が作成した文字配置や、F君が作ったリザルト背景などをここで描画する
            
            over_text = font.render("GAME OVER", True, RED)
            screen.blit(over_text, (300, 150))
            
            # スコアとハイスコアの表示（G君の担当箇所）
            score_text = small_font.render(f"YOUR SCORE: {current_score}", True, WHITE)
            highscore_text = small_font.render(f"HI-SCORE: {high_score}", True, YELLOW)
            screen.blit(score_text, (300, 250))
            screen.blit(highscore_text, (300, 300))
            
            retry_text = small_font.render("Press SPACE to Title", True, WHITE)
            screen.blit(retry_text, (270, 400))

        # 画面の更新
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":

    main()

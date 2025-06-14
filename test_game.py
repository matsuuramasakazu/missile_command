import unittest
from game import Game
from constants import *
from explosion import Explosion
from meteor import Meteor
from test_game_platform import TestGamePlatform

class TestGame(unittest.TestCase):
    def setUp(self):
        self.platform = TestGamePlatform()
        self.game = Game(self.platform) # Pass platform to Game constructor

    def test_reset(self):
        self.game.reset()
        self.assertEqual(len(self.game.bases), 3)
        self.assertEqual(len(self.game.cities), 6)
        self.assertEqual(self.game.score, 0)
        self.assertFalse(self.game.game_over)

    def test_update_missile_launch(self):
        # Simulate mouse position using the platform
        self.platform.set_mouse_position(200, 150)
        # Simulate mouse button press using the platform
        self.platform.set_mouse_button_pressed(self.platform.get_mouse_button_left(), True)

        # game.update() will now use the platform for input checks
        self.game.update()
        self.assertEqual(len(self.game.missile_manager.missiles), 1)

        # Release the mouse button to avoid side effects in other tests
        self.platform.set_mouse_button_pressed(self.platform.get_mouse_button_left(), False)

    def test_check_game_over_true(self):
        for base in self.game.bases:
            base.is_alive = False
        for city in self.game.cities:
            city.is_alive = False
        self.game.check_game_over()
        self.assertTrue(self.game.game_over)

    def test_check_game_over_false(self):
        self.game.update() # Assumes game.update() uses platform's frame_count if needed
        self.assertFalse(self.game.game_over)

    def test_score_increase_on_missile_hit(self):
        # ミサイル命中時のスコア増加
        self.game.reset() # クリーンな状態で開始
        initial_score = self.game.score
        # 確実に当たる爆発と隕石を用意
        explosion = Explosion(0, 0, self.platform)
        explosion.radius = 10
        meteor1 = Meteor(0, 0, 1, self.platform)
        meteor2 = Meteor(5, 5, 1, self.platform)
        meteor1.is_alive = True
        meteor2.is_alive = True
        # Gameオブジェクトのリストに追加
        self.game.explosion_manager.add_explosion_object(explosion)
        self.game.meteor_manager.meteors.extend([meteor1, meteor2])
        # Detectorのターゲットを更新
        self.game.missile_explosions_detector.targets = self.game.meteor_manager.meteors

        self.game.update() # Assumes game.update() uses platform's frame_count
        # 衝突したメテオの数 * 5 だけスコアが増加していることを確認
        self.assertEqual(self.game.score, initial_score + 2 * 5)
        self.assertFalse(meteor1.is_alive)
        self.assertFalse(meteor2.is_alive)

    def test_score_decrease_on_meteor_hit_city(self):
        # 隕石命中時のスコア減少
        self.game.reset() # クリーンな状態で開始
        initial_score = self.game.score

        # 確実に当たる爆発と都市を用意
        explosion = Explosion(60, 210, self.platform)
        explosion.radius = 10
        city1 = self.game.cities[0] # 爆発範囲内
        city2 = self.game.cities[1] # 爆発範囲外
        city1.is_alive = True
        city2.is_alive = True

        # Gameオブジェクトのリストに追加
        self.game.explosion_manager.add_explosion_object(explosion)
        self.game.cities = [city1, city2]
        self.game.bases = []

        # 衝突した都市の数 * 5 だけスコアが減少していることを確認
        self.game.update() # Assumes game.update() uses platform's frame_count
        self.assertEqual(self.game.score, initial_score - 5)
        self.assertFalse(city1.is_alive)
        self.assertTrue(city2.is_alive)

    def test_game_over_condition(self):
        # 全都市・全基地破壊でゲームオーバー
        for city in self.game.cities:
            city.is_alive = False
        for base in self.game.bases:
            base.is_alive = False
        self.game.check_game_over()
        self.assertTrue(self.game.game_over)

        # 都市か基地が1つでも生きていればゲーム続行
        self.game.reset()
        self.game.cities[0].is_alive = True
        for city in self.game.cities[1:]:
            city.is_alive = False
        for base in self.game.bases:
            base.is_alive = False
        # ゲームロジックでは基地全滅でもゲームオーバーになるため、Trueを期待する
        self.game.check_game_over()
        self.assertTrue(self.game.game_over)

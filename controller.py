from typing import Optional

from hero import Hero


class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Game(metaclass=SingletonMeta):
    def __init__(self):
        self.player = None
        self.enemy = None
        self.game_processing = False
        self.game_results = ""

    def run(self, player: Hero, enemy: Hero):
        self.player = player
        self.enemy = enemy
        self.game_processing = True

    def _check_health(self) -> Optional[str]:
        if self.player.health <= 0 and self.enemy.health <= 0:
            return self._end_game(result="В этой игре никто не победил.")
        if self.player.health <= 0:
            return self._end_game(result="Вы проиграли.")
        if self.enemy.health <= 0:
            return self._end_game(result="Вы выиграли!.")
        return None

    def _end_game(self, result: str):
        self.game_processing = False
        self.game_results = result
        return result

    def next_turn(self) -> str:
        if results := self._check_health():
            return results
        if not self.game_processing:
            return self.game_results

        results = self.enemy_hit()
        self.player.regenerate_stamina()
        self.enemy.regenerate_stamina()
        return results

    def enemy_hit(self) -> str:
        delta_damage: Optional[float] = self.enemy.hit(self.player)
        if delta_damage is not None:
            self.player.take_damage(delta_damage)
            results = f"Враг нанес вам урон {delta_damage}!"
        else:
            results = "Врагу не хватило выносливости на удар."

    def player_hit(self) -> str:
        delta_damage: Optional[float] = self.player.hit(self.enemy)
        if delta_damage is not None:
            self.enemy.take_damage(delta_damage)
            return f"Вы нанесли урон {delta_damage} врагу!{self.next_turn()}"
        return f"Вам не хватило выносливости на удар.{self.next_turn()}"

    def player_use_skill(self) -> str:
        delta_damage: Optional[float] = self.player.use_skill()
        if delta_damage is not None:
            self.enemy.take_damage(delta_damage)
            return f"Вы нанесли урон {delta_damage} врагу!{self.next_turn()}"
        return f"Вам не хватило выносливости на удар.{self.next_turn()}"



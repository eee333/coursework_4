from __future__ import annotations
from abc import ABC, abstractmethod
from random import randint
from typing import Type, Optional

from equipment import Weapon, Armor
from personages import Personage

BASE_STAMINA_PER_ROUND = 0.4


class Hero(ABC):
    def __init__(self, class_: Type[Personage], weapon: Weapon, armor: Armor, name: str):
        self.class_ = class_
        self.weapon = weapon
        self.armor = armor
        self._stamina = self.class_.max_stamina
        self._health = self.class_.max_health
        self.skill_used: bool = False
        self.name = name

    @property
    def health(self):
        return round(self._health, 1)

    @health.setter
    def health(self, value):
        self._health = value

    @property
    def stamina(self):
        return round(self._stamina, 1)

    @stamina.setter
    def stamina(self, value) :
        self._stamina = value

    @property
    def _total_armor(self) -> float:
        if self.stamina >= self.armor.stamina_per_turn:
            self.stamina -= self.armor.stamina_per_turn
            return self.armor.defence * self.class_.armor
        return 0

    def _hit(self, target: Hero) -> Optional[float]:
        if self.stamina < self.weapon.stamina_per_hit:
            return None
        hero_damage = self.weapon.damage * self.class_.attack
        delta_damage = hero_damage - target._total_armor
        if delta_damage < 0:
            return 0
        self.stamina -= self.weapon.stamina_per_hit
        return round(delta_damage, 1)

    def take_damage(self, damage: float):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def use_skill(self) -> Optional[float]:
        if self.stamina >= self.class_.skill.stamina and not self.skill_used:
            self.stamina -= self.class_.skill.stamina
            self.skill_used = True
            return round(self.class_.skill.damage, 1)
        return None

    def regenerate_stamina(self):
        delta_stamina = BASE_STAMINA_PER_ROUND * self.class_.stamina
        self.stamina += delta_stamina
        if self.stamina > self.class_.max_stamina:
            self.stamina = self.class_.max_stamina

    @abstractmethod
    def hit(self, target: Hero) -> Optional[float]:
        pass


class Player(Hero):
    def hit(self, target: Hero) -> Optional[float]:
        return self._hit(target)


class Enemy(Hero):
    def hit(self, target: Hero) -> Optional[float]:
        if randint(1, 100) < 11 and self.stamina >= self.class_.skill.stamina and not self.skill_used:
            self.use_skill()
        return self._hit(target)

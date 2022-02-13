from typing import Dict, Type
from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect
from equipment import EquipmentData
from hero import Player, Hero, Enemy
from personages import personage_classes, Personage
from utils import load_equipment

EQUIPMENT: EquipmentData = load_equipment()

app = Flask(__name__)
app.url_map.strict_slashes = False

heroes: Dict[str, Hero] = dict()



def render_choose_template(*args, **kwargs) -> str:
    return render_template(
        "hero_choosing.html",
        classes=personage_classes.values(),
        equipment=EQUIPMENT,
        **kwargs,
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/choose-hero", methods=["GET", "POST"])
def choose_hero():
    if request.method == "GET":
        return render_choose_template(header="Выберите героя")
    heroes["player"] = Player(
        class_=personage_classes[request.form["unit_class"]],
        weapon=EQUIPMENT.get_weapon(request.form["weapon"]),
        armor=EQUIPMENT.get_armor(request.form["armor"]),
        name=request.form["name"]
    )
    return redirect(url_for("choose_enemy"))


@app.route("/choose-enemy", methods=["GET", "POST"])
def choose_enemy():
    if request.method == "GET":
        return render_choose_template(header="Выберите врага")
    heroes["enemy"] = Enemy(
        class_=personage_classes[request.form["unit_class"]],
        weapon=EQUIPMENT.get_weapon(request.form["weapon"]),
        armor=EQUIPMENT.get_armor(request.form["armor"]),
        name=request.form["name"]
    )
    return redirect(url_for("fight"))


@app.route("/fight")
def fight():
    if "player" in heroes and "enemy" in heroes:
        return render_template("fight.html", heroes=heroes, result="Fight!")
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run()
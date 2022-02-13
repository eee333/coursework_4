from flask import Flask, render_template, request, url_for
from werkzeug.utils import redirect

from equipment import EquipmentData
from personages import personage_classes
from utils import load_equipment

EQUIPMENT: EquipmentData = load_equipment()

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/choose-hero", methods=["GET", "POST"])
def choose_hero():
    if request.method == "GET":
        return render_template(
            "hero_choosing.html",
            header="Выберите героя",
            classes=personage_classes.values(),
            equipment=EQUIPMENT
        )
    return redirect(url_for("choose_enemy"))


@app.route("/choose-enemy", methods=["GET", "POST"])
def choose_enemy():
    if request.method == "GET":
        return render_template(
            "hero_choosing.html",
            header="Выберите героя",
            classes=personage_classes.values(),
            equipment=EQUIPMENT
        )
    return ""


if __name__ == '__main__':
    app.run()
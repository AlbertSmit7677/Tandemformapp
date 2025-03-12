# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 13:24:54 2025

@author: alber
"""

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trainingsformulier.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class Registratie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.String(100), nullable=False)
    mobiel = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    geboortedatum = db.Column(db.String(10), nullable=False)
    trainingsjaren = db.Column(db.Integer, nullable=False)
    trainingen_per_week = db.Column(db.Integer, nullable=False)
    uren_per_week = db.Column(db.Integer, nullable=False)
    beschikbaarheid = db.Column(db.String(50), unique=True, nullable=False)

@app.route("/", methods=["GET", "POST"])
def formulier():
    if request.method == "POST":
        naam = request.form["naam"]
        mobiel = request.form["mobiel"]
        email = request.form["email"]
        geboortedatum = request.form["geboortedatum"]
        trainingsjaren = request.form["trainingsjaren"]
        trainingen_per_week = request.form["trainingen_per_week"]
        uren_per_week = request.form["uren_per_week"]
        beschikbaarheid = request.form["beschikbaarheid"]

        # Check of het tijdslot al bezet is
        if Registratie.query.filter_by(beschikbaarheid=beschikbaarheid).first():
            return "Dit tijdslot is al geboekt, kies een ander."

        nieuwe_registratie = Registratie(
            naam=naam, mobiel=mobiel, email=email,
            geboortedatum=geboortedatum, trainingsjaren=trainingsjaren,
            trainingen_per_week=trainingen_per_week, uren_per_week=uren_per_week,
            beschikbaarheid=beschikbaarheid
        )

        db.session.add(nieuwe_registratie)
        db.session.commit()

        return redirect(url_for("bevestiging"))

    # Haal alle beschikbare tijdsloten op
    beschikbare_tijden = get_beschikbare_tijdsloten()
    return render_template("formulier.html", beschikbare_tijden=beschikbare_tijden)

@app.route("/bevestiging")
def bevestiging():
    return "Je registratie is voltooid! Je ontvangt een bevestiging per e-mail."

def get_beschikbare_tijdsloten():
    # Lijst met alle beschikbare tijdsloten
    alle_tijdsloten = [
        f"Woensdag 26 maart 2025 - {hour}:00 VU" for hour in range(10, 18)
    ] + [
        f"Vrijdag 28 maart 2025 - {hour}:00 VU" for hour in range(10, 18)
    ] + [
        f"Maandag 31 maart 2025 - {hour}:00 VU" for hour in range(10, 22)
    ] + [
        f"Dinsdag 1 april 2025 - {hour}:00 VU" for hour in range(10, 22)
    ] + [
        f"Woensdag 2 april 2025 - {hour}:00 VU" for hour in range(10, 22)
    ] + [
        f"Donderdag 3 april 2025 - {hour}:00 VU" for hour in range(10, 22)
    ] + [
        f"Vrijdag 4 april 2025 - {hour}:00 VU" for hour in range(10, 19)
    ]

    # Haal alle reeds geboekte tijdsloten op
    geboekte_tijden = [r.beschikbaarheid for r in Registratie.query.all()]

    # Geef alleen de beschikbare tijden terug
    return [tijd for tijd in alle_tijdsloten if tijd not in geboekte_tijden]

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
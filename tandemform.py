# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 11:58:11 2025

@author: alber
"""



from flask import Flask, render_template, request

app = Flask(__name__)

# Lijst met beschikbare tijdslots
available_slots = [
    "Woensdag 26 maart 2025 10:00", "Woensdag 26 maart 2025 11:00", "Woensdag 26 maart 2025 12:00",
    "Woensdag 26 maart 2025 13:00", "Woensdag 26 maart 2025 14:00", "Woensdag 26 maart 2025 15:00",
    "Woensdag 26 maart 2025 16:00", "Woensdag 26 maart 2025 17:00",
    "Vrijdag 28 maart 2025 10:00", "Vrijdag 28 maart 2025 11:00", "Vrijdag 28 maart 2025 12:00",
    "Vrijdag 28 maart 2025 13:00", "Vrijdag 28 maart 2025 14:00", "Vrijdag 28 maart 2025 15:00",
    "Vrijdag 28 maart 2025 16:00", "Vrijdag 28 maart 2025 17:00"
]

# Tijdslots voor Maandag tot Donderdag
for day in range(31, 35):
    for hour in range(10, 22):
        available_slots.append(f"Maandag {day} maart t/m donderdag {day+3} april {hour}:00")

# Tijdslots voor Vrijdag
for hour in range(10, 19):
    available_slots.append(f"Vrijdag 4 april {hour}:00")

# Route voor het formulier
@app.route('/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        naam = request.form['naam']
        mobiel_nr = request.form['mobiel_nr']
        email = request.form['email']
        geboortedatum = request.form['geboortedatum']
        trainingsjaren = request.form['trainingsjaren']
        aantal_trainingen_per_week = request.form['aantal_trainingen_per_week']
        aantal_uren_training_per_week = request.form['aantal_uren_training_per_week']
        beschikbaarheid = request.form['beschikbaarheid']

        # Verwijder het geselecteerde tijdslot uit de beschikbare slots
        if beschikbaarheid in available_slots:
            available_slots.remove(beschikbaarheid)

        return f"Formulier ingediend! Naam: {naam}, Mobiel nr: {mobiel_nr}, Email: {email}, Geboortedatum: {geboortedatum}, Trainingsjaren: {trainingsjaren}, Aantal trainingen per week: {aantal_trainingen_per_week}, Aantal uren training per week: {aantal_uren_training_per_week}, Beschikbaarheid: {beschikbaarheid}"

    return render_template('form.html', available_slots=available_slots)

if __name__ == '__main__':
    app.run(debug=True)

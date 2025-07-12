from flask import Flask, render_template, request, redirect, url_for
import csv, os, math

app = Flask(__name__)
FICHIER = 'contacts.csv'
CONTACTS_PAR_PAGE = 5

def charger_contacts():
    contacts = []
    if os.path.exists(FICHIER):
        with open(FICHIER, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    contacts.append({'nom': row[0], 'telephone': row[1], 'email': row[2]})
    return contacts

def sauvegarder_contacts(contacts):
    with open(FICHIER, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for c in contacts:
            writer.writerow([c['nom'], c['telephone'], c['email']])

@app.route('/')
def index():
    recherche = request.args.get('recherche', '').strip()
    page = int(request.args.get('page', 1))
    tous_contacts = charger_contacts()

    if recherche:
        contacts = [c for c in tous_contacts if recherche.lower() in c['nom'].lower()]
    else:
        contacts = tous_contacts

    total_pages = math.ceil(len(contacts) / CONTACTS_PAR_PAGE)
    contacts_pagines = contacts[(page-1)*CONTACTS_PAR_PAGE : page*CONTACTS_PAR_PAGE]

    return render_template('index.html', contacts=contacts_pagines, page=page, total_pages=total_pages, recherche=recherche)

@app.route('/ajouter', methods=['POST'])
def ajouter():
    nom = request.form['nom']
    telephone = request.form['telephone']
    email = request.form['email']

    contacts = charger_contacts()
    contacts.append({'nom': nom, 'telephone': telephone, 'email': email})
    sauvegarder_contacts(contacts)
    return redirect(url_for('index'))

@app.route('/supprimer/<nom>')
def supprimer(nom):
    contacts = charger_contacts()
    contacts = [c for c in contacts if c['nom'].lower() != nom.lower()]
    sauvegarder_contacts(contacts)
    return redirect(url_for('index'))

@app.route('/modifier/<nom>', methods=['GET', 'POST'])
def modifier(nom):
    contacts = charger_contacts()
    contact = next((c for c in contacts if c['nom'].lower() == nom.lower()), None)

    if not contact:
        return "Contact non trouvé", 404

    if request.method == 'POST':
        nouveau_nom = request.form['nom']
        telephone = request.form['telephone']
        email = request.form['email']

        contact['nom'] = nouveau_nom
        contact['telephone'] = telephone
        contact['email'] = email
        sauvegarder_contacts(contacts)
        return redirect(url_for('index'))

    return render_template('modifier.html', contact=contact)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
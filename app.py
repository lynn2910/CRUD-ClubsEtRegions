from flask import Flask, request, render_template, redirect, flash
from api import constants
from api.logs import *

#
#
#   STORED DATAS
#
#

regions = [
    {'id': 1, 'nomRegion': 'FrancheComte'},
    {'id': 2, 'nomRegion': 'IleDeFrance'},
    {'id': 3, 'nomRegion': 'Bretagne'},
    {'id': 4, 'nomRegion': 'Occitanie'},
]

clubs = [
    {'id': 1, 'nomClub': 'BelfortEchecs', 'nbAdherent': '67', 'dateCreation': '1977-01-31', 'prixCotisation': '100',
     'region_id': 1, 'image': 'BelfortEchecs.jpg'},
    {'id': 2, 'nomClub': 'EchiquierQuimpérois', 'nbAdherent': '36', 'dateCreation': '1983-06-27',
     'prixCotisation': '90', 'region_id': 3, 'image': 'EchiquierQuimperois.png'},
    {'id': 3, 'nomClub': 'TremblayEnFrance', 'nbAdherent': '109', 'dateCreation': '1982-03-05', 'prixCotisation': '50',
     'region_id': 2, 'image': 'TremblayEnFrance.jpg'},
    {'id': 4, 'nomClub': 'EchiquierLedonien', 'nbAdherent': '25', 'dateCreation': '1966-06-12', 'prixCotisation': '71',
     'region_id': 1, 'image': 'EchiquierLedonien.jpg'},
    {'id': 5, 'nomClub': 'EchiquierNimois', 'nbAdherent': '85', 'dateCreation': '1987-03-21', 'prixCotisation': '120',
     'region_id': 4, 'image': 'EchiquierNimois.jpg'},
    {'id': 6, 'nomClub': 'LuteceEchecs', 'nbAdherent': '89', 'dateCreation': '1957-08-05', 'prixCotisation': '420',
     'region_id': 2, 'image': 'LuteceEchecs.jpg'},
    {'id': 7, 'nomClub': 'UsamEchiquierBrestois', 'nbAdherent': '73', 'dateCreation': '1964-06-25',
     'prixCotisation': '100', 'region_id': 3, 'image': 'UsamEchiquierBrestois.jpg'},
    {'id': 8, 'nomClub': 'EchecsClubMontpellier', 'nbAdherent': '119', 'dateCreation': '1981-04-15',
     'prixCotisation': '85', 'region_id': 4, 'image': 'EchecsClubMontpellier.jpg'},
    {'id': 9, 'nomClub': 'ClichyEchecs92', 'nbAdherent': '85', 'dateCreation': '1961-10-07', 'prixCotisation': '189',
     'region_id': 2, 'image': 'ClichyEchecs92.jpg'},
    {'id': 10, 'nomClub': 'RoiBlancMontbeliard', 'nbAdherent': '31', 'dateCreation': '1950-02-10',
     'prixCotisation': '76', 'region_id': 1, 'image': 'RoiBlancMontbeliard.jpg'},
    {'id': 11, 'nomClub': 'EchiquierToulousain', 'nbAdherent': '88', 'dateCreation': '1978-03-18',
     'prixCotisation': '140', 'region_id': 4, 'image': 'EchiquierToulousain.png'},
    {'id': 12, 'nomClub': 'RennesPaulBert', 'nbAdherent': '89', 'dateCreation': '1959-10-07', 'prixCotisation': '115',
     'region_id': 3, 'image': 'RennesPaulBert.jpg'}
]

#
#
#   API
#
#

app = Flask(__name__)
app.secret_key = constants.SECRET_KEY


@app.route('/')
def show_accueil():
    return render_template('layout.html')


# affiche-les regions	retourne la vue show_region.html
@app.route('/region/show', methods=["GET"])
def show_region():
    return render_template('region/show_region.html', regions=regions)


# affiche le formulaire pour ajouter une region	retourne la vue add_region.html
@app.route('/region/add', methods=["GET"])
def add_region():
    return render_template('region/add_region.html')


# validation (soumission) du formulaire pour ajouter une region	redirection sur la route /region/show
@app.route('/region/add', methods=["POST"])
def add_region_post():
    # TODO
    name = request.form.get('nomRegion', '')
    message = u"Region crée; { nomRegion: " + name + " }"
    info(message)
    flash(message, 'success')
    return redirect('/region/show')


# suppression d’une region	redirection sur la route /region/show
@app.route("/region/delete", methods=["GET"])
def delete_region():
    region_id = request.args.get('id', '')
    message = u"Region supprimée; { id: " + region_id + " }"
    info(message)
    flash(message, 'warning')
    return redirect('/region/show')


# affiche le formulaire pour modifier une region	retourne la vue add_region.html
@app.route('/region/edit', methods=["GET"])
def edit_region():
    region_id = request.args.get('id', '')
    region_id = int(region_id)
    region = regions[region_id-1]
    return render_template('region/edit_region.html', region=region)


# validation (soumission) du formulaire pour modifier une region	redirection sur la route /region/show
@app.route("/region/edit", methods=["POST"])
def valid_edit_region():
    name = request.form['nomRegion']
    region_id = request.form.get('id', '')

    message = u"Region supprimée; { id: " + region_id + ", nomRegion: " + name + " }"
    info(message)
    flash(message, 'success')
    return redirect('/region/show')


# affiche les clubs	retourne la vue show_club.html
@app.route("/club/show", methods=["GET"])
def show_club():
    return render_template("club/show_club.html", clubs=clubs)


# affiche le formulaire pour ajouter un club	retourne la vue add_club.html
@app.route("/club/add", methods=["GET"])
def add_club():
    return render_template("club/add_club.html", regions=regions)


# validation (soumission) du formulaire pour ajouter un club	redirection sur la route /club/show
@app.route("/club/add", methods=["POST"])
def valid_add_club():
    name = request.form.get('nomClub', '')
    adherents = request.form.get('nbAdherent', '')
    date_creation = request.form.get('dateCreation', '')
    cotisation = request.form.get('prixCotisation', '')
    region_id = request.form.get('region_id', '')
    logo = request.form.get('image', '')
    message = (u'Club ajouté; { nom:' + name + ', adherents :' + adherents + ', date_creation:' + date_creation
               + ', cotisation:' + cotisation + ', region_id:' + region_id + ', logo:' + logo)
    flash(message, 'success')
    return redirect('/club/show')


# suppression d’un club	redirection sur la route /club/show
@app.route("/club/delete", methods=["GET"])
def delete_club():
    club_id = request.args.get('id', '')
    message = u'Article supprimé; { id : ' + club_id + ' }'
    info(message)
    flash(message, 'warning')
    return redirect('/club/show')


# affiche le formulaire pour modifier un club	retourne la vue add_club.html
@app.route("/club/edit", methods=["GET"])
def edit_club():
    club_id = request.args.get('id', '')
    club_id = int(club_id)
    club = clubs[club_id-1]
    return render_template('club/edit_club.html', club=club, regions=regions)


# validation (soumission) du formulaire pour modifier un club	redirection sur la route /club/show
@app.route("/club/edit", methods=["POST"])
def valid_edit_club():
    club_id = request.form.get('id', '')
    nom_club = request.form.get('nomClub', '')
    nb_adherent = request.form.get('nbAdherent', '')
    date_creation = request.form.get('dateCreation', '')
    prix_cotisation = request.form.get('prixCotisation', '')
    region_id = request.form.get('region_id', '')
    image = request.form.get('image', '')
    message = (u'Club modifié; { id:' + club_id + ', ' + 'nomClub:' + nom_club + ', nb_adherent :' + nb_adherent +
               ', dateCreation:' + date_creation + ', prixCotisation:' + prix_cotisation
               + ', region_id:' + region_id + ', image:' + image + " }")
    flash(message, 'success')
    return redirect('/club/show')


# affichage du formulaire du filtre et des éléments d’une des tables python sous forme de ‘cards’
# retourne la vue show_club.html
@app.route("/club/filtre", methods=["GET"])
def filtre_club():
    return render_template('club/front_club_filtre_show.html', clubs=clubs, regions=regions)


if __name__ == '__main__':
    info(f'App is running on {constants.HOST}:{constants.PORT}')
    app.run(constants.HOST, constants.PORT)

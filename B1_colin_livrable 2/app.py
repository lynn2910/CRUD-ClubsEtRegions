import requests
from flask import g, Flask, request, render_template, redirect, flash
from api import constants
from api.logs import *
import datetime
import pymysql.cursors

#
#
#   API
#
#

app = Flask(__name__)
app.secret_key = constants.SECRET_KEY

app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route('/')
def show_accueil():
    return render_template('layout.html')


# affiche-les regions	retourne la vue show_region.html
@app.route('/region/show', methods=["GET"])
def show_region():
    return render_template('region/show_region.html', regions=get_regions())


# affiche le formulaire pour ajouter une region	retourne la vue add_region.html
@app.route('/region/add', methods=["GET"])
def add_region():
    return render_template('region/add_region.html')


# validation (soumission) du formulaire pour ajouter une region	redirection sur la route /region/show
@app.route('/region/add', methods=["POST"])
def add_region_post():
    name = request.form.get('nomRegion', '')

    mycursor = get_db().cursor()
    mycursor.execute(requests.ADD_REGION, name)

    get_db().commit()

    flash(f"La région {name} a été créée avec succès.", 'success')
    return redirect('/region/show')


# suppression d’une region	redirection sur la route /region/show
@app.route("/region/delete", methods=["GET"])
def delete_region():
    id_region = request.args.get('id', '')

    cursor = get_db().cursor()
    cursor.execute(requests.SELECT_CLUBS_ID, id_region)
    clubs = cursor.fetchall()

    if len(clubs) > 0:
        return render_template(
            "region/delete_check.html",
            clubs=clubs,
            id_region=id_region
        )
    else:
        cursor.execute(requests.DELETE_REGION, id_region)

        get_db().commit()

        flash(f"La région n°{id_region} a été supprimée.", 'success')
        return redirect('/region/show')


# affiche le formulaire pour modifier une region	retourne la vue add_region.html
@app.route('/region/edit', methods=["GET"])
def edit_region():
    id_region = request.args.get('id', '')

    mycursor = get_db().cursor()
    mycursor.execute(requests.SELECT_CLUBS_ID_CLEAN, id_region)

    region = mycursor.fetchone()

    return render_template('region/edit_region.html', region=region)


# validation (soumission) du formulaire pour modifier une region	redirection sur la route /region/show
@app.route("/region/edit", methods=["POST"])
def valid_edit_region():
    nom_region = request.form['nomRegion']
    id_region = request.form.get('id', '')

    mycursor = get_db().cursor()
    mycursor.execute(requests.UPDATE_REGION, (nom_region, id_region))

    get_db().commit()

    flash(f"La région n°{id_region} est désormais nommée {nom_region}", 'success')
    return redirect('/region/show')


# affiche les clubs	retourne la vue show_club.html
@app.route("/club/show", methods=["GET"])
def show_club():
    mycursor = get_db().cursor()
    mycursor.execute(requests.SELECT_CLUBS)
    fetched_clubs = mycursor.fetchall()

    return render_template("club/show_club.html", clubs=fetched_clubs)


# affiche le formulaire pour ajouter un club	retourne la vue add_club.html
@app.route("/club/add", methods=["GET"])
def add_club():
    return render_template("club/add_club.html", regions=get_regions())


# validation (soumission) du formulaire pour ajouter un club	redirection sur la route /club/show
@app.route("/club/add", methods=["POST"])
def valid_add_club():
    name = request.form.get('nomClub', '')
    adherents = request.form.get('nbAdherent', '')
    date_creation = request.form.get('dateCreation', '')
    cotisation = request.form.get('prixCotisation', '')
    region_id = request.form.get('region_id', '')
    logo = request.form.get('image', '')

    mycursor = get_db().cursor()
    mycursor.execute(
        requests.ADD_CLUB,
        (name, adherents, date_creation, cotisation, region_id, logo)
    )

    get_db().commit()

    message = (u'Club ajouté; { nom:' + name + ', adherents :' + adherents + ', date_creation:' + date_creation
               + ', cotisation:' + cotisation + ', region_id:' + region_id + ', logo:' + logo)
    flash(
        f"Le club {name} a été créé:\n- Adhérents: {adherents}\n- Cotisation: {cotisation}€"
        + "\n- Date de création: {date_creation}",
        'success'
    )
    return redirect('/club/show')


# suppression d’un club	redirection sur la route /club/show
@app.route("/club/delete", methods=["GET"])
def delete_club():
    id_club = request.args.get('id', '')

    mycursor = get_db().cursor()
    mycursor.execute(requests.DELETE_CLUB, id_club)

    get_db().commit()

    flash(f"Le club n°{id_club} a été supprimé.", 'success')

    delete_region_id = request.args.get("delete_region", None)
    if delete_region_id:
        return redirect(f"/region/delete?id={delete_region_id}")
    else:
        return redirect('/club/show')


# affiche le formulaire pour modifier un club	retourne la vue add_club.html
@app.route("/club/edit", methods=["GET"])
def edit_club():
    id_club = request.args.get('id', '')

    mycursor = get_db().cursor()
    mycursor.execute(requests.SELECT_SINGLE_CLUB, id_club)
    fetched_club = mycursor.fetchone()

    mycursor.execute(requests.SELECT_CLUBS_ID_CLEAN)
    regions = mycursor.fetchall()

    return render_template('club/edit_club.html', club=fetched_club, regions=regions)


# validation (soumission) du formulaire pour modifier un club	redirection sur la route /club/show
@app.route("/club/edit", methods=["POST"])
def valid_edit_club():
    id_club = request.form.get('id', '')
    nom_club = request.form.get('nomClub', '')
    nb_adherent = request.form.get('nbAdherent', '')
    date_creation = request.form.get('dateCreation', '')
    prix_cotisation = request.form.get('prixCotisation', '')
    region_id = request.form.get('region_id', '')
    image = request.form.get('image', '')
    message = (u'Club modifié; { id:' + id_club + ', ' + 'nomClub:' + nom_club + ', nb_adherent :' + nb_adherent +
               ', dateCreation:' + date_creation + ', prixCotisation:' + prix_cotisation
               + ', region_id:' + region_id + ', image:' + image + " }")

    mycursor = get_db().cursor()
    mycursor.execute(
        requests.UPDATE_CLUB,
        (nom_club, nb_adherent, date_creation, prix_cotisation, region_id, image, id_club)
    )

    get_db().commit()

    flash(message, 'success')
    return redirect('/club/show')


# affichage du formulaire du filtre et des éléments d’une des tables python sous forme de ‘cards’
# retourne la vue show_club.html
@app.route("/club/filtre", methods=["GET"])
def filtre_club():
    mycursor = get_db().cursor()
    mycursor.execute(requests.SELECT_CLUBS)
    fetched_club = mycursor.fetchone()

    filter_word = request.args.get('nom', None)
    filter_items = request.args.getlist('region')

    # Adhérents

    filter_adherents_min = request.args.get('min_adherents', "0").replace(' ', '').replace(",", ".")
    filter_adherents_max = request.args.get('max_adherents', "1000000").replace(' ', '').replace(",", ".")

    if len(filter_adherents_min) < 1 or filter_adherents_min == "":
        filter_adherents_min = 0
    else:
        filter_adherents_min = int(filter_adherents_min)

    if len(filter_adherents_max) < 1 or filter_adherents_max == "":
        filter_adherents_max = 1000000
    else:
        filter_adherents_max = int(filter_adherents_max)

    # Cotisation

    filter_cotisation_min = request.args.get('min_cotisation', "0").replace(' ', '').replace(",", ".")
    filter_cotisation_max = request.args.get('max_cotisation', "1000000").replace(' ', '').replace(",", ".")

    if len(filter_cotisation_min) < 1 or filter_cotisation_min == "":
        filter_cotisation_min = 0
    else:
        filter_cotisation_min = int(filter_cotisation_min)

    if len(filter_cotisation_max) < 1 or filter_cotisation_max == "":
        filter_cotisation_max = 1000000
    else:
        filter_cotisation_max = int(filter_cotisation_max)

    # Filter word

    if filter_word and filter_word != '':
        filter_word = f"%{filter_word}%"
    else:
        filter_word = "%"

    sql = requests.FILTER + ""

    if len(filter_items) > 0:
        sql += "AND ("
        for i in range(0, len(filter_items)):
            region = filter_items[i]
            if region.isdigit():
                sql += f"region_id = {region})"
            if i < len(filter_items) - 1:
                sql += " AND ("

    sql += ";"

    print(sql, (filter_word, filter_cotisation_min, filter_cotisation_max, filter_adherents_min, filter_adherents_max))

    mycursor = get_db().cursor()
    mycursor.execute(
        sql,
        (filter_word, filter_cotisation_min, filter_cotisation_max, filter_adherents_min, filter_adherents_max)
    )

    filtered_clubs = mycursor.fetchall()

    return render_template(
        'club/front_club_filtre_show.html',
        clubs=filtered_clubs,
        regions=get_regions(),
        args=request.args,
        selected_regions=filter_items,
    )


@app.route('/etat', methods=["GET"])
def etat():
    cursor = get_db().cursor()
    cursor.execute(requests.ETAT_GLOBAL)
    global_datas = cursor.fetchone()
    _ = cursor.fetchall()  # Nettoyage des données qui pourraient être en trop

    cursor.execute(requests.ETAT_TABLE)
    table = cursor.fetchall()

    return render_template(
        'region/etat.html',
        global_datas=global_datas,
        table=table
    )


def get_regions():
    mycursor = get_db().cursor()
    sql = "SELECT id_region AS id, nom_region AS nomRegion  FROM region;"
    mycursor.execute(sql)

    return mycursor.fetchall()


def get_db():
    if 'db' not in g:
        g.db = pymysql.connect(
            host="localhost",
            user="lynn",
            password="Pusyux8484",
            database="iut",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


if __name__ == '__main__':
    info(f'App is running on {constants.HOST}:{constants.PORT}')
    app.run(constants.HOST, constants.PORT)

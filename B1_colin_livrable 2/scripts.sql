-- Supprimer les tables si elles existent
DROP TABLE IF EXISTS clubs;
DROP TABLE IF EXISTS regions;
DROP TABLE IF EXISTS club;
DROP TABLE IF EXISTS region;

-- Créer les tables
CREATE TABLE region
(
    id_region INT AUTO_INCREMENT,
    nom_region VARCHAR(64),

    PRIMARY KEY (id_region)
);

CREATE TABLE club
(
    id_club         INT AUTO_INCREMENT,
    nom_club        VARCHAR(64),
    nb_adherent    INT,
    date_creation   DATE,
    prix_cotisation DECIMAL(5, 2),
    region_id       INT,
    image           VARCHAR(255),

    FOREIGN KEY (region_id) REFERENCES region (id_region),
    PRIMARY KEY (id_club)
);

-- Ajouter les enregistrements
INSERT INTO region (id_region, nom_region) VALUES
   ( NULL ,'FrancheComte'),
   ( NULL ,'IleDeFrance'),
   ( NULL ,'Bretagne'),
   ( NULL ,'Occitanie');

INSERT INTO club (id_club, nom_club, nb_adherent, date_creation, prix_cotisation, region_id, image) VALUES
   (NULL ,'BelfortEchecs','67','1977-01-31','100',1,'BelfortEchecs.jpg'),
   (NULL ,'EchiquierQuimpérois', '36', '1983-06-27', '90', 3,'EchiquierQuimperois.png'),
   (NULL ,'TremblayEnFrance', '109', '1982-03-05', '50', 2,'TremblayEnFrance.jpg'),
   (NULL ,'EchiquierLedonien', '25', '1966-06-12', '71', 1,'EchiquierLedonien.jpg'),
   (NULL ,'EchiquierNimois' , '85', '1987-03-21', '120', 4,'EchiquierNimois.jpg'),
   (NULL ,'LuteceEchecs', '89', '1957-08-05', '420', 2,'LuteceEchecs.jpg'),
   (NULL ,'UsamEchiquierBrestois', '73', '1964-06-25', '100', 3,'UsamEchiquierBrestois.jpg'),
   (NULL ,'EchecsClubMontpellier' , '119', '1981-04-15', '85', 4,'EchecsClubMontpellier.jpg'),
   (NULL ,'ClichyEchecs92', '85', '1961-10-07', '189', 2,'ClichyEchecs92.jpg'),
   (NULL ,'RoiBlancMontbeliard', '31', '1950-02-10', '76', 1,'RoiBlancMontbeliard.jpg'),
   (NULL ,'EchiquierToulousain', '88', '1978-03-18', '140', 4,'EchiquierToulousain.png'),
   (NULL ,'RennesPaulBert', '89', '1959-10-07', '115', 3,'RennesPaulBert.jpg');

-- Supprimer la clé étrangère
ALTER TABLE club DROP FOREIGN KEY club_ibfk_1;

-- Re-créer la contrainte de clé étrangère
ALTER TABLE club ADD CONSTRAINT club_ibfk_1 FOREIGN KEY (region_id) REFERENCES region (id_region);

-- Exemple de requête d'agrégation avec jointure
SELECT SUM(club.prix_cotisation), region.nom_region
FROM club LEFT JOIN region
ON club.region_id = region.id_region
GROUP BY region.nom_region;

-- Exemple de requête préparée pour modifier un enregistrement
PREPARE stmt1 FROM 'UPDATE club SET nom_club = ? WHERE id_club = ?';
SET @nom = 'NouveauNom', @id = 1;
EXECUTE stmt1 USING @nom, @id;
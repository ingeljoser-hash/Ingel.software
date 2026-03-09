-- Habilitar el uso de claves foráneas
PRAGMA foreign_keys = ON;

-- Crear tablas
CREATE TABLE Miembros (
    cedula INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL,
    apellido TEXT NOT NULL,
    telefono TEXT NOT NULL
);

CREATE TABLE Clases (
    id_sesion INTEGER PRIMARY KEY,
    nombre_clase TEXT NOT NULL,
    dia_semana TEXT NOT NULL,
    horario TEXT NOT NULL
);

CREATE Table IF NOT EXISTS Inscripcion (
    id_inscripcion INTEGER PRIMARY KEY,
    cedula INTEGER NOT NULL,
    id_sesion INTEGER NOT NULL,
    FOREIGN KEY (cedula) REFERENCES Miembros (cedula),
    FOREIGN KEY (id_sesion) REFERENCES Clases (id_sesion),

);

Insertar Miembros
INSERT INTO
    Miembros (cedula, nombre, apellido, telefono)
VALUES (
        '40258391726',
        'Federico',
        'Valverde',
        '8093457821'

    ),
    (
        '03176420951',
        'Brahim',
        'Diaz',
        '8296149053'
    ),
    (
        '22491837463',
        'Alexander',
        'Arnold',
        '8492734689'
    ),
    (
        '01567249019',
        'Eladio',
        'Carrion',
        '8095561294'
    ),
    (
        '11845023964',
        'Ingel',
        'Soto',
        '8494465081'
    );

Insertar Clases
INSERT INTO
    Clases (id_sesion, nombre_clase, dia_semana, horario)
VALUES (
        '58391',
        'Spinning',
        'Lunes',
        '5 a 7 p.m'

    ),
    (
        '76420',
        'Zumba',
        'Martes',
        '3 a 5 p.m'
    ),
    (
        '91837',
        'Cross Training',
        'Miercoles',
        '6 a 8 p.m'
    ),
    (
        '67249',
        'Yoga',
        'Jueves',
        '9 a 10 a.m'
    ),
    (
        '45023',
        'Pilates',
        'Viernes',
        '7 a 8 p.m'
    );

Insertar Inscripciones
INSERT INTO Inscripcion (id_inscripcion, cedula, id_sesion)
VALUES
(1, 40258391726, 58391),
(2, 03176420951, 76420),
(3, 22491837463, 91837),
(4, 01567249019, 67249),
(5, 11845023964, 45023);

Consulta con tablas relacionadas
SELECT
    Miembros.cedula,
    Miembros.nombre,
    Miembros.apellido,
    Inscripcion.id_inscripcion,
    Inscripcion.id_sesion
FROM Miembros
INNER JOIN Inscripcion
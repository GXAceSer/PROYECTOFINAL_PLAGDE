--Usuarios que estarán permitidos al uso----
CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    cargo VARCHAR(100),
    email VARCHAR(100) NOT NULL,
    contrasena VARCHAR(255) NOT NULL
);

-- Usuarios precargados
INSERT INTO usuario (nombre, cargo, email, contrasena) VALUES 
('usuario Demo', 'Admin', 'admin@test.com', 'admin123'),
('usuario Prueba', 'Empleado', 'user@test.com', 'user123');

-- Datos maestro
CREATE TABLE profesor (
    id_profesor VARCHAR(10) PRIMARY KEY,
    nombreP VARCHAR(100),
    materia VARCHAR(100)
);

-- Profesores precargados
INSERT INTO profesor (id_profesor, nombreP, materia) VALUES ('PROF001', 'Laura Méndez', 'Español');
INSERT INTO profesor (id_profesor, nombreP, materia) VALUES ('PROF002', 'Carlos Rivera', 'Matemáticas');



-- Tutores
CREATE TABLE tutor (
    id_T VARCHAR(20) PRIMARY KEY,
    nombreT VARCHAR(150) NOT NULL,
    apellido_PT VARCHAR(150) NOT NULL,
    apellido_MT VARCHAR(150) NOT NULL
);

--Datos tutores
INSERT INTO tutor (id_T, nombreT, apellido_PT, apellido_MT) VALUES
('3', 'Luis', 'Ramírez', 'Gómez'),
('4', 'Patricia', 'Cruz', 'Navarro');


-- Alumnos
CREATE TABLE alumno (
    matricula VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    apellido_P VARCHAR(150) NOT NULL,
    apellido_M VARCHAR(150) NOT NULL,
    grado VARCHAR(20),
    grupo VARCHAR(10),
    promedio DECIMAL(3,1)
);

---Datos alumnos--------------------
INSERT INTO alumno (matricula, nombre, apellido_P, apellido_M, grado, grupo, promedio) VALUES
('1', 'Ana', 'López', 'Ramírez', '3°', 'A', 9.1),
('2', 'Carlos', 'Martínez', 'Gómez', '2°', 'B', 8.7),
('3', 'Daniela', 'Pérez', 'Hernández', '1°', 'A', 9.5);


-- Relación tutor-alumno (muchos a muchos)
CREATE TABLE alumno_tutor (
    id_A VARCHAR(20) REFERENCES alumno(matricula) ON DELETE CASCADE,
    id_T VARCHAR(6) REFERENCES tutor(id_T) ON DELETE CASCADE,
    PRIMARY KEY (id_A, id_T)
);

INSERT INTO alumno_tutor (id_A, id_T) VALUES
('1', '4'),
('2', '3');

-- Datos Documentos: Diplomado
CREATE TABLE diplomado (
    id SERIAL PRIMARY KEY,
    fechaR DATE NOT NULL,
    id_alumno VARCHAR(20) UNIQUE REFERENCES alumno(matricula) ON DELETE CASCADE
);

-- Datos Documentos: Citatorio
CREATE TABLE citatorio (
    id SERIAL PRIMARY KEY,
    fecha_R DATE NOT NULL,
    fecha_Cita DATE NOT NULL,
    hora TIME,
    motivo VARCHAR(100),
    id_profesor VARCHAR(10) REFERENCES profesor(id_profesor)
);

-- Historial de documentos generados (SE PLANEABA HACER)
CREATE TABLE historial (
    id SERIAL PRIMARY KEY,
    id_usuario INTEGER REFERENCES usuario(id) ON DELETE CASCADE,
    tipo_Doc VARCHAR(50) NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    detalles TEXT
);

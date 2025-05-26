-- db_a56ecc_enedb.dbo.Usuarios definition

-- Drop table

-- DROP TABLE db_a56ecc_enedb.dbo.Usuarios;

CREATE TABLE db_a56ecc_enedb.dbo.Usuarios (
	id_usuario int IDENTITY(1,1) NOT NULL,
	nombre nvarchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	usuario nvarchar(50) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	password nvarchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	email nvarchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	rol nvarchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	departamento nvarchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	estado nvarchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS DEFAULT 'Activo' NULL,
	CONSTRAINT PK__Usuarios__4E3E04AD6DF85C58 PRIMARY KEY (id_usuario),
	CONSTRAINT UQ__Usuarios__9AFF8FC63C4F01A8 UNIQUE (usuario)
);


INSERT INTO [dbo].[Usuarios] (
    [nombre],
    [usuario],
    [password],
    [email],
    [rol],
    [departamento],
    [estado]
)
VALUES (
    'Ronald Gubio',         -- nombre
    'rgubio',             -- usuario
    'rgubio',        -- password (idealmente cifrada)
    'r.gubio@crait.com.com',  -- email
    'admin',      -- rol
    'TICs',                 -- departamento
    'Activo'              -- estado
);


--##--------------
-- db_a56ecc_enedb.dbo.Tickets definition

-- Drop table

-- DROP TABLE db_a56ecc_enedb.dbo.Tickets;

CREATE TABLE db_a56ecc_enedb.dbo.Tickets (
	id_ticket int IDENTITY(1,1) NOT NULL,
	titulo nvarchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	descripcion nvarchar(MAX) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	estado nvarchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS DEFAULT 'abierto' NULL,
	id_usuario int NULL,
	fecha_creacion datetime DEFAULT getdate() NULL,
	fecha_cierre datetime NULL,
	CONSTRAINT PK__Tickets__48C6F523E7BF71F6 PRIMARY KEY (id_ticket)
);

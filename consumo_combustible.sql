-- Tabla para registrar el consumo de combustible de camiones
CREATE TABLE db_a56ecc_enedb.dbo.ConsumoCombustible (
    id_consumo INT IDENTITY(1,1) PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL,
    apellido NVARCHAR(100) NOT NULL,
    cedula NVARCHAR(20) NOT NULL,
    placa NVARCHAR(20) NOT NULL,
    valor DECIMAL(18,2) NOT NULL,
    fecha DATETIME DEFAULT GETDATE(),
    foto_voucher NVARCHAR(255) NULL -- Ruta o nombre del archivo subido
);

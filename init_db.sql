-- init_db.sql
CREATE TABLE productos (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(120) NOT NULL,
  precio NUMERIC(10,2) NOT NULL,
  stock INT NOT NULL
);

CREATE TABLE compras (
  id SERIAL PRIMARY KEY,
  producto_id INT REFERENCES productos(id),
  cantidad INT NOT NULL,
  fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Datos de ejemplo
INSERT INTO productos (nombre, precio, stock) VALUES
('Alimento perro 3kg', 12000, 50),
('Juguete hueso', 3000, 30),
('Arena gato 5kg', 8000, 20),
('Snack perro 200g', 1500, 100),
('Collar ajustable T-L', 7000, 15);

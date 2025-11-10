-- init_db.sql
CREATE TABLE productos (
  id SERIAL PRIMARY KEY,
  nombre VARCHAR(120) NOT NULL,
  precio NUMERIC(10,2) NOT NULL,
  stock INT NOT NULL,
  imagen_url TEXT NOT NULL
);

CREATE TABLE compras (
  id SERIAL PRIMARY KEY,
  producto_id INT REFERENCES productos(id),
  cantidad INT NOT NULL,
  fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Datos de ejemplo
INSERT INTO productos (nombre, precio, stock) VALUES
('Alimento perro 3kg', 12000, 50, https://mercadocarozzi.cl/media/catalog/product/cache/7e6366646a99abfd85e17ed2a9ddf5d1/7/8/7802575533586.jpg),
('Juguete hueso', 3000, 30, https://http2.mlstatic.com/D_NQ_NP_912155-MLC95797215564_102025-O-hueso-de-juguete-para-mascotas-perros-gatos-de-goma-15cm.webp),
('Arena gato 5kg', 8000, 20, https://pethome.cl/imagenes/productos/vancat-arena-para-gatos-aglomerante-5-kg.webp),
('Snack perro 200g', 1500, 100, https://dojiw2m9tvv09.cloudfront.net/42482/product/pack_naturalistic_treats7627jpg3847.jpg),
('Collar ajustable T-L', 7000, 15, https://dojiw2m9tvv09.cloudfront.net/22023/product/61ya2ij4fl-_ac_sl1000_0931.jpg);

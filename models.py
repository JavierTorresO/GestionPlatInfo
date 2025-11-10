# models.py
from psycopg2.extras import RealDictCursor
from database import get_conn, put_conn

def list_products():
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    # Ahora también seleccionamos imagen_url
    cur.execute("SELECT id, nombre, precio, stock, imagen_url FROM productos ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    put_conn(conn)
    return rows

def get_product(pid):
    conn = get_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    # También incluye imagen_url aquí
    cur.execute("SELECT id, nombre, precio, stock, imagen_url FROM productos WHERE id=%s;", (pid,))
    row = cur.fetchone()
    cur.close()
    put_conn(conn)
    return row

def purchase_product(pid, qty):
    """
    Intenta comprar qty unidades del producto pid.
    Retorna (success:bool, message:str).
    Usa SELECT ... FOR UPDATE para evitar race conditions.
    """
    conn = get_conn()
    cur = conn.cursor()
    try:
        cur.execute("BEGIN;")
        cur.execute("SELECT stock, precio FROM productos WHERE id=%s FOR UPDATE;", (pid,))
        r = cur.fetchone()
        if not r:
            cur.execute("ROLLBACK;")
            return False, "Producto no existe"
        stock, precio = r[0], r[1]
        if stock < qty:
            cur.execute("ROLLBACK;")
            return False, "Sin stock suficiente"
        cur.execute("UPDATE productos SET stock = stock - %s WHERE id=%s;", (qty, pid))
        cur.execute("INSERT INTO compras (producto_id, cantidad) VALUES (%s, %s) RETURNING id;", (pid, qty))
        compra_id = cur.fetchone()[0]
        cur.execute("COMMIT;")
        return True, {"mensaje": "Compra registrada", "compra_id": compra_id}
    except Exception as e:
        try:
            cur.execute("ROLLBACK;")
        except:
            pass
        return False, str(e)
    finally:
        cur.close()
        put_conn(conn)

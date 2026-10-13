"""Persistencia SQLite para Mercado Local."""
import sqlite3
from contextlib import contextmanager
from pathlib import Path

SEED = [
    ("Café de origen", "Café tostado de altura, 500 g", 32000, "☕"),
    ("Miel artesanal", "Miel pura de cosecha local, 350 g", 24000, "🍯"),
    ("Chocolate 70%", "Chocolate artesanal, barra de 80 g", 14000, "🍫"),
    ("Granola casera", "Avena, semillas y frutos secos, 400 g", 21000, "🥣"),
]


@contextmanager
def connect(path):
    db = sqlite3.connect(path)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    try:
        with db:
            yield db
    finally:
        db.close()


def initialize(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with connect(path) as db:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY, name TEXT NOT NULL, description TEXT NOT NULL,
                price INTEGER NOT NULL CHECK(price > 0), emoji TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY, customer TEXT NOT NULL, email TEXT NOT NULL,
                total INTEGER NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL REFERENCES orders(id),
                product_id INTEGER NOT NULL REFERENCES products(id), quantity INTEGER NOT NULL CHECK(quantity BETWEEN 1 AND 20),
                unit_price INTEGER NOT NULL
            );
        """)
        count = db.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        if count == 0:
            db.executemany("INSERT INTO products(name,description,price,emoji) VALUES(?,?,?,?)", SEED)


def list_products(path):
    with connect(path) as db:
        return [dict(row) for row in db.execute("SELECT id,name,description,price,emoji FROM products ORDER BY id")]


def create_order(path, customer, email, items):
    if not isinstance(customer, str) or not 2 <= len(customer.strip()) <= 80:
        raise ValueError("El nombre debe tener entre 2 y 80 caracteres.")
    if not isinstance(email, str) or len(email) > 254 or "@" not in email or "." not in email.split("@")[-1]:
        raise ValueError("Escribe un correo electrónico válido.")
    if not isinstance(items, list) or not 1 <= len(items) <= 20:
        raise ValueError("El carrito debe tener entre 1 y 20 productos.")
    clean, ids = [], set()
    for item in items:
        if not isinstance(item, dict) or type(item.get("product_id")) is not int or type(item.get("quantity")) is not int:
            raise ValueError("Línea de pedido inválida.")
        pid, qty = item["product_id"], item["quantity"]
        if pid <= 0 or not 1 <= qty <= 20 or pid in ids:
            raise ValueError("Producto o cantidad inválida.")
        ids.add(pid)
        clean.append((pid, qty))
    with connect(path) as db:
        products = {}
        for pid, _ in clean:
            row = db.execute("SELECT id,price FROM products WHERE id=?", (pid,)).fetchone()
            if not row:
                raise ValueError("Uno de los productos ya no está disponible.")
            products[pid] = row["price"]
        total = sum(products[pid] * qty for pid, qty in clean)
        cur = db.execute("INSERT INTO orders(customer,email,total) VALUES(?,?,?)", (customer.strip(), email.strip().lower(), total))
        order_id = cur.lastrowid
        db.executemany("INSERT INTO order_items(order_id,product_id,quantity,unit_price) VALUES(?,?,?,?)",
                       [(order_id, pid, qty, products[pid]) for pid, qty in clean])
        return {"order_id": order_id, "total": total}

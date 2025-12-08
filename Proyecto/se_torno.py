import sqlite3
import csv
from pathlib import Path

DB_PATH = "Proyecto/se_torno.db"
CSV_PATH = "Proyecto/insertos_se_torno.csv"


# =========================
# 1. Esquema de la base de datos
# =========================

def init_db_schema():
    """Crea las tablas necesarias si no existen."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS Material (
            id_material INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            grupo_iso TEXT
        );

        CREATE TABLE IF NOT EXISTS Operacion (
            id_operacion INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Marca (
            id_marca INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            segmento TEXT
        );

        CREATE TABLE IF NOT EXISTS Inserto (
            id_inserto INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_iso TEXT NOT NULL,
            forma TEXT NOT NULL,
            angulo REAL NOT NULL,
            id_marca INTEGER NOT NULL,
            aplicacion_principal TEXT,
            material_grupo TEXT,
            precio_aprox REAL,
            descripcion TEXT,
            recubrimiento TEXT,
            profundidad_max_ranura REAL,
            UNIQUE (codigo_iso, forma, angulo, id_marca),
            FOREIGN KEY (id_marca) REFERENCES Marca(id_marca)
        );

        CREATE TABLE IF NOT EXISTS Parametros_Recomendados (
            id_param INTEGER PRIMARY KEY AUTOINCREMENT,
            id_inserto INTEGER NOT NULL,
            id_material INTEGER NOT NULL,
            id_operacion INTEGER NOT NULL,
            profundidad TEXT,
            acabado TEXT,
            Vc_min REAL,
            Vc_max REAL,
            ap_min REAL,
            ap_max REAL,
            f_min REAL,
            f_max REAL,
            nota_aplicacion TEXT,
            UNIQUE (id_inserto, id_material, id_operacion, profundidad, acabado),
            FOREIGN KEY (id_inserto) REFERENCES Inserto(id_inserto),
            FOREIGN KEY (id_material) REFERENCES Material(id_material),
            FOREIGN KEY (id_operacion) REFERENCES Operacion(id_operacion)
        );
        """
    )

    conn.commit()
    conn.close()


# =========================
# 2. Helpers para IDs y carga de datos
# =========================

def get_or_create_marca(cur, nombre, segmento):
    cur.execute("SELECT id_marca FROM Marca WHERE nombre = ?;", (nombre,))
    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute(
        "INSERT INTO Marca (nombre, segmento) VALUES (?, ?);",
        (nombre, segmento),
    )
    return cur.lastrowid


def get_or_create_material(cur, grupo_iso):
    """
    Mapear grupos ISO a nombres 'bonitos' para la tabla Material.
    P = acero al carbono, M = acero inoxidable, N = aluminio.
    """
    mapa = {
        "P": "Acero al carbono",
        "M": "Acero inoxidable",
        "N": "Aluminio",
    }
    nombre = mapa.get(grupo_iso, f"Grupo {grupo_iso}")

    cur.execute("SELECT id_material FROM Material WHERE nombre = ?;", (nombre,))
    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute(
        "INSERT INTO Material (nombre, grupo_iso) VALUES (?, ?);",
        (nombre, grupo_iso),
    )
    return cur.lastrowid


def get_or_create_operacion(cur, nombre):
    cur.execute("SELECT id_operacion FROM Operacion WHERE nombre = ?;", (nombre,))
    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute(
        "INSERT INTO Operacion (nombre) VALUES (?);",
        (nombre,),
    )
    return cur.lastrowid


def get_or_create_inserto(
    cur,
    codigo_iso,
    forma,
    angulo,
    id_marca,
    aplicacion_principal,
    material_grupo,
    precio_aprox,
    descripcion,
    recubrimiento,
    profundidad_max_ranura
):
    cur.execute(
        """
        SELECT id_inserto FROM Inserto
        WHERE codigo_iso = ? AND forma = ? AND angulo = ? AND id_marca = ?;
        """,
        (codigo_iso, forma, angulo, id_marca),
    )
    row = cur.fetchone()
    if row:
        cur.execute(
            """
            UPDATE Inserto
            SET aplicacion_principal = ?,
                material_grupo = ?,
                precio_aprox = ?,
                descripcion = ?,
                recubrimiento = ?,
                profundidad_max_ranura = ?
            WHERE id_inserto = ?;
            """,
            (
                aplicacion_principal,
                material_grupo,
                precio_aprox,
                descripcion,
                recubrimiento,
                profundidad_max_ranura,
                row[0],
            ),
        )
        return row[0]

    cur.execute(
        """
        INSERT INTO Inserto (
            codigo_iso, forma, angulo, id_marca,
            aplicacion_principal, material_grupo,
            precio_aprox, descripcion, recubrimiento,
            profundidad_max_ranura
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """,
        (
            codigo_iso,
            forma,
            angulo,
            id_marca,
            aplicacion_principal,
            material_grupo,
            precio_aprox,
            descripcion,
            recubrimiento,
            profundidad_max_ranura,
        ),
    )
    return cur.lastrowid


def create_or_update_parametros(
    cur,
    id_inserto,
    id_material,
    id_operacion,
    profundidad,
    acabado,
    vc_min,
    vc_max,
    ap_min,
    ap_max,
    f_min,
    f_max,
    nota,
):
    cur.execute(
        """
        SELECT id_param FROM Parametros_Recomendados
        WHERE id_inserto = ? AND id_material = ? AND id_operacion = ?
          AND profundidad = ? AND acabado = ?;
        """,
        (id_inserto, id_material, id_operacion, profundidad, acabado),
    )
    row = cur.fetchone()
    if row:
        cur.execute(
            """
            UPDATE Parametros_Recomendados
            SET Vc_min = ?, Vc_max = ?, ap_min = ?, ap_max = ?,
                f_min = ?, f_max = ?, nota_aplicacion = ?
            WHERE id_param = ?;
            """,
            (vc_min, vc_max, ap_min, ap_max, f_min, f_max, nota, row[0]),
        )
    else:
        cur.execute(
            """
            INSERT INTO Parametros_Recomendados (
                id_inserto, id_material, id_operacion,
                profundidad, acabado,
                Vc_min, Vc_max,
                ap_min, ap_max,
                f_min, f_max,
                nota_aplicacion
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """,
            (
                id_inserto,
                id_material,
                id_operacion,
                profundidad,
                acabado,
                vc_min,
                vc_max,
                ap_min,
                ap_max,
                f_min,
                f_max,
                nota,
            ),
        )


# =========================
# 3. Importar CSV a la BD
# =========================

def importar_csv():
    if not Path(CSV_PATH).exists():
        print(f"⚠ No se encontró el archivo CSV: {CSV_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        filas = list(reader)

    if not filas:
        print("⚠ El CSV está vacío.")
        conn.close()
        return

    print(f"Importando {len(filas)} filas desde {CSV_PATH} ...\n")

    for i, row in enumerate(filas, start=1):
        try:
            marca = row["marca"].strip()
            segmento = row["segmento"].strip()
            codigo_iso = row["codigo_iso"].strip()
            forma = row["forma"].strip()
            angulo = float(row["angulo"])
            aplicacion = row["aplicacion_principal"].strip()
            material_grupo = row["material_grupo"].strip()
            recubrimiento = row["recubrimiento"].strip()
            profundidad = row["profundidad"].strip().lower()
            acabado = row["acabado"].strip().lower()
            vc_min = float(row["vc_min"])
            vc_max = float(row["vc_max"])
            ap_min = float(row["ap_min"])
            ap_max = float(row["ap_max"])
            f_min = float(row["f_min"])
            f_max = float(row["f_max"])
            prof_max_str = row.get("profundidad_max_ranura", "").strip()
            profundidad_max_ranura = float(prof_max_str) if prof_max_str else None
            precio = float(row["precio_aprox"])
            observaciones = row.get("observaciones", "").strip()

            id_marca = get_or_create_marca(cur, marca, segmento)
            id_material = get_or_create_material(cur, material_grupo)
            id_operacion = get_or_create_operacion(cur, aplicacion)

            id_inserto = get_or_create_inserto(
                cur,
                codigo_iso,
                forma,
                angulo,
                id_marca,
                aplicacion,
                material_grupo,
                precio,
                observaciones,
                recubrimiento,
                profundidad_max_ranura,
            )

            create_or_update_parametros(
                cur,
                id_inserto,
                id_material,
                id_operacion,
                profundidad,
                acabado,
                vc_min,
                vc_max,
                ap_min,
                ap_max,
                f_min,
                f_max,
                observaciones,
            )

            print(f"✓ Fila {i}: {marca} {codigo_iso} importado/actualizado.")
        except Exception as e:
            print(f"⚠ Error en fila {i}: {e}")

    conn.commit()
    conn.close()
    print("\nImportación finalizada.\n")


# =========================
# 4. Interfaz por consola (sistema experto)
# =========================

def ask_choice(prompt, options):
    """Muestra un menú simple y devuelve la opción elegida (texto)."""
    print(prompt)
    for i, opt in enumerate(options, start=1):
        print(f"{i}. {opt}")
    while True:
        try:
            choice = int(input("Selecciona una opción: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
        except ValueError:
            pass
        print("Opción inválida, intenta de nuevo.\n")


def ask_user_inputs():
    """Recolecta los datos necesarios para el sistema experto."""
    print("=" * 60)
    print("SE-Torno - Asistente de selección de herramientas")
    print("=" * 60)

    material = ask_choice(
        "\nSelecciona el material de la pieza:",
        ["Acero al carbono", "Acero inoxidable", "Aluminio"],
    )

    operacion = ask_choice(
        "\nTipo de operación de torneado:",
        ["Desbaste", "Acabado", "Ranurado", "Tronzado"],
    )

    # AHORA: profundidad se pregunta para TODAS las operaciones
    profundidad = ask_choice(
        "\nProfundidad de corte aproximada:",
        ["baja", "media", "alta"],
    )

    acabado = ask_choice(
        "\nNivel del acabado superficial requerido:",
        ["bajo", "medio", "alto"],
    )

    forma_inserto = None
    prof_ranura_total = None  # SOLO para ranurado

    if operacion in ["Ranurado", "Tronzado"]:
        # Para ranurado y tronzado la complejidad geométrica global es irrelevante
        forma_inserto = "C"  # en la BD los modelamos como C normalizado

        if operacion == "Ranurado":
            # Pregunta adicional: profundidad total de la ranura
            opcion_prof_ranura = ask_choice(
                "\nProfundidad total de la ranura requerida:",
                [
                    "Hasta 10 mm",
                    "Hasta 12 mm",
                    "Hasta 18 mm",
                ],
            )
            if "10" in opcion_prof_ranura:
                prof_ranura_total = 10.0
            elif "12" in opcion_prof_ranura:
                prof_ranura_total = 12.0
            else:
                prof_ranura_total = 18.0

    else:
        # Para desbaste / acabado sí tiene sentido la geometría
        geometria = ask_choice(
            "\nComplejidad geométrica de la pieza:",
            [
                "Geometría simple (cilindros, conos suaves, hombros sencillos)",
                "Geometría compleja (radios pequeños, cambios bruscos, zonas estrechas)",
            ],
        )

        if geometria.startswith("Geometría simple"):
            forma_inserto = "C"
        else:
            pref = ask_choice(
                "\nSelecciona la forma de inserto rómbico preferida:",
                ["D (55°)", "V (35°)"],
            )
            forma_inserto = "D" if pref.startswith("D") else "V"

    while True:
        try:
            presupuesto = float(input("\nIntroduce tu presupuesto máximo (MXN): "))
            break
        except ValueError:
            print("Valor inválido, introduce un número.\n")

    return {
        "material": material,
        "operacion": operacion,
        "profundidad": profundidad,
        "acabado": acabado,
        "forma_inserto": forma_inserto,
        "presupuesto": presupuesto,
        "prof_ranura_total": prof_ranura_total,
    }


# =========================
# 5. Motor de inferencia + consultas
# =========================

def obtener_recomendaciones(hechos):
    """Aplica reglas y consulta la BD para obtener herramientas candidatas."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # IDs de material y operación
    cur.execute("SELECT id_material FROM Material WHERE nombre = ?;", (hechos["material"],))
    mat_row = cur.fetchone()
    if not mat_row:
        conn.close()
        return []

    id_material = mat_row["id_material"]

    cur.execute("SELECT id_operacion FROM Operacion WHERE nombre = ?;", (hechos["operacion"],))
    op_row = cur.fetchone()
    if not op_row:
        conn.close()
        return []

    id_operacion = op_row["id_operacion"]

    operacion = hechos["operacion"]
    forma = hechos["forma_inserto"]
    presupuesto = hechos["presupuesto"]
    acabado = hechos["acabado"].lower()
    profundidad = hechos["profundidad"].lower() if hechos["profundidad"] else None
    prof_ranura_total = hechos.get("prof_ranura_total")

    # Construimos consulta según el tipo de operación
    params = [id_material, id_operacion, forma]
    where_extra = ""

    if operacion in ["Desbaste", "Acabado"]:
        # Filtramos por profundidad + acabado
        where_extra = "AND p.profundidad = ? AND p.acabado = ?"
        params.extend([profundidad, acabado])

    elif operacion == "Tronzado":
        # AHORA también se usa profundidad + acabado
        where_extra = "AND p.profundidad = ? AND p.acabado = ?"
        params.extend([profundidad, acabado])

    elif operacion == "Ranurado":
        # Usamos profundidad + acabado y además profundidad máxima de ranura
        where_extra = "AND p.profundidad = ? AND p.acabado = ?"
        params.extend([profundidad, acabado])

        if prof_ranura_total is not None:
            where_extra += " AND (i.profundidad_max_ranura IS NULL OR i.profundidad_max_ranura >= ?)"
            params.append(prof_ranura_total)

    query = f"""
        SELECT 
            i.id_inserto,
            i.codigo_iso,
            i.forma,
            i.angulo,
            i.aplicacion_principal,
            i.precio_aprox,
            i.descripcion,
            m.nombre AS marca,
            m.segmento,
            p.Vc_min, p.Vc_max,
            p.ap_min, p.ap_max,
            p.f_min, p.f_max,
            p.profundidad,
            p.acabado,
            p.nota_aplicacion,
            i.profundidad_max_ranura
        FROM Inserto i
        JOIN Parametros_Recomendados p ON i.id_inserto = p.id_inserto
        JOIN Marca m ON i.id_marca = m.id_marca
        WHERE p.id_material = ?
          AND p.id_operacion = ?
          AND i.forma = ?
          {where_extra}
        ;
    """

    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()

    candidatas = [dict(row) for row in rows if row["precio_aprox"] <= presupuesto]
    return candidatas


def clasificar_recomendaciones(candidatas, presupuesto):
    """Clasifica herramientas como Ideal / Económica según segmento y precio."""
    if not candidatas:
        return {}

    candidatas.sort(key=lambda x: x["precio_aprox"])  # más barata primero
    economica = candidatas[0]

    ranking_segmento = {"Premium": 3, "Estandar": 2, "Económica": 1, "Economica": 1}
    ideal = max(
        candidatas,
        key=lambda x: ranking_segmento.get(x["segmento"], 0),
    )

    return {
        "ideal": ideal,
        "economica": economica,
    }


# =========================
# 6. Presentación de resultados
# =========================

def mostrar_resultados(hechos, clasificacion):
    print("\n" + "=" * 60)
    print("RECOMENDACIÓN DE HERRAMIENTAS - SE-Torno")
    print("=" * 60)

    if not clasificacion:
        print("No se encontraron herramientas dentro de tu presupuesto.\n")
        return

    ideal = clasificacion["ideal"]
    econ = clasificacion["economica"]

    print("\n➤ Herramienta IDEAL:")
    print(f"   Código inserto : {ideal['codigo_iso']}")
    print(f"   Forma / ángulo : {ideal['forma']} ({ideal['angulo']}°)")
    print(f"   Marca          : {ideal['marca']} ({ideal['segmento']})")
    print(f"   Precio aprox.  : ${ideal['precio_aprox']:.2f} MXN")
    print(f"   Aplicación     : {ideal['aplicacion_principal']}")
    print(f"   Nota           : {ideal['nota_aplicacion']}")

    print("\n➤ Herramienta ECONÓMICA:")
    print(f"   Código inserto : {econ['codigo_iso']}")
    print(f"   Forma / ángulo : {econ['forma']} ({econ['angulo']}°)")
    print(f"   Marca          : {econ['marca']} ({econ['segmento']})")
    print(f"   Precio aprox.  : ${econ['precio_aprox']:.2f} MXN")
    print(f"   Aplicación     : {econ['aplicacion_principal']}")
    print(f"   Nota           : {econ['nota_aplicacion']}")

    print("\n--- Explicación del sistema experto ---")
    print(
        f"Se seleccionó un inserto de forma {hechos['forma_inserto']} "
        f"de acuerdo con la operación '{hechos['operacion']}'."
    )
    print(
        f"El material indicado es {hechos['material']} y la operación es {hechos['operacion']}, "
        f"con profundidad de corte {hechos['profundidad']} y acabado {hechos['acabado']}."
    )
    print(
        f"Las herramientas mostradas cumplen con estos criterios técnicos y se encuentran "
        f"dentro del presupuesto de ${hechos['presupuesto']:.2f} MXN."
    )
    print("=" * 60 + "\n")


# =========================
# 7. main
# =========================

def main():
    init_db_schema()
    importar_csv()          # idempotente: puedes correrlo las veces que quieras
    hechos = ask_user_inputs()
    candidatas = obtener_recomendaciones(hechos)
    clasificacion = clasificar_recomendaciones(candidatas, hechos["presupuesto"])
    mostrar_resultados(hechos, clasificacion)


if __name__ == "__main__":
    main()

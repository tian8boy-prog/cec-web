# ✏️ EDITA SOLO ESTE ARCHIVO para personalizar tu página

NOMBRE_SITIO = "Crecimiento Espiritual Cristiano"
FRASE = "Pláticas de Dios, cuando las necesites."
PASTOR = "Pastor: Jose Luis Juarez Mejía"   # sale debajo de la frase; déjalo vacío ("") para ocultarlo

# Descripción que sale debajo del banner
DESCRIPCION_TITULO = "Una jornada de fe, transformación y propósito en Cristo"
DESCRIPCION_TEXTO = (
    "En “Crecimiento Espiritual Cristiano” creemos que la fe se fortalece cuando escuchamos, "
    "estudiamos y vivimos la Palabra de Dios. Aquí encontrarás pláticas bíblicas, testimonios y "
    "consejos prácticos para acercarte más a Dios, superar los momentos difíciles y crecer cada "
    "día en Cristo, sin importar en qué etapa de tu camino te encuentres. Estás en el lugar correcto: "
    "esta casa es también tuya.")
DESCRIPCION_TEMAS = (
    "En cada plática abordamos temas como estudio bíblico (la Palabra de Dios explicada con "
    "claridad, para aplicarla a tu vida diaria), oración y devoción (claves para cultivar una "
    "comunicación íntima y constante con Dios), testimonios (historias reales de lo que Dios hace "
    "en la vida de las personas) y vida en el Espíritu (cómo vivir tu fe en la familia, el trabajo "
    "y los desafíos de cada día).")

# Spotify: abre tu podcast en Spotify > Compartir > Copiar enlace
# El enlace se ve así: https://open.spotify.com/show/XXXXXXXX?si=...
# Pega solo el ID (las letras y números después de /show/)
SPOTIFY_SHOW_ID = "2AVzjupqzCvKAh0A2nUH4h"

# Reunión en línea de cada sábado
REUNION_DIA = 5                        # 5 = sábado (lunes=0 ... domingo=6)
REUNION_HORA = 20                      # 20 = 8:00 pm (formato 24 h)
REUNION_MINUTO = 0
REUNION_ZONA = "America/Mexico_City"
REUNION_ENLACE = "https://us04web.zoom.us/j/3544365614?pwd=czRoRzlWcThMVWYzRkFhUk01NCt5QT09"   # Zoom, Meet, etc.
REUNION_PLATAFORMA = "Zoom"

# Cuando una semana cambie la hora, agrega una línea con la fecha del sábado
# y la nueva hora (formato 24 h). Las fechas que ya pasaron no estorban, puedes dejarlas.
# Ejemplo: sábado 24 de octubre a las 6:00 pm  ->  "2026-10-24": (18, 0)
REUNION_EXCEPCIONES = {
    # "2026-10-24": (18, 0),
}

# ===== Versículo del día =====
# Se elige solo, de toda la Biblia, y cambia cada día por muchísimos años.
BIBLIA_ARCHIVO = "REINA_VALERA_1909.json"   # debe estar junto a app.py

# Para fijar uno a mano (por ejemplo en una fecha especial), escribe la
# referencia: "Juan 3:16" o "Salmo 23:1-3". Déjalo en None para el modo automático.
VERSICULO_FIJO = None

# Cada cuántos días sale uno de tus favoritos de referencias.json
# (3 = uno de cada tres días; 0 = nunca)
FAVORITOS_CADA = 3

# Filtros del modo automático
LARGO_MIN = 50           # evita versículos demasiado cortos
LARGO_MAX = 220          # evita versículos demasiado largos
LIBROS_EXCLUIDOS = []    # ej. ["Números", "Levítico"]
VERSICULOS_EXCLUIDOS = []  # ej. ["Génesis 38:9"] para quitar uno en particular
SEMILLA = "CEC"          # no la cambies: reordenaría todos los días

# Correcciones a mano: si algún versículo sale mal escrito en la Biblia, ponlo aquí.
# Escribe la referencia tal como aparece en la página.
CORRECCIONES = {
    "Salmo 118:24": "Este es el día que hizo Jehová; nos gozaremos y alegraremos en él.",
    "Salmos 118:24": "Este es el día que hizo Jehová; nos gozaremos y alegraremos en él.",
}

import hashlib
import json
import re
from functools import lru_cache
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from flask import Flask, render_template

import config
from biblia import Biblia

app = Flask(__name__)
BASE = Path(__file__).parent
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]


PALABRAS_BUENAS = ("dios", "jehová", "señor", "jesús", "cristo", "amor", "amar", "paz", "esperanza",
                   "gracia", "misericordia", "salvación", "salvo", "alma", "corazón", "bendit",
                   "bendec", "alegr", "gozo", "verdad", "vida", "luz", "fortaleza", "confi",
                   "espíritu", "bondad", "justicia", "sabiduría", "fe ", "fiel", "ayuda", "socorro")
PALABRAS_MALAS = ("mató", "mataron", "matar", "matad", "heri", "hirió", "degoll", "desnud", "ramera",
                  "fornicaci", "adulter", "concubina", "incircunc", "cadáver", "lepr", "inmund",
                  "holocausto", "ofrenda", "novillo", "carnero", "machos cabríos", "hijos de",
                  "destru", "destrú", "furor", "enemigos", "batalla", "guerra", "venganza",
                  "costumbre", "contrato", "tributo", "ejército", "ciudad de", "rey de")

BIBLIA = Biblia(BASE / config.BIBLIA_ARCHIVO)


PREFIJO_TITULO = re.compile(
    r"^(?:Salmo|Cántico|Oración|Alabanza|Mictam|Maskil|Masquil|Al músico|Para)\b[^.]{0,80}\.\s+"
    r"(?=[A-ZÁÉÍÓÚÑ]{2,}\b|[AYO]\s+[A-ZÁÉÍÓÚÑ]{2,}\b)")
ENCABEZADO = re.compile(r"^(Al Músico|Salmo|Cántico|Oración de|Masquil|Maskil|Mictam|Alabanza)")
LETRAS = re.compile(r"[^A-Za-zÁÉÍÓÚÑáéíóúñ]")
NOMBRES = {"jehova": "Jehová", "jah": "Jah", "dios": "Dios"}


def _mayus(t, siguiente=None):
    letras = LETRAS.sub("", t)
    if len(letras) >= 2:
        return letras.isupper()
    return len(letras) == 1 and letras.isupper() and siguiente is not None and _mayus(siguiente)


def limpiar(texto):
    """Arregla detalles de la Biblia en JSON: títulos de salmos pegados al versículo,
    palabras en MAYÚSCULAS ('JEHOVA es mi pastor') y espacios raros."""
    texto = PREFIJO_TITULO.sub("", " ".join(texto.split()))
    palabras = texto.split(" ")
    i = 0
    while i < len(palabras) and _mayus(palabras[i], palabras[i + 1] if i + 1 < len(palabras) else None):
        i += 1
    for j in range(i):
        w = palabras[j].lower()
        palabras[j] = NOMBRES.get(LETRAS.sub("", w), w)
    if i:
        palabras[0] = palabras[0][:1].upper() + palabras[0][1:]
    texto = " ".join(palabras)
    # Cualquier otra palabra en MAYÚSCULAS (JESUS, DIOS...) pasa a normal
    return re.sub(r"\b[A-ZÁÉÍÓÚÑ]{3,}\b",
                  lambda m: {"JEHOVA": "Jehová", "JESUS": "Jesús"}.get(m.group(0), m.group(0).capitalize()),
                  texto)


@lru_cache(maxsize=1)
def lista_automatica():
    """Versículos de TODA la Biblia que sirven para el día: ni muy cortos ni muy largos,
    de tono positivo. El orden parece al azar pero es siempre el mismo."""
    biblia = json.loads((BASE / config.BIBLIA_ARCHIVO).read_text(encoding="utf-8-sig"))
    lista = []
    for libro, capitulos in biblia.items():
        if libro in config.LIBROS_EXCLUIDOS:
            continue
        for cap, versos in capitulos.items():
            for num, texto in versos.items():
                texto = limpiar(texto)
                bajo = texto.lower()
                ref = f"{libro} {cap}:{num}"
                if (not ENCABEZADO.match(texto)
                        and config.LARGO_MIN <= len(texto) <= config.LARGO_MAX
                        and ref not in config.VERSICULOS_EXCLUIDOS
                        and any(p in bajo for p in PALABRAS_BUENAS)
                        and not any(p in bajo for p in PALABRAS_MALAS)):
                    lista.append({"texto": texto, "ref": ref})
    lista.sort(key=lambda v: hashlib.sha256((config.SEMILLA + v["ref"]).encode()).hexdigest())
    return lista


@lru_cache(maxsize=1)
def lista_favoritos():
    refs = json.loads((BASE / "referencias.json").read_text(encoding="utf-8"))
    favoritos = []
    for ref in refs:
        texto = BIBLIA.buscar(ref)
        if texto:
            favoritos.append({"texto": limpiar(texto), "ref": ref})
    return favoritos


def _elegir_versiculo():
    if config.VERSICULO_FIJO:
        texto = BIBLIA.buscar(config.VERSICULO_FIJO)
        if texto:
            return {"texto": limpiar(texto), "ref": config.VERSICULO_FIJO}
    n = datetime.now(ZoneInfo(config.REUNION_ZONA)).date().toordinal()
    cada, favoritos = config.FAVORITOS_CADA, lista_favoritos()
    if cada and favoritos and n % cada == 0:
        return favoritos[(n // cada) % len(favoritos)]
    auto = lista_automatica()
    return auto[n % len(auto)]


def versiculo_del_dia():
    v = _elegir_versiculo()
    if v["ref"] in config.CORRECCIONES:
        v = {**v, "texto": config.CORRECCIONES[v["ref"]]}
    return v


def proxima_reunion():
    zona = ZoneInfo(config.REUNION_ZONA)
    ahora = datetime.now(zona)
    dias_faltan = (config.REUNION_DIA - ahora.weekday()) % 7
    fecha = (ahora + timedelta(days=dias_faltan)).replace(
        hour=config.REUNION_HORA, minute=config.REUNION_MINUTO, second=0, microsecond=0)
    if fecha < ahora:
        fecha += timedelta(days=7)
    especial = fecha.date().isoformat() in config.REUNION_EXCEPCIONES
    if especial:
        h, m = config.REUNION_EXCEPCIONES[fecha.date().isoformat()]
        fecha = fecha.replace(hour=h, minute=m)
    return {
        "especial": especial,
        "fecha_texto": f"{DIAS[fecha.weekday()]} {fecha.day} de {MESES[fecha.month - 1]}",
        "hora_texto": fecha.strftime("%I:%M %p").lstrip("0").lower(),
        "iso": fecha.isoformat(),
    }


@app.after_request
def cabeceras_de_seguridad(resp):
    """Protecciones que el navegador aplica a tu página."""
    resp.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'self' https://fonts.googleapis.com; "
        "font-src https://fonts.gstatic.com; "
        "img-src 'self' data:; "
        "frame-src https://open.spotify.com; "
        "base-uri 'self'; form-action 'self'; frame-ancestors 'self'")
    resp.headers["X-Content-Type-Options"] = "nosniff"
    resp.headers["X-Frame-Options"] = "SAMEORIGIN"
    resp.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    resp.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    resp.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return resp


@app.route("/")
def inicio():
    return render_template("index.html", c=config,
                           versiculo=versiculo_del_dia(),
                           reunion=proxima_reunion())


if __name__ == "__main__":
    app.run(debug=True)   # SOLO para probar en tu compu; en Render se usa gunicorn

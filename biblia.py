"""Lee una Biblia en JSON y busca versículos por referencia, ej. 'Juan 3:16'."""
import json
import re
import unicodedata
from pathlib import Path


def _norm(nombre):
    s = unicodedata.normalize("NFD", str(nombre).lower().strip())
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = re.sub(r"^(iii|ii|i)\s", lambda m: f"{len(m.group(1))} ", s)
    s = re.sub(r"[^a-z0-9 ]", "", s)
    return re.sub(r"\s+", " ", s).strip().rstrip("s")   # Salmo = Salmos


def _versos(cap, v):
    if isinstance(v, dict) and "verses" in v:
        v = v["verses"]
    if isinstance(v, dict):
        for k, t in v.items():
            yield cap, int(k), t
    else:
        for i, t in enumerate(v, 1):
            if isinstance(t, dict):
                yield cap, int(t.get("verse", i)), t.get("text", "")
            else:
                yield cap, i, t


def _capitulos(c):
    items = ([(int(k), v) for k, v in c.items()] if isinstance(c, dict)
             else list(enumerate(c, 1)))
    for n, v in items:
        yield from _versos(n, v)


class Biblia:
    def __init__(self, ruta):
        self.v = {}
        self._cargar(json.loads(Path(ruta).read_text(encoding="utf-8-sig")))

    def _poner(self, libro, cap, ver, texto):
        self.v[(_norm(libro), int(cap), int(ver))] = str(texto).strip()

    def _cargar(self, d):
        if isinstance(d, dict) and "books" in d:
            d = d["books"]
        if isinstance(d, list) and d and "verse" in d[0] and "text" in d[0]:
            for x in d:                                   # lista plana de versículos
                self._poner(x.get("book") or x.get("book_name"), x["chapter"], x["verse"], x["text"])
        elif isinstance(d, list):                         # lista de libros
            for libro in d:
                nombre = libro.get("name") or libro.get("book") or libro.get("abbrev")
                for c, v, t in _capitulos(libro["chapters"]):
                    self._poner(nombre, c, v, t)
        elif isinstance(d, dict):                         # {"Génesis": {...}}
            for nombre, cont in d.items():
                for c, v, t in _capitulos(cont):
                    self._poner(nombre, c, v, t)

    def buscar(self, ref):
        """'Juan 3:16' o 'Salmo 23:1-3' -> texto, o None si no existe."""
        m = re.match(r"^(.+?)\s+(\d+):(\d+)(?:-(\d+))?$", ref.strip())
        if not m:
            return None
        libro, cap, ini = _norm(m.group(1)), int(m.group(2)), int(m.group(3))
        fin = int(m.group(4) or ini)
        partes = [self.v.get((libro, cap, n)) for n in range(ini, fin + 1)]
        return " ".join(partes) if all(partes) else None

import subprocess
import csv
import os
from typing import List


def run_cmd(cmd: str):
    """Ejecuta un comando en shell y devuelve CompletedProcess."""
    return subprocess.run(cmd, shell=True, text=True, capture_output=True)


def branch_exists(ref: str) -> bool:
    """Comprueba si existe una referencia (local o remota)."""
    r = run_cmd(f"git show-ref --verify --quiet refs/heads/{ref}")
    if r.returncode == 0:
        return True
    r = run_cmd(f"git show-ref --verify --quiet refs/remotes/origin/{ref}")
    return r.returncode == 0


def default_main_branch() -> str:
    """Devuelve 'main' o 'master' según exista en el repo (por este orden)."""
    for b in ("main", "master"):
        if run_cmd(f"git rev-parse --verify {b}").returncode == 0:
            return b
    # fallback: variable de entorno o 'main'
    return os.getenv("GITHUB_REF_NAME", "main")


def file_modified_in_branch(branch: str, filepath: str) -> bool:
    """Comprueba si hay commits en 'branch' que toquen 'filepath'."""
    r = run_cmd(f"git log --oneline {branch} -- {filepath}")
    return r.stdout.strip() != ""


def has_merge_commit(branch: str) -> bool:
    """Devuelve True si la rama tiene algún commit de merge."""
    r = run_cmd(f"git log --merges -n 1 --pretty=%H {branch}")
    return r.stdout.strip() != ""


def commits_on_ref(ref: str) -> int:
    r = run_cmd(f"git rev-list --count {ref}")
    try:
        return int(r.stdout.strip()) if r.returncode == 0 else 0
    except ValueError:
        return 0


def main():
    # Obtener usuario a partir del nombre del repositorio (P02)
    # Ej: UFV-INGINF/DIS_P02_Fraxito2 -> Fraxito2
    repo_name = os.getenv("GITHUB_REPOSITORY", "")
    if repo_name:
        github_user = repo_name.split("/")[-1].replace("DIS_P02_", "")
    else:
        github_user = "desconocido"

    nota = 10
    comentarios: List[str] = []

    # Asegurar historial completo y ramas remotas
    run_cmd("git fetch --all --prune")

    main_branch = default_main_branch()
    feature_branch = "feature/frase"
    remote_feature = f"origin/{feature_branch}"

    # 1) Comprobar que existe la rama feature/frase en remoto
    if not branch_exists(feature_branch) and not branch_exists(remote_feature):
        nota -= 4
        comentarios.append("No existe la rama 'feature/frase' en el repositorio remoto")

    # 2) Comprobar que hay commits en feature/frase
    if commits_on_ref(remote_feature) == 0 and commits_on_ref(feature_branch) == 0:
        nota -= 2
        comentarios.append("La rama 'feature/frase' no tiene commits")

    # 3) Comprobar que frases.txt existe
    frases_path = os.path.join("tarea", "frases.txt")
    if not os.path.exists(frases_path):
        nota -= 2
        comentarios.append("Falta el archivo 'tarea/frases.txt'")

    # 4) Comprobar que se ha modificado frases.txt en ambas ramas
    try:
        if not file_modified_in_branch(main_branch, frases_path):
            nota -= 2
            comentarios.append(f"No hay commits en '{main_branch}' que modifiquen {frases_path}")
    except Exception:
        # Si la rama main/master no existe, penalizar fuerte
        nota -= 3
        comentarios.append("No existe rama principal 'main' ni 'master'")

    if branch_exists(remote_feature) and not file_modified_in_branch(remote_feature, frases_path):
        nota -= 2
        comentarios.append(f"No hay commits en 'feature/frase' que modifiquen {frases_path}")

    # 5) Comprobar que se ha fusionado feature/frase en la principal
    # 5.1) Que la principal contenga el tip de feature (merge o FF)
    contains = run_cmd(f"git merge-base --is-ancestor {remote_feature} {main_branch}")
    if contains.returncode != 0:
        nota -= 2
        comentarios.append(f"'{main_branch}' no contiene los cambios de 'feature/frase' (falta merge)")

    # 5.2) Idealmente, que exista un commit de merge en la principal
    if not has_merge_commit(main_branch):
        nota -= 1
        comentarios.append(f"No se detecta commit de fusión en '{main_branch}'")

    # 6) Comprobar que no quedan marcas de conflicto en frases.txt
    if os.path.exists(frases_path):
        with open(frases_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
            if any(marker in content for marker in ("<<<<<<<", "=======", ">>>>>>>")):
                nota -= 3
                comentarios.append("Marcas de conflicto presentes en 'tarea/frases.txt'")

    # 7) Comprobar que hay historia/commits en el repo
    commits_total = run_cmd("git log --oneline").stdout.strip()
    if commits_total == "":
        nota = 0
        comentarios.append("Repositorio sin commits (¿has hecho git push?)")

    # No bajar de 0
    nota = max(nota, 0)

    # Guardar CSV (P2)
    with open("resultados.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Usuario GitHub", "Practica", "Nota", "Comentarios"])
        writer.writerow([github_user, "P2", nota, "; ".join(comentarios) if comentarios else "Todo correcto"])


if __name__ == "__main__":
    main()

# 🚀 P02 – Git avanzado (branch, merge, conflictos)

## 🎯 Objetivo de la práctica
En esta práctica aprenderás a trabajar con **ramas en Git**, fusionar cambios entre ellas y resolver conflictos.  
Son habilidades clave para cualquier desarrollador que trabaje en equipo y quiera mantener un flujo de trabajo limpio y organizado.

> 📌 **Práctica individual**  

---

## 📚 Lo que vas a aprender
- Crear y gestionar ramas (`git branch`, `git checkout`, `git switch`).
- Fusionar ramas (`git merge`).
- Provocar y resolver conflictos.
- Buenas prácticas con ramas.

---

## 🛠 Pasos a seguir

### 1️⃣ Clonar el repositorio
Clona el repositorio asignado por **GitHub Classroom**:
```bash
git clone <URL-de-tu-repositorio>
cd <nombre-del-repo>
```

### 2️⃣ Crear una nueva rama
Crea una rama llamada `feature/frase` y cámbiate a ella:
```bash
git checkout -b feature/frase
```
> Esto crea la rama y te sitúa en ella.

### 3️⃣ Editar un archivo en la nueva rama
- Abre el archivo `frases.txt` incluido en la carpeta `tarea` del repositorio.
- Añade **una nueva línea** al final con una cita que te guste.
- Guarda los cambios.

Confirma los cambios:
```bash
git add tarea/frases.txt
git commit -m "Añadida nueva frase en feature/frase"
```

### 4️⃣ Cambiar a la rama principal y modificar el mismo archivo
Vuelve a la rama `master`:
```bash
git checkout master
```
- Edita **la misma línea** que acabas de añadir en `feature/frase`.
- Guarda y confirma:
```bash
git add tarea/frases.txt
git commit -m "Modificada frase en master"
```

### 5️⃣ Fusionar ramas y provocar un conflicto
Intenta fusionar `feature/frase` en `master`:
```bash
git merge feature/frase
```
Git detectará un **conflicto**.

### 6️⃣ Resolver el conflicto
- Abre `frases.txt` y localiza las marcas:
```
<<<<<<< HEAD
(versión en master)
=======
(versión en feature/frase)
>>>>>>> feature/frase
```
- Elimina las marcas (`<<<<<<<`, `=======`, `>>>>>>>`) y deja el texto final como quieras.
- Guarda y confirma:
```bash
git add tarea/frases.txt
git commit -m "Conflicto resuelto entre master y feature/frase"
```

### 7️⃣ Subir las ramas a GitHub
```bash
git push origin master
git push origin feature/frase
```

---

## ✅ Criterios de evaluación
Se comprobará que:
- [ ] Has creado la rama `feature/frase` correctamente.
- [ ] Has hecho al menos un commit en la rama `feature/frase`.
- [ ] Has editado el mismo archivo en `master` y `feature/frase` provocando un conflicto.
- [ ] Has resuelto el conflicto correctamente.
- [ ] Has subido **ambas ramas** a GitHub.
- [ ] El historial (`git log --graph --oneline --all`) refleja la fusión.

---

## 💡 Consejos
- Usa `git status` frecuentemente para conocer el estado de tu repositorio.
- Antes de resolver conflictos, lee bien las marcas que pone Git.
- Visualiza el historial con:
```bash
git log --graph --oneline --all
```
- No borres la rama `feature/frase` hasta que hayas subido todo.

---

## 📎 Recursos recomendados
- [Documentación oficial de Git](https://git-scm.com/doc)
- [Aprende Git con ejercicios interactivos](https://learngitbranching.js.org/?locale=es_ES)
- [Resolución de conflictos en GitHub Docs](https://docs.github.com/es/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/about-merge-conflicts)

---

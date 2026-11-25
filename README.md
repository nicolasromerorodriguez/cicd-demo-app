# Demo de CI/CD con FastAPI y Render

La página `/` muestra la versión (`APP_VERSION`) y los primeros siete caracteres del commit. `/health` devuelve `status`, `version` y el SHA completo en `commit`. Sin el argumento de construcción, `APP_COMMIT` vale `local`.

## Pruebas y ejecución local

Usa Python 3.12, la misma versión del workflow. Con ese intérprete disponible como `python`, ejecuta desde la raíz del clon:

```bash
python -m venv /tmp/cicd-entrega-py312
source /tmp/cicd-entrega-py312/bin/activate
python -m pip install --no-cache-dir -r requirements.txt
python -m pytest -v
APP_COMMIT=0123456789abcdef0123456789abcdef01234567 python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Desde otra terminal consulta `http://127.0.0.1:8000/` y `http://127.0.0.1:8000/health`. La portada debe mostrar `0123456` y `/health` debe devolver el SHA de 40 caracteres. Para verificar el contenedor con las mismas dos URL, detén Uvicorn con Ctrl+C y ejecuta:

```bash
docker build --platform linux/amd64 --build-arg APP_COMMIT=0123456789abcdef0123456789abcdef01234567 -t cicd-demo-app:demo .
docker run --rm -p 127.0.0.1:8000:8000 cicd-demo-app:demo
```

## Del push a la URL pública

1. Un push a `main` dispara **CI/CD Pipeline** y ejecuta pytest.
2. Docker construye una sola imagen `linux/amd64` con el SHA en `APP_COMMIT` y la publica en Docker Hub con las etiquetas del commit y `latest`.
3. GitHub Actions toma el digest devuelto por ese paso y envía al hook de Render `imgURL` con la referencia `docker.io/<usuario>/cicd-demo-app@sha256:<digest>`.
4. Tras la aceptación del hook, Actions consulta `/health` con reintentos durante un máximo de cinco minutos. Finaliza con éxito cuando `commit` coincide con el SHA del push. Si la versión anterior todavía responde HTTP 200 con otro commit, continúa esperando.

El SHA de Git identifica el commit y el digest identifica el contenido exacto de la imagen publicada.

## Activación en Render y GitHub

1. En Render, crea un **Web Service → Existing Image** con `docker.io/<usuario>/cicd-demo-app:latest`, usando el usuario del registro configurado en el workflow. La etiqueta inicial debe existir en Docker Hub. Si el repositorio es privado, configura en Render una credencial de lectura del registro. [Imágenes preconstruidas en Render](https://render.com/docs/deploying-an-image)
2. En los ajustes del nuevo servicio, copia su **Deploy Hook**. En GitHub, ve a **Settings → Secrets and variables → Actions**. En **Secrets**, actualiza `RENDER_DEPLOY_HOOK_URL` con el hook del nuevo servicio y conserva `DOCKERHUB_USERNAME` y `DOCKERHUB_TOKEN`. En **Variables**, crea `RENDER_APP_URL` con la URL base pública del nuevo servicio. [Hooks de Render](https://render.com/docs/deploy-hooks) · [Variables de GitHub Actions](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-variables)
3. Integra la rama de entrega en `main` y ensaya el flujo completo con un cambio visible.

**Servicio Existing Image** · [Portada](https://cicd-demo-app-2.onrender.com/) · [Estado y commit en /health](https://cicd-demo-app-2.onrender.com/health)

## Guion de la demostración en vivo

| Tiempo | Qué mostrar |
| --- | --- |
| 0:00–1:00 | En `app/main.py`, cambia el texto «Despliegue automatizado activo.» por «Entrega final verificada.». Las pruebas comprueban el encabezado «Plataforma Demo CI/CD». Haz `git add app/main.py`, `git commit -m "Actualiza texto de la demo"`, `git rev-parse HEAD` y `git push origin main` desde `main`. |
| 1:00–3:00 | Abre la ejecución automática en Actions y muestra la salida de pytest. |
| 3:00–5:00 | Muestra la construcción y publicación. Busca en Docker Hub la etiqueta del SHA y compara su digest con el que registra Actions. |
| 5:00–9:00 | Muestra la aceptación del hook y el despliegue en los eventos de Render mientras Actions comprueba `/health`. |
| 9:00–10:00 | Abre la URL nueva, comprueba el texto editado y el SHA corto. En `/health`, comprueba que `commit` coincide con `git rev-parse HEAD` y con el SHA de la ejecución. |

Si presentan dos personas, una puede cubrir Git y las pruebas y la otra Docker Hub, Render y la verificación. Con tres personas, la tercera puede encargarse de Render y la verificación. Los cinco minutos posteriores quedan para las preguntas.

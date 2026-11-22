import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="CI/CD Demo App")

APP_VERSION = os.getenv("APP_VERSION", "v1.0.0 - Base")


@app.get("/health")
def health():
    return {"status": "ok", "version": APP_VERSION}


@app.get("/", response_class=HTMLResponse)
def home():
    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8" />
      <title>Demo CI/CD</title>
      <style>
        body {{ font-family: Arial, sans-serif; max-width: 720px; margin: 60px auto; padding: 0 20px; }}
        .badge {{ display: inline-block; background: #eef2ff; color: #3730a3; padding: 6px 12px; border-radius: 6px; font-weight: bold; }}
        .card {{ border: 1px solid #e5e7eb; border-radius: 10px; padding: 24px; margin-top: 20px; }}
      </style>
    </head>
    <body>
      <h1>Plataforma Demo CI/CD</h1>
      <span class="badge">Versión actual: {APP_VERSION}</span>
      <div class="card">
        <p><strong>Estado:</strong> Despliegue automatizado activo.</p>
        <p>Edita este texto o <code>APP_VERSION</code>, haz <code>git push</code> y observa el pipeline.</p>
      </div>
    </body>
    </html>
    """
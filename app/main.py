import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="CI/CD Demo App")

APP_VERSION = os.getenv("APP_VERSION", "v2")
APP_COMMIT = os.getenv("APP_COMMIT", "local")

PIPELINE_STAGES = [
    {"step": "01", "name": "Commit y Push", "detail": "Disparo automático en la rama main"},
    {"step": "02", "name": "Pruebas con pytest", "detail": "Validación de endpoints y lógica antes de empaquetar"},
    {"step": "03", "name": "Imagen Inmutable", "detail": "Build en Docker y publicación por tag SHA y digest"},
    {"step": "04", "name": "Despliegue y /health", "detail": "Actualización en Render y verificación del commit"},
]


@app.get("/health")
def health():
    return {"status": "ok", "version": APP_VERSION, "commit": APP_COMMIT}


@app.get("/api/pipeline")
def pipeline_info():
    return {
        "service": "cicd-demo-app",
        "version": APP_VERSION,
        "commit": APP_COMMIT,
        "stages": PIPELINE_STAGES,
    }


@app.get("/", response_class=HTMLResponse)
def home():
    short_commit = APP_COMMIT[:7] if APP_COMMIT and APP_COMMIT != "local" else "local"
    stages_html = "\n".join(
        f"""
        <li>
          <span class="step-num">{stage["step"]}</span>
          <div>
            <strong>{stage["name"]}</strong>
            <span>{stage["detail"]}</span>
          </div>
        </li>
        """
        for stage in PIPELINE_STAGES
    )

    return f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      <title>Demo CI/CD</title>
      <style>
        :root {{
          --bg: #f8fafc;
          --surface: #ffffff;
          --text: #0f172a;
          --muted: #475569;
          --border: #e2e8f0;
          --accent: #1d4ed8;
          --accent-bg: #eff6ff;
          --ok-bg: #ecfdf5;
          --ok-text: #047857;
        }}
        * {{ box-sizing: border-box; }}
        body {{
          font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
          background: var(--bg);
          color: var(--text);
          max-width: 780px;
          margin: 48px auto;
          padding: 0 20px;
          line-height: 1.5;
        }}
        .header {{
          display: flex;
          flex-wrap: wrap;
          align-items: center;
          justify-content: space-between;
          gap: 12px;
          margin-bottom: 20px;
        }}
        h1 {{ margin: 0; font-size: 1.75rem; }}
        .subtitle {{ margin: 4px 0 0; color: var(--muted); }}
        .status-pill {{
          background: var(--ok-bg);
          color: var(--ok-text);
          padding: 6px 12px;
          border-radius: 999px;
          font-size: 0.875rem;
          font-weight: 600;
        }}
        .meta {{
          display: flex;
          flex-wrap: wrap;
          gap: 10px;
          margin-bottom: 20px;
        }}
        .badge {{
          background: var(--accent-bg);
          color: var(--accent);
          padding: 6px 12px;
          border-radius: 8px;
          font-size: 0.9rem;
          font-weight: 600;
        }}
        code {{
          background: #f1f5f9;
          padding: 2px 6px;
          border-radius: 5px;
          font-size: 0.9em;
        }}
        .card {{
          background: var(--surface);
          border: 1px solid var(--border);
          border-radius: 12px;
          padding: 24px;
          box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
        }}
        .card h2 {{
          margin: 0 0 14px;
          font-size: 1.1rem;
        }}
        .stage-list {{
          list-style: none;
          padding: 0;
          margin: 0;
          display: grid;
          gap: 12px;
        }}
        .stage-list li {{
          display: flex;
          align-items: flex-start;
          gap: 12px;
          padding: 12px;
          border: 1px solid var(--border);
          border-radius: 10px;
          background: var(--bg);
        }}
        .step-num {{
          background: var(--accent);
          color: #ffffff;
          font-weight: 700;
          font-size: 0.8rem;
          padding: 4px 8px;
          border-radius: 6px;
          margin-top: 2px;
        }}
        .stage-list strong {{ display: block; font-size: 0.95rem; }}
        .stage-list span {{ color: var(--muted); font-size: 0.875rem; }}
        .footer {{
          margin-top: 18px;
          display: flex;
          gap: 16px;
          font-size: 0.9rem;
        }}
        a {{ color: var(--accent); text-decoration: none; font-weight: 600; }}
        a:hover {{ text-decoration: underline; }}
      </style>
    </head>
    <body>
      <div class="header">
        <div>
          <h1>Plataforma Demo CI/CD</h1>
          <p class="subtitle">Servicio web contenedorizado con entrega continua y trazabilidad por commit.</p>
        </div>
        <span class="status-pill">Servicio activo</span>
      </div>

      <div class="meta">
        <span class="badge">Versión: {APP_VERSION}</span>
        <span class="badge">Commit: <code>{short_commit}</code></span>
      </div>

      <div class="card">
        <h2>Etapas del flujo automatizado</h2>
        <ul class="stage-list">
          {stages_html}
        </ul>
        <div class="footer">
          <a href="/health">Ver /health</a>
          <a href="/api/pipeline">Ver /api/pipeline</a>
        </div>
      </div>
    </body>
    </html>
    """
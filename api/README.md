# KundliKosh API

Thin FastAPI HTTP wrapper around the engine. Designed for **free-tier** deployment.

## Local run

```bash
pip install -e ../engine
pip install 'fastapi>=0.110' 'uvicorn[standard]>=0.29'
PYTHONPATH=../engine uvicorn app:app --reload --port 8000
```

Then open http://localhost:8000/docs for the interactive Swagger UI.

## Endpoints

| Method | Path             | Purpose                              |
|--------|------------------|--------------------------------------|
| POST   | `/chart`         | full natal chart                     |
| POST   | `/dasha`         | current + upcoming Vimshottari       |
| POST   | `/yogas`         | yogas + doshas                       |
| POST   | `/varga`         | divisional chart (D9/D10/D7/D3/D12)  |
| POST   | `/compatibility` | Ashtakoot Guna Milan + Manglik       |
| GET    | `/health`        | liveness probe                       |

Sample request:

```json
POST /chart
{
  "name": "Vandana",
  "date": "2003-12-08",
  "time": "13:30",
  "timezone": "Asia/Kolkata",
  "latitude": 21.1702,
  "longitude": 72.8311
}
```

## Deployment options (free tier)

| Provider          | Free quota                           | Cold start | Notes |
|-------------------|--------------------------------------|------------|-------|
| **Render**        | 750 hrs/mo (sleeps after 15 min idle)| ~30 s      | Easiest. Connect repo, point at `api/` |
| **Fly.io**        | 3 small VMs always-on                | ~5 s       | Best perf if you keep within limits |
| **HF Spaces**     | unlimited public                      | ~10 s      | Public — fine for a public engine API |
| **Railway**       | $5 credit/mo                          | none       | Almost free for this workload |

We'll deploy to Render for v1 because the cold-start is acceptable for a daily-use app.

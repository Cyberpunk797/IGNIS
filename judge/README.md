# Ignis Judge (Server-Side)

This service provides LeetCode-style compilation and execution on a server. It runs untrusted code inside Docker
containers (no network, resource limits, read-only rootfs).

## Requirements (Judge Host)

- Docker installed and runnable by the judge process
- Python 3.10+

## Run

```bash
cd axlu-zesi-cp
pip install -r judge/requirements.txt

# Optional but strongly recommended (protects your judge)
export JUDGE_API_KEY="change-me"

uvicorn judge.server:app --host 0.0.0.0 --port 8000
```

## Environment

- `JUDGE_API_KEY`: if set, clients must send header `X-Api-Key: <value>`
- `JUDGE_DOCKER_IMAGE`: defaults to `gcc:13`

## Endpoints

- `GET /health`
- `POST /compile`
- `POST /run`

## Security Notes

- Do not expose this service publicly without auth and network controls.
- Consider running behind a reverse proxy with rate limiting.

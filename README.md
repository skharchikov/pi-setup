# pi-setup

Single source of truth for Raspberry Pi homelab Docker services. Tracked in Git, deployed via Portainer Git Stacks.

## Host

- Raspberry Pi (Debian Bookworm, ARM64)

## Services

| Dir | Containers | Port | Notes |
|-----|------------|------|-------|
| `adguard/` | adguardhome | 53 (DNS) | Runtime data in `adguard/{confdir,workdir}/` (gitignored) |
| `greeter/` | greeter-greeting_api | 5050 | Flask API, built locally from `Dockerfile` |
| `monitoring/` | grafana, prometheus, cadvisor, node-exporter | 3000 (Grafana) | Provisioning in `monitoring/grafana/provisioning/` |
| `openclaw/` | openclaw-gateway | 18789 | Built locally from `Dockerfile` |
| `portainer/` | portainer | 9000 | Self-hosted; data at `/opt/portainer` (host bind) |

## Bootstrap fresh Pi

```bash
git clone https://github.com/skharchikov/pi-setup.git ~/pi-setup
cd ~/pi-setup

# Seed env files per service
cp greeter/.env.example greeter/.env             && $EDITOR greeter/.env
cp openclaw/.env.example openclaw/.env           && $EDITOR openclaw/.env
cp monitoring/grafana/.env.example monitoring/grafana/.env && $EDITOR monitoring/grafana/.env

# Bring up each stack
for svc in adguard greeter monitoring openclaw portainer; do
  (cd "$svc" && docker compose up -d)
done
```

## Secrets

`.env` files are gitignored. Templates committed as `.env.example`:

| Service | Required vars |
|---------|---------------|
| `greeter` | `OPENROUTER_API_KEY` |
| `openclaw` | `OPENAI_API_KEY`, `OPENCLAW_GATEWAY_TOKEN`, runtime vars |
| `monitoring/grafana` | `GF_SECURITY_ADMIN_USER`, `GF_SECURITY_ADMIN_PASSWORD`, paths |

Also gitignored:
- `adguard/{confdir,workdir}/` — AdGuard runtime data
- `monitoring/{grafana,prometheus}/data/` — TSDB + Grafana DB

## Deployment (Portainer Git Stacks)

Each service is registered as a Git-backed stack in Portainer:

1. Portainer UI → **Stacks → Add stack**
2. Build method: **Repository**
3. URL: this repo, ref: `refs/heads/main`
4. Compose path: `<service>/docker-compose.yaml` (or `.yml`)
5. Auth: PAT with `repo` scope — stored once in Portainer Git credentials
6. GitOps updates: enable polling (e.g. 5m), enable re-pull image
7. Environment variables: paste from local `.env` (or upload via UI)

Push to `main` → Portainer pulls within polling window → redeploys changed stacks.

## Layout

```
adguard/        DNS filter
greeter/        Greeting API (Python/Flask)
monitoring/     Grafana + Prometheus + exporters
openclaw/       OpenClaw gateway
portainer/      Container management UI
```

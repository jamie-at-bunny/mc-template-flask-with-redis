# Flask KV API with Redis for Magic Containers

A minimal Flask key-value API backed by Redis, ready to deploy on [Bunny Magic Containers](https://bunny.net/magic-containers/).

## What's included

- `app.py` - Flask server with `GET`, `PUT`, and `DELETE` endpoints for key-value storage
- `Dockerfile` - Slim Python image with Gunicorn
- `docker-compose.yml` - Local development setup with Redis
- `bunny.json` - Magic Containers app config with both `app` and `redis` containers
- `.github/workflows/deploy.yml` - GitHub Actions workflow to build, push to GitHub Container Registry, and deploy to Magic Containers

## Run locally

```bash
docker compose up
```

```bash
# Set a value
curl -X PUT http://localhost:8000/kv/greeting -d '{"value": "Hello world"}' -H "Content-Type: application/json"
# {"key":"greeting","value":"Hello world"}

# Get a value
curl http://localhost:8000/kv/greeting
# {"key":"greeting","value":"Hello world"}

# Delete a value
curl -X DELETE http://localhost:8000/kv/greeting
```

## Deploy to Magic Containers

This template uses **multiple containers**: an `app` container for the Flask API and a `redis` container for data storage. Magic Containers runs both containers together in the same app, and they communicate over an internal network.

### 1. Fork and push

Fork this repository and push to the `main` branch. The GitHub Actions workflow will automatically build the Docker image and push it to `ghcr.io/<your-username>/mc-template-flask-with-redis` tagged with both `latest` and the commit SHA.

### 2. Make the package public

Go to your GitHub profile → **Packages** → select the `mc-template-flask-with-redis` package → **Package settings** → change visibility to **Public**.

### 3. Create an app on Magic Containers

1. Log in to the [bunny.net dashboard](https://dash.bunny.net) and navigate to **Magic Containers**.
2. Click **Create App**.
3. Add the **app** container:
   - **Registry**: GitHub Container Registry (`ghcr.io`)
   - **Image**: `ghcr.io/<your-username>/mc-template-flask-with-redis:latest`
   - **Environment variable**: `REDIS_URL` = `redis://redis:6379`
   - Add an **Endpoint** on port `8000`
4. Add the **redis** container:
   - **Registry**: Docker Hub
   - **Image**: `redis:7-alpine`
   - Add a **Persistent Volume** mounted at `/data` (this keeps your data across restarts)
5. Confirm and deploy.

Containers within the same app can reach each other by name — the `app` container connects to `redis:6379` using the `REDIS_URL` environment variable.

### 4. Test it

Once deployed, you'll get a `*.bunny.run` URL:

```bash
curl -X PUT https://mc-xxx.bunny.run/kv/greeting -d '{"value": "Hello from Magic Containers"}' -H "Content-Type: application/json"
curl https://mc-xxx.bunny.run/kv/greeting
```

## Continuous deployment

The workflow automatically deploys to Magic Containers on every push to `main`. Configure the following in your repository settings:

- **Variable** `APP_ID` — your Magic Containers app ID
- **Secret** `BUNNYNET_API_KEY` — your bunny.net API key

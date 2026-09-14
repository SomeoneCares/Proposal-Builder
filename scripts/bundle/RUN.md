# Running the Proposal Builder

Needs a Linux host (or Docker Desktop on Windows/macOS) with Docker Engine and the
Compose plugin. No Python, LibreOffice or internet access is needed on the host:
everything is inside the image.

## Start

```bash
tar -xzf proposal-builder-<tag>.tar.gz
cd proposal-builder-<tag>
./start.sh
```

`start.sh` creates `.env` on the first run with a random Module Library editor password
(printed once, kept in `.env`), loads the image and starts the container. Open
`http://<host>:8501`.

## Settings (`.env`)

| Setting | Meaning |
| --- | --- |
| `PROPOSAL_EDITOR_PASSWORD` | Module Library editor password; empty disables editing |
| `PROPOSAL_BUILDER_BIND`, `PROPOSAL_BUILDER_PORT` | Listen address and port (use `127.0.0.1` behind a reverse proxy) |
| `HERMES_API_URL`, `HERMES_API_KEY` | Optional customer research through a Hermes API server; empty switches it off |

After changing `.env`, run `docker compose up -d` again.

## Upgrade

Unpack the new bundle, copy the old `.env` into the new folder and run `./start.sh`.
Module Library edits live in the Docker volume `<folder>_library` and are kept. If
the new folder has a different name, keep using the old folder's name with
`docker compose -p <old-folder-name> up -d` so the same volume is used.

## Everyday commands

```bash
docker compose ps            # status and health
docker compose logs -f       # logs
docker compose down          # stop (the library volume is kept)
```

## Back up the Module Library

```bash
docker run --rm -v "$(basename "$PWD")_library:/data" -v "$PWD:/backup" busybox \
  tar -czf /backup/library-$(date +%F).tar.gz -C /data .
```

To bring edits from another server, unpack such an archive into the volume the same
way (`tar -xzf ... -C /data`) and restart. Files must be owned by uid 10001:
`docker run --rm -v "$(basename "$PWD")_library:/data" busybox chown -R 10001:10001 /data`.

## HTTPS

The builder speaks plain HTTP. On a shared network, put it behind a reverse proxy
with a certificate (for example nginx or Caddy) and set `PROPOSAL_BUILDER_BIND=127.0.0.1`.
The proxy must pass WebSocket upgrades (Streamlit uses them).

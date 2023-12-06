# DreamLink Web Server

This is the source code for the official DreamLink web server.

## Running locally:

  1. Clone the repository.
  2. Inside the repository, run: `poetry install --no-root` (assuming poetry is installed).
  3. Enter the virtualenv: `poetry shell` or `source .venv/bin/activate`.
  3. Inspect `dreamlink/config.py` to determine environment variables to set.
  4. Start the application by running: `sanic dreamlink`.

You can configure your DreamLink application to point to an alternate/local nexus by creating or amending `~/.config/dreamlink/config.json` and adding the `nexus.root` key. This application serves the nexus on the path `/nexus`. Thus, if running locally on port `8000`, the value should be: `http://localhost:8000/nexus`.
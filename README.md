# DreamLink Web Server

<div align="center">
    <img src="splash.png">
</div>

This is the source code for the official DreamLink web server. We require the following system dependencies:

  1. `jq`
  2. `postgresql`
  3. `bun`

## Installation & Setup

Install dependencies using:

```bash
bun install
```

Create an environment file (`env.json`) in the root directory containing:

```json
{
    "databaseURL": "xxx",
    "jwtSecret" : "xxx",
    "port": xxx
}
```

Generate the initial DB types:

```bash
bun kysely-codegen --url $(cat env.json | jq -r .databaseURL)
```

Migrate the database and regenerate  DB types:

```bash
bun migrate.ts
bun kysely-codegen --url $(cat env.json | jq -r .databaseURL)
```

## Running the server

Run using:

```bash
bun server.ts
```
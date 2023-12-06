from os import environ

default_title = "Dreamlink"
responsive_breakpoint = 840
secure_cookies = False

max_db_connections = int(environ.get("MAX_DB_CONNECTIONS", "10"))
database_url = environ["DATABASE_URL"]
staging_path = environ.get("STAGING_PATH", "staging/")
zones_path = environ.get("LEVELS_PATH", "zones/")
jwt_secret = environ.get("JWT_SECRET", "")
invite_code_required = environ.get("INVITE_CODE_REQUIRED", "true").lower() == "true"
store_strategy = environ.get("STORE_STRATEGY", "local")
store_s3_bucket_name = environ.get("STORE_S3_BUCKET_NAME")

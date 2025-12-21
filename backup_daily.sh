

set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-/Users/apple/Desktop/project/backups}"
DSN="${GOST_DSN:-dbname=gostitut user=apple host=localhost port=5432}"
TS="$(date +%Y%m%d_%H%M%S)"
FILE="$BACKUP_DIR/gostitut_$TS.dump"

mkdir -p "$BACKUP_DIR"

echo "[backup] $(date) starting dump -> $FILE"
/usr/local/opt/postgresql@17/bin/pg_dump --format=custom --file="$FILE" --dbname="$DSN"

find "$BACKUP_DIR" -type f -name 'gostitut_*.dump' -mtime +14 -print -delete

echo "[backup] $(date) done"


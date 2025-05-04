set -ex

script_dir_path=$(dirname "${BASH_SOURCE[0]}")
base_path="$script_dir_path/.."
$base_path/.venv/bin/alembic -c $base_path/app/db/alembic/alembic.ini upgrade head

$base_path/.venv/bin/fastapi run $base_path/app/main.py --port 8080
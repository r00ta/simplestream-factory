# FastAPI + SQLAlchemy microservice template

This is r00ta's microservice template using uv, FastAPI and SQLAlchemy.  

## init 

Install uv, then 

```commandline
uv sync
```

## Add a new alembic migration

```commandline
uv run alembic -c app/db/alembic/alembic.in revision --autogenerate -m "new migration"
```

## Apply migrations

```commandline
uv run alembic -c app/db/alembic/alembic.ini upgrade head
```

## Run 

```commandline
uv run fastapi run app/main.py --port 8080 --host 0.0.0.0
```

## License

MIT

<div align="center">
  <a target="_blank" href="https://astral.sh" style="background:none">
    <img src="https://raw.githubusercontent.com/astral-sh/uv/main/assets/svg/Astral.svg" alt="Made by Astral">
  </a>
</div>

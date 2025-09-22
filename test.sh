#!\bin\bash
docker compose exec qa_app pytest -v --disable-warnings --maxfail=1
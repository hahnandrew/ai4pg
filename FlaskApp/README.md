# Flask backend

Python 3.11.5
## Install
```sh
# windows
cd FlaskApp
pip install --verbose  -r .\requirements.txt --target .\site-packages\windows --upgrade

# linux
cd FlaskApp
pip install --verbose  -r .\requirements.txt --target .\site-packages\darwin --upgrade
```

## Run
* set env vars
### Windows
```ps1
cd Env:
Set-Content -Path  FLASK_BACKEND_ENV -Value "DEV"
Set-Content -Path  SQLALCHEMY_POSTGRESSQL_0_CONN_STRING -Value "postgresql://postgres:q9T2Lb1BSt3T76b@db.izbpqvbzdqgydzeekyxz.supabase.co:5432/postgres"
Set-Content -Path  OPENAI_API_KEY_0 -Value "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"


cd C:\Users\Restop-8192\My_Apps\AI-for-pg\project\FlaskApp

python app.py
```

### Mac OS
```
cd FlaskApp
export FLASK_BACKEND_ENV=DEV
export SQLALCHEMY_POSTGRESSQL_0_CONN_STRING=postgresql://postgres:q9T2Lb1BSt3T76b@db.izbpqvbzdqgydzeekyxz.supabase.co:5432/postgres

export OPENAI_API_KEY_0=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
python app.py
```

# Postgres DB
* host supabase
## Info
* pass :  C(^wykR8r9c[3O}
  url  :   db.izbpqvbzdqgydzeekyxz.supabase.co
  db      : postgres
  username: postgres
  port : 5432

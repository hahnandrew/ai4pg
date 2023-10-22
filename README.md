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
cd [path prefix]\AI-for-pg\project\FlaskApp

python app.py
```

### Mac OS
```
cd FlaskApp
export FLASK_BACKEND_ENV=DEV
python app.py
```

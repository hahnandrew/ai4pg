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
```
cd Env:
Set-Content -Path  FLASK_BACKEND_ENV -Value "DEV" 
cd C:\Users\Restop-8192\My_Apps\AI-for-pg\project\FlaskApp

python app.py
```

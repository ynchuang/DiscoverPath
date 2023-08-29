## Modeling Modules

### Env.
```
virtualenv -p python3 venv
. ./venv/bin/activate
pip install -r requirements.txt
mkdir data
```

### Testing Dataset
```
- Please download the data from the following link
- Move all of the following data files in the folder "data"

https://drive.google.com/file/d/1QKWRGjpgZiKTe0RZkNjoKle1T3mt6zi1/view?usp=share_link
https://drive.google.com/file/d/1nyXc1iIGHLwbuA4Cv7zKGabye-f2EoUc/view?usp=sharing
https://drive.google.com/file/d/1KbnXqeaLSqRa_uUjOpCVb6uJbpYe0wZi/view?usp=sharing

- Move all of the following data files in the folder "rec_data"
https://drive.google.com/drive/folders/1DwT_TlPjkEsOUjP95916D3l2ZI9DE_E2?usp=sharing
```

### Modeler

### Server
test with basic functionality
```
python ./sever/flask_serve.py --data [Data-File-Folder] --rec_data [Rec-Data-File-Folder]
```

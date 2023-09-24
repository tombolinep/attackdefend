# attackdefend

cd C:\Users\peter\IdealProjects\attackdefend\src

copy and paste to copy 1 liner:

pyinstaller --name=dobnob --add-data "assets;assets" --add-data "controller;controller" --add-data "events;events"
--add-data "model;model" --add-data "view;view" --add-data "assets/images;assets/images" --add-data "
assets/original_images;assets/original_images" --add-data "assets/sounds;assets/sounds" --add-data "
model/enemy;model/enemy" --add-data "constants.py;." --add-data "utils.py;." --console main.py

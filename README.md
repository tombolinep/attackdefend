# Space Jungle
![Alt Text](https://github.com/tombolinep/attackdefend/blob/main/src/assets/screenshots/Screenshot%202024-03-24%20175346.png)

# Upgrades!
![Alt Text](https://github.com/tombolinep/attackdefend/blob/main/src/assets/screenshots/Screenshot%202024-03-24%20175408.png)


## Dev notes
cd C:\Users\peter\IdealProjects\attackdefend\src

copy and paste to copy 1 liner:

pyinstaller --name=spacejungle --add-data "assets;assets" --add-data "controller;controller" --add-data "events;events"
--add-data "model;model" --add-data "view;view" --add-data "assets/images;assets/images" --add-data "
assets/original_images;assets/original_images" --add-data "assets/sounds;assets/sounds" --add-data "
model/enemy;model/enemy" --add-data "constants.py;." --add-data "utils.py;." main.py


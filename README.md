# attackdefend

cd C:\Users\peter\IdealProjects\attackdefend\src

pyinstaller --name=dobnob --add-data "assets;assets" --add-data "controller;controller" --add-data "events;events"
--add-data "model;model" --add-data "view;view" --add-data "assets\images;assets\images" --add-data "
assets\original_images;assets\original_images" --add-data "assets\sounds;assets\sounds" --add-data "
model\enemy;model\enemy" --console main.py

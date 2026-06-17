#!/bin/bash
python3 -mvenv ../pythonvenv
source ../pythonvenv/bin/activate
pip3 install opencv-python numpy mediapipe pygame

echo "Téléchargement du modèle MediaPipe Pose..."
wget -q --show-progress \
  -O assets/pose_landmarker_lite.task \
  "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task"
echo "Modèle téléchargé."

python3 main.py

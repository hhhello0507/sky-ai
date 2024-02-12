import os

appdata_path = os.getenv('APPDATA')
app_folder_path = os.path.join(appdata_path, 'skyai')
model_folder_path = os.path.join(app_folder_path, 'models')
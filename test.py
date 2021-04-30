import os
print(os.path.abspath(r'United_school-master\client\pdf'))
print(os.path.abspath(os.path.dirname(__file__)))
print(current_app.root_path)
filename='Google_Stock_Price_Test.csv'
print(os.path.join(os.path.abspath(os.path.dirname(__file__)),r'static\uploads',filename))
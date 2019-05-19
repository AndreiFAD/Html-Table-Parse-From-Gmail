# Html table read from Gmail
#### It reads HTML table from Gmail and after reading, changes the label on email<br><br>

#### If you receive data in your email body that you want to read<br>
Create two label in Gmail<br>
example "input" and "output"<br>
<img width="230" alt="Képernyőfotó 2019-05-18 - 20 21 02" src="https://user-images.githubusercontent.com/24839474/57973713-8d64b000-79ad-11e9-8f05-df21596e3406.png"><br>
and create rule for label “input” in order to get the emails under that label<br>
After the process it changes the label to “output”<br><br>
#### From this email:<br>
<img width="519" alt="Képernyőfotó 2019-05-18 - 20 18 44" src="https://user-images.githubusercontent.com/24839474/57973717-95245480-79ad-11e9-94fd-5d91fe454639.png"><br><br>
#### the script read this:<br>
<img width="670" alt="image" src="https://user-images.githubusercontent.com/24839474/57973733-ce5cc480-79ad-11e9-948f-91d9071a81ed.png"><br><br>
#### In config.json file you can configurate your login data and labels name<br>
After that you can do anything with data, example import to database or save it.<br><br>

#### If you want to build .exe use setup.py. Run this command in terminal:<br>
$ python setup.py build<br><br>

#### create task in windows Task Scheduler<br>
create run.bat file and add this line:<br>
start /d "//fullpath/Gmail_Tables_Read" Gmail_Tables_Read.exe<br>

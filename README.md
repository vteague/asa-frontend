# asa-frontend
Here are the steps to run this application:
1.  make sure python3 is available on your machine and the pip3 command works.
2.  download the code of aus-senate-audit from https://github.com/berjc/aus-senate-audit
3.  use command "pip3 install aus-senate-audit" on the terminal to install aus-senate-audit
4.  use command "pip3 install git+https://github.com/QingqianYang/dividebatur.git@master" to install dividebatur because the original dividebatur has bug and this is the debugged version
5.  make sure flask module is installed by using "pip3 install flask"
6.  check if module itsdangerous and Jinja2 is installed by using command "pip3 install xxx" separately
7.  download the Werkzeug module from https://pypi.python.org/pypi/Werkzeug
8.  make sure flask_login is installed by using "pip3 install flask_login"
9.  make sure mysql is install and the password for the root of mysql has been set
10.  change the null to the password that you have for mysql in App.py's "app.config['MYSQL_DATABASE_PASSWORD'] = ''"
11. use command "mysql -uroot -p'here is your password'<'path to the file schema.sql under the folder /scripts'" to build the database
12. use command "pip3 install flask-mysql"
13. download module from https://pypi.python.org/pypi/Flask-Table/ and cd to the path that contains the module package and use command "pip3 install flask_table"
14. use command "pip3 install flask_security" to install flask_security
15. change the path of the variable "UPLOAD_FOLDER","DATA_DIR" and "OUTPUT_DIR" to your own path and put the audit data (e.g Australian senate election data) in the directory of the variable "DATA_DIR"
16. cd to the path of the asa-frontend and then use command "python3 App.py" to run on terminal and open the link that shows on the terminal

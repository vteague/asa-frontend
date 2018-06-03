# asa-frontend
This readme is based on the **macOS** system and the ASAfront system is built on **Python 3.6.4**. Here are the steps to run this application:
1. make sure **python3** is available on your machine and the **pip3** command works.
2. make sure **mysql** is install and the **password** for the root of mysql has been set
3. Change your **database user name** or **password** in the config file
4. use **command** "mysql -uroot -p'here is your password'<'path to the file schema.sql under the folder /migrations'" to build the database
5. use **command** "mysql -uroot -p'here is your password'<'path to the file 2018_5_27_create_samplers_table.sql under the folder /migrations'" to create a new table
6. **Download** the Australian senate election data from https://drive.google.com/file/d/0B2FYEn1taR3dMTVGWThtbDJuLVk/view and put the unzipped files from the data folder to data/original, for example,~/data/original/vic
7. **Download** the code of aus-senate-audit from https://github.com/berjc/aus-senate-audit
8. use **command** "pip3 install aus-senate-audit" on the terminal to install aus-senate-audit
9. use **command** "pip3 install git+https://github.com/QingqianYang/dividebatur.git@master" to install dividebatur because the original dividebatur has bug and this is the debugged version
10. use **command** "pip3 install virtualenv" to install the package for virtual environment
11. **cd** to the path of the project and then use **command** "virtualenv venv" to build a folder for virtual environment
13. if you are using the **IDE Pycharm**, you can go to Preferences-> Project: your folder name -> Project Interpreter and then choose the virtual environment that you newly build(e.g. 3.6.4 virtualenv at ~/PycharmProjects/ASAfront/venv). Then open a new terminal page and there will be a “(venv)” for the prompt
14. if you are using **command line**, use **command** "source venv/bin/activate" to activate the virtual environment
15. use **command** "pip3 install -r requirements.txt" to install all other modules
16. use **command** "python3 manage.py runserver" to run the system and then visit http://127.0.0.1:5000/

**Tips: As Flask supports python3 in an unpleasant way, if the pip3 command does not work for installation, you can try pip command instead**

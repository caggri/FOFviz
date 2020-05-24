# FOFviz: Flow of Funds Analysis System
FOFViz is an senior year project. FOFviz is a web-based user friendly solution
for macroeconomic data visualization and
financial forecasting

Instructor: Asst. Prof. Seyid Amjad Ali

# Running the project

* You need Python 3 to run the project.

* It is highly recommended to use a Python Virtual Environment.
* Make sure you have Python 3, pip and Virtual Environment. Make sure you have downloaded Python > 3.4, pip is bundled with newer versions. 

* If you don't have Python 3, pip, Virtual Environment do following steps.

  1. Check your Python version
      * for Windows by typing
          ```
          python --version
          ```  
      * for UNIX-Like Operation Systems (Mac OS X / OS X / macOS / GNU Linux Distributions) by typing
          ```
          python3 --version
          ```
      * If you don't have Python 3
         * Python 3 can be downloaded from
             ```
             https://www.python.org/
             ```

  2. Installation of  Virtual Environment
      * for Windows by typing
          ```
          py -m pip install --upgrade pip
          ```  
      * for UNIX-Like Operation Systems by typing
          ```
          python3 -m pip install --user --upgrade pip  
          ```


* To create and start a Virtual Environment
  * Create a Virtual Environment by typing
     ```
     python3 -m venv virtual_environment_name
     ```
     This command will create a folder with the given name.

  * Starting Virtual Environment
    * for Windows by typing
        ```
        project-env\Scripts\activate.bat
        ```  
    * for UNIX-Like Operation Systems by typing
        ```
       source project-env/bin/activate
        ```
    
    * Virtual environment is started if you see name of virtual environment's name inside parentheses 
    
* All project dependencies listed in reqs.txt file.
    * to install dependencies, type
        ```
        pip install -r reqs.txt
        ```  
        This command will install all dependencies automatically.


Before starting project needs a model migration. Make migration by typing:

```
python manage.py migrate
```


Installation process completed, now you can run the project by typing:

```
python manage.py runserver
```
  
* Virtual Environment can be deactivated by typing,
```
deactivate
```


# Museum Dating

Our application intends to propose cultural dates that you can enjoy in solo, or even share them with whoever you would like! Based on the layout of Tinder, this time you're not matching with somebody but with something. This thing is the exhibited item that you'll visit inside one of the museums in the city of Ghent.


## Installation

Install all the packages needed for the entire project.
The packages can be installed in a pip environment with

### Python environment
```bash
  python3 -m venv bds_project python==3.8.12
  bds_project/bin/pip install -r src/pip_requirements.txt
```

### PySpark

#### Spark
Download and unzip Apache Spark version 3.3.2, pre-built for hadoop version 2.7 using this [link](https://www.apache.org/dyn/closer.lua/spark/spark-3.3.2/spark-3.3.2-bin-hadoop2.tgz)

Configure new environment variable:
```
SPARK_HOME -> C:\$path_to_folder\spark\spark-3.3.2-bin-hadoop2
```
#### Java
Download and install JDK using this [link](https://www.oracle.com/in/java/technologies/downloads/#jdk20-windows)

Configure new environment variable:
```
JAVA_HOME -> C:\$path_to_folder\java
```

#### Hadoop
Download and install winutils.exe for the corresponding hadoop version (in our case 2.7.*) using this [link](https://github.com/steveloughran/winutils/tree/master/hadoop-2.7.1/bin), then place it in the correct folder as such
```
C:\$path_to_folder\hadoop\bin\winutils.exe
```

Configure new environment variable:
```
HADOOP_HOME -> C:\$path_to_folder\hadoop
```

#### System PATH variable
You also need to add the following paths to your PATH variable:
```
%SPARK_HOME%\bin
%HADOOP_HOME%\bin
%JAVA_HOME%\bin
```

### Image datasets
For deployement reason, the objects' images used to render the application are not integrated inside the repository. Thus, we still need to realize those last steps to run the application as intended:

    1. Download all the images-* folders from this link: https://cloud.ilabt.imec.be/index.php/s/Tircbrpgoco5K8K
    
    2. Include the folders inside the ./staticFiles/img/ folder following the pattern:
        - Folder images-<name>.zip need to be unzip in ./staticFiles/img/<name>

So if each step were followed, we should have 5 folders nested in ./staticFiles/img/ looking like this: 

    --- ./staticFiles/img/
     |-- design
     |-- alijn
     |-- archief
     |-- industrie
     |-- stam


## Tech Stack

**Frontend:** HTML, JS, CSS

**Backend:** Flask

**Work on the data:** PySpark, Pandas


## Authors
- [@ItsKhaled](https://www.github.com/ItsKhaled)
- [@thib-info](https://www.github.com/thib-info)

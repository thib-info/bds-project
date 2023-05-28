
# Museum Dating

Our application intend to propose cultural date that you can enjoy in solo or share with someone. Based on the layout of Tinder, this time you're not matching with somebody but with something. And this something is the object that you'll visit inside one of the museum of Ghent city.


## Installation

Install all the packages needed for the entire project.
The packages can be installed in a pip environment with

```bash
  python3 -m venv bds_project python==3.8.12
  bds_project/bin/pip install -r src/pip_requirements.txt
```

For deployement reason, the objects' images used to render the application are not integrated inside the repository. Thus, we still need to realize those last steps to run the application as intended:

    1. Download all the images-* folders from the link: https://cloud.ilabt.imec.be/index.php/s/Tircbrpgoco5K8K
    
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

**Work on the data:** SparQL


## Authors

- [@thib-info](https://www.github.com/thib-info)
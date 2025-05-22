# data_prep_and_clean
Data Preparation and Cleaning 2025

## Goals
In the foreground, it is not exclusively the correct completion of the missing modules, 
but rather the definition of suitable experiments to determine dependencies and rules with regard to different configurations.

## Preliminaries
To complete the tasks, you should checkout this project. 
This contains the code skeleton and data sets for using the record linkage system.
You should integrate the modules and data sets into your Python project.

Before implementation, you should familiarize yourself with the individual modules and the structure for the various tasks.
For a more detailed understanding, you can run ```recordLinkage.py```. It uses the provided data records and already implemented functions. 
This makes the output of the different modules comprehensible. To test the program for correctness, 
it is recommended to use the data records without impurities, the 
```clean-A-1000.csv``` and ```clean-B-1000.csv``` that can be found in the ```datasets``` folder. The other data records can then be used.


## Structure

```plaintext
├── 📁 data
|   ├── 📃 load_dataset.py     <-- Loads dataset for linkage.
│
├── 📁 blocking
│   ├── 📃 blocking.py     <-- Blocking schemes
│   ├── 📃 blocking_functions.py     <-- Blocking functions
│   └── 📁 blocking_key_selection    <-- Automatic blocking key selection
│
├── 📁 classification
|   ├── 📃 threshold_classification.py  <-- Threshold-based classification methods
│   └──📁 machine_learning
|       ├── 📃 util.py              <-- Generate k-folds for a set of similarity feature vectors
│       ├── 📃 supervised.py        <-- Model training & prediction
│       └── 📃 active_learning.py   <-- training data selection & model training
│
├── 📁 comparisons
│   ├── 📃 comparison.py            <-- Compare records in blocks
|   └── 📃 comparison.py            <-- string similarity functions
│
├── 📁 evaluation
│   └── 📃 evaluation.py            <-- Quality & Efficiency metrics
│   
├── 📁 datasets
├── 📃 record_linkage              <-- Main program consisting of the whole pipeline
├── 📃 requirements.txt            <-- Dependencies and libraries.
└── 📃 README.md                   <-- Project documentation.
```



## Tasks
1. Blocking
2. Comparsion
3. Classification
4. Evaluation

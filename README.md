# Coral (c-core)

## Overview

Coral is a tool for analyzing proteomics data. It provides functionalities for data preprocessing, normalization, imputation, and statistical analysis using the `limma` package in R.

## Docker Image Build

### Building Your Own Docker Image

Building your own Docker image is optional. You can use the pre-built image from Docker Hub.

```bash
docker build . -t coral -f dockerfile/Dockerfile
```

### Running from Built Docker Image

```bash
docker run --rm -v "./data:/data" coral -u "/data/For_Curtain_Raw_PPM1H- PROTAC_TP.txt" -a "/data/annotation.txt" -o "/data/output.txt" -c "/data/comparison.txt" -x "T: Index,T: Gene"
```

## Running from Docker Hub Image

```bash
docker run --rm -v "./data:/data" noatgnu/coral:0.0.1 -u "/data/For_Curtain_Raw_PPM1H- PROTAC_TP.txt" -a "/data/annotation.txt" -o "/data/output.txt" -c "/data/comparison.txt" -x "T: Index,T: Gene"
```

## Installation

### Pip Install

Install R and set the `R_HOME` environment variable to the R installation directory. Also, install the `QFeatures` package and its dependencies.

```bash
pip install ccore-coral
```

## Running from Pip Install

```bash
coral -u "/data/For_Curtain_Raw_PPM1H- PROTAC_TP.txt" -a "/data/annotation.txt" -o "/data/output.txt" -c "/data/comparison.txt" -x "T: Index,T: Gene"
```

## CLI Usage

```bash
usage: coral [-h] [-u unprocessed] [-a annotation] [-o output] [-c comparison] [-x index] [-f column_na_filter_threshold] [-r row_na_filter_threshold] [-i imputation_method] [-n normalization_method] [-g aggregation_method] [-t aggregation_column]

Options:
    -u unprocessed, --unprocessed unprocessed
                        Filepath to the unprocessed data file.
    -a annotation, --annotation annotation
                        Filepath to the annotation file.
    -o output, --output output
                        Filepath to the output file.
    -c comparison, --comparison comparison
                        Filepath to the comparison file.
    -x index, --index index
                        Column names to be used as index.
    -f column_na_filter_threshold, --column_na_filter_threshold column_na_filter_threshold
                        Threshold for column-wise NA filtering.
    -r row_na_filter_threshold, --row_na_filter_threshold row_na_filter_threshold
                        Threshold for row-wise NA filtering.
    -i imputation_method, --imputation_method imputation_method
                        Method for imputation.
    -n normalization_method, --normalization_method normalization_method
                        Method for normalization.
    -g aggregation_method, --aggregation_method aggregation_method
                        Method for aggregation.
    -t aggregation_column, --aggregation_column aggregation_column
                        Column name to be used for aggregation.
```

## Usage as a Module

```python
import pandas as pd
from coral.data import Coral

coral = Coral()
# Read in the unprocessed data
coral.load_unproccessed_file("data/For_Curtain_Raw_PPM1H- PROTAC_TP.txt")
# Add sample column names
coral.add_sample("...")
# Add condition or group names
coral.add_condition("...")
# Add sample group mapping
coral.add_condition_map("condition_name", "sample_name")
# Add comparison
coral.add_comparison("condition_A", "condition_B", "comparison_name")
# Add index columns
coral.index_columns = ["index_column_name"]
# Filter columns by NA
coral.filter_missing_columns(0.7)
# Create QFeatures object
coral.prepare()
# Filter rows by NA
coral.filter_missing_rows(0.7)
# Impute missing values
coral.impute("knn")
# Log2 transform
coral.log_transform()
# Aggregate features
coral.aggregate_features("new_feature_column")
# Normalize
coral.normalize()
# Prepare limma matrix
coral.prepare_for_limma()
# Run limma
results = []
for d in coral.run_limma():
    results.append(d)
if len(results) > 1:
    # Merge limma results
    results = pd.concat(results)
else:
    results = results[0]
# Write results
results.to_csv("output.txt", sep="\t", index=False)
```
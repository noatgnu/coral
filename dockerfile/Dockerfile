FROM python:3.10-bullseye
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ARG DEBIAN_FRONTEND=noninteractive
LABEL authors="Toan Phung"

RUN apt-get update
WORKDIR /app
RUN apt-get install -y --no-install-recommends r-base r-base-dev && rm -rf /var/lib/apt/lists/*
RUN R -e 'install.packages("devtools")'
RUN R -e "install.packages('BiocManager',dependencies=TRUE, repos='http://cran.rstudio.com/')"
RUN R -e "install.packages(c('remotes', 'dplyr', 'ggplot2'))"
RUN R -e "library('BiocManager');BiocManager::install(c('MSstats', 'MSstatsPTM', 'limma', 'preprocessCore', 'impute', 'QFeatures', 'norm', 'pcaMethods', 'imputeLCMD', 'corrplot', 'PerseusR', 'data.table', 'XML', 'doParallel', 'stringr', 'MASS', 'Rcpp', 'Biostrings', 'Biobase'))"
COPY . /app/
RUN pip install -r requirements.txt


ENTRYPOINT ["python", "main.py"]
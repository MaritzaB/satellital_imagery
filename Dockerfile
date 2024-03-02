FROM ubuntu:latest

ENV TZ=US/Pacific

RUN ln --symbolic --no-dereference --force /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install --yes --no-install-recommends apt-utils

RUN apt-get update && \
    apt upgrade --yes && \
    apt-get install make --yes

RUN apt-get update && apt-get install latex2html --yes

RUN apt-get update && \
    apt-get install --yes --no-install-recommends \
    gettext-base \
    git \
    make \
    pandoc \
    python3 \ 
    python3-dev \
    python3-pip


RUN pip install --upgrade \
    -U scikit-learn \
    basemap \
    black -U \
    folium \
    geopandas \
    geopy \
    imblearn \
    ipykernel \
    matplotlib \
    netcdf4 \
    numpy \
    openpyxl \
    pandas \
    pytest \
    rasterio \
    rioxarray \
    seaborn \
    wget \
    xarray

# Coral Reef introduction ot data 

Author: Lavinia Schlyter
Version: 1.0

This repo is a succession/subsection of the Coral Reef repo but intended to be more reproducible as part of the course "Introduction to research" at EPFL. It will take several scripts from the original folder and make them such that they are more reproducible and follow coding conventions.


The goal of this notebook is to have a broad overview of the data for Australia (The Great Barrier Reef). That includes:
- Plot the survey points on map
- Basic data analysis for missing values
- Analyse the different components of the image
- Plot the distrubtion of the components (such as hard corals, soft corals ...) over the years 

## Coral data presentation 

Seaview Survey Photo-quadrat and Image Classification Dataset 

#### Data provider
The data is provided by the _XL Catlin Seaview Survey Project_ that was developped as a collaboration between the University of Queensland and ocean conservaton non-profit Underwater Earth.


The goal of their project is to collect rapid, detailed, globally distributed scientific surveys of coral reefs to support research and conservation.
The data colletion took part between 2012-2018 with a custom camera that produced high quality photographs of the reef at transect that were usually 1.5-2 km long. Images were taken between 0.5-2m to ensure constistent spatial resolution (around 10 pixels/cm).

#### Data specifics
The raw data is a collection of over one million images covering around 1m² of the sea floor. You also have human-classified annotations that may be used to train and validate image classifiers.
Deep learning algorithms (VGG-D 16 network architecture) were used to estimate the benthic cover from each photo. The relative abundance of each benthic group was also estimated by using deep learning algorithms.

For this project we are interested in the benthic cover of the corals derived from the images and we will thus not focus on the images. 

#### Data sets used
The "seaviewsurvey_surveys.csv", contains **the proportional cover of reef cover** between _hard_ or _soft_ corals, _other invertebrates_ or _other_ or algea. 
It also has "lat_start, lng_start", the latitude and longitude of start of survey but also the end "lat_end, lng_end". 

Useful additional information of the dataframe may be found in "Seaview_data_explanation.pdf" (in Data folder) for understanding variables such as Transect ID, survey ID

# Use the official Python image from the Docker Hub
FROM python:3.10.4

# Copy the requirements file into the container
COPY requirements.txt ./

# Install the dependencies
RUN pip install -r requirements.txt

# Create a directory for the CSV files
RUN mkdir -p interpolatedcsv

# Create a directory for the model files
RUN mkdir -p regressionmodel

# Copy the CSV files into the container
COPY interpolatedcsv/interpolatedca.csv /interpolatedcsv/
COPY interpolatedcsv/interpolatedHb.csv /interpolatedcsv/
COPY interpolatedcsv/interpolatedgl.csv /interpolatedcsv/
COPY interpolatedcsv/interpolatedalb.csv /interpolatedcsv/
COPY interpolatedcsv/interpolatedalbu.csv /interpolatedcsv/
COPY interpolatedcsv/interpolatedcals.csv /interpolatedcsv/
COPY interpolatedcsv/interpolatedGlucser.csv /interpolatedcsv/
COPY interpolatedcsv/interpolatedGlucu.csv /interpolatedcsv/
COPY interpolatedcsv/interpolatedtpser.csv /interpolatedcsv/
COPY interpolatedcsv/interpolatedhbblood.csv /interpolatedcsv/
COPY interpolatedcsv/interpolatedmpu.csv /interpolatedcsv/

# Copy the model files into the container
COPY regressionmodel/RandomForest_ModelCa.joblib /regressionmodel/
COPY regressionmodel/RandomForest_ModelHb.joblib /regressionmodel/
COPY regressionmodel/RandomForest_ModelGl.joblib /regressionmodel/
COPY regressionmodel/RandomForest_Modelalb.joblib /regressionmodel/
COPY regressionmodel/RandomForest_Modelalburine.joblib /regressionmodel/
COPY regressionmodel/RandomForest_Modeltpserum.joblib /regressionmodel/
COPY regressionmodel/RandomForest_Modelcalserum.joblib /regressionmodel/
COPY regressionmodel/RandomForest_ModelGlucserum.joblib /regressionmodel/
COPY regressionmodel/RandomForest_ModelGlucurine.joblib /regressionmodel/
COPY regressionmodel/RandomForest_Modelhbblood.joblib /regressionmodel/
COPY regressionmodel/RandomForest_Modelmpurine.joblib /regressionmodel/

COPY 10model.py /10model.py
COPY 10model.html /10model.html

# Expose the port that the application will run on
EXPOSE 5000

# Command to run the Python script
ENTRYPOINT ["python", "/10model.py"]

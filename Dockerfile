# Use the official Python image from the Docker Hub
FROM python:3.10.4

# Copy the requirements file into the container
COPY requirements.txt ./

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the CSV files into the container
COPY interpolatedca.csv /
COPY interpolatedHb.csv /
COPY interpolatedgl.csv /
COPY interpolatedalb.csv /
COPY interpolatedalbu.csv /
COPY interpolatedcals.csv /
COPY interpolatedGlucser.csv /
COPY interpolatedGlucu.csv /
COPY interpolatedtpser.csv /
COPY interpolatedhbblood.csv /
COPY interpolatedmpu.csv /

# Copy the model files into the container
COPY RandomForest_ModelCa.joblib /
COPY RandomForest_ModelHb.joblib /
COPY RandomForest_ModelGl.joblib /
COPY RandomForest_Modelalb.joblib /
COPY RandomForest_Modelalburine.joblib /
COPY RandomForest_Modeltpserum.joblib /
COPY RandomForest_Modelcalserum.joblib /
COPY RandomForest_ModelGlucserum.joblib /
COPY RandomForest_ModelGlucurine.joblib /
COPY RandomForest_Modelhbblood.joblib /
COPY RandomForest_Modelmpurine.joblib /

COPY 10model.py /10model.py
COPY 10model.html /10model.html

# Expose the port that the application will run on
EXPOSE 5000

# Command to run the Python script
ENTRYPOINT ["python", "/10model.py"]

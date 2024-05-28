from flask import Flask, request
import pandas as pd
from joblib import load
from tabulate import tabulate
app = Flask(__name__)
models = {
    'calcium':load('RandomForest_ModelCa.joblib'),
    'glucose':load('RandomForest_ModelGl.joblib'),
    'haemoglobin':load('RandomForest_ModelHb.joblib'),
    'albuminserum': load('RandomForest_Modelalb.joblib'),
    'calciumserum': load('RandomForest_Modelcalserum.joblib'),
    'totalproteinserum': load('RandomForest_Modeltpserum.joblib'),
    'glucoseserum': load('RandomForest_ModelGlucserum.joblib'),
    'albuminurine': load('RandomForest_Modelalburine.joblib'),
    'glucoseurine': load('RandomForest_ModelGlucurine.joblib'),
    'microproteinurine': load('RandomForest_Modelmpurine.joblib'),
    'hbblood': load('RandomForest_Modelhbblood.joblib')  # Load the new hbblood model
}
datasets = {
    'calcium': pd.read_csv("interpolatedca.csv"),
    'glucose': pd.read_csv("interpolatedgl.csv"),
    'haemoglobin': pd.read_csv("interpolatedHb.csv"),
    'albuminserum': pd.read_csv("interpolatedalb.csv"),
    'calciumserum': pd.read_csv("interpolatedcals.csv"),
    'totalproteinserum': pd.read_csv("interpolatedtpser.csv"),
    'glucoseserum': pd.read_csv("interpolatedGlucser.csv"),
    'albuminurine': pd.read_csv("interpolatedalbu.csv"),
    'glucoseurine': pd.read_csv("interpolatedGlucu.csv"),
    'microproteinurine': pd.read_csv("interpolatedmpu.csv"),
    'hbblood': pd.read_csv("interpolatedhbblood.csv")  # Load the new hbblood dataset
}
def predict_concentration_four_values(model, df, row_values):
    if len(row_values) == 1:
        row_values = row_values * 4
    user_input = pd.DataFrame({
        df.columns[1]: [row_values[0]], 
        df.columns[2]: [row_values[1]], 
        df.columns[3]: [row_values[2]], 
        df.columns[4]: [row_values[3]]
    })
    concentration_prediction = model.predict(user_input)
    return round(concentration_prediction[0], 2)
def predict_concentration_three_values(model, df, row_values):
    if len(row_values) == 1:
        row_values = row_values * 3
    user_input = pd.DataFrame({
        df.columns[1]: [row_values[0]], 
        df.columns[2]: [row_values[1]], 
        df.columns[3]: [row_values[2]]
    })
    concentration_prediction = model.predict(user_input)
    return round(concentration_prediction[0], 2)
def predict_concentration_two_values(model, df, row_values):
    if len(row_values) == 1:
        row_values = row_values * 2
    user_input = pd.DataFrame({
        df.columns[1]: [row_values[0]], 
        df.columns[2]: [row_values[1]]
    })
    concentration_prediction = model.predict(user_input)
    return round(concentration_prediction[0], 2)

def predict_concentration_one_value(model, df, row_values):
    user_input = pd.DataFrame({df.columns[1]: [row_values[0]]})
    concentration_prediction = model.predict(user_input)
    return round(concentration_prediction[0], 2)
@app.route("/")
def root():
    with open("10model.html") as file:
        return file.read()
@app.route('/predict', methods=['POST'])
def predict():
    sample_types = {
        'blood': ['calcium','glucose','haemoglobin','hbblood'],
        'serum': ['totalproteinserum', 'glucoseserum', 'albuminserum', 'calciumserum'],
        'urine': ['glucoseurine', 'albuminurine', 'microproteinurine']
    }
    sample_type = request.form['sample_type'].strip().lower()
    parameter = request.form['parameter'].strip().lower()
    input_values = request.form['input_values'].strip().split(',')
    input_values = [float(value) for value in input_values]
    if sample_type not in sample_types or parameter not in sample_types[sample_type]:
        return "Invalid sample type or parameter selected."
    model = models[parameter]
    df = datasets[parameter]
    results = []
    for input_value in input_values:
        if parameter in ['calcium','glucose','haemoglobin']:
            predicted_concentration = predict_concentration_three_values(model, df, [input_value])
        elif parameter == 'hbblood':
            predicted_concentration = predict_concentration_four_values(model, df, [input_value])
        elif parameter in ['albuminserum', 'calciumserum', 'totalproteinserum', 'glucoseserum', 'glucoseurine', 'microproteinurine']:
            predicted_concentration = predict_concentration_two_values(model, df, [input_value])
        elif parameter == 'albuminurine':
            predicted_concentration = predict_concentration_one_value(model, df, [input_value])
        results.append([input_value, predicted_concentration])
    result_table = tabulate(results, headers=["Input Value", "Predicted Concentration"], tablefmt="grid")
    return f"<pre> {result_table} </pre>"
if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0', debug=False)     

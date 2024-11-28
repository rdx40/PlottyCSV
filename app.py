from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
import plotly.express as px
import json
from plotly.utils import PlotlyJSONEncoder  # Correct import
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    df = pd.read_csv(filepath)
    columns = df.columns.tolist()
    
    return render_template('upload.html', columns=columns, filename=file.filename)
@app.route('/plot', methods=['POST'])
def plot():
    filename = request.form['filename']
    column_x = request.form['column_x']
    column_y = request.form['column_y']
    
    df = pd.read_csv(os.path.join(UPLOAD_FOLDER, filename))
    fig = px.scatter(df, x=column_x, y=column_y, title=f'Plot of {column_y} vs {column_x}')
    
    fig.update_layout(
        xaxis=dict(
            title=column_x,
            rangeslider=dict(visible=True),  # Enable range slider
        ),
        yaxis_title=column_y,
    )
    plot_json = json.dumps(fig, cls=PlotlyJSONEncoder)  # Use correct encoder
    return render_template('plot.html', plot_json=plot_json)
if __name__ == '__main__':
    app.run(debug=True)


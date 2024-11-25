from flask import Flask, request, render_template, redirect, url_for, jsonify
import pandas as pd
import numpy as np
import pyshark
import pickle

app = Flask(__name__)

# Load the model
with open('new_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Define the features
all_columns = ['dur', 'proto', 'service', 'state', 'spkts', 'dpkts', 'sbytes',
               'dbytes', 'rate', 'sttl', 'dttl', 'sload', 'dload', 'sloss', 'dloss',
               'sinpkt', 'dinpkt', 'sjit', 'djit', 'swin', 'stcpb', 'dtcpb', 'dwin',
               'tcprtt', 'synack', 'ackdat', 'smean', 'dmean', 'trans_depth',
               'response_body_len', 'ct_srv_src', 'ct_state_ttl', 'ct_dst_ltm',
               'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm',
               'is_ftp_login', 'ct_ftp_cmd', 'ct_flw_http_mthd', 'ct_src_ltm',
               'ct_srv_dst', 'is_sm_ips_ports']

trained_features = ['dur', 'proto', 'service', 'state', 'spkts', 'dpkts', 'sbytes',
                    'dbytes', 'rate', 'sttl', 'dttl', 'sload', 'dload', 'sloss', 
                    'dloss', 'sinpkt', 'dinpkt', 'sjit', 'djit', 'swin', 'stcpb', 
                    'dtcpb', 'dwin', 'tcprtt', 'synack', 'ackdat', 'smean', 'dmean', 
                    'trans_depth', 'response_body_len', 'ct_srv_src', 'ct_state_ttl', 
                    'ct_dst_ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 
                    'is_ftp_login', 'ct_ftp_cmd', 'ct_flw_http_mthd', 'ct_src_ltm', 
                    'ct_srv_dst', 'is_sm_ips_ports']

# Function to preprocess the data by encoding categorical columns
def preprocess_data(df):
    # One-hot encode categorical features
    df = pd.get_dummies(df, columns=['proto', 'service', 'state'], drop_first=True)
    
    # Add missing columns with zeros for alignment with model's expected features
    for col in trained_features:
        if col not in df.columns:
            df[col] = 0
    
    # Reorder columns to match the trained feature order
    df = df[trained_features]
    return df

# Route for home page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle CSV file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(url_for('index'))
    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))
    if file:
        df = pd.read_csv(file)
        df = preprocess_data(df)  # Preprocess the data
        predictions = model.predict(df)
        results = [{"Packet": i + 1, "Prediction": "Safe" if pred == "Normal" else pred} for i, pred in enumerate(predictions)]
        return render_template('results.html', results=results)

# Route to start packet sniffing
@app.route('/sniff', methods=['POST'])
def sniff_packets():
    packet_results = process_packets(packet_limit=10)
    return jsonify(packet_results)

# Function to process packets and predict using the model
def process_packets(interface='Wi-Fi', packet_limit=10):
    capture = pyshark.LiveCapture(interface=interface)
    packets = capture.sniff_continuously(packet_count=packet_limit)
    results = []

    for packet_count, packet in enumerate(packets, start=1):
        features = extract_top_10_features(packet)
        df = pd.DataFrame([features])
        
        for column in all_columns:
            if column not in df.columns:
                df[column] = np.nan

        df = preprocess_data(df)  # Preprocess the data
        prediction = model.predict(df)
        results.append({
            "Packet": packet_count,
            "Prediction": "Normal" if prediction[0] == "Normal" else prediction[0]
        })
    return results

if __name__ == '__main__':
    app.run(debug=True)

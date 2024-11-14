import asyncio
from flask import Flask, render_template, jsonify, request
import pyshark
import pandas as pd
import numpy as np
import pickle

app = Flask(__name__)

with open('new_model.pkl', 'rb') as f:
    model = pickle.load(f)

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

def extract_top_10_features(packet):
    features = {}
    try:
        features['sttl'] = int(packet.ip.ttl) if hasattr(packet, 'ip') else np.nan
        features['sbytes'] = int(packet.length) if hasattr(packet, 'length') else np.nan
        features['smean'] = np.nan
        features['tcprtt'] = float(packet.tcp.analysis_ack_rtt) if hasattr(packet, 'tcp') and hasattr(packet.tcp, 'analysis_ack_rtt') else np.nan
    except AttributeError as e:
        print(f"Error extracting feature: {e}")
    return features

async def async_process_packets(interface='Wi-Fi', model=model, packet_limit=10):
    capture = pyshark.LiveCapture(interface=interface)
    packets = capture.sniff_continuously(packet_count=packet_limit)
    results = []
    
    for packet_count, packet in enumerate(packets, start=1):
        features = extract_top_10_features(packet)
        df = pd.DataFrame([features])
        
        for column in all_columns:
            if column not in df.columns:
                df[column] = np.nan

        for col in df.columns:
            if col not in features:
                df[col] = 0

        df_filtered = df[trained_features]
        prediction = model.predict(df_filtered)
        
        result = f"Packet {packet_count} Prediction: " + ("Safe" if prediction[0] == "Normal" else prediction[0])
        results.append(result)
    
    return results

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

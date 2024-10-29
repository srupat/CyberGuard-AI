import pyshark
import pandas as pd
import numpy as np
import pickle

# Load the trained model
with open('random_forest_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Define the columns from the training dataset
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

# Capture and extract packet features using PyShark
def extract_top_10_features(packet):
    features = {}

    # Attempt to capture each required feature (top 10)
    try:
        features['sttl'] = int(packet.ip.ttl) if hasattr(packet, 'ip') else np.nan
        # For 'ct_state_ttl', 'rate', 'dload', 'sload', 'ct_srv_dst', etc.
        # You may need to estimate or calculate these values based on available data
        # in PyShark, as PyShark may not directly support these exact fields.

        features['sbytes'] = int(packet.length) if hasattr(packet, 'length') else np.nan
        features['smean'] = np.nan  # Placeholder as an example (not directly in PyShark)
        features['tcprtt'] = float(packet.tcp.analysis_ack_rtt) if hasattr(packet, 'tcp') and hasattr(packet.tcp, 'analysis_ack_rtt') else np.nan

        # Assign NaN or calculate other features as needed
    except AttributeError as e:
        print(f"Error extracting feature: {e}")
    
    return features

def process_packets(interface='Wi-Fi', model=model, packet_limit=10):
    capture = pyshark.LiveCapture(interface=interface)
    
    # Capture the specified number of packets only
    packets = capture.sniff_continuously(packet_count=packet_limit)
    
    # Process each captured packet
    for packet_count, packet in enumerate(packets, start=1):
        features = extract_top_10_features(packet)

        # Create DataFrame with NaN/0 values for missing columns
        df = pd.DataFrame([features])
        for column in all_columns:
            if column not in df.columns:
                df[column] = np.nan  # Fill missing columns with NaN

        # Fill missing columns with 0 for non-top-10 columns if required
        for col in df.columns:
            if col not in features:
                df[col] = 0
                
        df_filtered = df[trained_features]

        # Predict using the trained model
        prediction = model.predict(df_filtered)
        print(f"Packet {packet_count} Prediction:", "Attack" if prediction[0] == 1 else "Safe")

# Start processing packets with the specified limit
process_packets(packet_limit=10)

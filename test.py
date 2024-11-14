import pandas as pd
import numpy as np
import pickle

with open('new_model.pkl', 'rb') as f:
    model = pickle.load(f)

protocol_encoding = {'tcp': 1, 'udp': 2, 'icmp': 3}

faulty_packet = {
    'dur': 0.0,
    'proto': protocol_encoding.get('tcp', 0), 
    'service': np.nan,
    'state': np.nan,
    'spkts': 10,
    'dpkts': 8,
    'sbytes': 564,
    'dbytes': 354,
    'rate': 25.197692,
    'sttl': 254,
    'dttl': 252,
    'sload': 6023.73,
    'dload': 3675.898,
    'sloss': 2,
    'dloss': 1,
    'sinpkt': np.nan,
    'dinpkt': np.nan,
    'sjit': 5000,
    'djit': 5000,
    'swin': 0,
    'stcpb': 0,
    'dtcpb': 0,
    'dwin': 0,
    'tcprtt': 5,
    'synack': 2,
    'ackdat': 2,
    'smean': 10000,
    'dmean': 10000,
    'trans_depth': 10,
    'response_body_len': 0,
    'ct_srv_src': 0,
    'ct_state_ttl': 0,
    'ct_dst_ltm': 0,
    'ct_src_dport_ltm': 0,
    'ct_dst_sport_ltm': 0,
    'ct_dst_src_ltm': 0,
    'is_ftp_login': 0,
    'ct_ftp_cmd': 0,
    'ct_flw_http_mthd': 0,
    'ct_src_ltm': 0,
    'ct_srv_dst': 0,
    'is_sm_ips_ports': 1
}

faulty_packet_df = pd.DataFrame([faulty_packet])
all_columns = [
    'dur', 'proto', 'service', 'state', 'spkts', 'dpkts', 'sbytes', 'dbytes',
    'rate', 'sttl', 'dttl', 'sload', 'dload', 'sloss', 'dloss', 'sinpkt', 'dinpkt',
    'sjit', 'djit', 'swin', 'stcpb', 'dtcpb', 'dwin', 'tcprtt', 'synack', 'ackdat',
    'smean', 'dmean', 'trans_depth', 'response_body_len', 'ct_srv_src', 'ct_state_ttl',
    'ct_dst_ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm',
    'is_ftp_login', 'ct_ftp_cmd', 'ct_flw_http_mthd', 'ct_src_ltm', 'ct_srv_dst', 
    'is_sm_ips_ports'
]
for column in all_columns:
    if column not in faulty_packet_df.columns:
        faulty_packet_df[column] = np.nan  

trained_features = [
    'dur', 'proto', 'service', 'state', 'spkts', 'dpkts', 'sbytes', 'dbytes',
    'rate', 'sttl', 'dttl', 'sload', 'dload', 'sloss', 'dloss', 'sinpkt', 'dinpkt',
    'sjit', 'djit', 'swin', 'stcpb', 'dtcpb', 'dwin', 'tcprtt', 'synack', 'ackdat',
    'smean', 'dmean', 'trans_depth', 'response_body_len', 'ct_srv_src', 'ct_state_ttl',
    'ct_dst_ltm', 'ct_src_dport_ltm', 'ct_dst_sport_ltm', 'ct_dst_src_ltm', 
    'is_ftp_login', 'ct_ftp_cmd', 'ct_flw_http_mthd', 'ct_src_ltm', 'ct_srv_dst', 
    'is_sm_ips_ports'
]
faulty_packet_df = faulty_packet_df[trained_features]

prediction = model.predict(faulty_packet_df)
print("Attack category:", prediction[0])

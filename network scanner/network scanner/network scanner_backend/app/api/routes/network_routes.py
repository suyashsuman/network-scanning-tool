from flask import Blueprint, request, jsonify
import subprocess
import re
import os
from threading import Lock
from flask_socketio import emit
from app import socketio
import eventlet

nmap_path = os.getenv('NMAP_PATH', 'nmap')
network_bp = Blueprint('network_bp', __name__)
scan_processes = {}
process_lock = Lock()

@socketio.on('connect', namespace='/test')
def handle_connect():
    print("Client connected to socket")
    user_id = request.args.get('userId')
    if user_id:
        print(f"User {user_id} connected to socket")
        emit('connected', {'status': 'connected'}, namespace='/test')

@network_bp.route('/network-scan', methods=['POST'])
def network_scan():
    print("\n=== Starting Network Scan ===")
    data = request.get_json()
    ip_address = data.get('ip_address')
    top_ports = data.get('top_ports')
    ports = data.get('ports')
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    if not re.match(r'^\d{1,3}(\.\d{1,3}){3}$', ip_address):
        return jsonify({"error": "Invalid IP address format"}), 400

    if top_ports and ports:
        return jsonify({"error": "Please specify either top_ports or specific ports, not both"}), 400

    ports_argument = f"--top-ports {top_ports}" if top_ports else f"-p {ports}"
    command = f"{nmap_path} -v {ports_argument} {ip_address}"
    
    def run_scan():
        try:
            process = subprocess.Popen(
                command.split(),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            with process_lock:
                scan_processes[user_id] = process
            
            while True:
                output = process.stdout.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    cleaned_output = output.strip()
                    print(f"Emitting output: {cleaned_output}")
                    socketio.emit('nmap_output', {'data': cleaned_output}, namespace='/test')
                eventlet.sleep(0)
            
            return_code = process.poll()
            
            with process_lock:
                if user_id in scan_processes:
                    del scan_processes[user_id]
            
            if return_code == 0:
                socketio.emit('scan_complete', namespace='/test')
            else:
                socketio.emit('scan_error', 
                            {'error': f'Scan failed with return code {return_code}'}, 
                            namespace='/test')
                
        except Exception as e:
            print(f"Error in scan process: {str(e)}")
            socketio.emit('scan_error', {'error': str(e)}, namespace='/test')
            
    eventlet.spawn(run_scan)
    return jsonify({"message": "Scan initiated", "user_id": user_id}), 202

@network_bp.route('/stop-scan', methods=['POST'])
def stop_scan():
    data = request.get_json()
    user_id = data.get('user_id')

    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    with process_lock:
        process = scan_processes.get(user_id)
        
        if not process:
            return jsonify({"message": "No active scan found"}), 200
        
        try:
            process.terminate()
            del scan_processes[user_id]
            socketio.emit('scan_stopped', 
                        {'message': 'Scan stopped by user'}, 
                        namespace='/test')
        except Exception as e:
            return jsonify({"error": f"Error stopping scan: {str(e)}"}), 500

    return jsonify({"message": "Scan stopped successfully"}), 200



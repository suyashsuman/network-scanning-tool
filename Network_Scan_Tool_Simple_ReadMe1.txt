
# Network Scan Tool

This tool helps you scan a network to find open ports on an IP address. You can choose to scan the most common ports or specify your own custom ports.

---

## Features
- **IP Address Scanning**: Check for open ports on any IP address.
- **Top Ports**: Scan popular ports quickly.
- **Custom Ports**: Enter specific ports you want to check.
- **Stop Scans**: Cancel scans anytime.
- **Simple Results**: See open ports, their states, and services.

---

## How to Use
1. Enter the IP address.
2. Choose to scan top ports or add custom ports.
3. Hit "Start Scan" to begin.
4. View the results on the right side.
5. Stop a scan anytime using the "Stop Scan" button.


### Backend 
1. Go to the `backend` folder:
   ```bash
   cd scansphere_backend
   ```
2. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the backend server:
   ```bash
   python run.py
   ```

### Frontend 
1. Go to the `frontend` folder:
   ```bash
   cd ../scansphere_frontend
   ```
2. Install required packages:
   ```bash
   npm install
   ```
3. Start the app:
   ```bash
   npm run dev
   ```

Open your browser and go to:
```
http://localhost:3000
```

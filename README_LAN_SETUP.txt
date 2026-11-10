IT SERVICE MANAGER - CENTRAL LAN SETUP

ADMIN/SERVER PC
1. Keep SERVER_IP.txt as the current IP of the Admin/Server PC.
   Current default: 10.10.139.81
2. Run SETUP_SERVER_FIREWALL.bat as Administrator once.
3. Run START_LAN_SERVER.bat and keep the black server window open.
4. Admin can open http://10.10.139.81:9000/ or use Open_IT_Service_Manager_ADMIN.bat.

CLIENT PCs
1. Put this folder on the client PC (or copy the client BAT + SERVER_IP.txt).
2. SERVER_IP.txt must contain the Admin/Server PC IP, not the client PC IP.
3. Run Open_IT_Service_Manager_CLIENT.bat.
4. It opens http://SERVER_IP:9000/.

FUTURE SERVER IP CHANGE
Edit only SERVER_IP.txt and replace the old IP with the new Admin/Server PC IP.
Example: 10.10.139.81 -> 10.10.140.25
No source-code edit is required.

DEPARTMENT LOGIN
IT Hardware and IT Network both use the department password screen.
Default department password is 1234 unless it has already been changed.

CLIENT COUNT
No hard-coded 50-client limit is included. The practical capacity depends on the server PC and LAN.

IMPORTANT
Do not open index.html directly from file:// on clients. Use the BAT or http://SERVER-IP:9000/ so the central server/database is used.

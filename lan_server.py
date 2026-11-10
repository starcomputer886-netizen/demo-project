import json, os, sqlite3, threading, time
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

# Cloud ke liye absolute path set karna
BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, 'IT_Service_Manager_LAN.db')
ROOT = BASE

# Render jo PORT dega wahi use hoga, warna 9000
PORT = int(os.environ.get('PORT', 9000))

def init_db():
    try:
        con = sqlite3.connect(DB_PATH)
        con.execute('CREATE TABLE IF NOT EXISTS app_state (id INTEGER PRIMARY KEY CHECK(id=1), state TEXT NOT NULL, version INTEGER NOT NULL, updated_at REAL NOT NULL)')
        con.commit()
        con.close()
    except Exception as e:
        print(f"Database init error: {e}", flush=True)

LOCK = threading.RLock()

def get_state():
    with LOCK:
        con=sqlite3.connect(DB_PATH)
        row=con.execute('SELECT state,version,updated_at FROM app_state WHERE id=1').fetchone()
        con.close()
        if not row: return None,0,0
        return json.loads(row[0]), row[1], row[2]

def put_state(state):
    payload=json.dumps(state, ensure_ascii=False, separators=(',',':'))
    with LOCK:
        con=sqlite3.connect(DB_PATH)
        row=con.execute('SELECT version FROM app_state WHERE id=1').fetchone()
        version=(row[0] if row else 0)+1
        now=time.time()
        con.execute('INSERT INTO app_state(id,state,version,updated_at) VALUES(1,?,?,?) ON CONFLICT(id) DO UPDATE SET state=excluded.state, version=excluded.version, updated_at=excluded.updated_at',(payload,version,now))
        con.commit(); con.close()
        return version,now

class Handler(SimpleHTTPRequestHandler):
    def __init__(self,*args,**kwargs): 
        super().__init__(*args,directory=ROOT,**kwargs)
        
    def _json(self, code, obj):
        raw=json.dumps(obj,ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Content-Length',str(len(raw)))
        self.send_header('Cache-Control','no-store')
        self.send_header('Access-Control-Allow-Origin','*') # CORS fix
        self.end_headers()
        self.wfile.write(raw)
        
    def do_GET(self):
        if urlparse(self.path).path == '/api/state':
            state,version,updated=get_state()
            self._json(200,{'ok':True,'state':state,'version':version,'updatedAt':updated})
            return
        
        # --- YEH NAYA CODE ADD KIYA HAI ---
        # Taaki root URL khulte hi index.html load ho
        if self.path == '/' or self.path == '':
            self.path = '/index.html'
        # ----------------------------------
        
        return super().do_GET()
        
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin','*')
        self.send_header('Access-Control-Allow-Methods','GET,POST,OPTIONS')
        self.send_header('Access-Control-Allow-Headers','Content-Type')
        self.end_headers()
        
    def do_POST(self):
        if urlparse(self.path).path != '/api/state': 
            self.send_error(404)
            return
        try:
            n=int(self.headers.get('Content-Length','0'))
            body=self.rfile.read(n)
            obj=json.loads(body.decode('utf-8'))
            state=obj.get('state') if isinstance(obj,dict) and 'state' in obj else obj
            if not isinstance(state,dict): raise ValueError('state must be an object')
            version,updated=put_state(state)
            self._json(200,{'ok':True,'version':version,'updatedAt':updated})
        except Exception as e: 
            self._json(400,{'ok':False,'error':str(e)})
            
    def log_message(self, fmt,*args):
        print('[%s] %s' % (self.log_date_time_string(), fmt%args), flush=True)

if __name__=='__main__':
    init_db()
    print('IT Service Manager LAN Server is starting...', flush=True)
    print('Listening on 0.0.0.0:%d' % PORT, flush=True)
    print('Database:', DB_PATH, flush=True)
    
    # Render par bind hone ke liye yeh setup zaroori hai
    server = ThreadingHTTPServer(('0.0.0.0', PORT), Handler)
    server.serve_forever()

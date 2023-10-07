from http.server import HTTPServer
import cv2

import base64
import json
import numpy as np
from http.server import BaseHTTPRequestHandler
import cv2






server_addr = "192.168.233.156"
server_port = 6969
file_path = "The Hitchhiker's Guide to the Galaxy (2005) [1080p]/The.Hitchhikers.Guide.to.the.Galaxy.2005.1080p.BluRay.x264.YIFY.mp4"
rows , cols = 1 , 2
frame_rate = 60

frames = []
limit_frame = True
frame_limit = 5000

max_frames = 100


cur_frame = 0
splited_frame = []
new_frame = True
waiting_clients = [False for i in range(rows * cols)]

vidCap = cv2.VideoCapture(file_path)
frame_rate = vidCap.get(cv2.CAP_PROP_FPS)




def append_frames(count):
    global frames

    once = True
    success = False
    while once or success:
        success , image = vidCap.read()

        # happend at the first frame
        if not success and once:
            print("[Error] failed to read vidCapture first frame")
            exit(0) 
        once = False

        frames.append(image)

        if len(frames) > count:
            break
def load_buffer():
    global cur_frame
    global frames

    cur_frame = 0

    frames = frames[max_frames:]
    append_frames(max_frames)


# load the double buffer frames from the video
append_frames(max_frames * 2)
print("[OK] loading video is done")



class DaServer(BaseHTTPRequestHandler):

    def __init__(self, request, client_address, server) -> None:
        global rows
        global cols



        super().__init__(request, client_address, server)

        
        


    def split_img(self,frame):
        global rows
        global cols
        global splited_frame

        if(str(type(frame)) == "<class 'NoneType'>"):
            return


        splited_rows = []
        for y in range(rows):
            splited_rows.append(frame[y * len(frame) // rows:(y + 1) * len(frame) // rows])

        splited_frame = []
        for splited_row in splited_rows:
            for x in range(cols):
                col = []
                for row in splited_row:
                    col.append(row[x * len(frame[0]) // cols:(x + 1) * len(frame[0]) // cols])
                splited_frame.append(col)



    def get_load(self):
        global rows
        global cols
        global frame_rate

        self.send_response(200)

        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header("Content-Type","application/json")
        self.end_headers()
        self.wfile.write(bytes(f"""{"{"}
                                    "rows" :      {rows},
                                    "cols" :      {cols},
                                    "frame_rate": {frame_rate}
                                {"}"}                                
                                """
                                ,"utf-8"))
    def do_GET(self):
        if self.path == "/load":
            self.get_load()

 
    def post_update(self):
        global rows
        global frames
        global new_frame
        global cur_frame
        global splited_frame
        global waiting_clients
        


        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header("Content-Type","multipart/form-data")
        self.end_headers()

        body_size =  int(self.headers.get("Content-Length"))
        json_data = json.loads(self.rfile.read(body_size).decode())
        frame_idx = json_data["col"] + json_data["row"] * rows


        # print("asdasd",frame_idx,waiting_clients[frame_idx],waiting_clients,'=>',new_frame)


        if new_frame:
            # reload new frame and split it
            self.split_img(frames[cur_frame])
            waiting_clients = [False for _ in range(rows * cols)]
            new_frame = False

            cur_frame = cur_frame + 1
            if (cur_frame % max_frames) == 0:
                load_buffer()

        
        if waiting_clients[frame_idx]:

            # client already has img
            self.wfile.write(bytes("keep old","utf-8"))
            return

        _ , buffer = cv2.imencode('.jpg',np.array(splited_frame[frame_idx]))
        img_str = base64.b64encode(buffer)
        self.wfile.write(bytes(f"{img_str}","utf-8"))



        # keep clients on sync   
        waiting_clients[frame_idx] = True

        if False not in waiting_clients:
            new_frame = True







    def do_POST(self):
        print("--post request--")
        print(f"post request: path {self.path}")
        
        if "/update" in self.path:
            self.post_update()













daServer = HTTPServer((server_addr,server_port),DaServer)
try:
    print(f"[OK] daServer is serving at addr {server_addr}:{server_port}")
    daServer.serve_forever()
except KeyboardInterrupt:
    print("\n[OK] closing daServer")

daServer.server_close()

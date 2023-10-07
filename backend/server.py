import cv2
import base64
import numpy as np
import cv2


import asyncio
from websockets.server import serve






server_addr = "localhost" # put ur addr here
server_port = 6969

file_path = "Rick Astley - Never Gonna Give You Up (Official Music Video) [TubeRipper.com].mp4"
rows , cols = 2 , 2
frame_rate = 60

frames = []
max_frames = 100

cur_frame = 0
splited_frame = []
new_frame = True

clients = [None for _ in range(rows * cols)]
vidCap = None
frame_idx = 0


is_running = False



def split_img(frame):
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






async def stream_video():
    global frame_idx
    while True:
        split_img(frames[frame_idx])


        for idx ,client in enumerate(clients):
            if client:
                _ , buffer = cv2.imencode('.jpg',np.array(splited_frame[idx]))
                img_str = base64.b64encode(buffer)
                await client.send(f"STREAM_STARTED::{img_str}")
        

        frame_idx += 1
        if (frame_idx % max_frames) == 0:
            frame_idx = 0
            load_buffer()


        await asyncio.sleep(1 / frame_rate)


    


async def parse_client_msg(msg,websocket):
    [msg_id , msg_info] = msg
    print(msg_id,msg_info)

    if msg_id == "BACKDOOR_HELLO":
        await websocket.send("BACKDOOR_HELLO :: hi client")
    elif msg_id == "LOAD_DATA":
        data = f"""{{
            "rows" : {rows},
            "cols" : {cols},
            "frame_rate" : {frame_rate}
        }}"""
        await websocket.send(f"LOAD_DATA_JSON::{data}")
    elif msg_id == "START_STREAM":
        global is_running
        
        clients[int(msg_info)] = websocket
        
        if not is_running:
            is_running = True
            await stream_video()






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



vidCap = cv2.VideoCapture(file_path)
frame_rate = vidCap.get(cv2.CAP_PROP_FPS)

# load the double buffer frames from the video
append_frames(max_frames * 2)
print("[OK] loading video is done")


async def on_message(websocket):
    async for message in websocket:
       await parse_client_msg(message.split("::"),websocket)
async def main():
    async with serve(on_message,server_addr , server_port):
        await asyncio.Future()  # run forever


print("[OK] server is running")
asyncio.run(main())

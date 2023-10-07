# WatchOut
Streaming videos to multiple screens to watch it with the friends you dont have.    
Mine idea is to stack computer on the wall and watch a movie with the friends, more computer u have the closer to the cinema experience u will get.        
quantity over quality :).




# How To Run
-   make have a shared server, example i used my phone hotspot and connected all the screens to it.
-   one pc will run the server and podcast the video

<br>

## Server
-   server will have to set the server_addr variable in "backend/server.py" and  "src/client_socket.js" to his ip addr he will get it from ```ifconfig``` for linux users or ```ipconfig``` for windows users.
-   or u can just use localhost as the addr
-   set the path of the video in file_path variable in "backend/server.py".
```
    python3  backend/server.py && npm run dev
```
<br>

## Client
-   client will have to be connected to the same hotspot.
-   and go to the http://192.XXX.XXX.XXX:5173/ link smth like that.


# Dev-Imgs
![test run](dev-imgs/working_gif.gif)
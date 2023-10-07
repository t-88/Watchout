function encode_msg(id , info) { return id + "::" + info;}




const SocketAPI = {};
SocketAPI.server_addr = "localhost" // put addr here
SocketAPI.server_port = "6969" 



SocketAPI.client = undefined;

SocketAPI.on_open = () => {
    SocketAPI.client.send(encode_msg("BACKDOOR_HELLO","hi server"));
}
SocketAPI.on_message = (event) => {
    let [msg_id , msg_data] = event.data.split("::");
    
    if (msg_id == "LOAD_DATA_JSON") {
        let data = JSON.parse(msg_data);
        if(SocketAPI.hasOwnProperty(msg_id)) { SocketAPI[msg_id](data);}
    } else if(msg_id == "STREAM_STARTED") {
        msg_data = msg_data.slice(2)
        msg_data = msg_data.slice(0,msg_data.length  - 1);
        msg_data = "data:image/png;charset=utf-8;base64," + msg_data
        if(SocketAPI.hasOwnProperty(msg_id)) { SocketAPI[msg_id](msg_data);}
    }
}

SocketAPI.callback = (id,callback) => {
    if(SocketAPI.hasOwnProperty(id)) {
        throw "id for callback already used";
    }
    SocketAPI[id] = callback;
}

SocketAPI.init = (addr,port) => {
    SocketAPI.client = new WebSocket(`ws://${SocketAPI.server_addr}:${SocketAPI.server_port}`);
    SocketAPI.client.onopen = SocketAPI.on_open;
    SocketAPI.client.onmessage = SocketAPI.on_message;
};


SocketAPI.send = (id,msg = "") => {
    SocketAPI.client.send(encode_msg(id,msg));
}


export default SocketAPI;
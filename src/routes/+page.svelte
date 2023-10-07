{#if !is_running}
<main id="app">

    <h1>Hello Watchers</h1>

    <button on:click={send_load_request} >Say Hi To The Server</button>
    
    {#if did_say_hi_to_server} 
    <div>
        <center><h1>which window are u?</h1></center>
    </div>    
        <div id="windows-rows">
            {#each Array(rows) as _ , y }
            <div id="windows-cols">
                {#each Array(cols) as _ , x }
                    <button class="window" 
                         id="{(selected.row == y && selected.col == x) ? "selected-window" : ""}" 
                         on:click={() => select_window(x,y)}>
                    </button>
                {/each}
            </div>
            {/each}
        </div>
    {/if}


    {#if did_say_hi_to_server && selected.row != -1 && selected.col != -1} 
        <br>
        <button on:click={send_start_request}>Start Watching</button>    
        <h1>:)</h1>
    {/if}
</main>
{:else}
    <img id="img"  src={img_path} alt="path??">
{/if}



<script>
    import "./global.css";
    import { onMount } from "svelte";
    import SocketAPI from "../client_socket";


    let rows = 0;
    let cols = 0;
    let selected = {row : -1,col : -1,};

    let img_path;

    let is_running = false; 
    let did_say_hi_to_server = false;


    // load data from server, rows , cols
    function send_load_request() { SocketAPI.send("LOAD_DATA");}
    function send_start_request(){ SocketAPI.send("START_STREAM",selected.col +  selected.row * rows);}



    function select_window(x,y) {
        selected.row = y;
        selected.col = x;
        selected = {...selected};
    }

    // load data callback
    function load_data_callback(data) {
        rows = data.rows;
        cols = data.cols;
        
        did_say_hi_to_server = true;
    };

    // every frame callback
    function update_callback(data) {
        img_path = data;
        is_running = true;
    }

    onMount(() => {
        SocketAPI.callback("LOAD_DATA_JSON",load_data_callback)
        SocketAPI.callback("STREAM_STARTED",update_callback)
        SocketAPI.init();
    });

</script>


<style>
    #app {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;

        margin-top: 69px;

        gap: 20px;

    }
    #windows-rows {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
    }


    .window {
        width:  69px;
        height: 69px;
        background: transparent;


        margin: 0px;

        border: solid  2px white ;
        border-radius: 0px;

    }

    .window:hover {
        background-color: #BBBBBB;
    }
    #selected-window {
        background-color: white;
    }


    #img {
        height: 100vh;
        width: 100vw;
    }

    h1 {
        font-size: 2em;
        align-self: center;

    }



</style>

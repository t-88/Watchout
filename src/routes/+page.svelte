{#if !is_running}
<main id="app">

    <h1>Hello Watchers</h1>

    <button on:click={load} >Say Hi To The Server</button>
    
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
        <button on:click={init_server}>Start Watching</button>    
        <h1>:)</h1>
    {/if}
</main>
{:else}
    <img id="img"  src={img_path} alt="path??">
{/if}



<script>
    import "./global.css";

    const server_addr = "http://" + "192.168.233.156" + ":6969";
    let is_running = false; 

    let did_say_hi_to_server = false;

    let rows = 0;
    let cols = 0;
    let frame_rate = 60

    let selected = {
        row : -1,
        col : -1,
    };

    let img_path;


    async function load() {
        console.log("loading data from server");

        let res = await fetch(`${server_addr}/load`);
        let data = await res.text();
        data = JSON.parse(data);

        rows = data.rows;
        cols = data.cols;
        frame_rate = data.frame_rate;

        did_say_hi_to_server = true;
    };

    async function init_server() {
        if(is_running) {
            console.log("why are u running??");
            return;
        };
        is_running = true;
        update();
    }

    async function update() {
        const res = await fetch(`${server_addr}/update${selected.row}${selected.col}`,{
            method : "POST",
            mode : "cors",
            body : JSON.stringify(selected)
        });
        let data = await res.text();

        if (data == "keep old") {
            setTimeout(update,frame_rate);
            return
        }



        data = data.slice(2)
        data = data.slice(0,data.length  - 1);



        img_path = "data:image/png;charset=utf-8;base64,";
        img_path += data;        

        setTimeout(update,frame_rate);
    }


    function select_window(x,y) {
        selected.row = y;
        selected.col = x;

        selected = {...selected};
    }


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

let rows = 2, cols = 2;
let screens = [];
let screen_db = {};

import img from "$lib/images/rickroll.jpeg";
import video from "$lib/images/Chip8.mp4";

import ffmpeg from "ffmpeg";
let rick_roll = img;


function genrate_id() {
	while (true) {
		let id = Math.floor(Math.random() * 100)
		if(!screens.includes(id)) {
			return id;
		}
	}
}


export async function handle({ event, resolve }) {

	if(event.url.pathname == "/saveinfo") {
		let body = await event.request.text();
		body = JSON.parse(body);

		rows = parseInt(body.rows);
		cols = parseInt(body.cols);

		screens = [];
		for (let index = 0; index < rows * cols; index++) {
			screens.push(-1);
		}

		return new Response('custom response');
	}
	if (event.url.pathname.startsWith('/info')) {
		const res = new  Response(JSON.stringify({"rows":rows,"cols":cols}),{  status : 200,});
		return res;
	} 

	if (event.url.pathname.startsWith('/submit_idx')) { 
		let body = await event.request.text();
		body = JSON.parse(body);

		let id = genrate_id();
		screens[body.selected] = id;
	
		screen_db[id] = body.selected;

		const res = new  Response(JSON.stringify({"id":id}),{  status : 200,});
		return res;
	}

	if (event.url.pathname.startsWith('/update_client')) { 
		let body = await event.request.text();
		body = JSON.parse(body);	


		let process = new ffmpeg(video);
		console.log(process);

		const res = new  Response(JSON.stringify({path:rick_roll}),{status : 200});
		return res;
	}

	const response = await resolve(event);
	return response;
}
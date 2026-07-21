"use client";

import {useState} from "react";

export default function Login(){

const [username,setUsername]=useState("");
const [password,setPassword]=useState("");

async function login(){

alert("LOGIN CLICKED");

try{

const res = await fetch(
"https://dark-cows-smoke.loca.lt/login",
{
method:"POST",
headers:{
"Content-Type":"application/json"
},
body:JSON.stringify({
username,
password
})
}
);

const data = await res.json();

alert("RESPONSE: "+JSON.stringify(data));

if(data.access_token){

localStorage.setItem(
"token",
data.access_token
);

window.location.href="/dashboard";

}

else{

alert(JSON.stringify(data));

}

}

catch(e){

alert("FETCH ERROR: "+e);

}

}

return(
<div className="min-h-screen bg-sky-100 flex items-center justify-center text-gray-900">

<div className="bg-white shadow-xl rounded-xl p-8 w-96">

<h1 className="text-3xl font-bold text-sky-700">
NONO Login
</h1>

<input
className="border p-3 w-full mt-5"
placeholder="Username"
value={username}
onChange={e=>setUsername(e.target.value)}
/>

<input
className="border p-3 w-full mt-3"
type="password"
placeholder="Password"
value={password}
onChange={e=>setPassword(e.target.value)}
/>

<button
className="bg-sky-600 text-white w-full p-3 rounded mt-5"
onClick={login}
>
Login
</button>

</div>

</div>
)

}

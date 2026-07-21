"use client";

import {useEffect,useState} from "react";

const API="https://dark-cows-smoke.loca.lt";

export default function Dashboard(){

const [projects,setProjects]=useState<any[]>([]);
const [name,setName]=useState("");
const [runtime,setRuntime]=useState("python");
const [repo,setRepo]=useState("");
const [loading,setLoading]=useState(false);


async function loadProjects(){

const token=localStorage.getItem("token");

const res=await fetch(`${API}/projects`,{
headers:{
Authorization:`Bearer ${token}`
}
});

const data=await res.json();

if(Array.isArray(data))
setProjects(data);

}


async function createProject(){

setLoading(true);

const token=localStorage.getItem("token");

const res=await fetch(
`${API}/projects?name=${name}&runtime=${runtime}&repo=${repo}`,
{
method:"POST",
headers:{
Authorization:`Bearer ${token}`
}
}
);

const data=await res.json();

alert(JSON.stringify(data));

setName("");
setRepo("");

loadProjects();

setLoading(false);

}


useEffect(()=>{
loadProjects();
},[]);


return (

<div className="min-h-screen bg-sky-100 p-6 text-gray-900">

<div className="max-w-5xl mx-auto">

<h1 className="text-4xl font-bold text-sky-700">
NONO Cloud
</h1>

<p className="mt-2">
Deploy your apps like Railway / Render
</p>


<div className="bg-white rounded-xl shadow p-5 mt-6">

<h2 className="text-xl font-bold">
Create Project
</h2>


<input
className="border p-2 w-full mt-3"
placeholder="Project name"
value={name}
onChange={e=>setName(e.target.value)}
/>


<input
className="border p-2 w-full mt-3"
placeholder="GitHub repo URL"
value={repo}
onChange={e=>setRepo(e.target.value)}
/>


<select
className="border p-2 w-full mt-3"
value={runtime}
onChange={e=>setRuntime(e.target.value)}
>

<option value="python">
Python
</option>

<option value="node">
NodeJS
</option>

</select>


<button
className="bg-sky-600 text-white px-5 py-2 rounded mt-4"
onClick={createProject}
>

{
loading?"Deploying...":"Deploy Project"
}

</button>


</div>


<div className="bg-white rounded-xl shadow p-5 mt-6">

<h2 className="text-xl font-bold">
Your Projects
</h2>


{
projects.length===0 &&
<p>No projects found</p>
}


{
projects.map(p=>(

<div
key={p.id}
className="border rounded p-3 mt-3"
>

<div className="font-bold">
{p.name}
</div>

<div>
Runtime: {p.runtime}
</div>

<div>
Status:
<span className="ml-2 text-sky-700">
{p.status}
</span>
</div>


</div>

))
}


</div>


</div>

</div>

)

}

function makeChart(id, label) {
    return new Chart(document.getElementById(id), {
        type:'line',
        data:{
            labels:[],
            datasets:[{
                label:label,
                data:[],
                borderColor:'#ff2e2e',
                tension:0.3
            }]
        },
        options:{
            animation:false,
            scales:{ y:{min:0,max:100} }
        }
    });
}

const cpu = makeChart("cpu","CPU %");
const ram = makeChart("ram","RAM %");
const gpu = makeChart("gpu","GPU %");
const temp = makeChart("temp","Temp °C");


function push(chart,val){
    chart.data.labels.push("");
    chart.data.datasets[0].data.push(val);
    if(chart.data.labels.length>50){
        chart.data.labels.shift();
        chart.data.datasets[0].data.shift();
    }
    chart.update();
}


async function updateStats(){
    const r = await fetch("/stats");
    const d = await r.json();

    push(cpu,d.cpu);
    push(ram,d.ram);
    push(gpu,d.gpu);
    push(temp,d.temp);

    const diskDiv = document.getElementById("disks");
    diskDiv.innerHTML="";

    d.disks.forEach(x=>{
        diskDiv.innerHTML += `
            <div>${x.mount} (${x.usage}%)</div>
            <div class="bar"><div class="fill" style="width:${x.usage}%"></div></div>
        `;
    });
}


async function updateProcesses(){
    const r = await fetch("/processes");
    const list = await r.json();

    const table = document.getElementById("procs");
    table.innerHTML="";

    list.forEach(p=>{
        table.innerHTML += `
            <tr>
              <td>${p[0]}</td>
              <td>${p[1]}</td>
              <td>${p[2]}%</td>
              <td><button onclick="kill(${p[0]})">Kill</button></td>
            </tr>
        `;
    });
}


async function kill(pid){
    await fetch("/kill/"+pid);
}

setInterval(()=>{
    updateStats();
    updateProcesses();
},1000);

function addMonths(d,m){const x=new Date(d.getTime());const day=x.getDate();x.setMonth(x.getMonth()+m);if(x.getDate()<day)x.setDate(0);return x;}
export default { async fetch(request){
  const url=new URL(request.url);
  if(url.pathname==="/api/schedule"){
    const period=(url.searchParams.get("period")||"monthly").toLowerCase();
    const start=url.searchParams.get("start"); if(!start) return new Response(JSON.stringify({error:"start required"}),{status:400});
    const count=parseInt(url.searchParams.get("count")||"12",10);
    const step=period==="annual"?12:period==="semiannual"?6:period==="quarterly"?3:1;
    let cur=new Date(start); const dates=[];
    for(let i=0;i<count;i++){ dates.push(cur.toISOString().slice(0,10)); cur=addMonths(cur,step); }
    return new Response(JSON.stringify({period,start,count,dates}), { headers: {"content-type":"application/json"}});
  }
  return new Response(JSON.stringify({ok:true}), { headers: {"content-type":"application/json"}});
}}
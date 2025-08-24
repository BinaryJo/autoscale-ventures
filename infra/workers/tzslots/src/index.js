function addMinutes(d,m){return new Date(d.getTime()+m*60000)}
export default { async fetch(request){
  const url=new URL(request.url);
  if(url.pathname==="/api/slots"){
    const tz=url.searchParams.get("tz")||"UTC";
    const startISO=url.searchParams.get("start");
    if(!startISO) return new Response(JSON.stringify({error:"start required ISO"}),{status:400});
    const blocks=parseInt(url.searchParams.get("blocks")||"30",10);
    const blockMinutes=parseInt(url.searchParams.get("block_minutes")||"120",10);
    let cur=new Date(startISO);const slots=[];
    for(let i=0;i<blocks;i++){ const end=addMinutes(cur,blockMinutes); slots.push({index:i,start:cur.toISOString(),end:end.toISOString(),tz}); cur=end; }
    return new Response(JSON.stringify(slots), { headers: {"content-type":"application/json"}});
  }
  return new Response(JSON.stringify({ok:true}), { headers: {"content-type":"application/json"}});
}}
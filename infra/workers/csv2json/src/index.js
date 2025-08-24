function parseCSV(text){
  const rows=[];let row=[];let field='';let q=false;
  for(let i=0;i<text.length;i++){const c=text[i];
    if(q){ if(c=='"'){ if(text[i+1]=='"'){field+='"';i++;} else {q=false;} } else {field+=c;} }
    else { if(c=='"') q=true; else if(c==','){row.push(field);field='';}
      else if(c=='\n'||c=='\r'){ if(c=='\r'&&text[i+1]=='\n') i++; row.push(field);field=''; rows.push(row); row=[];}
      else field+=c;}
  }
  if(field.length||row.length){row.push(field);rows.push(row);}
  if(!rows.length) return [];
  const headers=rows[0];
  return rows.slice(1).filter(r=>r.length&&r.join('').trim().length).map(r=>Object.fromEntries(headers.map((h,i)=>[h,r[i]??''])));
}
export default { async fetch(request){
  const url = new URL(request.url);
  if(url.pathname==="/api/convert/csv2json"){
    let csv=url.searchParams.get("csv");
    if(!csv && request.method!=="GET"){ csv=await request.text(); }
    csv=csv||"";
    const out=parseCSV(csv);
    return new Response(JSON.stringify(out), { headers: {"content-type":"application/json"}});
  }
  return new Response(JSON.stringify({ok:true}), { headers: {"content-type":"application/json"}});
}}
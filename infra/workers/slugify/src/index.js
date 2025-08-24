export default {
  async fetch(request) {
    const url = new URL(request.url);
    if (url.pathname === "/api/convert/slugify") {
      const text = (url.searchParams.get("text") || "");
      const slug = text.toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9]+/g,'-').replace(/(^-|-$)/g,'');
      return new Response(JSON.stringify({ slug }), { headers: { "content-type": "application/json" }});
    }
    return new Response(JSON.stringify({ ok: true }), { headers: { "content-type": "application/json" }});
  }
}
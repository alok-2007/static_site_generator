export default {
    async fetch(request, env, ctx) {
        const url = new URL(request.url);
        let path = url.pathname;

        if (path.endsWith("/")) {
            path += "index.html";
        } else if (!path.includes(".")) {
            path += "/index.html";
        }

        try {
            const object = await env.BUCKET.get(path);
            if (!object) {
                return new Response("404 Not Found", { status: 404 });
            }

            const contentType = getContentType(path);
            return new Response(object.body, {
                headers: {
                    "content-type": contentType,
                    "cache-control": "public, max-age=31536000",
                },
            });

        } catch (err) {
            return new Response("Internal Error", {status: 500});
        }
    }
}

function getContentType(path) {
    if (path.endsWith(".html")) return "text/html";
    if (path.endsWith(".css")) return "text/css";
    if (path.endsWith(".js")) return "application/javascript";
    if (path.endsWith(".json")) return "application/json";
    if (path.endsWith(".png")) return "image/png";
    if (path.endsWith(".jpg") || path.endsWith(".jpeg")) return "image/jpeg";
    if (path.endsWith(".svg")) return "image/svg+xml";
    return "application/octet-stream";
}
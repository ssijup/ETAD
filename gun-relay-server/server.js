const Gun = require('gun');
const http = require('http');
const url = require('url');

const server = http.createServer((req, res) => {
    const parsedUrl = url.parse(req.url, true);
    const path = parsedUrl.pathname;
    const method = req.method.toUpperCase();

    if (method === 'GET') {
        console.log('METHOD IS GET')
        gun.get(path).once(data => {
            if (data) {
                console.log('data from gun' , data)
                // Convert Gun's output to a dictionary
                const messages = Object.values(data).map(msg => ({
                    message: msg.message,
                    username: msg.username,
                    timestamp: msg.timestamp
                    
                }));
                console.log('2222222222222222')
                res.writeHead(200, {'Content-Type': 'application/json'});
                res.end(JSON.stringify(messages));
            } else {
                res.writeHead(404, {'Content-Type': 'application/json'});
                res.end(JSON.stringify({error: 'Messages not found'}));
            }
        });
    } else if (method === 'PUT') {
        let body = '';
        req.on('data', chunk => {
            body += chunk.toString();
        });
        req.on('end', () => {
            const data = JSON.parse(body);
            gun.get(path).put(data);
            res.writeHead(200, {'Content-Type': 'application/json'});
            res.end(JSON.stringify({success: true}));
        });
    } else {
        res.writeHead(200);
        res.end('Gun relay server is running');
    }
});

const gun = Gun({ web: server });

server.listen(8765, () => {
    console.log('Gun relay server running on port 8765');
});











// const Gun = require('gun');
// const http = require('http');
// const url = require('url');

// const server = http.createServer((req, res) => {
//     const parsedUrl = url.parse(req.url, true);
//     const path = parsedUrl.pathname;
//     const method = req.method.toUpperCase();

//     if (method === 'GET') {
//         gun.get(path).once(data => {
//             if (data) {
//                 res.writeHead(200, {'Content-Type': 'application/json'});
//                 res.end(JSON.stringify(data));
//             } else {
//                 res.writeHead(404, {'Content-Type': 'application/json'});
//                 res.end(JSON.stringify({error: 'Messages not found'}));
//             }
//         });
//     } else if (method === 'PUT') {
//         let body = '';
//         req.on('data', chunk => {
//             body += chunk.toString();
//         });
//         req.on('end', () => {
//             const data = JSON.parse(body);
//             gun.get(path).put(data);
//             res.writeHead(200, {'Content-Type': 'application/json'});
//             res.end(JSON.stringify({success: true}));
//         });
//     } else {
//         res.writeHead(200);
//         res.end('Gun relay server is running');
//     }
// });

// const gun = Gun({ web: server });

// server.listen(8765, () => {
//     console.log('Gun relay server running on port 8765');
// });







// const Gun = require('gun');
// const http = require('http');
// const url = require('url');

// const server = http.createServer((req, res) => {
//     const parsedUrl = url.parse(req.url, true);
//     const path = parsedUrl.pathname;
//     const method = req.method.toUpperCase();

//     if (method === 'GET' && path.startsWith('/users/')) {
//         const userEmail = path.split('/').pop();
        
//         // Fetch user data from Gun
//         gun.get(userEmail).once(userDetails => {
//             if (userDetails) {
//                 res.writeHead(200, {'Content-Type': 'application/json'});
//                 res.end(JSON.stringify(userDetails));
//             } else {
//                 res.writeHead(404, {'Content-Type': 'application/json'});
//                 res.end(JSON.stringify({error: 'User not found'}));
//             }
//         });
//     } else {
//         res.writeHead(200);
//         res.end('Gun relay server is running');
//     }
// });

// const gun = Gun({ web: server });

// server.listen(8765, () => {
//     console.log('Gun relay server running on port 8765');
// });






// const Gun = require('gun');
// const http = require('http');

// const server = http.createServer((req, res) => {
//     res.writeHead(200);
//     res.end('Gun relay server is running');
// });

// const gun = Gun({ web: server });

// server.listen(8765, () => {
//     console.log('Gun relay server running on port 8765');
// });




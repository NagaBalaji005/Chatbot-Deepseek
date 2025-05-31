const CACHE_NAME = 'ai-chatbot-v3';
const STATIC_ASSETS = [
    '/',
    '/public/background.jpg',
    '/public/favicon.ico'
];

// Install event
self.addEventListener('install', (event) => {
    console.log('Service Worker installing...');
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('Caching static assets');
                return cache.addAll(STATIC_ASSETS).catch((error) => {
                    console.warn('Failed to cache some assets:', error);
                    // Don't fail installation if some assets fail to cache
                    return Promise.resolve();
                });
            })
            .catch((error) => {
                console.error('Cache installation failed:', error);
            })
    );
    self.skipWaiting();
});

// Activate event
self.addEventListener('activate', (event) => {
    console.log('Service Worker activating...');
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    self.clients.claim();
});

// Fetch event - Network first for API, Cache first for static assets
self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);
    
    // Skip non-GET requests
    if (event.request.method !== 'GET') {
        return;
    }
    
    // Skip cross-origin requests
    if (url.origin !== self.location.origin) {
        return;
    }
    
    // NEVER cache API endpoints or streaming responses
    if (url.pathname.startsWith('/api/') || 
        url.pathname === '/health' ||
        event.request.headers.get('accept') === 'text/event-stream') {
        console.log('Bypassing cache for API request:', url.pathname);
        return;
    }
    
    // Cache strategy for static assets
    if (url.pathname === '/' || 
        url.pathname.startsWith('/public/') ||
        url.pathname === '/background.jpg' || 
        url.pathname === '/favicon.ico' ||
        url.pathname === '/sw.js') {
        
        event.respondWith(
            caches.match(event.request)
                .then((cachedResponse) => {
                    if (cachedResponse) {
                        console.log('Serving from cache:', url.pathname);
                        
                        // For the main page, also try to update cache in background
                        if (url.pathname === '/') {
                            fetch(event.request)
                                .then((fetchResponse) => {
                                    if (fetchResponse && fetchResponse.status === 200 && fetchResponse.type === 'basic') {
                                        caches.open(CACHE_NAME)
                                            .then((cache) => {
                                                cache.put(event.request, fetchResponse.clone());
                                                console.log('Updated cache for:', url.pathname);
                                            })
                                            .catch(console.error);
                                    }
                                })
                                .catch(() => {
                                    // Ignore network errors in background update
                                });
                        }
                        
                        return cachedResponse;
                    }
                    
                    console.log('Not in cache, fetching:', url.pathname);
                    
                    // If not in cache, fetch from network
                    return fetch(event.request)
                        .then((fetchResponse) => {
                            if (fetchResponse && fetchResponse.status === 200 && fetchResponse.type === 'basic') {
                                const responseToCache = fetchResponse.clone();
                                caches.open(CACHE_NAME)
                                    .then((cache) => {
                                        cache.put(event.request, responseToCache);
                                        console.log('Cached:', url.pathname);
                                    })
                                    .catch(console.error);
                            }
                            return fetchResponse;
                        })
                        .catch((error) => {
                            console.error('Fetch failed for:', url.pathname, error);
                            
                            // For the main page, return a basic offline page
                            if (url.pathname === '/') {
                                return new Response(`
                                    <!DOCTYPE html>
                                    <html lang="en">
                                    <head>
                                        <title>AI Chatbot - Offline</title>
                                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                        <meta charset="UTF-8">
                                        <style>
                                            * {
                                                margin: 0;
                                                padding: 0;
                                                box-sizing: border-box;
                                            }
                                            body { 
                                                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                                                display: flex; 
                                                justify-content: center; 
                                                align-items: center; 
                                                min-height: 100vh; 
                                                margin: 0; 
                                                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                                                color: white;
                                                text-align: center;
                                                padding: 20px;
                                            }
                                            .container { 
                                                max-width: 400px; 
                                                padding: 30px; 
                                                background: rgba(255, 255, 255, 0.1);
                                                border-radius: 20px;
                                                backdrop-filter: blur(10px);
                                                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                                            }
                                            h1 { 
                                                margin-bottom: 20px; 
                                                font-size: 2.5em;
                                                font-weight: 300;
                                            }
                                            p {
                                                margin-bottom: 30px;
                                                font-size: 1.1em;
                                                line-height: 1.6;
                                                opacity: 0.9;
                                            }
                                            button { 
                                                background: rgba(255, 255, 255, 0.2); 
                                                color: white; 
                                                border: 2px solid rgba(255, 255, 255, 0.3);
                                                padding: 15px 30px; 
                                                border-radius: 50px; 
                                                cursor: pointer;
                                                font-size: 16px;
                                                font-weight: 600;
                                                transition: all 0.3s ease;
                                                text-transform: uppercase;
                                                letter-spacing: 1px;
                                            }
                                            button:hover { 
                                                background: rgba(255, 255, 255, 0.3);
                                                border-color: rgba(255, 255, 255, 0.5);
                                                transform: translateY(-2px);
                                                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
                                            }
                                            .status {
                                                font-size: 0.9em;
                                                opacity: 0.7;
                                                margin-top: 20px;
                                            }
                                        </style>
                                    </head>
                                    <body>
                                        <div class="container">
                                            <h1>🤖</h1>
                                            <h2>AI Chatbot</h2>
                                            <p>You're currently offline. Please check your internet connection to continue chatting with the AI assistant.</p>
                                            <button onclick="window.location.reload()">Try Again</button>
                                            <div class="status">Service Worker Active</div>
                                        </div>
                                        <script>
                                            // Auto-retry when online
                                            window.addEventListener('online', () => {
                                                window.location.reload();
                                            });
                                            
                                            // Check connection periodically
                                            setInterval(() => {
                                                if (navigator.onLine) {
                                                    fetch('/')
                                                        .then(() => window.location.reload())
                                                        .catch(() => {});
                                                }
                                            }, 5000);
                                        </script>
                                    </body>
                                    </html>
                                `, {
                                    headers: {
                                        'Content-Type': 'text/html; charset=utf-8',
                                    },
                                });
                            }
                            
                            throw error;
                        });
                })
                .catch((error) => {
                    console.error('Cache match failed for:', url.pathname, error);
                    return fetch(event.request);
                })
        );
    }
});

// Handle messages from the main thread
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
});

// Provide version info
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'GET_VERSION') {
        event.ports[0].postMessage({
            version: CACHE_NAME,
            cached_assets: STATIC_ASSETS.length
        });
    }
});
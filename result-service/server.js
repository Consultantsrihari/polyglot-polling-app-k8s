// ./result-service/server.js
const express = require('express');
const redis = require('redis');

const app = express();
const PORT = 80;

// Create Redis client
const redisClient = redis.createClient({
    // The URL uses the hostname 'redis' from our Docker Compose setup
    url: `redis://${process.env.REDIS_HOST || 'redis'}:6379`
});

redisClient.on('error', (err) => console.log('Redis Client Error', err));

app.get('/', async (req, res) => {
    try {
        // Get all vote counts from the 'votes' hash
        const votes = await redisClient.hGetAll('votes');
        const catVotes = votes.cats || 0;
        const dogVotes = votes.dogs || 0;

        // Simple HTML response to display the results
        res.send(`
            <html>
                <head>
                    <title>Polling Results</title>
                    <style>
                        body { font-family: sans-serif; container; text-align: center; padding-top: 50px; }
                        .result { border: 1px solid #ccc; padding: 20px; margin: 20px auto; width: 200px; }
                    </style>
                    <meta http-equiv="refresh" content="5">
                </head>
                <body>
                    <h1>Polling Results</h1>
                    <div class="result">Cats: ${catVotes}</div>
                    <div class="result">Dogs: ${dogVotes}</div>
                </body>
            </html>
        `);
    } catch (err) {
        console.error(err);
        res.status(500).send('Error retrieving votes');
    }
});

// Start the server after connecting to Redis
(async () => {
    await redisClient.connect();
    app.listen(PORT, '0.0.0.0', () => {
        console.log(`Result service listening on port ${PORT}`);
    });
})();
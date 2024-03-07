#!/usr/bin/node
/**
 * Connecting  to redis server
 */
import { createClient, print } from 'redis';

const clnt = createClient();

clnt.on('error', (err) => {
  console.log('Redis client not connected to the server:', err.toString());
});

clnt.on('connect', () => {
  console.log('Redis client connected to the server');
});

clnt.MULTI()
  .HSET('HolbertonSchools', 'Portland', 50, print)
  .HSET('HolbertonSchools', 'Seattle', 80, print)
  .HSET('HolbertonSchools', 'New York', 20, print)
  .HSET('HolbertonSchools', 'Bogota', 20, print)
  .HSET('HolbertonSchools', 'Cali', 40, print)
  .HSET('HolbertonSchools', 'Paris', 2, print)
  .EXEC();

clnt.HGETALL('HolbertonSchools', (err, hashSet) => {
  console.log(hashSet);
});

#!/usr/bin/node
/**
 * Connecting  to redis server
 */
import { createClient } from 'redis';

const clnt = createClient();

clnt.on('error', (err) => {
  console.log('Redis client not connected to the server:', err.toString());
});

clnt.on('connect', () => {
  console.log('Redis client connected to the server');
});

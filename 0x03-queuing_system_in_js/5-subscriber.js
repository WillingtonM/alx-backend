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

const msgListener = (msg) => console.log(msg);

clnt.SUBSCRIBE('holberton school channel');

clnt.on('message', (chnl, msg) => {
  if (chnl === 'holberton school channel') {
    if (msg === 'KILL_SERVER') {
      clnt.UNSUBSCRIBE();
      clnt.QUIT();
    }
    msgListener(msg);
  }
});

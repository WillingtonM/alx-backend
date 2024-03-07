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

function setNewSchool(schoolName, val) {
  clnt.SET(schoolName, val, print);
}

function displaySchoolValue(schoolName) {
  clnt.GET(schoolName, (err, val) => {
    console.log(val);
  });
}

displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');

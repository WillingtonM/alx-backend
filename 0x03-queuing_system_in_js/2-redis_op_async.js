#!/usr/bin/node
/**
 * Connecting  to redis server
 */
import { promisify } from 'util';
import { createClient, print } from 'redis';

const clnt = createClient();

clnt.on('error', (err) => {
  console.log('Redis client not connected to the server:', err.toString());
});

clnt.on('connect', () => {
  console.log('Redis client connected to the server');
});

function setNewSchool(schoolName, value) {
  clnt.SET(schoolName, value, print);
}

async function displaySchoolValue(schoolName) {
  const GET = promisify(clnt.GET).bind(clnt);
  try {
    const val = await GET(schoolName);
    console.log(val);
  } catch (err) {
    console.log(err.toString());
  }
}

(async () => {
  await displaySchoolValue('Holberton');
  setNewSchool('HolbertonSanFrancisco', '100');
  await displaySchoolValue('HolbertonSanFrancisco');
})();

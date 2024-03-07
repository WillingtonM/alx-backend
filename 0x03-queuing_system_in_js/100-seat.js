#!/usr/bin/node
/**
 * Can I have a seat
 */
import { promisify } from 'util';
import { createClient } from 'redis';
import { createQueue } from 'kue';
import express from 'express';

const clientRedis = createClient();
let enabledReservation;

clientRedis.on('error', (err) => {
  console.log('Redis client not connected to the server:', err.toString());
});

function seatReserve(num) {
  return clientRedis.SET('available_seats', num);
}

function getCurrAvailableSeat() {
  const GET = promisify(clientRedis.GET).bind(clientRedis);
  return GET('available_seats');
}

const queueCreate = createQueue();

const app = express();

app.get('/available_seats', (req, res) => {
  getCurrAvailableSeat().then((seats) => {
      res.json({ numberOfAvailableSeats: seats });
    }).catch((err) => {
      console.log(err);
      res.status(500).json(null);
    });
});

app.get('/reserve_seat', (req, res) => {
  if (enabledReservation === false) {
    return res.json({ status: 'Reservation are blocked' });
  }
  const qjob = queueCreate.create('reserve_seat', { task: 'reserve a seat' });
  qjob.on('complete', (status) => {
      console.log(`Seat reservation job ${qjob.id} completed`);
    }).on('failed', (err) => {
      console.log(`Seat reservation job ${qjob.id} failed: ${err.message || err.toString()}`);
    }).save((err) => {
      if (err) return res.json({ status: 'Reservation failed' });
      return res.json({ status: 'Reservation in process' });
    });
});

app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });
  queueCreate.process('reserve_seat', async (job, done) => {
    let availSeats = await getCurrAvailableSeat();
    availSeats -= 1;
    seatReserve(availSeats);
    if (availSeats >= 0) {
      if (availSeats === 0) enabledReservation = false;
      done();
    }
    done(new Error('Not enough seats available'));
  });
});

app.listen(1245, () => {
  seatReserve(50);
  enabledReservation = true;
  console.log('API available on localhost via port 1245');
});

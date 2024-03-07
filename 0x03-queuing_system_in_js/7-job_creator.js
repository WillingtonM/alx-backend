#!/usr/bin/node
/**
 * Track progress and errors with Kue
 */
import { createQueue } from 'kue';

const queueCreate = createQueue();

const jobs = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account',
  },
  {
    phoneNumber: '4153518781',
    message: 'This is the code 4562 to verify your account',
  },
  {
    phoneNumber: '4153518743',
    message: 'This is the code 4321 to verify your account',
  },
  {
    phoneNumber: '4153538781',
    message: 'This is the code 4562 to verify your account',
  },
  {
    phoneNumber: '4153118782',
    message: 'This is the code 4321 to verify your account',
  },
  {
    phoneNumber: '4153718781',
    message: 'This is the code 4562 to verify your account',
  },
  {
    phoneNumber: '4159518782',
    message: 'This is the code 4321 to verify your account',
  },
  {
    phoneNumber: '4158718781',
    message: 'This is the code 4562 to verify your account',
  },
  {
    phoneNumber: '4153818782',
    message: 'This is the code 4321 to verify your account',
  },
  {
    phoneNumber: '4154318781',
    message: 'This is the code 4562 to verify your account',
  },
  {
    phoneNumber: '4151218782',
    message: 'This is the code 4321 to verify your account',
  },
];

for (let qjob of jobs) {
  qjob = queueCreate.create('push_notification_code_2', qjob);
  qjob.on('complete', (res) => {
      console.log(`Notification job ${qjob.id} completed`);
    })
    .on('failed', (err) => {
      console.log(`Notification job ${qjob.id} failed: ${err.message || err.toString()}`);
    })
    .on('progress', (prog, data) => {
      console.log(`Notification job ${qjob.id} ${prog}% complete`);
    })
    .save((err) => {
      console.log(`Notification job created: ${qjob.id}`);
    });
}

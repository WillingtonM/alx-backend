#!/usr/bin/node
/**
 * Create job
 */
import { createQueue } from 'kue';

const queueCreate = createQueue();
const dataJob = { phoneNumber: '+27762345123', message: 'Kindly verify your identification' };

const qjob = queueCreate
  .create('push_notification_code', dataJob)
  .save((err) => {
    if (!err) console.log(`Notification job created: ${qjob.id}`);
  });

qjob.on('complete', (res) => {
  console.log('Notification job completed');
});

qjob.on('failed', (err) => {
  console.log('Notification job failed');
});

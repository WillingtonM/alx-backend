#!/usr/bin/node
/**
 * Job processor
 */
import { createQueue } from 'kue';

const queueCreate = createQueue();

function sendNotification(phoneNumber, message) {
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
}

queueCreate.process('push_notification_code', (jobNotif, done) => {
  sendNotification(jobNotif.data.phoneNumber, jobNotif.data.message);
  done();
});

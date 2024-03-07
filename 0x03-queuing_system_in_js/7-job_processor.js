#!/usr/bin/node
/**
 * Track progress and errors with Kue
 */
import { createQueue } from 'kue';

const blcklist = ['4153518780', '4153518781'];

const queueCreate = createQueue();

function sendNotification(phoneNumber, message, job, done) {
  const tot = 100;
  function next(pos) {
    if (pos === 0 || pos === (tot / 2)) {
      job.progress(p, tot);
      if (pos === (tot / 2)) {
        console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
      }
    }
    if (blcklist.includes(job.data.phoneNumber)) {
      return done(new Error(`Phone number ${job.data.phoneNumber} is blacklisted`));
    }
    if (pos === tot) {
      return done();
    }
    return next(pos + 1);
  }
  next(0);
}

queueCreate.process('push_notification_code_2', 2, (qjob, done) => {
  sendNotification(qjob.data.phoneNumber, qjob.data.message, qjob, done);
});

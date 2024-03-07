#!/usr/bin/node
/**
 * Writing job creation function
 */
function createPushNotificationsJobs(jobs, queue) {
  if (!(jobs instanceof Array)) {
    throw new Error('Jobs is not an array');
  }
  for (let qjob of jobs) {
    qjob = queue.create('push_notification_code_3', qjob);
    qjob
      .on('complete', (res) => {
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
}

module.exports = createPushNotificationsJobs;

#!/usr/bin/node
/**
 * Writing test for job creation
 */
import { createQueue } from 'kue';
import chai from 'chai';
import sinon from 'sinon';
import createPushNotificationsJobs from './8-job';

const chaiExpect = chai.expect;

const queueCreate = createQueue();

const jobs = [
  {
    phoneNumber: '4153518780',
    message: 'This is the code 1234 to verify your account',
  },
];

describe('createPushNotificationsJobs', () => {
  beforeEach(() => {
    sinon.spy(console, 'log');
  });

  before(() => {
    queueCreate.testMode.enter();
  });

  afterEach(() => {
    sinon.restore();
    queueCreate.testMode.clear();
  });

  after(() => {
    queueCreate.testMode.exit()
  });

  it('Display error message if jobs is not an array', () => {
    chaiExpect(() => createPushNotificationsJobs(1, queueCreate)).to.throw();
    chaiExpect(() => createPushNotificationsJobs(1, queueCreate)).to.throw(/Jobs is not an array/);
  });

  it('Throws error if queue is not a valid kue', function() {
    chaiExpect(() => createPushNotificationsJobs(jobs, "")).to.throw();
  });

  it('Test creation of jobs', () => {
    createPushNotificationsJobs(jobs, queueCreate);
    chaiExpect(queueCreate.testMode.jobs.length).to.equal(1);
    chaiExpect(queueCreate.testMode.jobs[0].type).to.equal('push_notification_code_3');
    chaiExpect(queueCreate.testMode.jobs[0].data).to.eql(jobs[0]);
    chaiExpect(console.log.calledOnceWith(`Notification job created: ${queueCreate.testMode.jobs[0].id}`)).to.be.true;
  });

  it('Test job progress event report', (done) => {
    createPushNotificationsJobs(jobs, queueCreate);
    queueCreate.testMode.jobs[0].addListener('progress', () => {
      const qid = queueCreate.testMode.jobs[0].id;
      chaiExpect(console.log.calledWith(`Notification job ${qid} 50% complete`)).to.be.true;
      done();
    });
    queueCreate.testMode.jobs[0].emit('progress', 50, 100);
  });

  it('test job failed event report', (done) => {
    createPushNotificationsJobs(jobs, queueCreate);
    queueCreate.testMode.jobs[0].addListener('failed', () => {
      const qid = queueCreate.testMode.jobs[0].id;
      chaiExpect(console.log.calledWith(`Notification job ${qid} failed: job failed!`)).to.be.true;
      done();
    });
    queueCreate.testMode.jobs[0].emit('failed', new Error('job failed!'));
  });

  it('test job completed event report', (done) => {
    createPushNotificationsJobs(jobs, queueCreate);
    queueCreate.testMode.jobs[0].addListener('complete', () => {
      const qid = queueCreate.testMode.jobs[0].id;
      chaiExpect(console.log.calledWith(`Notification job ${qid} completed`)).to.be.true;
      done();
    });
    queueCreate.testMode.jobs[0].emit('complete', true);
  });
});

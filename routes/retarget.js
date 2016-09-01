var express = require('express');
var http    = require('http');
var _       = require('underscore');
var request = require('request');
var qs      = require('querystring');
//var simple_recaptcha = require('simple-recaptcha');
var router  = express.Router();

router.get('/', function(req, res) {
	var db 		= req.retargetdb;
	console.log(req.query);
	if (!req.query['hitId'] || req.query['hitId']=="TEST"){
		res.render('retarget', { title: 'Retargeted Design Evaluation', type: 1 });
	}else{
		db.collection('experimentType').find_one({'hit_id':req.query['hitId']}, function(err, result) {
	        if (result) {
						console.log(req.query['hitId']+", " + result[0]['type']);
						res.render('retarget', { title: 'Retargeted Design Evaluation', type: result[0]['type'] });
	        }
	    });

	}

});

router.post('/log', function(req, res){
	var db 		= req.retargetdb;
	var newLog	= {};
  newLog.timestamp         = req.body.timestamp;
	newLog.hit_id 		     = req.body.hitId;
	newLog.assignment_id     = req.body.assignmentId;
	newLog.worker_id 	     = req.body.workerId;
	newLog.action 		     = req.body.action;
	newLog.data 		     = req.body.data;
	db.collection('logs').insert(newLog, function(err, result) {
        if (err) {
            return console.log(new Date(), 'insert error', err);
        }
        if (result) {
            res.json({ code: 0, message: 'Successfully Created!', result: result[0]});
        }
    });

});
module.exports = router;

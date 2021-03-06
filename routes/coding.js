var express = require('express');
var http    = require('http');
var _       = require('underscore');
var request = require('request');
var qs      = require('querystring');
//var simple_recaptcha = require('simple-recaptcha');
var router  = express.Router();

router.get('/', function(req, res) {
	console.log(req.params);
  	res.render('coding', { title: 'Evaluation Experiment' });
});
/*
router.get('/admin', function(req, res) {
    console.log(req.params);
    res.render('bubble_admin', { title: 'Bubble Experiment Admin' });
});*/
router.get('/images', function(req, res){
	var db = req.codingdb;
	var hitId = req.query.hitId;
    console.log(hitId);
    var query = {hit_id: hitId};
    if (hitId.search("TEST")!=-1){
        query = {};
    }
	db.collection('stimuli').find(query).toArray(function(err, result){
        if (err) {
            return console.log(new Date(), 'error in loading images', err);
        }
        console.log(result);
        if (result) {
            var images = result;  
                      
            if (hitId.search("TEST")!=-1){
                images = _.sample(images, 5);
            }
            // target images
            var targets = _.map(images, function(img){ return { url: img.img_url, desc:img.desc, pid: img.pid }; })

            res.json({ targets: targets });
        }
	});
});
router.post('/recaptcha', function(req, res){
    
    var postData = {
        secret :'6LcvMf8SAAAAANwRhpM0Mt7JH46AqFDwnfMzMiHg',
        ip : req.ip,
        response : req.body.recaptcha_response
    };
    var url = 'https://www.google.com/recaptcha/api/siteverify?'+qs.stringify(postData);
    console.log(url);
    
    // Set up the request
    request.post(
        url,
        {},
        function (error, response, body){
            if (!error && response.statusCode == 200) {
                
                
                body = JSON.parse(body);
                console.log(body);
                if (body.success==true){
                    res.send({code: 0, message:"successfully verified!"});
                }else{
                    res.send({code: 1, message:"verification failed!"});
                }
            }
        });

/*
    simple_recaptcha(privateKey, ip, challenge, response, function(err) {
        if (err) res.send({code: 1, message:err.message});
        res.send({code: 0, message:"verified!"});
    });
*/
});
/*
router.get('/logs', function(req, res){
    var db = req.codingdb;
    console.log(req.query);
    var pageSize = parseInt(req.query.pageSize);
    var lastID   = req.query.lastID;
    var query    = {}
    if (lastID!=''){
        query._id = { '$gt':req.toObjectID(lastID) };
    }
    console.log(query);
    db.collection('logs').find(query).sort({"_id":1}).limit(pageSize).toArray(function(err, result){
        if (err) {
            return console.log(new Date(), 'error in loading images', err);
        }
        console.log('loaded: ' + result.length);
        if (result.length!=0) {
            
            res.json({ lastID : result[result.length-1]._id, logs : result});
        }else{
            res.json({lastID: null, logs: result})
        }
    });
})*/
router.post('/log', function(req, res){
	var db 		= req.codingdb;
	var newLog	= {};
    newLog.timestamp         = req.body.timestamp;
	newLog.hit_id 		     = req.body.hitId;
	newLog.assignment_id     = req.body.assignmentId;
	newLog.worker_id 	     = req.body.workerId;
	newLog.action 		     = req.body.action;
	newLog.data 		     = req.body.data;	
    console.log(newLog);
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
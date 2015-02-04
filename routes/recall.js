var express = require('express');
var http    = require('http');
var _       = require('underscore');
var request = require('request');
var qs      = require('querystring');
//var simple_recaptcha = require('simple-recaptcha');
var router  = express.Router();

router.get('/', function(req, res) {
	console.log(req.params);
  	res.render('recall', { title: 'Visualization Recall Study' });
});
router.get('/admin', function(req, res) {
    console.log(req.params);
    res.render('recall_admin', { title: 'Recall Experiment Admin' });
});
router.get('/inspect_images', function(req, res) {
    console.log(req.params);
    res.render('recall-image-inspection', { title: 'Recall Experiment Image Inspection' });
});
router.get('/all_images', function(req, res){
    var db = req.recalldb;
    db.collection('images').find().toArray(function(err, result){
        if (err) {
            return console.log(new Date(), 'error in loading images', err);
        }
        
        if (result) {
            res.json({ images : result});            
        }
    });
}); 
router.get('/images', function(req, res){
	var db = req.recalldb;
	var hitId = req.query.hitId;
    console.log(hitId);
    var query = {hit_id: hitId};
    if (hitId.search("TEST")!=-1){
        query = {};
    }    
	db.collection('images').find(query).toArray(function(err, result){
        if (err) {
            return console.log(new Date(), 'error in loading images', err);
        }
        
        if (result) {
            var images = result;

            if (hitId.search("TEST")!=-1){
                images = _.filter(images, function(assignment){
                    return assignment.group==8;
                });               
            }
            var group = images[0].group;
            //console.log('group: ' + group);
            db.collection('progress').find({group: group }).toArray(function(err, progress){

                var minAssignment = _.min(progress, function(assignment){ return assignment.count});
                var finalSet = _.filter(images, function(assignment){ return assignment.group==group && assignment.instance==minAssignment.instance; })
                //console.log('instance: ' + minAssignment.instance);
                console.log(finalSet);
                minAssignment.count = parseInt(minAssignment.count) + 1;
                console.log(minAssignment);
                db.collection('progress').update({group: minAssignment.group, instance: minAssignment.instance }, { "$set": {count: minAssignment.count}}, 
                    function(err, result){
                        if (err) {
                            return console.log(new Date(), 'update error', err);
                        }
                        if (result) {            
                            res.json({ assignment: minAssignment, targets: finalSet[0].img_urls });
                        }

                    });
                
            })
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
});
router.put('/progress', function(req, res){
    var db      = req.recalldb;
    var query  = {};
    query.group     = parseInt(req.body.group);
    query.instance  = parseInt(req.body.instance);
    var newCount    = parseInt(req.body.count);

    console.log(query);
    console.log("count: " + newCount);
    db.collection('progress').update(query, { "$set": {count: newCount}}, function(err, result) {
        if (err) {
            return console.log(new Date(), 'update error', err);
        }
        console.log(result);
        if (result) {            
            res.json({ code: 0, message: 'Successfully Updated!', result: result[0]});
        }

    });

});
router.get('/logs', function(req, res){
    var db = req.recalldb;
    db.collection('logs').find().toArray(function(err, result){
        if (err) {
            return console.log(new Date(), 'error in loading images', err);
        }
        //console.log(result);
        if (result) {
            
            res.json(result);
        }
    });
})
router.post('/log', function(req, res){
	var db 		= req.recalldb;
	var newLog	= {};
    newLog.timestamp    = req.body.timestamp;
    newLog.hit_id            = req.body.hitId;
    newLog.assignment_id     = req.body.assignmentId;
    newLog.worker_id         = req.body.workerId;
	newLog.action 		= req.body.action;
    newLog.group        = req.body.group;
    newLog.instance     = req.body.instance;
	newLog.data 		= req.body.data;	
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
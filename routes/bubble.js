var express = require('express');
var http    = require('http');
var _       = require('underscore');
var request = require('request');
var qs      = require('querystring');
//var simple_recaptcha = require('simple-recaptcha');
var router  = express.Router();

router.get('/', function(req, res) {
	console.log(req.params);
  	res.render('bubble', { title: 'Bubble Experiment' });
});
router.get('/images', function(req, res){
	var db = req.bubbledb;
	var hitId = req.body.hitId;
	db.collection('images').find().toArray(function(err, result){
        if (err) {
            return console.log(new Date(), 'error in loading images', err);
        }
        //console.log(result);
        if (result) {
            var images = result;
            
            // target images
            var targets = _.take(_.map(images, function(img){ return img.img_url; }), 3);

            // filler images
            var blurred = _.take(_.map(images, function(img){ return img.blur_img_url; }), 3);

            res.json({ targets: targets, blurred: blurred});
        }
	});
});
router.post('/recaptcha', function(req, res){
    
    var postData = {
        secret :'6Lc4B_8SAAAAALzTevL05JYiED5zHfiLaHNE2KwJ',
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
router.post('/log', function(req, res){
	var db 		= req.bubbledb;
	var newLog	= {};
	newLog.hitId 		= req.body.hitId;
	newLog.assignmentId = req.body.assignmentId;
	newLog.workerId 	= req.body.workerId;
	newLog.action 		= req.body.action;
	newLog.data 		= req.body.data;	
    console.log(newLog);
	db.collection('logs').insert(newLog, function(err, result) {
        if (err) {
            return console.log(new Date(), 'insert error', err);
        }
        if (result) {            
            res.json({ code: 0, message: 'Successfully Created!', recall: result[0]});
        }

    });

});
module.exports = router;
var express = require('express');
var router = express.Router();
var _ = require('underscore');

router.get('/', function(req, res) {
	console.log(req.params);
  	res.render('bubble', { title: 'Bubble Experiment' });
});
router.get('/images', function(req, res){
	var db = req.bubbledb;
	var hitID = req.body.hitID;
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
router.post('/log', function(req, res){
	var db 		= req.bubbledb;
	var newLog	= {};
	newLog.hitID 		= req.body.hitID;
	newLog.assignmentID = req.body.assignmentID;
	newLog.workderID 	= req.body.workderID;
	newLog.action 		= req.body.action;
	newLog.data 		= req.body.data;	
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
var express = require('express');
var router = express.Router();
var _ = require('underscore');
/* GET home page. */
router.get('/', function(req, res) {
    console.log(req.params);
  res.render('index', { title: 'Memorability Experiment' });
});
router.get('/test', function(req, res) {
    console.log(req.params);
  res.render('test', { title: 'Coding Test' });
});
router.get('/images', function(req, res){
	var db = req.db;
	db.collection('images').find().toArray(function(err, result){
        if (err) {
            return console.log(new Date(), 'error in loading images', err);
        }
        //console.log(result);
        if (result) {
            var images = result;
            
            // target images
            var targets = _.take(_.shuffle(images), 1);

            // filler images
            var fillers = _.take(_.shuffle(images), 1);

            res.json({ targets: targets, fillers: fillers});
        }
	});
});
router.post('/desc', function(req, res){
	var db 		= req.db;
	var newRecall = {imgId: req.body.imgId, imgUrl: req.body.imgUrl, imgDesc: req.body.imgDesc};
	db.collection('recall').insert(newRecall, function(err, result) {
        if (err) {
            return console.log(new Date(), 'insert error', err);
        }
        if (result) {            
            res.json({ code: 0, message: 'Successfully Created!', recall: result[0]});
        }

    });

});
module.exports = router;

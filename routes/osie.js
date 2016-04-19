var express = require('express');
var http = require('http');
var _ = require('underscore');
var request = require('request');
var qs = require('querystring');
//var simple_recaptcha = require('simple-recaptcha');
var router = express.Router();

router.get('/', function(req, res) {
  console.log(req.params);
  res.render('osie', {
    title: 'BubbleView Experiment'
  });
});
router.get('/eval', function(req, res) {
    console.log(req.params);
    res.render('osie_eval', { title: 'BubbleView Experiment Admin' });
});
// router.get('/eval', function(req, res) {
//     console.log(req.params);
//     res.render('osie_eval', { title: 'Salicon Experiment Admin' });
// });


router.get('/images', function(req, res) {
  var db = req.osiedb;
  var hitId = req.query.hitId;
  console.log(hitId);
  var query = {
    hit_id: hitId
  };
  if (hitId.search("TEST") != -1) {
    query = {};
  }
  db.collection('images').find(query).toArray(function(err, result) {
    if (err) {
      return console.log(new Date(), 'error in loading images', err);
    }

    if (result) {
      var images = result;

      if (hitId.search("TEST")!=-1){
          images = _.sample(images, 2);
      }
      // target images
      var shuffled = _.shuffle(images);
      var targets = _.map(shuffled, function(img) {
          return img.img_url;
        })
        // filler images
      var blurred = _.map(shuffled, function(img) {
        return img.blur_img_url;
      })
      // console.log(images);
      //set experimental conditions

      res.json({
        targets: targets,
        blurred: blurred
      });
    }
  });
});
router.post('/recaptcha', function(req, res) {
  var postData = {
    secret: '6LcvMf8SAAAAANwRhpM0Mt7JH46AqFDwnfMzMiHg',
    ip: req.ip,
    response: req.body.recaptcha_response
  };
  var url = 'https://www.google.com/recaptcha/api/siteverify?' + qs.stringify(postData);
  console.log(url);

  // Set up the request
  request.post(
    url, {},
    function(error, response, body) {
      if (!error && response.statusCode == 200) {


        body = JSON.parse(body);
        console.log(body);
        if (body.success == true) {
          res.send({
            code: 0,
            message: "successfully verified!"
          });
        } else {
          res.send({
            code: 1,
            message: "verification failed!"
          });
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
router.get('/ratings', function(req, res){
    var db = req.osiedb;
    var rater = req.query.rater;
    console.log(rater);
    db.collection('expertRatings').find({ rater: rater}).toArray(function(err, result){
        res.json(result);
    });
})
router.post('/rating', function(req, res){
    var db      = req.osiedb;
    var rating  = {};
    rating.hit_id               = req.body.hit_id;
    rating.assignment_id        = req.body.assignment_id;
    rating.image                = req.body.image;
    rating.rater                = req.body.rater;
    rating.relevancy            = req.body.relevancy;
    rating.accuracy             = req.body.accuracy;
    rating.comprehensive        = req.body.comprehensive;
    console.log(rating);
    db.collection('expertRatings').update(
        {image: rating.image, assignment_id: rating.assignment_id, rater: rating.rater},
        rating,
        { upsert: true },
        function(err, result) {
            if (err) {
                return console.log(new Date(), 'update error', err);
            }
            if (result) {
                res.json({ code: 0, message: 'Successfully updated!', result: result[0]});
            }

    });

});
router.get('/pagelogs', function(req, res){
    var db = req.osiedb;
    console.log(req.query);
    var pageSize = parseInt(req.query.pageSize);
    var pageNum  = parseInt(req.query.pageNum);
    var dbName   = req.query.dbName;
    console.log("pageSize = " + pageSize);

    if (dbName==null || dbName==''){
        dbName = "refLogs30x30"
    }
    console.log("dbName = " + dbName);
    // var lastID   = req.query.lastID;
    // var query    = {}
    // if (lastID!=''){
    //     query._id = { '$gt':req.toObjectID(lastID) };
    // }
    db.collection(dbName).count(function(err, count){
        db.collection(dbName).find({}, null, {
            limit:  pageSize,
            skip:   pageNum > 1 ? ((pageNum - 1) * pageSize) : 0,
            sort: {
                '_id': -1
            }
        }).toArray(function(err, result){
            if (err) {
                return console.log(new Date(), 'error in loading images', err);
            }
            console.log('loaded: ' + result.length);

            res.json({ pageNum : pageNum, pageSize:pageSize, totalPage: Math.ceil(count*1.0/pageSize), logs : result});
        });
    });

})
router.post('/log', function(req, res) {
  var db = req.osiedb;
  var newLog = {};
  newLog.timestamp = req.body.timestamp;
  newLog.hit_id = req.body.hitId;
  newLog.assignment_id = req.body.assignmentId;
  newLog.worker_id = req.body.workerId;
  newLog.action = req.body.action;
  newLog.data = req.body.data;
  // console.log(newLog);
  db.collection('logs').insert(newLog, function(err, result) {
    if (err) {
      return console.log(new Date(), 'insert error', err);
    }
    if (result) {
      res.json({
        code: 0,
        message: 'Successfully Created!',
        result: result[0]
      });
    }

  });

});
module.exports = router;

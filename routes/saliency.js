var express = require('express');
var http = require('http');
var _ = require('underscore');
var request = require('request');
var qs = require('querystring');
//var simple_recaptcha = require('simple-recaptcha');
var router = express.Router();


router.get('/filter', function(req, res) {
    console.log(req.params);
    res.render('saliency_filter', { title: 'Image Filtering Interface' });
});
// router.get('/eval', function(req, res) {
//     console.log(req.params);
//     res.render('salicon_eval', { title: 'Salicon Experiment Admin' });
// });


router.get('/images', function(req, res) {
  var db = req.saliencydb;

  db.collection('images').find().toArray(function(err, result) {
    if (err) {
      return console.log(new Date(), 'error in loading images', err);
    }

    if (result) {
      res.json(result);
    }
  });
});
// router.get('/pageimages', function(req, res){
//     var db = req.saliencydb;
//     console.log(req.query);
//     var pageSize = parseInt(req.query.pageSize);
//     var pageNum  = parseInt(req.query.pageNum);
//     db.collection('images').count(function(err, count){
//         db.collection('images').find({}, null, {
//             limit:  pageSize,
//             skip:   pageNum > 1 ? ((pageNum - 1) * pageSize) : 0,
//             sort: {
//                 '_id': -1
//             }
//         }).toArray(function(err, result){
//             if (err) {
//                 return console.log(new Date(), 'error in loading images', err);
//             }
//             console.log('loaded: ' + result.length);

//             res.json({ pageNum : pageNum, pageSize:pageSize, totalPage: Math.ceil(count*1.0/pageSize), logs : result});
//         });
//     });

// })
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
router.get('/checks', function(req, res){
    var db = req.saliencydb;
    var rater = req.query.rater;
    console.log(rater);
    db.collection('checks').find({ rater: rater}).toArray(function(err, result){
        res.json(result);
    });
})

router.post('/check', function(req, res){
    var db      = req.saliencydb;
    var check  = {};

    check.image             = req.body.image;
    check.rater             = req.body.rater;
    check.use               = req.body.use;
    check.is_graphic        = req.body.is_graphic;
    check.is_table          = req.body.is_table;
    check.is_infographic    = req.body.is_infographic;
    console.log(check);
    db.collection('checks').update(
        {image: check.image, rater: check.rater},
        check,
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

module.exports = router;

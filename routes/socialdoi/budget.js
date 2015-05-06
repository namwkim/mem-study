var express = require('express');
var http    = require('http');
var _       = require('underscore');
var request = require('request');
var qs      = require('querystring');
//var simple_recaptcha = require('simple-recaptcha');
var router  = express.Router();


router.get('/', function(req, res) {
	console.log(req.params);
  	res.render('./socialdoi/budget', { title: 'Budget Study' });
});
router.get('/cstree', function(req, res) {
    console.log(req.params);
    res.render('./socialdoi/cstree', { title: 'Budget Study' });
});
router.get('/doitree', function(req, res) {
    console.log(req.params);
    res.render('./socialdoi/doitree', { title: 'Budget Study' });
});
router.get('/vistest', function(req, res) {
    console.log(req.params);
    res.render('./socialdoi/vistest', { title: 'Budget Study' });
});
router.get('/doival', function(req, res){
    var db = req.socialdoi;
    db.collection('logs').find().toArray(function(err, result){
        var selected = _.chain(result)
                        .filter(function(d) { return d.action=="finish"})
                        .map(function(d){ return JSON.parse(d.data); })
                        .reduce(function(a, b){ return a.concat(b); }, [])     
                        .value();  

        var total = 0, maxCnt = 0;
        var bycabinet   = _.groupBy(selected, function(d){ return d.cabinet; })
        for (var i in bycabinet){
            total += bycabinet[i].length;
            if (bycabinet[i].length > maxCnt)
                maxCnt = bycabinet[i].length;
        }
        max = maxCnt/total;
        for (var i in bycabinet)
            bycabinet[i] = { visitCnt:bycabinet[i].length, visitRatio: bycabinet[i].length/total, visitDOI: max-bycabinet[i].length/total};
        
        var bydept      = _.groupBy(selected, function(d){ return d.department; })
        for (var i in bydept)
            bydept[i] = { visitCnt:bydept[i].length, visitRatio: bydept[i].length/total, visitDOI: max-bydept[i].length/total};

        var byprogram   = _.groupBy(selected, function(d){ return d.program; })
        for (var i in byprogram)
            byprogram[i] = { visitCnt:byprogram[i].length, visitRatio: byprogram[i].length/total, visitDOI: max-byprogram[i].length/total};

        res.json({ totalCnt: total, maxRatio: max, bycabinet: bycabinet, bydept: bydept, byprogram: byprogram });
    });
});
router.get('/budgets', function(req, res){
    var db = req.socialdoi;

    db.collection('budgets').find().toArray(function(err, result){
        
        console.log(result[0])
        
        var budgetname  = "Operating Budget 2015"
        var budgets     = { name: budgetname, budgetname : budgetname, children: []};
        var total       = 0;
        //group by cabinet
        var bycabinet   = _.groupBy(result, function(d){ return d.cabinet; })

        for (var cabinetName in bycabinet){
            var cabinet = { name: cabinetName, budgetname : budgetname, cabinet: cabinetName, children :[], approved:0}
            
            //group by department            
            var bydept = _.groupBy(bycabinet[cabinetName], function(d) { return d.department; })
            
            for (var deptName in bydept){
                var dept = { name: deptName, budgetname : budgetname, cabinet: cabinetName, department: deptName, approved:0}
                dept.children = _.sortBy(bydept[deptName], function(d){ return -d.approved; });
                dept.approved = _.reduce(bydept[deptName], function(m, d){ return m + d.approved; }, 0);

                _.each(dept.children, function(d){
                    d.name = d.program;
                })
                cabinet.children.push(dept);
            }
            cabinet.children = _.sortBy(cabinet.children, function(d){ return -d.approved; });
            cabinet.approved = _.reduce(cabinet.children, function(m, d){ return m + d.approved; }, 0);
            budgets.children.push(cabinet)
        }        
        budgets.children = _.sortBy(budgets.children, function(d){ return -d.approved; });
        budgets.approved = _.reduce(budgets.children, function(m, d){ return m + d.approved; }, 0);

        
        res.json(budgets);
    });
})



router.get('/logs', function(req, res){
    var db = req.socialdoi;
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
})
router.post('/log', function(req, res){
	var db 		= req.socialdoi;
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
module.exports = router;
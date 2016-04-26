var express = require('express');
var path = require('path');
//var favicon = require('serve-favicon');
var logger = require('morgan');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');

var routes          = require('./routes/index');
var bubbleRouter    = require('./routes/bubble');
var saliconRouter    = require('./routes/salicon');
var osieRouter    = require('./routes/osie');
var websalyRouter    = require('./routes/websaly');
var gdesignRouter    = require('./routes/gdesign');
var recallRouter    = require('./routes/recall');
var codingRouter    = require('./routes/coding');
var doiRouter    = require('./routes/socialdoi/index');

//var users = require('./routes/users');

var app = express();

// mongodb settings
var mongo = require('mongoskin');
var db = mongo.db("mongodb://localhost:27017/mem_study", {native_parser: true});
var bubbledb = mongo.db("mongodb://localhost:27017/bubblestudy", {native_parser: true});
var osiedb = mongo.db("mongodb://localhost:27017/osiestudy", {native_parser: true});
var salicondb = mongo.db("mongodb://localhost:27017/saliconstudy", {native_parser: true});
var websalydb = mongo.db("mongodb://localhost:27017/websalystudy", {native_parser: true});
var recalldb = mongo.db("mongodb://localhost:27017/recallstudy", {native_parser: true});
var codingdb = mongo.db("mongodb://localhost:27017/coding", {native_parser: true});
var socialdoidb = mongo.db("mongodb://localhost:27017/socialdoi", {native_parser: true});
var gdesigndb = mongo.db("mongodb://localhost:27017/gdesignstudy", {native_parser: true});

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'hjs');

//app.use(favicon());
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({
  extended: true
}));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public'), { dotfiles: 'allow'}));


// db settings
app.use(function(req, res, next){
    req.db = db;
    req.codingdb = codingdb;
    req.bubbledb = bubbledb;
    req.salicondb = salicondb;
    req.gdesigndb = gdesigndb;
    req.osiedb = osiedb;
    req.websalydb = websalydb;
    req.recalldb = recalldb;
    req.socialdoi = socialdoidb
    req.toObjectID = mongo.helper.toObjectID;
    next();
});

app.use('/', routes);
app.use('/coding', codingRouter);
app.use('/bubble', bubbleRouter);
app.use('/osie', osieRouter);
app.use('/websaly', websalyRouter);
app.use('/salicon', saliconRouter);
app.use('/recall', recallRouter);
app.use('/gdesign', gdesignRouter);
app.use('/socialdoi', doiRouter.budgetRouter);
//app.use('/users', users);

/// catch 404 and forward to error handler
app.use(function(req, res, next) {
    var err = new Error('Not Found');
    err.status = 404;
    next(err);
});

/// error handlers

// development error handler
// will print stacktrace
if (app.get('env') === 'development') {
    app.use(function(err, req, res, next) {
        res.status(err.status || 500);
        res.render('error', {
            message: err.message,
            error: err
        });
    });
}

// production error handler
// no stacktraces leaked to user
app.use(function(err, req, res, next) {
    res.status(err.status || 500);
    res.render('error', {
        message: err.message,
        error: {}
    });
});


module.exports = app;

var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {

    console.log("Index monitor index")

  res.render('index', { title: 'Cpu Monitor ' });
});

module.exports = router;

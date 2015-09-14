var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/cpu', function(req, res, next) {
    alert('CPU')
    console.log("CPU monitor index")
    res.send('this is a cpu!')
    // res.render('cpu', { title: 'Cpu Monitor view' });
});

module.exports = router;

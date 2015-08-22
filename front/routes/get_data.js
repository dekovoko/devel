var $ = require('jquery');
var express = require('express');
var router = express.Router();

router.post('/', function(err, req, res){
  console.log(err);
  connection = module.parent.exports('db_connection');
  console.log(req.body);
  select_get_l2id = 'select id, l2id from t_user where id = ? limit'
  connection.query(select_get_l2id, req.body,function  (err,result) {
    console.log(err);
    res.send('index', result);
  });
});

module.exports = router;

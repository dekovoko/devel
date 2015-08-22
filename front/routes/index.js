var express = require('express');
var router = express.Router();

router.get('/', function(req, res) {
  res.render('index', { title: 'Express' });
});

router.post('/login', function(req, res){

  id = req.body.id;
  pass = req.body.password;

  connection = module.parent.exports.set('db_connection');
  login_chk_sql = "select id, l2id from t_user where id = ? and password = ?";

  connection.query(login_chk_sql, [ id , pass ] , function (err, result) {
    //mysqlエラー時
    if ( err ) { res.render('index',{}); } 

    //IDがない・passwordが間違っている場合
    else if ( result.length == 0  ) {
          res.render('index', { title: 'Express' });
    }

    //ID・password一致の場合
    else {
      exports.index = function(req, res){
        //セッションありの場合
        if (req.session) { console.log(req.session); }
        else {
          req.session.user = { user: "hayo", pass: "fuga" };
          res.render('index', { title: 'Express' });
        }
      }
    }
  });
});

/*
router.post('/getid', function(req, res){
  id = req.body.id;
  pass = req.body.password;
  console.log(pass);
  connection = module.parent.exports.set('db_connection');
  get_l2id_sql = "select id, l2id from t_user where id = ? and password = ?";
  connection.query(get_l2id_sql, [ id , pass ] , function (err, result) {
    if ( err ) { res.send({}); }
    else if ( result.length == 0  ) { res.send({}); }
    else { res.send(result[0]); }
  });
});
*/



module.exports = router;

const express = require('express')
const path = require('path')
const PORT = process.env.PORT || 5000
const fs = require('fs');
const bodyParser = require('body-parser');

const app=express();

  app.use(express.static(path.join(__dirname, 'public')))
  app.set('views', path.join(__dirname, 'views'))
  app.set('view engine', 'ejs')
app.use(bodyParser.urlencoded({ extended: true }));

app.use(bodyParser.json())


//fs.writeSync("current.json",'{"abc":"123"}');




// handling get requests
app.get('/',(req,res)=>{
	let a =JSON.parse(fs.readFileSync('MinCout.json'))
	res.send(a)
})


app.get('/client',(req,res)=>{
	let a =JSON.parse(fs.readFileSync('MoutCin.json'))
	res.send(a)
})

app.get('/ui',(req,res)=>{
	 res.sendFile(path.join(__dirname + '/ui.html'));
})
app.get('/ui2',(req,res)=>{
	 res.sendFile(path.join(__dirname + '/ui2.html'));
})

app.post('/post', (req, res) => {
	console.log(req.body)
    fs.writeFileSync("MoutCin.json",JSON.stringify(req.body));
    res.sendStatus(200);
})
app.post('/clientpost',(req,res)=>{
	

	fs.writeFileSync("MinCout.json",JSON.stringify(req.body));
	res.sendStatus(200);
})

  
  app.listen(PORT, () => console.log(`Listening on ${ PORT }`))
//git add .
//git commit -m "Added a Procfile."
//git push heroku master
//https://litfur.herokuapp.com/
//fs.writeSync("abc.json",req.body);
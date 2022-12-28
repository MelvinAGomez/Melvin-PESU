var express =require("express")
var bodyParser =require("body-parser")
var mongoose = require("mongoose")
const path = require('path');
const publicPath=path.join(__dirname,'public')
const ejs = require('ejs')


const app =express()

app.use(bodyParser.json())
app.use(express.static(publicPath));
app.use(bodyParser.urlencoded({
	extended:true
}))

mongoose.connect('mongodb://localhost:27017/db_t',{
	useNewUrlParser:true,
	useUnifiedTopology:true
});

var db=mongoose.connection;
db.on('error',()=>console.log("error in connecting to database"));
db.once('open',()=>console.log("connected to database"));

/*db.createCollection("fav_songs", function(err, res) {  
if (err) throw err;  
console.log("fav_songs  is created!");  });*/

global.name;

app.post("/sign_up",async(req,res)=>{
	global.name =req.body.name;
	var email =req.body.email;
	var phno =req.body.phno;
	var password =req.body.password;
	
	var data = {
		"name" : global.name,
		"email" : email,
		"phno" : phno,
		"password" : password
	}
	
	var collection = await db.collection('users')
	data = await collection.find({})
	data = await data.toArray()
	
	var count = 0

	for(var i=0;i<data.length;i++)
	{	
		if(data[i].name == global.name && data[i].email == email && data[i].phno == phno && data[i].password == password)
		{
			count = 1;
		}
	}
	if(count == 1)
	{
		console.log("found")
	}
	else
	{
		console.log("incorrect detailis:deatils not found in dbs FU");
		return res.redirect('index.html')
	}

	
	return res.redirect('choose_genre.html')
})




app.use(express.static("public"));
app.post("/choose_genre",async(req,res)=>{
	global.genre1=req.body.KPOP;
	global.genre2=req.body.POP;
	global.genre3=req.body.RAP;
	global.genre4=req.body.ROCK;
	
	
	var 	favlist = db.collection('fav_songs');
	favsongs =await favlist.find({"user":name})
	favsongs =await favsongs.toArray()
	console.log(favsongs);
	
	
	
	
	if (genre1!=undefined){
		console.log(genre1);
		var songlist = await db.collection('user_songs')
		songs = await songlist.find({"user":"mels","genre":"KPOP"})
		songs = await songs.toArray()
		app.set('view engine','ejs');
		displaylist=[];
		favlist.deleteMany({"user":name});
		
		res.render('songs',{
			displaylist: songs,
			favlist:favsongs
			
		})
		
		
		//return res.redirect('songs.html')
	}
	if (genre2!=undefined){
		console.log(genre1);
		var songlist = await db.collection('user_songs')
		songs = await songlist.find({"user":"mels","genre":"POP"})
		songs = await songs.toArray()
		app.set('view engine','ejs');
		displaylist=[];
		
		
		res.render('songs',{
			displaylist: songs,
			favlist:favsongs
		})
	}
	if (genre3!=undefined){
		console.log(genre1);
		var songlist = await db.collection('user_songs')
		songs = await songlist.find({"user":"mels","genre":"RAP"})
		songs = await songs.toArray()
		app.set('view engine','ejs');
		displaylist=[];
		
		
		res.render('songs',{
			displaylist: songs,
			favlist:favsongs
		})
	}
	if (genre4!=undefined){
		console.log(genre1);
		var songlist = await db.collection('user_songs')
		songs = await songlist.find({"user":"mels","genre":"ROCK"})
		songs = await songs.toArray()
		app.set('view engine','ejs');
		displaylist=[];
		
		
		res.render('songs',{
			displaylist: songs,
			favlist:favsongs
		})
	}
	

})





app.post("/delete_song",async(req,res)=>{

Object.keys(req.body).forEach(async function(key){ 

		var songlist = db.collection('user_songs')
		
		var favlist = db.collection('fav_songs');
		favsongs =await favlist.find({"user":name})
		favsongs =await favsongs.toArray()
		//console.log(favsongs);
		
		var myquery = { "song": key };
		songlist.deleteOne(myquery, function(err, obj) {
		if (err) throw err;
		console.log("1 document deleted");
		})
		})
		
		
		


		
		if (genre1!=undefined){
		var songlist = await db.collection('user_songs')	
		songs = await songlist.find({"user":"mels","genre":"KPOP"})
		songs = await songs.toArray()
		app.set('view engine','ejs');
		displaylist=[];
		
		
		res.render('songs',{
			displaylist: songs,
			favlist:favsongs
		})
		
		
		//return res.redirect('songs.html')
	}
	if (genre2!=undefined){
		var songlist = await db.collection('user_songs')
		songs = await songlist.find({"user":"mels","genre":"POP"})
		songs = await songs.toArray()
		app.set('view engine','ejs');
		displaylist=[];
		
		
		res.render('songs',{
			displaylist: songs,
			favlist:favsongs
		})
	}
	if (genre3!=undefined){
		var songlist = await db.collection('user_songs')
		songs = await songlist.find({"user":"mels","genre":"RAP"})
		songs = await songs.toArray()
		app.set('view engine','ejs');
		displaylist=[];
		
		
		res.render('songs',{
			displaylist: songs,
			favlist:favsongs
		})
	}
	if (genre4!=undefined){
		var songlist = await db.collection('user_songs')
		songs = await songlist.find({"user":"mels","genre":"ROCK"})
		songs = await songs.toArray()
		app.set('view engine','ejs');
		displaylist=[];
		
		
		res.render('songs',{
			displaylist: songs,
			favlist:favsongs
		})
	}
		

})

app.use(express.static("public"));
app.post("/fav_song",async(req,res)=>{
	var songlist = await db.collection('fav_songs')
	
	Object.keys(req.body).forEach(function(key){ 
		songlist.insertOne({"user":name,"song":key})
		
	})
	    favsongs =await songlist.find({"user":name})
		favsongs =await favsongs.toArray()
		app.set('view engine','ejs');
		displaylist=[];
		
		console.log(favsongs);
		
		res.render('favsongs',{
		displaylist: favsongs   
		})
		
	
})




app.post("/removefav_song",async(req,res)=>{

Object.keys(req.body).forEach(function(key){ 

		var songlist = db.collection('fav_songs')
		
		var myquery = { "song": key };
		songlist.deleteOne(myquery, function(err, obj) {
		if (err) throw err;
		console.log("1 document deleted");
		})
		})
		
		var songlist = await db.collection('fav_songs')
		songs = await songlist.find({"user":name})
		songs = await songs.toArray()
		app.set('view engine','ejs');
		displaylist=[];
		
		
		res.render('favsongs',{
			displaylist: songs
		})
		

})











app.get("/",(req,res)=>{
	res.send("Hello From Server")
	res.set({
		"Allow-access-Allow-Origin": '*'
	})
	return res.redirect('index.html');
}).listen(3000);

console.log("listening on port 3000");
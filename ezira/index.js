const express = require('express');
const path = require('path');
var http = require("https");


const app = express();
//app.set('view engine', 'ejs');



var options = {
  "method": "GET",
  "hostname": "api.themoviedb.org",
  "port": null,
  "path": "/3/genre/movie/list?language=en-US&api_key=f78ad0ed633858582689fccb24551e90",
  "headers": {}
};

//GET Genres Information
var genre;

var req = http.request(options, function (res) {
  var chunks = [];

  res.on("data", function (chunk) {
    chunks.push(chunk);
  });

  res.on("end", function () {
    var body = Buffer.concat(chunks);
    console.log(body.toString());
    genre = JSON.parse(body);
  });
});

req.write("{}");
req.end();

app.get('/genre', (req, res) => {
  res.json(genre);
});

app.get('/',function(req,res)
{
  res.sendFile(path.join(__dirname + "/views/genres.html"));
});


//Set Static Folder
app.use(express.static(path.join(__dirname, 'public')));

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => console.log(`Server started on PORT ${PORT}`));

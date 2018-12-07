var twitter_data = d3.json("http://127.0.0.1:5000/approve").then( function(dat) {
  var approval = []
  var date = []

  for (i =0; i < dat.length; i++) {
    approval.push(dat[i].approve)
    date.push(dat[i].enddate)
  } 
  
  console.log(approval)

  var trace1 = {
    x: date,
    y: approval,
    type: 'lines'
  };

  var data = [trace1]

  Plotly.newPlot('myDiv', data);

});
var approve = d3.json("https://jammin-brah.herokuapp.com/compare").then( function(dat) {

  var approval = []
  var dates = []
  var favs = []

  for (i =0; i < dat.length; i++) {
    var date = new Date(dat[i].enddate['$date'])

    dates.push(date)
    approval.push(dat[i].adjusted_approve)
    favs.push(dat[i].Favs)
  } 
  
  console.log(approval)

  var trace1 = {
    x: dates,
    y: approval,
    type: 'lines',
    name: 'Approval Rating'
  };

  var trace2 = {
    x: dates,
    y: favs,
    type: 'lines',
    yaxis: 'y2',
    name: 'Twitter Favorites'
  }; 

  var layout = {
    title: 'Trump Approval vs. Twitter Favorites',
    yaxis: {title: 'Rating',
  },
    yaxis2: {
      title: 'Favorite Count',
      overlaying: 'y',
      side: 'right'
    }
  };


  var data = [trace1,trace2]

  Plotly.newPlot('myDiv', data, layout);

});

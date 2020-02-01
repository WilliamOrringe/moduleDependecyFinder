function setup() {
  createCanvas(800, 1000);
  background(255);
  translate(width / 2, height / 2);
  data = readTextFile("toDraw.txt")
  doStuff(data);
}
function doStuff(data){
  var new_data = split(data,"@")
  new_values = [];
  for(var i = 0; i < new_data.length; i++){
    var new_array = []
    new_array = split(new_data[i],")")
    new_values.push(new_array)
  }
  console.log(new_values)
  findLink(new_values);
}
let displayArray = [];
let new_list ="";
function findLink(new_values){
  displayArray = [];
  for(var i = new_values.length-2; i >= 0; i--){
    new_list = str(new_values[i][0]);
    var newStr = recurse(i,new_values,new_list);
    newStr = str(i) + ": " + str(newStr);
    displayArray.push(newStr);
  }
}
function recurse(index,new_values,addList){
  console.log(new_values[index] + " : " + new_values[index][2])
  if(new_values[index][2] == "None"){
    var nameOf = str(addList) + "------> None";
  //  console.log(addList);
    return nameOf;
  }else{
    for(var i = 0; i < new_values.length-1;i++){
    //  if(i != index){ // add a for loop here for inifinite dependencies
        if(new_values[index][2] == new_values[i][1]){
          console.log("DESCENDING" + ": i = " + str(i));
            addList = (addList + "------>" + str(new_values[i][0]));
          return recurse(i,new_values,addList);
        }
        if (new_values[index][3] == new_values[i][1]) {
            addList = (addList + "------>" + str(new_values[i][0]));
          return recurse(i,new_values,addList);
      }
    }
  }
  return addList + "------> " + str(new_values[index][2]);
}
var new_values = [];
let sSlider, pSlider;
let bool = true;
function draw() {
  var textSizes = 9;
  background(255);
  displayArray.sort(function(a,b){
    return a.length - b.length;
  })
  for(var i = 0; i < displayArray.length; i++){
    textSize(textSizes);
    text(displayArray[i],30,textSizes + i*14);
  }
}
let data= "";
function readTextFile(file)
{
  var datas = "";
    var rawFile = new XMLHttpRequest();
    rawFile.open("GET", file, false);
    rawFile.onreadystatechange = function ()
    {
        if(rawFile.readyState === 4)
        {
            if(rawFile.status === 200 || rawFile.status == 0)
            {
                var allText = rawFile.responseText;
                datas = (allText);
            }
        }
    }
    rawFile.send(null);
    return datas;
}

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
    new_array = split(new_data[i],":")
    new_values.push(new_array)
  }
  console.log(new_values)
  findLink(new_values);
}
let displayArray = [];
let new_list ="";
function findLink(new_values){
  displayArray = [];
  for(var i = new_values.length-1; i > 0; i--){
    new_list = new_values[i][0];
    var newStr = recurse(i,new_values,new_list);
    displayArray.push(newStr);
  }
}
function recurse(index,new_values,addList){
  if(new_values[index][2] == "None"){
    var nameOf = str(addList) + "------> None";
    console.log(addList);
    return nameOf;
  }else{
    for(var i = 0; i < new_values.length;i++){
      //console.log(new_values[index]);
      if(i != index){
      if(new_values[index][2] == new_values[i][1]){
        console.log("DESCENDING" + ": i = " + str(i));
        if(addList != str(new_values[index][0])){
          addList = (addList + "------>" + str(new_values[index][0]));
        }
        return recurse(i,new_values,addList);
      }else if (new_values[index][3] == new_values[i][1] && new_values[index][3] != null) {
        console.log("COOL" + str(i));
        if(addList != str(new_values[index][0])){
          addList = (addList +"------>" + str(new_values[index][0]));
        }
        return recurse(i,new_values,addList);
        }
      }
    }
    return addList;
  }
}
var new_values = [];
//var data = "";
let sSlider, pSlider;
let bool = true;
function draw() {
  background(255);
  for(var i = 0; i < new_values.length; i++){
    textSize(9);
    text(displayArray[i],30,i*14);
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

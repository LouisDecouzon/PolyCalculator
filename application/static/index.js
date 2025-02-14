function display(val){
    if(val == "AC"){
        document.getElementById("result").value=""
    }
    else{
        document.getElementById("result").value+=val
    }
}

function sendCalculus(){
    var calculus = document.getElementById("result").value
    console.log(calculus)
    console.log(JSON.stringify({ calculus: calculus }))
    fetch("/calculus",{
        method: 'POST', 
        headers:{
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ calculus: calculus })
    })
    .then(() => {
        document.getElementById("result").value = "";
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
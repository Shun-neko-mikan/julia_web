function startAPI(){
    let xhr = new XMLHttpRequest();
    let min_x = document.getElementById("min_x").value;
    let max_x = document.getElementById("max_x").value;
    let min_y = document.getElementById("min_y").value;
    let max_y = document.getElementById("max_y").value;
    let comp_const = document.getElementById("comp_const").value;
    let loader = document.getElementById("loader");
    
    loader.style.display = "block";
    xhr.open("GET","http://127.0.0.1:8000/satori/cal_julia?min_x="+min_x+"&max_x="+max_x+"&min_y="+min_y+"&max_y="+max_y+"&comp_const="+comp_const, true);
    xhr.responseType = "blob";
    let err_msg = document.getElementById("err_msg");
    let img = document.getElementById("img");
    err_msg.innerHTML = "";
    img.src = "";
    xhr.onload = function() {
        if(xhr.status == 400){
            let msg = xhr.response;
            let reader = new FileReader();
            reader.onload = function() {
                let text = reader.result;
                err_msg.innerHTML = text;
            }
            reader.readAsText(msg);
            img.src = "";
            
        } else if(xhr.status == 200){
            // xhr.responseType = "blob";
            let blob = new Blob([xhr.response], {type: "image/jpeg"});
            let url = window.URL.createObjectURL(blob);
            img.src = url;
            err_msg.innerHTML = "";
        }
        loader.style.display = "none";
    }
    xhr.send(null);
    return true;
}
/*Extract all the text having 'p' (Paragraph) as a tag and combine them*/
let sentences = document.getElementsByTagName('p');
text = ""
for(var i = 0; i < (sentences.length); i += 1){
    context = sentences[i].textContent;
    text = text + " " + context;
}

/*Whenever a page is reloaded call myFunction()*/
chrome.runtime.onConnect.addListener(
  myfunction()
)

/* Function for reading the response that we got back from Flask*/
function readBody(http) {
    var data;
    if (!http.responseType || http.responseType === "text") {
        data = http.responseText;
    }
    return data;
}

/*A Function that sends the text from the webpage to Flask and sends the response it gets back to popup.html*/
function myfunction(){
    console.log(text)
    /* Using XMLHttpRequest to send and receive data between flask and js*/
    var http = new XMLHttpRequest();
    /*Running on local server as of now*/
    http.open("POST", "http://localhost:8000/", true);
    http.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    http.onreadystatechange = function()
    {
        if(http.readyState == 4 && http.status == 200) {
            summary=readBody(http)
            console.log("Summary")
            console.log(summary)
            /*This function sends the text it gets back from Flask to popup.js as soon as it receieves a message from popup.js*/
            chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
                sendResponse({
                data: summary
                }); 
        });
    }
}
    http.send(text)
}



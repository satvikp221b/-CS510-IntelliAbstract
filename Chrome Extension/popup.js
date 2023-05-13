/*This function sends a message to content.js as soon as the button is clciekd and displays what it gets in return on the popup.html (Extension)*/
function popup() {
    chrome.tabs.query({currentWindow: true, active: true}, function (tabs){
    var activeTab = tabs[0];
    chrome.tabs.sendMessage(activeTab.id, {"message": "Message Sent From Popup.html to Content.js"},function(response){
        if(typeof response === 'undefined'){
                document.getElementById('Summary').innerHTML = "Please reload the page to get the summary!"
            }
            else{
                document.getElementById('Summary').innerHTML="Summary: "+response.data;
            }
        });
   });
}

/*This function activates as soon as we click on 'Summarize Text' Button */

document.addEventListener("DOMContentLoaded", function() {
  document.getElementById("clickIt").addEventListener("click", popup);
});



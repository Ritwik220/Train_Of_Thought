document.addEventListener("DOMContentLoaded", () => {
    let heading = document.querySelector('#Heading1');
    let cursor = "|";
    let text = "Welcome to ChatVerse!Start a conversation — your words matter. 💬";
    TypeWriter(heading, text, 90);
    let register = document.querySelector('#Register');
    let login = document.querySelector('#Login');
    register.addEventListener('click', () => {
        window.location = window.location.origin + "/Chat/register" ;
    });
    login.addEventListener('click', () => {
        window.location = window.location.origin + "/Chat/login" ;
    });
})
function TypeWriter(element, text, delay) {
    let index = 0;
    // let audio = new Audio("mixkit-hard-single-key-press-in-a-laptop-2542.wav")
    function type() {
        if(index == text.length)
          element.innerHTML = element.innerHTML.replace("|", "");
        else if (index < text.length) {
            element.innerHTML = element.innerHTML.replace("|", "");
            element.innerHTML += (text.charAt(index) + "|");

            // audio.play();
            index++;
            if(index==21){
                element.innerHTML = element.innerHTML.replace("|", "");
                element = document.querySelector('#Heading2');
            }
            setTimeout(type, delay);
        }
    }
    type();
}

function copyToClipboard() {
    var passwordText = document.getElementById("generated-password").innerText;
    navigator.clipboard.writeText(passwordText).then(function() {
        showToast('Password copied to clipboard');
    }, function(err) {
        console.error('Could not copy text: ', err);
    });
}

function showToast(message) {
    var toast = document.createElement("div");
    toast.className = "toast";
    toast.innerText = message;
    document.body.appendChild(toast);

    setTimeout(function() {
        toast.className += " show";
    }, 100); // Delay to trigger CSS animation

    setTimeout(function() {
        toast.className = toast.className.replace(" show", "");
        document.body.removeChild(toast);
    }, 3000);
}

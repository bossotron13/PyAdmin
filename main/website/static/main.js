function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

function StartServer() {
    if (returnStats() != "Online, Accepting Players."){
        window.location.href = "/start?SID=" + getCookie("SessionID")
    }
};

function StopServer() {
    if (returnStats() != "Offline"){
        window.location.href = "/stop?SID=" + getCookie("SessionID")
    }
};

function RestartServer() {
    window.location.href = "/restart?SID=" + getCookie("SessionID")
} ;

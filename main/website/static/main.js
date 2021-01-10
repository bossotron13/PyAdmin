function StartServer() {
    if (returnStats() != "Online, Accepting Players."){
        window.location.href = "/start"
    }
};

function StopServer() {
    if (returnStats() != "Offline"){
        window.location.href = "/stop"
    }
};

function RestartServer() {
    window.location.href = "/restart"
} ;

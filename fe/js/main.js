window.onload = function() {
    // Init
    var clipboard = new ClipboardJS('.copy-connection');
    var socket = io.connect('http://' + document.domain + ':' + location.port);
    var statusMessagesParent = document.getElementById("status-messages");
    var gameCardsParent = document.getElementById("game-cards");
    setTheme();

    socket.on('server_info', function(data) {
        clearGameCards(gameCardsParent);
        buildGameCards(gameCardsParent, data);
    });

    socket.on('messages', function(data) {
        clearStatusMessages(statusMessagesParent);
        buildStatusMessages(statusMessagesParent, data);
    });

    socket.on('message-notify', function(notification) {
        var notification = new Notification(notification.title, {
            "body": notification.subtitle
        });
    });

    socket.on('connect', function() {
        setDisconnectedBanner(false);
    });

    socket.on('disconnect', function() {
        setDisconnectedBanner(true);
    });

};

function buildGameCards(parentNode, serverDataList) {
    // todo compile this only once? even if its only on pageload
    let templateSource = document.getElementById("template-server-card").innerHTML;
    let template = Handlebars.compile(templateSource);

    // Bye bye loading spinner
    let sp = document.getElementById("game-cards-spinner");
    if (sp) sp.parentNode.removeChild(sp);

    serverDataList.forEach(function(data) {
        if (data.error) {
          console.warn(`Could not gamedig "${data.game.name}". Card not built.`);
          return;
        }

        let render = template(data);
        let card = document.createElement("div");
        card.setAttribute("class", "column is-one-third-desktop");
        card.innerHTML = render;
        parentNode.appendChild(card);
    });
}

function clearGameCards(parentNode) {
    while (parentNode.firstChild) {
        parentNode.removeChild(parentNode.firstChild);
    }
}

function buildStatusMessages(parentNode, statusMessages) {
    // todo compile this only once? even if its only on pageload
    let templateSource = document.getElementById("template-status-message").innerHTML;
    let template = Handlebars.compile(templateSource);

    // Bye bye loading spinner
    let sp = document.getElementById("status-messages-spinner");
    if (sp) sp.parentNode.removeChild(sp);

    statusMessages.forEach(function(data) {
        let render = template(data);
        let card = document.createElement("div");
        card.setAttribute("class", "tile is-parent is-vertical");
        card.innerHTML = render;
        parentNode.appendChild(card);
    });
}

function clearStatusMessages(parentNode) {
    while (parentNode.firstChild) {
        parentNode.removeChild(parentNode.firstChild);
    }
}

function setTheme() {
    // load stock (light) bulma over the drop-in dark theme. 
    // Kinda shitty method but who tf uses light themes lmao 
    // todo improve
    var url = new URL(window.location.href);
    var theme = url.searchParams.get("theme");
    var t = url.searchParams.get("t");
    if (theme == "light" || theme == "l" || t == "light" || t == "l") {
        var newCssLinkNode = document.createElement("link");
        newCssLinkNode.setAttribute("rel", "stylesheet");
        newCssLinkNode.setAttribute("type", "text/css");
        newCssLinkNode.setAttribute("href", "https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.4/css/bulma.min.css");
        document.getElementsByTagName("head").item(0).appendChild(newCssLinkNode);
    }
}

function toggleMessageControls() {
    let controls = document.getElementById("message-controls");
    controls.style.display = controls.style.display == 'none' ? 'block' : 'none';
}

function setDisconnectedBanner(show) {
    let banner = document.getElementById("disconnected-banner");
    banner.style.display = show ? 'block' : 'none';

    // set or unset the navbar stickness
    let docEl = document.documentElement
    docEl.classList.toggle('has-navbar-fixed-top')
}

// request notification permission
Notification.requestPermission();


//todo loading spinners whenever content isnt there
//todo some notification if server dies/ws is dropped
window.onload = function() {
  var clipboard = new ClipboardJS('.copy-connection');
  var url = new URL(window.location.href);
  var theme = url.searchParams.get("theme");
  if (theme == "light" || theme == "l") setLightTheme();
  
  var gameParent = document.getElementById("game-boxes");
  var statusParent = document.getElementById("status-messages");

  var socket = io.connect('http://' + document.domain + ':' + location.port);

  console.log(socket)

  socket.on('server_info', function(data) {
    clearGameStatusBoxes(gameParent)
    buildGameStatusBoxes(gameParent, data)
  });

  socket.on('messages', function(data) {
    clearStatusMessages(statusParent)
    buildStatusMessages(statusParent, data)
  });

  socket.on('message-notify', function(notification) {
    var notification = new Notification(notification.title, {
      "body": notification.subtitle
    });
  });

  setTimeout(function(){console.log(socket)}, 6000);
}

function buildGameStatusBoxes(parentNode, data) {
    for (var i = 0; i < data.length; i++) {
        console.log(data[i])
        gameInfo = document.createElement("div")
        gameInfo.setAttribute("class", "column is-one-third-desktop")
        gameInfo.innerHTML = tmpl("tmpl-game-box", data[i])
        parentNode.appendChild(gameInfo);
    }
}

function clearGameStatusBoxes(parentNode) {
    while (parentNode.firstChild) {
        parentNode.removeChild(parentNode.firstChild);
    }
}

function buildStatusMessages(parentNode, data) {
    for (var i = 0; i < data.length; i++) {
        gameInfo = document.createElement("div")
        gameInfo.setAttribute("class", "tile is-parent is-vertical")
        gameInfo.innerHTML = tmpl("tmpl-status-message", data[i])
        parentNode.appendChild(gameInfo);
    }
}

function clearStatusMessages(parentNode) {
    while (parentNode.firstChild) {
        parentNode.removeChild(parentNode.firstChild);
    }
}

function setLightTheme() {
    // load stock (light) bulma over the dark theme
    // lazy, but it works (because they style the same attributes & elements)
    var newlink = document.createElement("link");
    newlink.setAttribute("rel", "stylesheet");
    newlink.setAttribute("type", "text/css");
    newlink.setAttribute("href", "https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.4/css/bulma.min.css");
    document.getElementsByTagName("head").item(0).appendChild(newlink)
}
// [csgo, tf2, minecraft_survival, minecraft_creative, quake_live, factorio]

// request permissions for notifications
Notification.requestPermission();

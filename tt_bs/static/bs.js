var canvas = document.getElementById("board");
var context = canvas.getContext('2d');

var board = {
    w: 0,
    h: 0,
    gridSize: 35,
    tX: 20,
    tY: 20,
    mouseX: 0,
    mouseY: 0,
    mouseDownX: 0,
    mouseDownY: 0,
    mouseDownTime: 0,
    dragging: false,
    selectedSquare: null,
    hoverSquare: null,
    shots: [],
    squares: [],
    teams: [],
    displayCoords: function(x, y, selected) {},
    render: function() {
        context.clearRect(0,0, canvas.width, canvas.height);
        const visibleSquares = board.getVisibleCoords();
        for (var i=0; i < this.shots.length; i++) {
            board.fillSquare(this.shots[i], "rgba(100, 100, 100, 0.2)");
        }

        // Draw squares
        for (var i=0; i < board.squares.length; i++) {
            var square = board.squares[i];
            if (board.isInBounds(visibleSquares, square)) {
                if (square.shooter != null) {
                    var shooterColor = getTeamColor(board.teams, square.shooter);
                    if (ownerColor == shooterColor) {
                        shooterColor = "#000000"
                    }
                    if (square.owner != null) {
                        var ownerColor = getTeamColor(board.teams, square.owner);
                        board.fillSquare(square, ownerColor);
                    }
                    board.crossSquare(square, shooterColor);
                }
            }
        }
        if (board.selectedSquare) {
            board.fillSquare(board.selectedSquare, "rgba(225, 20, 20, 0.7)");
        }
        if (board.hoverSquare) {
            board.fillSquare(board.hoverSquare, "rgba(255, 255, 255, 0.2)");
        }
        board.drawGrid();
    },
    isInBounds: function(v, square) {
        return square.x >= v.minX && square.x <= v.maxX && square.y >= v.minY && square.y <= v.maxY;
    },
    getVisibleCoords: function() {
        var minX = Math.floor(-board.tX / board.gridSize);
        var minY = Math.floor(-board.tY / board.gridSize);
        var maxX = Math.ceil(minX + canvas.width / board.gridSize);
        var maxY = Math.ceil(minY + canvas.height / board.gridSize);
        return { minX: Math.max(minX, 0), minY: Math.max(minY, 0),
            maxX: Math.min(maxX, board.w), maxY: Math.min(maxY, board.h) };
    },
    drawGrid: function() {
        context.beginPath();
        context.lineWidth = 1;
        context.strokeStyle = '#007700';
        var limits = board.getVisibleCoords();
        var limitX = Math.min(canvas.width, board.w*board.gridSize);
        var limitY = Math.min(canvas.height, board.h*board.gridSize);
        for (var i=limits.minX; i <= limits.maxX; i++) {
            context.moveTo(board.tX + i*board.gridSize, limits.minY * board.gridSize + board.tY);
            context.lineTo(board.tX + i*board.gridSize, limits.maxY * board.gridSize + board.tY);
        }
        for (var i=limits.minY; i <= limits.maxY; i++) {
            context.moveTo(limits.minX * board.gridSize + board.tX, i*board.gridSize + board.tY);
            context.lineTo(limits.maxX * board.gridSize + board.tX, i*board.gridSize + board.tY);
        }
        context.stroke();
    },
    onClick: function(event) {
        selectedSquare = board.getSquare(event);

        if (selectedSquare) {
            board.displayCoords(selectedSquare.x, selectedSquare.y, true);
        }
        board.selectedSquare = selectedSquare;
        board.render();
    },
    onMouseDown: function(event) {
        board.dragging = true;
        board.mouseX = event.clientX;
        board.mouseY = event.clientY;
        board.mouseDownX = event.clientX;
        board.mouseDownY = event.clientY;
        board.mouseDownTime = Date.now();
    },
    onMouseMove: function(event) {
        if (board.dragging) {
            board.tX += event.clientX - board.mouseX;
            board.tY += event.clientY - board.mouseY;
            board.mouseX = event.clientX;
            board.mouseY = event.clientY;
            board.render();
        } else {
            var hoverSquare = board.getSquare(event);
            if (hoverSquare) {
                board.displayCoords(hoverSquare.x, hoverSquare.y, board.selectedSquare != null);
            }
            if (hoverSquare != board.hoverSquare) {
                board.hoverSquare = hoverSquare;
                board.render();
            }
        }
    },
    onMouseUp: function(event) {
        if ((Math.abs(board.mouseDownX - event.clientX) < 5 && Math.abs(board.mouseDownY - event.clientY) < 5)
            || Date.now() - board.mouseDownTime < 100) {
            board.onClick(event);
        }

        board.dragging = false;
        board.mouseDownY = 0;
        board.mouseDownX = 0;
        board.mouseDownTime = 0;

        const lim = board.getVisibleCoords();

        client.getSquares(lim.minX, lim.minY, lim.maxX, lim.maxY, function(response) {
                board.squares = response.squares;
                board.render();
            }
        )
    },
    onMouseOut: function(event) {
        if (board.selectedSquare) {
            board.displayCoords(board.selectedSquare.x, board.selectedSquare.y, true);
        }
    },
    getSquare: function(event) {
        var x = Math.floor((event.clientX - event.target.offsetLeft - board.tX) / board.gridSize);
        var y = Math.floor((event.clientY - event.target.offsetTop - board.tY) / board.gridSize);
        if (x < 0 || x >= board.w || y < 0 || y >= board.h) return null;
        return { 'x' : x, 'y' : y };
    },
    fillSquare: function(square, color)  {
        var x = square.x * board.gridSize + board.tX;
        var y = square.y * board.gridSize + board.tY;
        context.beginPath();
        context.fillStyle = color;
        context.fillRect(x, y, board.gridSize, board.gridSize);
    },
    crossSquare: function(square, color) {
        var x = square.x * board.gridSize + board.tX;
        var y = square.y * board.gridSize + board.tY;
        context.beginPath();
        context.moveTo(x, y);
        context.lineTo(x + board.gridSize, y + board.gridSize);
        context.moveTo(x + board.gridSize, y);
        context.lineTo(x, y + board.gridSize);
        context.lineWidth = 3;
        context.strokeStyle = color;
        context.stroke();
    },
    shootSelected: function(captcha, success, failure) {
        if (board.selectedSquare) {
            client.shoot(selectedSquare.x, selectedSquare.y, captcha, success, failure);
            board.shots.push({x: selectedSquare.x, y: selectedSquare.y});
        }
        board.selectedSquare = null;
        board.displayCoords(0, 0, false);
        board.render();
    }
};

var client = {
    teamsCallback: function(teams) {},
    init: function(endpoint, game) {
        this.endpoint = endpoint;
        this.game = game;
    },
    fetchGame: function(success) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var jsonResponse = JSON.parse(this.responseText);
                setSize(jsonResponse.width, jsonResponse.height);
                board.squares = jsonResponse.squares;
                board.teams = jsonResponse.teams;
                success(jsonResponse);
            }
        };
        xhttp.open("GET", this.endpoint + this.game, true);
        xhttp.send();
    },
    shoot: function(x, y, captcha, success, failure) {
        if (!client.team) {
            failure(400, "Et ole valinnut tiimiä :O");
            return;
        }
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4) {
                switch (this.status) {
                    case 200:
                        var shot = JSON.parse(this.responseText)
                        if (shot.hit) {
                            if (shot.square.team == client.team) {
                                failure(200, "Hups, ammuit omaa tiimiä :b");
                            } else {
                                success("Jes, osuma :D");
                            }
                        } else {
                            failure(200, "Harmi, ei onnea tällä kertaa :C");
                        }
                        board.squares.push(shot.square);
                        board.render();
                        client.refreshTeams();
                        break;
                    case 204:
                        failure(204, "Ei mittään :(");
                        break;
                    case 403:
                        failure(403, "Yritä nyt ees vähän ihmismäisempi olla");
                        break;
                    case 429:
                        failure(429, "Nyt ammut kyllä ihan liian nopeeta >:O");
                        break;
                    default:
                        failure(this.status, "Jotakin meni pieleen :/");
                }
            }
        };
        xhttp.open("POST", this.endpoint + this.game + "/shoot?team=" + this.team + "&x=" + x + "&y=" + y + "&recaptcha_response_field=" + captcha, true);
        xhttp.send();
    },
    getSquares: function(x1, y1, x2, y2, callback) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                callback(JSON.parse(this.responseText));
            }
        };
        xhttp.open("GET", this.endpoint + this.game + "/squares?xmin=" + x1 + "&xmax=" + x2 + "&ymin=" + y1 + "&ymax=" + y2, true);
        xhttp.send();
    },
    refreshTeams: function() {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                client.teamsCallback(JSON.parse(this.responseText).teams, client.team);
            }
        };
        xhttp.open("GET", this.endpoint + this.game + "/teams", true);
        xhttp.send();
    },
    selectTeam: function(myTeam) {
        client.team = myTeam;
    }
};

function resize() {
    var rect = canvas.parentNode.getBoundingClientRect();
    canvas.width = rect.width;
    canvas.height = rect.height;
    board.render();
}

function setSize(w, h) {
    board.w = w;
    board.h = h;
    board.tX = -Math.random() * w * board.gridSize;
    board.tY = -Math.random() * h * board.gridSize;
    board.render();
}

function getTeamColor(teams, team) {
    for (var i = 0; i < teams.length; i++) {
        if (teams[i].name == team) {
            return teams[i].color;
        }
    }
}

// Get the first Touch from a TouchEvent and pass it to the mouse listener
var touchListener = function(mouseListener) {
    return function(event) {
        mouseListener(event.touches[0]);
    }
};

window.addEventListener('resize', resize, false);
// canvas.addEventListener('click', board.onClick);
canvas.addEventListener("mousedown", board.onMouseDown);
canvas.addEventListener("mousemove", board.onMouseMove);
canvas.addEventListener("mouseup", board.onMouseUp);
canvas.addEventListener("mouseout", board.onMouseOut);
canvas.addEventListener("touchstart", touchListener(board.onMouseDown));
canvas.addEventListener("touchmove", touchListener(board.onMouseMove));
canvas.addEventListener("touchend", touchListener(board.onMouseUp));
setSize(100, 100);
resize();
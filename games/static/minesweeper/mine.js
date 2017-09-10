var row = 16, col = 32;
var maxRow = 64, maxCol = 120;
var mineCnt = 99;
var map = []; //has mine or not
var disc = []; //is discovered
var flg = []; //is set flag or not
var num = []; //mine nearby
var hasMine;

//record where the mouse is down
var msDownRow;
var msDownCol;

//timer
var timer;
var time;

function random(min, max)
{
	return Math.floor(Math.random() * (max - min + 1)) + min;
}

//set all block empty and all undiscovered
function initVar()
{
	hasMine = false;
	for (var i = 0; i < row; i++)
	{
		map[i] = [];
		disc[i] = [];
		num[i] = [];
		flg[i] = [];
		for (var j = 0; j < col; j++)
		{
			map[i][j] = false;
			disc[i][j] = false;
			flg[i][j] = false;
			num[i][j] = 0;
		}
	}
}

function setMine(r, c)
{
	hasMine = true;
	var blocks = [];
	for (var i = 0; i < row; i++)
	{
		for (var j = 0; j < col; j++)
		{
			if (!(Math.abs(i - r) <= 1 && Math.abs(j - c) <= 1))
			{
				blocks.push([i, j]);
		
			}
		}
	}

	for (var cnt = mineCnt; cnt >= 1; cnt--)
	{
		var ind = random(0, blocks.length - 1);
		var pos = blocks[ind];
		map[pos[0]][pos[1]] = true;
		
		//delete the selected one
		blocks[ind] = blocks[0];
		blocks[0] = pos;
		blocks.shift();
	}

	for (var i = 0; i < row; i++)
	{
		for (var j = 0; j < col; j++)
		{
			var cnt = 0;
			for (var m = -1; m <= 1; m++)
			{
				for (var n = -1; n <= 1; n++)
				{
					if (i + m >= 0 && i + m <= row - 1 && j + n >= 0 && j + n <= col - 1 && !(m === 0 && n === 0))
					{
						if (map[i + m][j + n] === true)
						{
							cnt++;
						}
					}
				}
			}
			num[i][j] = cnt;
		}
	}
}

function initGraph()
{
	//set universal attributes
	var mineDiv = document.getElementById("mineDiv");
	mineDiv.setAttribute("oncontextmenu", "return false;");
	mineDiv.setAttribute("ondragstart", "return false;");
	mineDiv.setAttribute("ondrop", "return false;");
	document.getElementById("content-div").parentElement.className = "";

	while (mineDiv.firstChild)
	{
		mineDiv.removeChild(mineDiv.firstChild);
	}

	//first add left mines
	var imgSpan = document.createElement("span");
	var mineIcon = document.createElement("img");
	mineIcon.className = "mineIcon";
	var mineSpan = document.createElement("span");
	mineIcon.src = "/static/minesweeper/mines.svg";
	mineSpan.innerHTML = mineCnt.toString();
	mineSpan.id = "mineCnt";
	imgSpan.id = "imgSpan";
	imgSpan.addEventListener("click", showMines, false);
	imgSpan.appendChild(mineIcon);

	//then the clock
	var clkSpan = document.createElement("span");
	var clkIcon = document.createElement("img");
	clkIcon.className = "clkIcon";
	var timeSpan = document.createElement("span");
	clkIcon.src = "/static/minesweeper/clock.svg";
	timeSpan.innerHTML = "0";
	timeSpan.id = "time";
	clkSpan.id = "clkSpan";
	clkSpan.addEventListener("click", alterTimer, false);
	clkSpan.appendChild(clkIcon);

	var clear = document.createElement("div");
	clear.className = "clear";

	mineDiv.appendChild(imgSpan);
	mineDiv.appendChild(mineSpan);
	mineDiv.appendChild(clkSpan);
	mineDiv.appendChild(timeSpan);
	mineDiv.appendChild(clear);
	
	//deal with mouseup outer number block
	mineDiv.addEventListener("mouseup", updateGraph, false);
	
	//then add the main table
	
	var table = document.createElement("table");
	table.id = "tb";
	mineDiv.appendChild(table);
	
	for (var i = 0; i < row; i++)
	{
		var trow = document.createElement("tr");
		table.appendChild(trow);
		for (var j = 0; j < col; j++)
		{
			var tdata = document.createElement("td");
			tdata.id = i.toString() + " " + j.toString();
			var image = document.createElement("img");
			image.src = "/static/minesweeper/un.svg";
			tdata.appendChild(image);
			tdata.addEventListener("mousedown", mouseDownEvent, false);
			tdata.addEventListener("mouseup", mouseUpEvent, false);
			trow.appendChild(tdata);
		}
	}
}

function updateGraph()
{
	//update mineleft
	var cnt = 0;
	for (var i = 0; i < row; i++)
	{
		for (var j = 0; j < col; j++)
		{
			if (flg[i][j] === true)
			{
				cnt++;
			}
		}
	}
	var mineLeft = mineCnt - cnt;
	document.getElementById("mineCnt").innerHTML = mineLeft.toString();

	//update table
	for (var i = 0; i < row; i++)
	{
		for (var j = 0; j < col; j++)
		{
			var td = document.getElementById(i.toString() + " " + j.toString());
			if (disc[i][j] === true)
			{
				var name = "/static/minesweeper/" + num[i][j].toString() + ".svg";
				if (td.childNodes[0].getAttribute("src") !== name)
				{				
					td.childNodes[0].setAttribute("src", name);
				}
			}
			else if(flg[i][j] === true)
			{
				if (td.childNodes[0].getAttribute("src") !== "/static/minesweeper/flag.svg")
				{				
					td.childNodes[0].setAttribute("src", "/static/minesweeper/flag.svg");
				}
				 
			}
			else
			{
				if (td.childNodes[0].getAttribute("src") !== "/static/minesweeper/un.svg")
				{				
					td.childNodes[0].setAttribute("src", "/static/minesweeper/un.svg");
				}
			}
		}
	}
}

//show win
function showWin()
{
	for (var i = 0; i < row; i++)
	{
		for (var j = 0; j < col; j++)
		{
			if (map[i][j] === true)
			{
				var td = document.getElementById(i.toString() + " " + j.toString());
				td.childNodes[0].setAttribute("src", "/static/minesweeper/smile.svg");
			}
		}
	}
}

//showDie
function showDie()
{
	for (var i = 0; i < row; i++)
	{
		for (var j = 0; j < col; j++)
		{
			var td = document.getElementById(i.toString() + " " + j.toString());
			if (map[i][j] === true && flg[i][j] === false)
			{
				td.childNodes[0].setAttribute("src", "/static/minesweeper/mine.svg");
			}
			else if (map[i][j] === true && flg[i][j] === true)
			{
				td.childNodes[0].setAttribute("src", "/static/minesweeper/flag.svg");
			}
			else if (map[i][j] === false && flg[i][j] === true)
			{
				td.childNodes[0].setAttribute("src", "/static/minesweeper/wrong flag.svg");
			}
			else//the number or vacant block
			{
				var name = "/static/minesweeper/" + num[i][j].toString() + ".svg";
				td.childNodes[0].setAttribute("src", name); 
			}
		}
	}
}

//dig operation
function dig(r, c)
{
	r = parseInt(r);
	c = parseInt(c);
	if (!(disc[r][c] === false && flg[r][c] === false))//cannot dig
	{
		return true;
	}

	if (map[r][c] === true)//meets mine
	{
		return false;
	}
	else if (num[r][c] >= 1)//meets num
	{
		disc[r][c] = true;
		return true;
	}
	else//meets vacant
	{
		disc[r][c] = true;
		var res = true;
		for (var m = -1; m <= 1; m++)
		{
			for (var n = -1; n <= 1; n++)
			{
				if (r + m >= 0 && r + m <= row - 1 && c + n >= 0 && c + n <= col - 1 && !(m === 0 && n === 0))
				{
					if (!dig(r + m, c + n))
					{
						res = false;
					}
				}
			}
		}
		return res;
	}
}

//chord operation
function chord(r, c)
{
	r = parseInt(r);
	c = parseInt(c);
	if (!(disc[r][c] === true && num[r][c] >= 1))//cannot chord
	{
		return true;
	}

	var flgs = 0;
	for (var m = -1; m <= 1; m++)
	{
		for (var n = -1; n <= 1; n++)
		{
			if (r + m >= 0 && r + m <= row - 1 && c + n >= 0 && c + n <= col - 1 && !(m === 0 && n === 0))
			{
				if (flg[r + m][c + n] === true)
				{
					flgs++;
				}
			}
		}
	}
	if (flgs === num[r][c])
	{
		var res = true;
		for (var m = -1; m <= 1; m++)
		{
			for (var n = -1; n <= 1; n++)
			{
				if (r + m >= 0 && r + m <= row - 1 && c + n >= 0 && c + n <= col - 1 && !(m === 0 && n === 0))
				{
					if (!dig(r + m, c + n))
					{
						res = false;
					}
				}
			}
		}
		return res;
	}
	else//cannot chord
	{
		return true;
	}
}

function judgeWin()
{
	var res = true;
	for (var i = 0; i < row; i++)
	{
		for (var j = 0; j < col; j++)
		{
			if (map[i][j] === false && disc[i][j] === false)
			{
				res = false;
			}
		}
	}
	return res;
}

function mouseDownEvent(evt)
{
	dealMouseDown(this, evt); 
	return false;
}

function mouseUpEvent(evt)
{
	dealMouseUp(this, evt); 
	return false;
}

function updateTimer()
{
	time++;
	document.getElementById("time").innerHTML = time.toString();
}

function dealMouseDown(block, ev)
{
	var id = block.id.split(" ");
	msDownRow = parseInt(id[0]);
	msDownCol = parseInt(id[1]);

	//if it is number state
	var r = msDownRow, c = msDownCol;
	if (num[r][c] >= 1 && disc[r][c] === true)//if it is the number block
	{
		for (var m = -1; m <= 1; m++)
		{
			for (var n = -1; n <= 1; n++)
			{
				if (r + m >= 0 && r + m <= row - 1 && c + n >= 0 && c + n <= col - 1 && !(m === 0 && n === 0))
				{
					if (disc[r + m][c + n] === false && flg[r + m][c + n] === false)
					{
						document.getElementById((r + m).toString() + " " + (c + n).toString()).childNodes[0].setAttribute("src", "/static/minesweeper/dark.svg");
					}
				}
			}
		}
	}
}

function dealMouseUp(block, ev)
{
	var id = block.id.split(" ");
	var msUpRow = parseInt(id[0]), msUpCol = parseInt(id[1]);
	var isDead;

	//if the mouse does not move to another block
	if (msUpRow === msDownRow && msUpCol === msDownCol)
	{
		//start timer
		if (timer === -1)
		{
			timer = setInterval(updateTimer ,1000);
			startTime = new Date();
		}

		//judge left or right click
		if (ev.which === 1)
		{
			isDead = !leftClick(block);
		}
		else if (ev.which === 3)
		{
			rightClick(block);
		}	
	}
	updateGraph();

	if (isDead === true)
	{
		showDie();
		endGame();
	}
	
	if (judgeWin() === true)
	{
		showWin();
		endGame();
	}
}

function leftClick(block)//false die
{
	var id = block.id.split(" ");
	var r = parseInt(id[0]), c = parseInt(id[1]);
	var res = true;//for invalid click
	
	if (hasMine === false)
	{
		setMine(r, c);
	}
	

	if (disc[r][c] === false && flg[r][c] === false)//dig operation
	{
		res = dig(r, c);
	}
	else if (disc[r][c] === true && num[r][c] >= 1)//chord
	{
		res = chord(r, c);
	}
	return res;
}

function rightClick(block)
{
	var id = block.id.split(" ");
	var r = parseInt(id[0]), c = parseInt(id[1]);

	if (disc[r][c] === false)
	{
		flg[r][c] = !flg[r][c];
	}
}

function endGame()
{
	document.getElementById("mineDiv").removeEventListener("mouseup", updateGraph, false);
	document.getElementById("imgSpan").removeEventListener("click", showMines, false);
	document.getElementById("clkSpan").removeEventListener("click", alterTimer, false);
	if (timer >= 0)
	{
		clearInterval(timer);
	}
	for (var i = 0; i < row; i++)
	{
		for (var j = 0; j < col; j++)
		{
			var tdata = document.getElementById(i.toString() + " " + j.toString());
			tdata.removeEventListener("mousedown", mouseDownEvent, false);
			tdata.removeEventListener("mouseup", mouseUpEvent, false);
		}
	}
}

function showMines()
{
	for (var i = 0; i < row; i++)
	{
		for (var j = 0; j < col; j++)
		{
			if (map[i][j] === true)
			{
				var tdata = document.getElementById(i.toString() + " " + j.toString());
				tdata.childNodes[0].setAttribute("src", "/static/minesweeper/mine.svg");
			}
		}
	}
}

function alterTimer()
{
	if (timer === -2)
	{
		timer = setInterval(updateTimer ,1000);
	}
	else
	{
		clearInterval(timer);
		timer = -2;
	}
}

function play(r, c, mines)
{
	row = r;
	col = c;
	mineCnt = mines;
	if (timer >= 0)
	{
		clearInterval(timer);
	}
 	timer = -1;
 	time = 0;
	initVar();
	initGraph();
}

function start()
{
	// document.getElementById("setDiv").style.display = "none";
	var r = document.getElementById("height").value;
	var c = document.getElementById("width").value;
	var count = document.getElementById("count").value;
	r = (r < 4) ? 4 : r;
	c = (c < 4) ? 4 : c;
	r = (r > maxRow) ? maxRow : r;
	c = (c > maxCol) ? maxCol : c;
	count = (count < 1) ? 1 : count;
	count = (count > r * c - 9) ? r * c - 9 : count;
	document.getElementById("height").value = r;
	document.getElementById("width").value = c;
	document.getElementById("count").value = count;
	play(r, c, count);
}

(function() {
   start();
})();

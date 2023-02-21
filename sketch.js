
// @author Adam Lastowka
// This is probably the messiest code I have ever written, and that's saying something.
// So many edge cases, weird formatting rules, junk code...
// Very few comments, too. Good luck understanding this.

"use strict";

var mouse;

function preload() {
}

function setup() {
	createCanvas(windowWidth, windowHeight);
	document.body.style.overflow = 'hidden'
}

function drawGrid() {
	var spc = 100/(2 ** round(Math.log(CCAM.zoom)/Math.log(2)));
	var r = 7/CCAM.zoom;
	var LU = CCAM.screenToMouse(0, 0);
	var RD = CCAM.screenToMouse(width, height);
	stroke(60, 68, 81);
	strokeWeight(1/CCAM.zoom);
	
	for(var x = round(LU.x/spc)*spc - spc; x < round(RD.x/spc)*spc + spc; x+= spc)
	for(var y = round(LU.y/spc)*spc - spc; y < round(RD.y/spc)*spc + spc; y+= spc) {
		line(x - r, y, x + r, y);
		line(x, y - r, x, y + r);
	}
	strokeWeight(1);
}

function draw() {
	mouse = CCAM.screenToMouse(mouseX, mouseY);
	CCAM.update();
	CCAM.apply();

	textFont('Atkinson Hyperlegible');
	background(40, 45, 49);
	drawGrid();
	fill(244, 225, 117);
	noStroke();
	textSize(100);
	text("Impedance Calculator", 0, 0);
	textSize(32);
	text("By Adam Lastowka", 0, 70);

	CCAM.unapply();

}

function windowResized() {
	resizeCanvas(windowWidth, windowHeight);
 }
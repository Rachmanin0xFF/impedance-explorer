
function resistance(value) {
    return new Cpl(value, 0);
}
function reactance(value) {
    return new Cpl(0, value);
}

function Z_capacitor(w, C) {
    return reactance(0, -1/(w*C));
}
function Z_inductor(w, L) {
    return reactance(0, w*L);
}
function Z_resistor(w, R) {
    return resistance(R);
}

class Node {
    constructor(x_pos, y_pos) {
        this.x = x_pos;
        this.y = y_pos;
    }
    display() {
        ellipse(this.x, this.y, 10, 10);
    }
}

class Network {
    constructor() {
        this.data = []
    }
}
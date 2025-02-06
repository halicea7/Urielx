let font;
let particles = [];
let pg;            // Off-screen graphics buffer
let sampleStep = 5; // Adjust this to control particle density

let stars = [];
let numStars = 150; // Number of background stars

function preload() {
  // Load your custom font; update the path as needed.
  font = loadFont('assets/airstrikecond.ttf');
}

function setup() {
  // Create a canvas that fills the entire window.
  createCanvas(windowWidth, windowHeight);
  
  // Create star objects for the background.
  for (let i = 0; i < numStars; i++) {
    stars.push(new Star(random(width), random(height), random(0.1, 0.5), random(1, 3)));
  }
  
  // Create an off-screen graphics buffer using the full window size.
  pg = createGraphics(width, height);
  pg.pixelDensity(1);  // Ensures a 1:1 pixel ratio for easier sampling
  pg.background(0);
  pg.textFont(font);
  pg.textSize(162);
  pg.fill(255);
  
  // *** Centering the Text ***
  // Set text alignment to center (both horizontally and vertically).
  pg.textAlign(CENTER, CENTER);
  // Draw the text at the center of the off-screen buffer.
  pg.text('URIELx', width / 2, height / 2);
  
  // Load the pixel data from the off-screen buffer.
  pg.loadPixels();
  
  // Loop over the buffer pixels and create a Particle for each pixel
  // that is part of the white text.
  for (let x = 0; x < pg.width; x += sampleStep) {
    for (let y = 0; y < pg.height; y += sampleStep) {
      let index = (x + y * pg.width) * 4; // each pixel has 4 values (r, g, b, a)
      let r = pg.pixels[index];           // red channel value
      if (r > 128) { 
        particles.push(new Particle(x, y));
      }
    }
  }
}

function draw() {
  // Draw a black background.
  background(0);
  
  // Draw the starry background first.
  for (let s of stars) {
    s.update();
    s.show();
  }
  
  // Then update and display the text particles on top.
  for (let p of particles) {
    p.behaviors();
    p.update();
    p.show();
  }
}

// When the window is resized, adjust the canvas and regenerate the off-screen graphics.
function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
  
  // Recreate the off-screen graphics buffer to match the new canvas size.
  pg = createGraphics(windowWidth, windowHeight);
  pg.pixelDensity(1);
  pg.background(0);
  pg.textFont(font);
  pg.textSize(162);
  pg.fill(255);
  
  // Center the text in the new buffer.
  pg.textAlign(CENTER, CENTER);
  pg.text('SkyLock', windowWidth / 2, windowHeight / 2);
  
  pg.loadPixels();
  
  // Clear and rebuild the particles array based on the new pg.
  particles = [];
  for (let x = 0; x < pg.width; x += sampleStep) {
    for (let y = 0; y < pg.height; y += sampleStep) {
      let index = (x + y * pg.width) * 4;
      let r = pg.pixels[index];
      if (r > 128) {
        particles.push(new Particle(x, y));
      }
    }
  }
}

// --- Star Class for the Background ---
class Star {
  constructor(x, y, speed, size) {
    this.pos = createVector(x, y);
    this.speed = speed; // Horizontal drift speed
    this.size = size;
    this.offset = random(TWO_PI); // Phase offset for a twinkling effect
  }
  
  update() {
    // Stars drift horizontally; when off the right edge, wrap to the left.
    this.pos.x += this.speed;
    if (this.pos.x > width) {
      this.pos.x = 0;
      this.pos.y = random(height);
    }
  }
  
  show() {
    // Modulate brightness using a sine function for a twinkling effect.
    let brightness = map(sin(frameCount * 0.05 + this.offset), -1, 1, 100, 255);
    noStroke();
    fill(brightness);
    ellipse(this.pos.x, this.pos.y, this.size, this.size);
  }
}

// --- Particle Class for the Text Animation ---
class Particle {
  constructor(x, y) {
    // The target is the pixel position from our off-screen text image.
    this.target = createVector(x, y);
    // Start at a random location on the canvas.
    this.pos = createVector(random(width), random(height));
    this.vel = p5.Vector.random2D();
    this.acc = createVector();
    this.maxSpeed = 10;
    this.maxForce = 1;
  }
  
  // Calculate steering forces for arriving at the target and fleeing the mouse.
  behaviors() {
    let arriveForce = this.arrive(this.target);
    let mouse = createVector(mouseX, mouseY);
    let fleeForce = this.flee(mouse);
    
    // Weight the forces as needed.
    arriveForce.mult(1);
    fleeForce.mult(5);
    
    this.applyForce(arriveForce);
    this.applyForce(fleeForce);
  }
  
  applyForce(force) {
    this.acc.add(force);
  }
  
  // Steering behavior for smoothly arriving at the target.
  arrive(target) {
    let desired = p5.Vector.sub(target, this.pos);
    let d = desired.mag();
    let speed = this.maxSpeed;
    if (d < 100) {
      speed = map(d, 0, 100, 0, this.maxSpeed);
    }
    desired.setMag(speed);
    let steer = p5.Vector.sub(desired, this.vel);
    steer.limit(this.maxForce);
    return steer;
  }
  
  // Steering behavior for fleeing from the mouse.
  flee(target) {
    let desired = p5.Vector.sub(target, this.pos);
    let d = desired.mag();
    if (d < 50) {
      desired.setMag(this.maxSpeed);
      desired.mult(-1);
      let steer = p5.Vector.sub(desired, this.vel);
      steer.limit(this.maxForce);
      return steer;
    }
    return createVector(0, 0);
  }
  
  update() {
    this.pos.add(this.vel);
    this.vel.add(this.acc);
    this.acc.mult(0);
  }
  
  show() {
    noStroke();
    fill(255);
    ellipse(this.pos.x, this.pos.y, 1, 1); // Draw each particle as a tiny circle
  }
}

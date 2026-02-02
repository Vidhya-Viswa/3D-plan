const data = {
    "Height": 848,
    "Width": 1200,
    "averageDoor": 46.333333333333336,
    "classes": [
        {
            "name": "door"
        },
        {
            "name": "wall"
        },
        {
            "name": "wall"
        },
        {
            "name": "door"
        },
        {
            "name": "door"
        },
        {
            "name": "wall"
        },
        {
            "name": "wall"
        },
        {
            "name": "door"
        },
        {
            "name": "wall"
        },
        {
            "name": "window"
        },
        {
            "name": "wall"
        },
        {
            "name": "wall"
        },
        {
            "name": "wall"
        },
        {
            "name": "wall"
        },
        {
            "name": "wall"
        },
        {
            "name": "wall"
        },
        {
            "name": "wall"
        },
        {
            "name": "wall"
        },
        {
            "name": "door"
        },
        {
            "name": "wall"
        },
        {
            "name": "wall"
        },
        {
            "name": "wall"
        },
        {
            "name": "door"
        },
        {
            "name": "wall"
        },
        {
            "name": "window"
        },
        {
            "name": "wall"
        },
        {
            "name": "wall"
        },
        {
            "name": "wall"
        },
        {
            "name": "wall"
        },
        {
            "name": "window"
        },
        {
            "name": "window"
        },
        {
            "name": "wall"
        },
        {
            "name": "window"
        }
    ],
    "points": [
        {
            "x1": 719,
            "x2": 779,
            "y1": 540,
            "y2": 550
        },
        {
            "x1": 769,
            "x2": 1063,
            "y1": 264,
            "y2": 274
        },
        {
            "x1": 534,
            "x2": 541,
            "y1": 263,
            "y2": 441
        },
        {
            "x1": 581,
            "x2": 627,
            "y1": 437,
            "y2": 443
        },
        {
            "x1": 744,
            "x2": 792,
            "y1": 453,
            "y2": 460
        },
        {
            "x1": 802,
            "x2": 809,
            "y1": 265,
            "y2": 466
        },
        {
            "x1": 529,
            "x2": 719,
            "y1": 540,
            "y2": 550
        },
        {
            "x1": 802,
            "x2": 809,
            "y1": 466,
            "y2": 513
        },
        {
            "x1": 633,
            "x2": 639,
            "y1": 267,
            "y2": 453
        },
        {
            "x1": 442,
            "x2": 484,
            "y1": 264,
            "y2": 273
        },
        {
            "x1": 780,
            "x2": 863,
            "y1": 539,
            "y2": 550
        },
        {
            "x1": 801,
            "x2": 809,
            "y1": 516,
            "y2": 550
        },
        {
            "x1": 634,
            "x2": 744,
            "y1": 453,
            "y2": 460
        },
        {
            "x1": 100,
            "x2": 358,
            "y1": 264,
            "y2": 274
        },
        {
            "x1": 547,
            "x2": 554,
            "y1": 500,
            "y2": 547
        },
        {
            "x1": 101,
            "x2": 112,
            "y1": 474,
            "y2": 550
        },
        {
            "x1": 101,
            "x2": 168,
            "y1": 540,
            "y2": 550
        },
        {
            "x1": 534,
            "x2": 579,
            "y1": 437,
            "y2": 443
        },
        {
            "x1": 560,
            "x2": 597,
            "y1": 501,
            "y2": 509
        },
        {
            "x1": 1009,
            "x2": 1067,
            "y1": 539,
            "y2": 551
        },
        {
            "x1": 1054,
            "x2": 1065,
            "y1": 317,
            "y2": 545
        },
        {
            "x1": 101,
            "x2": 112,
            "y1": 263,
            "y2": 339
        },
        {
            "x1": 548,
            "x2": 554,
            "y1": 455,
            "y2": 495
        },
        {
            "x1": 418,
            "x2": 440,
            "y1": 264,
            "y2": 274
        },
        {
            "x1": 377,
            "x2": 417,
            "y1": 264,
            "y2": 273
        },
        {
            "x1": 213,
            "x2": 380,
            "y1": 539,
            "y2": 550
        },
        {
            "x1": 603,
            "x2": 610,
            "y1": 502,
            "y2": 549
        },
        {
            "x1": 960,
            "x2": 1065,
            "y1": 355,
            "y2": 363
        },
        {
            "x1": 486,
            "x2": 648,
            "y1": 264,
            "y2": 274
        },
        {
            "x1": 677,
            "x2": 768,
            "y1": 264,
            "y2": 274
        },
        {
            "x1": 170,
            "x2": 212,
            "y1": 540,
            "y2": 550
        },
        {
            "x1": 802,
            "x2": 860,
            "y1": 356,
            "y2": 364
        },
        {
            "x1": 103,
            "x2": 112,
            "y1": 428,
            "y2": 474
        }
    ]
}

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xf0f0f0);

const camera = new THREE.PerspectiveCamera(
  60,
  window.innerWidth / window.innerHeight,
  1,
  5000
);
camera.position.set(0, 800, 1200);
camera.lookAt(0, 0, 0);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

scene.add(new THREE.AmbientLight(0xffffff, 0.7));
const light = new THREE.DirectionalLight(0xffffff, 0.6);
light.position.set(500, 1000, 500);
scene.add(light);

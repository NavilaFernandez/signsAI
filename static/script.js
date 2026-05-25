let camaraActiva = false;
let intervaloPrediccion = null;

// ── PALABRAS PARA DELETREAR ──────────────────────────────────
const palabras = [
    "HOLA", "CASA", "AMOR", "SOL", "MAR",
    "LUZ", "PAZ", "FIN", "RED", "MAP"
];

let palabraObjetivo = "";
let letraIndex = 0;
let letrasCompletadas = [];

// ── CÁMARA ───────────────────────────────────────────────────
function toggleCamara() {
    if (!camaraActiva) {
        activarCamara();
    } else {
        desactivarCamara();
    }
}

function activarCamara() {
    camaraActiva = true;
    document.getElementById('videoStream').src = '/video';
    document.getElementById('btnCamara').textContent = '⏹ Apagar cámara';
    document.getElementById('btnCamara').classList.add('activo');
    document.getElementById('placeholderCamara').style.display = 'none';
    document.getElementById('videoStream').style.display = 'block';

    // Inicia predicciones
    intervaloPrediccion = setInterval(obtenerPrediccion, 800);
}

function desactivarCamara() {
    camaraActiva = false;
    document.getElementById('videoStream').src = '';
    document.getElementById('btnCamara').textContent = '📷 Activar cámara';
    document.getElementById('btnCamara').classList.remove('activo');
    document.getElementById('placeholderCamara').style.display = 'flex';
    document.getElementById('videoStream').style.display = 'none';
    document.getElementById('letraDisplay').textContent = '?';
    document.getElementById('barraConfianza').style.width = '0%';
    document.getElementById('confianzaTexto').textContent = '0%';

    clearInterval(intervaloPrediccion);
}

// ── PREDICCIÓN ───────────────────────────────────────────────
async function obtenerPrediccion() {
    try {
        const res = await fetch('/prediccion');
        const data = await res.json();

        if (data.letra) {
            document.getElementById('letraDisplay').textContent = data.letra;
            document.getElementById('barraConfianza').style.width = data.confianza + '%';
            document.getElementById('confianzaTexto').textContent = data.confianza + '%';

            // Verifica si la letra coincide con la esperada
            if (palabraObjetivo && data.confianza > 80) {
                verificarLetra(data.letra);
            }
        }
    } catch (e) {
        console.log('Error:', e);
    }
}

// ── MODO DELETREAR ───────────────────────────────────────────
function nuevaPalabra() {
    palabraObjetivo = palabras[Math.floor(Math.random() * palabras.length)];
    letraIndex = 0;
    letrasCompletadas = [];
    renderizarPalabra();
    document.getElementById('mensajeResultado').textContent = '';
    document.getElementById('mensajeResultado').className = 'mensaje-resultado';
}

function renderizarPalabra() {
    const contenedor = document.getElementById('palabraObjetivo');
    contenedor.innerHTML = '';

    for (let i = 0; i < palabraObjetivo.length; i++) {
        const span = document.createElement('span');
        span.textContent = palabraObjetivo[i];
        span.classList.add('letra-objetivo');

        if (i < letraIndex) {
            span.classList.add('completada');
        } else if (i === letraIndex) {
            span.classList.add('actual');
        }

        contenedor.appendChild(span);
    }
}

function verificarLetra(letraDetectada) {
    const letraEsperada = palabraObjetivo[letraIndex];

    if (letraDetectada.toUpperCase() === letraEsperada.toUpperCase()) {
        letrasCompletadas.push(letraEsperada);
        letraIndex++;
        renderizarPalabra();

        if (letraIndex >= palabraObjetivo.length) {
            // Palabra completada
            document.getElementById('mensajeResultado').textContent = '🎉 ¡Palabra completada!';
            document.getElementById('mensajeResultado').className = 'mensaje-resultado exito';
            setTimeout(nuevaPalabra, 2000);
        } else {
            document.getElementById('mensajeResultado').textContent = '✅ ¡Letra correcta!';
            document.getElementById('mensajeResultado').className = 'mensaje-resultado correcto';
        }
    }
}

function saltarPalabra() {
    nuevaPalabra();
}

// Inicia con una palabra al cargar
window.onload = () => {
    nuevaPalabra();
};
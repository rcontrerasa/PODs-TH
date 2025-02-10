// ==UserScript==
// @name         Cambiar Puertos Automáticamente
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Cambia el parámetro "port"
// @author       Rodrigo Contreras
// @match        https://172.16.0.137/?form=webshell&port=*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
// Lista de puertos
const portRange = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 25, 26, 27, 28, 29, 30, 31, 33, 34, 35, 36, 37, 38, 39];

// Obtén el índice actual del puerto desde la URL
function getCurrentPortIndex() {
    const url = new URL(window.location.href);
    const currentPort = parseInt(url.searchParams.get('port'), 10);
    return portRange.indexOf(currentPort);
}

// Función para actualizar el puerto en la URL
function updatePort() {
    // Obtén el índice actual del puerto
    let currentIndex = getCurrentPortIndex();

    // Si no se encuentra el puerto actual en la lista, comienza desde el inicio
    if (currentIndex === -1) {
        currentIndex = 0;
    }

    // Calcula el siguiente índice
    const nextIndex = (currentIndex + 1) % portRange.length;

    // Crea la nueva URL con el siguiente puerto
    const url = new URL(window.location.href);
    url.searchParams.set('port', portRange[nextIndex]);

    // Redirige a la nueva URL
    window.location.href = url.toString();
}

// Ejecutar la función cada 3,8 segundos
setInterval(updatePort, 3800);
})();

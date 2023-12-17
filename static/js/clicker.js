let cookies = 0;

const probability = 0.1;


function handleIncrementResponse(data) {
    cookies = data.contador_principal;

    if (data.success) {
        console.log(data.message);

        if (cookies >= 9999) {
            
            playCelebrationSound();

            
            displayCelebrationMessage();

            
            fetch('/restarPuntosGanados', {
                method: 'POST'
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('Se restaron 9999 puntos con éxito');

                    
                    updateCookiesDisplay();
                } else {
                    console.error('Error al restar 9999 puntos: ', data.message);
                }
            })
            .catch(error => {
                console.error('Error al restar 9999 puntos: ', error);
            });
        } else {
            
            updateCookiesDisplay();
        }
    } else {
        
        window.alert('Error al aumentar el contador: ' + data.message);
        console.error(data.message);
    }
}

function playCelebrationSound() {
    const celebration = new Audio('static/sounds/celebration.mp3');
    celebration.play().catch(error => {
        console.error('Error al reproducir el sonido de celebración:', error);
    });
}

function clickCookie() {
    fetch('/aumentarContador', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(handleIncrementResponse)  
    .catch(error => {
        console.error('Error al aumentar el contador: ', error);
    });
}

cookie.addEventListener("click", clickCookie);

function updateCookiesDisplay() {
    const cookieCountElement = document.getElementById("cookieCount");
    cookieCountElement.innerHTML = cookies + " cookies";

    if (cookies <= 0) {
        
        alert("¡Perdiste!");
        restablecerContador();
    } else if (cookies >= 9999) {
        
        alert("¡Ganaste!");
        
    }
}

document.getElementById('icono1').addEventListener('click', function() {
    
    var panelTienda = document.getElementById('panelTienda');
  
    
    if (panelTienda.style.display === 'none') {
      
      panelTienda.style.display = 'block';
    } else {
      
      panelTienda.style.display = 'none';
    }
  });

  function handleTripleClick() {
    
    document.getElementById('tripleClick').disabled = true;

    
    fetch('/restarGalletasTripleClick', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log(data.message);
        } else {
            
            window.alert(data.message);
            console.error(data.message);
        }
    })
    .catch(error => {
        console.error('Error al restar galletas: ', error);
    });
}

function handleDoubleClick() {  
    
    document.getElementById('dobleClick').disabled = true;

    
    fetch('/restarGalletas', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log(data.message);
        } else {
            
            window.alert(data.message);
            console.error(data.message);
        }
    })
    .catch(error => {
        console.error('Error al restar galletas: ', error);
    });
}

function handleSkinClick(skinType) {
    
    fetch('/restarGalletas', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log(data.message);

            
            if (skinType === 'skin1') {
                cookie.image.src = "static/img/perfectCookie.png";
                document.body.className = 'skin1';
            } else if (skinType === 'skin2') {
                cookie.image.src = "static/img/galleta2.png";
                document.body.className = 'skin2';
            } else if (skinType === 'skin3') {
                cookie.image.src = "static/img/galleta4.png";
                document.body.className = 'skin3';
            }
            
            updateCookiesDisplay();
        } else {
            
            window.alert(data.message);
            console.error(data.message);
        }
    })
    .catch(error => {
        console.error('Error al restar galletas: ', error);
    });
}

function restablecerContador() {
    fetch('/restablecerContador', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        
        console.log(data.message);

        if (data.success) {
            
            cookies = 100;
            updateCookiesDisplay();
        } else {
            
            console.error('Error al restablecer el contador: ', data.message);
        }
    })
    .catch(error => {
        console.error('Error al restablecer el contador: ', error);
    });
}

function aumentarContador(){
    fetch('/aumentarContador', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        cookies = data.contador_principal;
        updateCookiesDisplay();
    
        if (data.success) {
            console.log(data.message);
    
            
            if (data.message.includes('Ganaste')) {
                var confirmacion = window.confirm('¡Ganaste! Se restaron 9900 puntos. ¿Quieres continuar?');
    
                if (confirmacion) {
                    
                } else {
                    
                }
            } else {
                
                window.alert(data.message);
            }
        } else {
           
            window.alert('Error al aumentar el contador: ' + data.message);
            console.error(data.message);
        }
    })
    .catch(error => {
        console.error('Error al aumentar el contador: ', error);
    });
}

function restablecerContador() {
    fetch('/restablecerContador', {
        method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
        
        console.log(data.message);

        if (data.success) {
            
            cookies = 100;
            updateCookiesDisplay();
        } else {
            
            console.error('Error al restablecer el contador: ', data.message);
        }
    })
    .catch(error => {
        console.error('Error al restablecer el contador: ', error);
    });
}

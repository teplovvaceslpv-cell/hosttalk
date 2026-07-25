window.addEventListener("DOMContentLoaded", function () {
    chat = document.getElementById('chat')
    let notificationA = new Audio(`static/recieved.mp3`)
    let notificationB = new Audio(`static/sent.mp3`)

    document.querySelectorAll(`[splash="icon"]`).forEach(llkv => {
        llkv.addEventListener("animationend", function () {
            llkv.closest("splash").style.display = "none"
        })
    })

    window.sdihkid = io()

    // --- ИСПРАВЛЕННЫЙ ВВОД ИМЕНИ ---
    // Всегда запрашиваем имя при заходе (игнорируем старое из localStorage)
    let usrahh = prompt("Enter username to continue")
    
    // Если нажали Cancel или оставили пустым, даем имя по умолчанию
    if (!usrahh || usrahh.trim() === "") {
        usrahh = "Guest"
    }
    
    // Сохраняем в localStorage (чтобы запомнить для следующего раза, но окно будет появляться снова)
    localStorage.setItem("userID", usrahh)

    // Генератор случайного, но постоянного цвета для имени
    function getColorForName(name) {
        let hash = 0;
        for (let i = 0; i < name.length; i++) {
            hash = name.charCodeAt(i) + ((hash << 5) - hash);
        }
        return 'hsl(' + (hash % 360) + ', 70%, 50%)';
    }

    // --- ПОДКЛЮЧЕНИЕ К СЕРВЕРУ ---
    sdihkid.on('connect', function () {
        // Отправляем объект {name: "Вася"}, как и требует ваш сервер
        sdihkid.emit('join', {name: usrahh})
    })

    const orgAud = this.window.Audio
    window.Audio = function (...args) {
        const audio = new orgAud(...args)
        audio.volume = 0.3
        return audio
    }

    // --- ПОЛУЧЕНИЕ СООБЩЕНИЙ ---
    sdihkid.on("mainchat", d => {
        const each$$cov = document.createElement("div")
        const each$$msg = document.createElement("p")

        each$$msg.innerHTML = `${d.msg}`

        if (d.msg.length >= 31) {
            each$$msg.setAttribute('large', '2')
            each$$cov.setAttribute('large', '2c')
        }

        // Если сообщение отправил текущий пользователь
        if (d.name == usrahh) {
            each$$msg.setAttribute('mine', 'yesvro')
            each$$cov.setAttribute('mine', 'yescover')
            each$$cov.setAttribute('setmarg', '02')
        } 
        // Если сообщение от другого пользователя
        else {
            let a = document.createElement('p')
            a.innerHTML = d.name
            a.setAttribute('tag', 'user')
            
            // ДОБАВЛЯЕМ ЦВЕТ ИМЕНИ
            a.style.color = getColorForName(d.name)

            each$$msg.setAttribute('mine', 'fuhnaw')
            each$$cov.setAttribute('mine', 'nocover')
            each$$cov.appendChild(a)
        }

        each$$cov.setAttribute("bubble", "cover")
        chat.appendChild(each$$cov)
        each$$cov.appendChild(each$$msg)
        window.scrollTo(0, document.body.scrollHeight);
    })

    // --- ОТПРАВКА СООБЩЕНИЙ ---
    window.sendingmyahh = function () {
        const inp = document.querySelector('[dih="yo"]')
        if (inp.value.trim() !== "") {
            sdihkid.emit("mainchat", inp.value)
            inp.value = ""
            notificationB.play()
            window.scrollTo(0, document.body.scrollHeight);
        }
    }

    document.querySelector('[dih="yo"]').addEventListener('keydown', function (dih) {
        if (dih.key == "Enter") {
            sendingmyahh()
        }
    })

    function focusin() { document.querySelector('[dih="yo"]').focus() }
    document.querySelector('[oc="p"]').addEventListener('click', focusin)
    window.addEventListener('keydown', (dih) => {
        if (dih.target.closest(`popup-window`)) return
        focusin()
    })
})
.pragma library
.import QtQuick.LocalStorage 2.0 as SQL

var cache = {}
var pending = {}
var queue = []
var busy = false
var retryAfter = 0
var database = null

function db() {
    if (database) return database
    try {
        database = SQL.LocalStorage.openDatabaseSync("MinecraftPublicNewsPtBR", "1.0", "Traduções de títulos e resumos públicos do Minecraft", 2000000)
        database.transaction(function(tx) {
            tx.executeSql("CREATE TABLE IF NOT EXISTS translations (source TEXT PRIMARY KEY, translated TEXT NOT NULL)")
        })
    } catch (e) { database = null }
    return database
}

function cached(source) {
    if (cache[source] !== undefined) return cache[source]
    var value = ""
    var store = db()
    if (store) {
        try {
            store.readTransaction(function(tx) {
                var rows = tx.executeSql("SELECT translated FROM translations WHERE source = ?", [source]).rows
                if (rows.length) value = rows.item(0).translated
            })
        } catch (e) {}
    }
    if (value) cache[source] = value
    return value
}

function remember(source, translated) {
    cache[source] = translated
    var store = db()
    if (store) {
        try {
            store.transaction(function(tx) {
                tx.executeSql("INSERT OR REPLACE INTO translations (source, translated) VALUES (?, ?)", [source, translated])
            })
        } catch (e) {}
    }
}

// Only NewsScreen calls this function, with public article titles and summaries.
function translate(source, owner, callback) {
    source = String(source || "")
    if (!source) { callback(""); return }
    var curated = qsTranslate("RemoteNews", source)
    if (curated !== source) { callback(curated); return }
    var saved = cached(source)
    if (saved) { callback(saved); return }
    if (unescape(encodeURIComponent(source)).length > 500) {
        var parts = [], rest = source
        while (rest.length) {
            var end = Math.min(rest.length, 450)
            while (end > 1 && (rest.charCodeAt(end - 1) >= 0xD800 && rest.charCodeAt(end - 1) <= 0xDBFF || unescape(encodeURIComponent(rest.substring(0, end))).length > 480)) end--
            if (end < rest.length) {
                var space = rest.lastIndexOf(" ", end)
                if (space > 0) end = space
            }
            parts.push(rest.substring(0, end).trim())
            rest = rest.substring(end).trim()
        }
        var result = new Array(parts.length), remaining = parts.length
        parts.forEach(function(part, index) {
            translate(part, owner, function(value) {
                result[index] = value
                remaining--
                if (!remaining) {
                    var joined = result.join(" ")
                    if (joined.indexOf(qsTranslate("NewsLocalization", "Translation unavailable")) < 0) remember(source, joined)
                    callback(joined)
                }
            })
        })
        return
    }
    if (Date.now() < retryAfter) { callback(qsTranslate("NewsLocalization", "Translation unavailable") + ": " + source); return }
    if (pending[source]) { pending[source].push(callback); return }
    pending[source] = [callback]
    queue.push({source: source, owner: owner})
    advance()
}

function advance() {
    if (busy || !queue.length) return
    busy = true
    var job = queue.shift()
    if (Date.now() < retryAfter) {
        var waiting = pending[job.source] || []
        delete pending[job.source]
        for (var c = 0; c < waiting.length; c++) { try { waiting[c](qsTranslate("NewsLocalization", "Translation unavailable") + ": " + job.source) } catch (e) {} }
        busy = false
        advance()
        return
    }
    var request = new XMLHttpRequest()
    var completed = false
    var timer = Qt.createQmlObject('import QtQuick; Timer { interval: 15000; repeat: false }', job.owner, "PublicNewsTranslationTimeout")
    function finish(value) {
        if (completed) return
        completed = true
        timer.stop()
        timer.destroy()
        if (value) remember(job.source, value)
        var callbacks = pending[job.source] || []
        delete pending[job.source]
        for (var i = 0; i < callbacks.length; i++) {
            try { callbacks[i](value || qsTranslate("NewsLocalization", "Translation unavailable") + ": " + job.source) } catch (e) {}
        }
        var next = Qt.createQmlObject('import QtQuick; Timer { interval: 750; repeat: false }', job.owner, "PublicNewsTranslationSpacing")
        next.triggered.connect(function() { next.destroy(); busy = false; advance() })
        next.start()
    }
    timer.triggered.connect(function() { finish(""); request.abort() })
    request.onreadystatechange = function() {
        if (request.readyState !== XMLHttpRequest.DONE || completed) return
        var translated = ""
        if (request.status === 200) {
            try {
                var response = JSON.parse(request.responseText)
                if (Number(response.responseStatus) === 200 && !response.quotaFinished && response.responseData) translated = response.responseData.translatedText || ""
                else retryAfter = Date.now() + 300000
            } catch (e) {}
        }
        if (request.status === 429) retryAfter = Date.now() + 300000
        finish(translated)
    }
    request.open("GET", "https://api.mymemory.translated.net/get?langpair=en%7Cpt-BR&q=" + encodeURIComponent(job.source), true)
    request.setRequestHeader("User-Agent", "Mozilla/5.0")
    timer.start()
    request.send()
}

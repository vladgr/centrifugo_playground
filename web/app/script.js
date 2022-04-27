// ------- ApiClient helper class to work with FastApi

class ApiClient {
    apiUrl = 'http://127.0.0.1:5000'
    getTokenUrl = '/get_token'
    sendMessageUrl = '/send_message'

    async getToken() {
        const url = this.apiUrl + this.getTokenUrl
        const response = await fetch(url, { method: 'GET' })
        const data = await response.json()
        return data.token
    }

    async sendMessage() {
        const url = this.apiUrl + this.sendMessageUrl

        const data = { anything: 'Test message' }

        const options = {
            method: 'POST',
            body: JSON.stringify(data)
        }

        options.headers = {
            Accept: 'application/json',
            'Content-Type': 'application/json'
        }

        await fetch(url, options)
    }
}

// -------

const wsCentrifugoUrl = 'ws://localhost:8000/connection/websocket'

const apiClient = new ApiClient()
const centClient = new Centrifuge(wsCentrifugoUrl)

const channelName = 'news'

// Connect to Centrifugo as soon as page ready
document.addEventListener('DOMContentLoaded', async (event) => {
    const token = await apiClient.getToken()
    centClient.setToken(token)

    centClient.on('connect', () => {
        console.log('WebSocket connected')
    })

    centClient.on('disconnect', (ctx) => {
        console.log('WebSocket disconnected')
        console.log(ctx)
    })

    centClient.connect()
})

// ------- Buttons handlers

function subscribe() {
    console.log(`Client subscribed to ${channelName}`)

    centClient.subscribe(channelName, (msg) => {
        console.log(msg)
    })
}

function unsubscribe() {
    console.log('Unsubscribe from news')
}

function sendMessage() {
    apiClient.sendMessage()
}
